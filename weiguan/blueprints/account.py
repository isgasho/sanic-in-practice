from sanic import Blueprint

from ..utils import sha256_hash
from ..models import UserSchema
from ..services import UserService
from .common import response_json, ResponseCode, authenticated, dump_user_info

account = Blueprint('account', url_prefix='/account')


@account.post('/register')
async def register(request):
    data = request.json
    username = data['username']
    password = data['password']

    user_service = UserService(
        request.app.config, request.app.db, request.app.cache)
    user = await user_service.create(username=username, password=password)

    return response_json(user=await dump_user_info(request, user))


@account.post('/login')
async def login(request):
    data = request.json
    username = data.get('username')
    mobile = data.get('mobile')
    password = data['password']

    user_service = UserService(
        request.app.config, request.app.db, request.app.cache)
    if username is not None:
        user = await user_service.info_by_username(username)
    elif mobile is not None:
        user = await user_service.info_by_mobile(mobile)
    else:
        user = None

    if (user is not None and
            sha256_hash(password, user['salt']) == user['password']):
        request['session']['user'] = await dump_user_info(request, user)

        return response_json(user=request['session']['user'])
    else:
        return response_json(ResponseCode.FAIL, '帐号或密码错误')


@account.get('/logout')
async def logout(request):
    user = request['session'].pop('user')

    return response_json(user=user)


@account.get('/info')
async def info(request):
    user = request['session'].get('user')

    return response_json(user=user)


@account.post('/edit')
@authenticated()
async def edit(request):
    user_id = request['session']['user']['id']

    data = request.json
    username = data.get('username')
    password = data.get('password')
    mobile = data.get('mobile')
    email = data.get('email')
    avatar_id = data.get('avatarId')
    intro = data.get('intro')
    code = data.get('code')

    user_service = UserService(
        request.app.config, request.app.db, request.app.cache)

    if ((mobile is not None and
            not (await user_service.check_mobile_verify_code('edit', mobile, code))) or
            (email is not None and
             not (await user_service.check_email_verify_code('edit', email, code)))):
        return response_json(ResponseCode.FAIL, '验证码错误')

    user = await user_service.edit(
        user_id, username=username, password=password, mobile=mobile,
        email=email, avatar_id=avatar_id, intro=intro)

    request['session']['user'] = await dump_user_info(request, user)

    return response_json(user=request['session']['user'])


@account.post('/send/mobile/verify/code')
@authenticated()
async def send_mobile_verify_code(request):
    data = request.json
    type = data['type']
    mobile = data['mobile']

    user_service = UserService(
        request.app.config, request.app.db, request.app.cache)
    code = await user_service.send_mobile_verify_code(type, mobile)

    return response_json(verify_code=code)
