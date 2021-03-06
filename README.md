# Sanic in Practice

This project is the reference source code of online video course [叽歪课堂 - Python Sanic 高并发服务开发实战](https://blog.jaggerwang.net/jwcourse-python-sanic-high-currency-service-develop-in-practice/), including Sanic web framework usage examples, SQLAlchemy sql toolkit usage examples, and a lite version of [Weiguan](https://weiguan.app/) app's api server. The api server developed in this project can be used as the backend service of the mobile client app which is developed in project [Flutter in Practice](https://github.com/jaggerwang/flutter-in-practice).

> To students of course: 最新的实战项目目录结构已按照 [干净架构](https://blog.jaggerwang.net/clean-architecture-in-practice/) 进行了整理，另外还使用了 [IoC 容器](https://blog.jaggerwang.net/simplify-business-objects-management-by-ioc-container/) 来简化业务对象的管理。代码结构调整较大，如想获取之前版本，可查看提交记录。

## Dependent frameworks and packages

1. [Sanic](https://github.com/huge-success/sanic) Asynchronous web framework and server
1. [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) SQL toolkit and orm framework
1. [AIOMySQL](https://github.com/aio-libs/aiomysql) Asynchronous access mysql
1. [AIORedis](https://github.com/aio-libs/aioredis) Asynchronous access redis
1. [MarshMallow](https://github.com/marshmallow-code/marshmallow/) Object serialization
1. [Fire](https://github.com/google/python-fire) CLI application framework
1. [APScheduler](https://github.com/agronholm/apscheduler) Run interval jobs
1. [Dependency Injector](https://github.com/ets-labs/python-dependency-injector) Dependency injection microframework for Python

## APIs

| Path  | Method | Description |
| ------------- | ------------- | ------------- |
| /account/register | POST | Register account |
| /account/login | POST | Login account |
| /account/logout | GET | Logout account |
| /account/info | GET | Get logined account |
| /account/modify | POST | Modify logined account |
| /account/send/mobile/verify/code | POST | Send mobile verify code |
| /message/ws | Websocket | Create websocket connection for message |
| /post/publish | POST | Publish post |
| /post/delete | POST | Delete post |
| /post/info | GET | Get post info |
| /post/published | GET | Get published posts of some user |
| /post/like | POST | Like post |
| /post/unlike | POST | Unlike post |
| /post/liked | GET | Liked posts of some user |
| /post/following | GET | Posts of following users of someone |
| /storage/upload | POST | Upload file |
| /storage/file/info | GET | Get file meta info |
| /user/info | GET | Get user info |
| /user/follow | POST | Follow user |
| /user/unfollow | POST | Unfollow user |
| /user/followings | GET | Following users of someone |
| /user/followers | GET | Fans of some user |

## How to run

This project need python v3.7+.

### By python virtual environment

#### Prapare python virtual environment

```bash
git clone https://github.com/jaggerwang/sanic-in-practice.git && cd sanic-in-practice
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You can quit the virtual environment by execute command `deactivate`.

#### Prepare mysql and redis service

Install mysql and redis server, and start them. After mysql started, create a database for this project, and an account to access the created database.

```sql
CREATE DATABASE `weiguan` DEFAULT CHARACTER SET 'utf8mb4';
GRANT ALL PRIVILEGES ON `weiguan`.* TO 'weiguan'@'%' IDENTIFIED BY 'jwcourse.com';
```

#### Configure application

Change configs in `weiguan/config/base.py` as your need, especially mysql, redis and path related configs. You can also change configs by environment variables, you need add `WG_` prefix to each config you want to change.

#### Create tables

```bash
python -u -m weiguan.cli.app model create-tables
```

#### Start server

```bash
python -u -m weiguan.web.app
```

#### Start scheduler

```bash
python -u -m weiguan.cli.app schedule run
```

The api service's endpoint is at `http://localhost:8000/`.

### By docker compose

You need install [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) at first.

#### Configure compose

Change the content of `docker-compose.yml` as needed, especially the host path of mounted volumes.

#### Start all services

```bash
docker-compose up
```

It will start server, scheduler, mysql and redis services. If you need to stop and remove all services, you can execute command `docker-compose down`. The server and scheduler services will start failed before creating the project's database, you should run `docker-compose up` again after created the database.

#### Create database and tables

First, login to mysql container and create a database for this project. The password of mysql `root` account is `jwcourse.com`.

```bash
$ docker container exec -it sanic-in-practice_mysql_1 bash
$ mysql -u root -p
> CREATE DATABASE `weiguan` DEFAULT CHARACTER SET 'utf8mb4';
> GRANT ALL PRIVILEGES ON `weiguan`.* TO 'weiguan'@'%' IDENTIFIED BY 'jwcourse.com';
```

Second, login to server container and create tables for this project.

```bash
docker container exec -it sanic-in-practice_server_1 bash
python -u -m weiguan.cli.app model create-tables
```

Then you can access all apis at endpoint `http://localhost:8001/`.

### Developing in vscode's remote container

This project support developing in [VSCode](https://code.visualstudio.com/)'s remote container, you can create your own development environment in just one click. You need install vscode and it's extension "Remote - Containers" at first.

#### Configure remote container

Configure `docker-compose.dev.yml` and `.devcontainer/devcontainer.json` as your need, especially the host path of mount volumes. The file `docker-compose.dev.yml` will override some configs of the base file `docker-compose.yml` for better developing experience. Such as auto build application image, mount local project folder into container, etc. It also mount host's `~/.ssh` folder into container for executing git command in container.

#### Open project in remote container

Click remote development button at bottom-left corner of vscode, or open command palette, then execute command `Remote-Containers: Reopen Folder in Container`. It'll build application image, and start a server container, including it's dependency containers, as this project's development environment.

The workspace folder of the remote project is at `/workspace`, which mounted the local project's folder. You can now run and restart the remote project as nomal local project. If you need execute some command, you can login to the server container or use `docker container exec`.

The left steps is the same as run application by docker compose, such as create database and tables, access apis, etc.
