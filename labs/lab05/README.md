<div align="center">
<h1><a id="intro">Лабораторная работа №5</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Барышев_М._С.-8b9aff" alt="Contributor Badge"></a></div>

***
Данная лабораторная работа посвещена изучению Docker и как с ним работать. Эта лабораторная работа послужит подпоркой для старта в выявлении и определении уязвимостей на уровне сканирования контейнеров при сборке приложений. 

***

## Задание

- [x] 1. Поставьте `Docker` и `buildkit`

```bash
$ brew install buildkit
$ brew install docker
```

- [x] 2. Перейдите в `source` и выведите на терминале, далее проанализируйте следующие команды консоли

```bash
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world
$ docker run --rm -it hello-appsec-world

$ docker save -o hello.tar hello-appsec-world
$ docker load -i hello.tar
$ docker load -i image.tar
```
- [x] 3. Откройте `Dockerfile` и сделайте его анализ. Сделайте `commit`
- [x] 4. Замените в `Dockerfile`значение скрипта на `python` тем, который вы сделали ранее в прошлых лабораторных работах. Вложите свой файл `python` в директорию. Сделайте анализ своего измененного `Dockerfile` и внесите изменения. Сделайте `commit`. 

> Пример анализа по текущему `Dockerfile` в репозитории

```dockerfile
# Этап 1: сборка зависимостей
FROM python:3.11-slim AS builder
WORKDIR /hello
# Копируем файл с зависимостями
COPY requirements.txt . 
# Устанавливаем зависимости в отдельную директорию wheelhouse для кеширования
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

# Этап 2: запускаемый образ
FROM python:3.11-slim
WORKDIR /hello
# Копируем файл с зависимостями
COPY --from=builder /wheels /wheels # Копируем собранные wheel-пакеты
COPY requirements.txt . 
# Устанавливаем зависимости из wheel-пакетов
RUN pip install --no-index --find-links=/wheels -r requirements.txt
# Копируем исходный код приложения
COPY hello.py .

# Переменные окружения для улучшенной работы Python
ENV PYTHONUNBUFFERED=1
# Запускаем приложение
CMD ["python", "hello.py"] 
```

- [x] 5. Выведите на терминале и проанализируйте следующие команды консоли. Сравните хеш сумму вашего архива с `image.tar` из репозитория, выведите на терминал.

```bash
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world
$ docker save -o hello_ypur_project.tar hello-appsec-world

$ docker load -i hello_ypur_project.tar
$ docker run hello-appsec-world

$ docker load -i image.tar
$ docker run hello-appsec-world
```

- [x] 6. Доработайте свой `python` скрипт подключаемыми библиотеками, далее их необходимо разместить в `requirements.txt`. Размещение библиотек в следующем формате:

```
flask==2.2.3
requests==2.28.1
```

- [x] 7. Сделайте `commit`. Повторите сборку приложения по вашему `Dockerfile` для доработанного скрипта `python`. Сохраните `image` в виде .`tar` архива. Сделайте `commit`.
- [x] 8. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ docker login
$ docker tag hello-appsec-world yourusername/hello-appsec-world
$ docker push yourusername/hello-appsec-world
$ docker inspect yourusername/hello-appsec-world
$ docker container create --name first hello-appsec-world # выпишите id контейнера

$ docker image pull geminishkv/hello-appsec-world
$ docker inspect geminishkvdev/hello-appsec-world
$ docker container create --name second hello-appsec-world

``` 

- [x] 9. Выведите на терминале и проанализируйте в консоли процессы, которые запущены, владельцев по пользователям

```bash 
 $ docker container run -it ubuntu /bin/bash
``` 
 
- [x] 10. Выведите оба контейнера first и second на терминал
- [x] 11. Перейдите в основной корень `lab05` и выведите на терминале, и проанализируйте

```bash 
$ docker-compose up --build
``` 

- [x] 12. Откройте соседнее окно терминала и и выведите на терминале

```bash 
$ open -a "Google Chrome" http://localhost:8000
```

- [x] 13. Остановите работу `docker-compose`.

```bash 
$ docker ps -a
$ docker ps -q
$ docker images

$ docker ps -q | xargs docker stop
$ docker-compose down
```
- [x] 14. Доработайте `docker-compose` и скрипт, который вы подготовили ранее, что бы вы смогли воспроизвести шаги п.11 по п.13 с демонстрацией. Сделайте `commit`.
- [x] 15. Залейте изменения в свой удаленный репозиторий, проверьте историю `commit`.
- [x] 16. Подготовьте отчет `gist`.
 
***

## Выполнение задание

- [x] 1. Поставьте `Docker` и `buildkit`

```bash
$ brew install buildkit
$ brew install docker
```

- [x] 2. Перейдите в `source` и выведите на терминале, далее проанализируйте следующие команды консоли

```bash
$ docker buildx build -t hellow-appsec-world .

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker buildx build -t hello-appsec-world .

[+] Building 10.8s (7/12) docker:defaultlt> [internal] load build definition from Dockerfile 0.1s
 => [internal] load build definition from Dockerfile  

$ docker run hello-appsec-world

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker run hello-appsec-world
hello appsec world

$ docker run --rm -it hello-appsec-world
# --rm удаляет контейнер после завершения, -it — интерактивный TTY

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker run --rm -it hello-appsec-world
hello appsec world


$ docker save -o hello.tar hello-appsec-world
$ docker load -i hello.tar

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker save -o hello.tar hello-appsec-world
                                                                  
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker load -i hello.tar
Loaded image: hello-appsec-world:latest

$ docker load -i image.tar

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker load -i image.tar
f1b30ab99183: Loading layer  30.14MB/30.14MB
c24001014542: Loading layer  1.274MB/1.274MB
7a4b2171e46d: Loading layer  14.31MB/14.31MB
591779db3273: Loading layer     250B/250B
efd49302dd30: Loading layer      95B/95B
8fe7432c3de3: Loading layer      96B/96B
e687a26fd0a6: Loading layer     141B/141B
71299f61dc2b: Loading layer  4.065MB/4.065MB
5b8b2e16a223: Loading layer     344B/344B
The image hello-appsec-world:latest already exists, renaming the old one with ID sha256:9e130229838d03076a0f3f37c47e7e491b123c5ec787371321ccca26b23a2b78 to empty string
Loaded image: hello-appsec-world:latest

```
- [x] 3. Откройте `Dockerfile` и сделайте его анализ. Сделайте `commit`
- [x] 4. Замените в `Dockerfile`значение скрипта на `python` тем, который вы сделали ранее в прошлых лабораторных работах. Вложите свой файл `python` в директорию. Сделайте анализ своего измененного `Dockerfile` и внесите изменения. Сделайте `commit`. 

```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker buildx build -t hello-appsec-world .                    
[+] Building 12.3s (13/13) FINISHED  docker:default
.......
                                                                                      
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker run --rm hello-appsec-world 

# Если в задании говорится о файле из лабы2, в котором используется графика, то докер выведет ошибку запуска
# Поэтому отключаем графику и запускаем

#Предупреждение fc-list is missing является ожидаемым для минимального headless-контейнера и не влияет на выполнение приложения.

pygame 2.5.2 (SDL 2.28.2, Python 3.11.14)
Hello from the pygame community. https://www.pygame.org/contribute.html
/usr/local/lib/python3.11/site-packages/pygame/sysfont.py:223: UserWarning: 'fc-list' is missing, system fonts cannot be loaded on your platform
  warnings.warn(
Pygame initialized successfully in headless mode
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ cat new.py #новый файл                                                 
import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame

pygame.init()

screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

font = pygame.font.SysFont(None, 75)
text = font.render("Hello appsec world*", True, (0, 255, 0))

print("Pygame initialized successfully in headless mode")
```

- [x] 5. Выведите на терминале и проанализируйте следующие команды консоли. Сравните хеш сумму вашего архива с `image.tar` из репозитория, выведите на терминал.

```bash
$ docker buildx build -t hellow-appsec-world .
$ docker run hello-appsec-world

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker run --rm hello-appsec-world
pygame 2.5.2 (SDL 2.28.2, Python 3.11.14)
Hello from the pygame community. https://www.pygame.org/contribute.html
/usr/local/lib/python3.11/site-packages/pygame/sysfont.py:223: UserWarning: 'fc-list' is missing, system fonts cannot be loaded on your platform
  warnings.warn(
Pygame initialized successfully in headless mode
                                                 
$ docker save -o hello_ypur_project.tar hello-appsec-world
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ ls -lh hello_your_project.tar
-rw------- 1 lullaby lullaby 183M Dec 14 17:21 hello_your_project.tar

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ sha256sum image.tar | tee /tmp/hash_repo.txt
9a8bebe1ff86415103fb184a0ee9c70afaeaad7cc062db37438bce48557b51d2  image.tar
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ sha256sum hello_your_project.tar | tee /tmp/hash_my.txt

02e24e107220f18d9dab12342cbdd5222ec3497a8f53bc733b1d73e1d6eda693  hello_your_project.tar


$ docker load -i hello_ypur_project.tar
$ docker run hello-appsec-world
                                                                               
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker load -i hello_your_project.tar
The image hello-appsec-world:latest already exists, renaming the old one with ID sha256:f386bd63aa82e8393bdd081873b60fa5d8938ffb1b7f53bed6bbbd947358f847 to empty string
Loaded image: hello-appsec-world:latest
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker run --rm hello-appsec-world
pygame 2.5.2 (SDL 2.28.2, Python 3.11.14)
Hello from the pygame community. https://www.pygame.org/contribute.html
/usr/local/lib/python3.11/site-packages/pygame/sysfont.py:223: UserWarning: 'fc-list' is missing, system fonts cannot be loaded on your platform
  warnings.warn(
Pygame initialized successfully in headless mode

#Тут образ собран под арм, поэтому будет ошибка
$ docker load -i image.tar
$ docker run hello-appsec-world

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker load -i image.tar
The image hello-appsec-world:latest already exists, renaming the old one with ID sha256:c7831b300415b2da61d42434477c22bc294ee7ec2c7be8ad5cec0308ce9f98ca to empty string
Loaded image: hello-appsec-world:latest
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker run --rm hello-appsec-world
WARNING: The requested image's platform (linux/arm64) does not match the detected host platform (linux/amd64/v2) and no specific platform was requested
exec /usr/local/bin/python: exec format error

```

- [x] 6. Доработайте свой `python` скрипт подключаемыми библиотеками, далее их необходимо разместить в `requirements.txt`. Размещение библиотек в следующем формате
- [x] 7. Сделайте `commit`. Повторите сборку приложения по вашему `Dockerfile` для доработанного скрипта `python`. Сохраните `image` в виде .`tar` архива. Сделайте `commit`.
```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ cat requirements.txt 
pygame==2.5.2
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ git add requirements.txt 
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ git commit -m "add dependency - pygame"
[lab05-docker f6d4093] add dependency - pygame
 1 file changed, 1 insertion(+)
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker save -o hello_with_deps.tar hello-appsec-world
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ ls -lh hello_with_deps.tar
-rw------- 1 lullaby lullaby 183M Dec 14 17:29 hello_with_deps.tar
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ git add hello_with_deps.tar
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ git commit -m "Lab05: save image to tar"
[lab05-docker 2a94fc5] Lab05: save image to tar
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 labs/lab05/source/hello_with_deps.tar

 ┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ git log --oneline -5                    
2a94fc5 (HEAD -> lab05-docker) Lab05: save image to tar
f6d4093 add dependency - pygame
3808a26 new dockerfile
6df2b38 analyze Dockerfile
ba2288a (origin/develop, origin/HEAD, develop) release v1.3.0

```
- [x] 8. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ docker login
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker login -u mishabmstu
Password: 
WARNING! Your password will be stored unencrypted in /home/lullaby/.docker/config.json.
Configure a credential helper to remove this warning. See
https://docs.docker.com/engine/reference/commandline/login/#credential-stores
Login Succeeded

$ docker tag hello-appsec-world yourusername/hello-appsec-world
$ docker push yourusername/hello-appsec-world

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker tag hello-appsec-world mishabmstu/hello-appsec-world #Создаёт новый тег для локального образа.
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker push mishabmstu/hello-appsec-world       # Загружает образ в Docker Hub.           
Using default tag: latest
The push refers to repository [docker.io/mishabmstu/hello-appsec-world]
...
latest: digest: sha256:6a58306488390e848994d69bd7e4c9f50a1accb949920a6408016a2f04dbc471 size: 2411

$ docker inspect yourusername/hello-appsec-world
#Показывает метаданные образа: ENV, CMD, User, Layers, Architecture
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker inspect mishabmstu/hello-appsec-world   
[
    {
        "Id": "sha256:c7831b300415b2da61d42434477c22bc294ee7ec2c7be8ad5cec0308ce9f98ca",
        "RepoTags": [
            "hello-appsec-world:latest",
            "mishabmstu/hello-appsec-world:latest"
        ],
        ...}]



$ docker container create --name first hello-appsec-world 
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker container create --name first hello-appsec-world
f8ddf6343cae52e7aaf30beaffd35bc9696586f4d18313545464b3e33fa6a4d9


$ docker image pull geminishkv/hello-appsec-world
$ docker inspect geminishkvdev/hello-appsec-world
$ docker container create --name second hello-appsec-world
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker container create --name second hello-appsec-world
e8a50e406a691866d84f64042734f03096150d8817764881eea1888bf2110613

``` 

- [x] 9. Выведите на терминале и проанализируйте в консоли процессы, которые запущены, владельцев по пользователям

```bash 
 $ docker container run -it ubuntu /bin/bash
# Не получается получить доступ к регистру, поэтому локальный контейнер использовал
 ┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker container run -it ubuntu /bin/bash
Unable to find image 'ubuntu:latest' locally
docker: Error response from daemon: Get "https://registry-1.docker.io/v2/": net/http: TLS handshake timeout.
See 'docker run --help'.

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker run --rm -it hello-appsec-world sh

$ whoami
appuser
$ id
uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)

``` 
 
- [x] 10. Выведите оба контейнера first и second на терминал
```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05/source]
└─$ docker ps -a | grep -E "first|second"

e8a50e406a69   hello-appsec-world   "python new.py"     6 minutes ago    Created                             second
f8ddf6343cae   hello-appsec-world   "python new.py"     12 minutes ago   Created                             first
```
- [x] 11. Перейдите в основной корень `lab05` и выведите на терминале, и проанализируйте

```bash 
$ docker-compose up --build

 ✔ client                    Built                                                      0.0s 
 ✔ server                    Built                                                      0.0s 
 ✔ Network lab05_app_net     Created                                                    0.2s 
 ✔ Container lab05-server-1  Created                                                    0.1s 
 ✔ Container lab05-client-1  Created                                                    0.1s 
Attaching to client-1, server-1
server-1  |  * Serving Flask app 'app'
server-1  |  * Debug mode: off
server-1  | WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
server-1  |  * Running on all addresses (0.0.0.0)
server-1  |  * Running on http://127.0.0.1:8000
server-1  |  * Running on http://172.18.0.2:8000
server-1  | Press CTRL+C to quit
server-1  | 172.18.0.3 - - [14/Dec/2025 14:56:41] "GET / HTTP/1.1" 200 -
client-1  | 
client-1  |     <html>                                                                       
client-1  |     <head><title>Colorful Output</title></head>                                  
client-1  |     <body style="font-family: monospace; font-size: 24px;">                      
server-1  | 172.18.0.1 - - [14/Dec/2025 14:58:14] "GET / HTTP/1.1" 200 - 
``` 

- [x] 12. Откройте соседнее окно терминала и выведите на терминале

```bash 
$ open -a "Google Chrome" http://localhost:8000

┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ curl -I http://localhost:8000

HTTP/1.1 200 OK
Server: Werkzeug/2.3.7 Python/3.11.14
Date: Sun, 14 Dec 2025 15:01:00 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 761
Connection: close

```

- [x] 13. Остановите работу `docker-compose`.

```bash 
$ docker ps -a
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05]
└─$ docker ps -a                         
CONTAINER ID   IMAGE                COMMAND              CREATED          STATUS                        PORTS     NAMES
4f1c2784a067   lab05-client         "python client.py"   5 minutes ago    Exited (0) 3 minutes ago                lab05-client-1
b75a4025103f   lab05-server         "python app.py"      5 minutes ago    Exited (137) 31 seconds ago             lab05-server-1
e8a50e406a69   hello-appsec-world   "python new.py"      12 minutes ago   Created                                 second
f8ddf6343cae   hello-appsec-world   "python new.py"      18 minutes ago   Created                                 first
86c22da09dd3   9e130229838d         "python hello.py"    44 hours ago     Exited (0) 44 hours ago                 festive_jemison
67fdd9963f1e   hello-world          "/hello"             44 hours ago     Exited (0) 44 hours ago                 inspiring_moser

$ docker ps -q
$ docker images
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05]
└─$ docker ps -q                                                                                           
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05]
└─$ docker images
REPOSITORY                      TAG       IMAGE ID       CREATED             SIZE
lab05-client                    latest    43a86e9342ca   5 minutes ago       138MB
lab05-server                    latest    edcaf28c30e7   6 minutes ago       141MB
hello-appsec-world              latest    c7831b300415   About an hour ago   185MB
mishabmstu/hello-appsec-world   latest    c7831b300415   About an hour ago   185MB
<none>                          <none>    347ec28f7f17   2 hours ago         185MB
<none>                          <none>    9e130229838d   44 hours ago        135MB
<none>                          <none>    f386bd63aa82   3 weeks ago         160MB
hello-world                     latest    1b44b5a3e06a   4 months ago        10.1kB
                     

$ docker ps -q | xargs docker stop
$ docker-compose down

┌──(lullaby㉿kali)-[~/course_labs/labs/lab05]
└─$ docker ps -q | xargs docker stop
"docker stop" requires at least 1 argument.
See 'docker stop --help'.

Usage:  docker stop [OPTIONS] CONTAINER [CONTAINER...]

Stop one or more running containers
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05]
└─$ docker ps

CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
                                                                                             
┌──(lullaby㉿kali)-[~/course_labs/labs/lab05]
└─$ docker-compose down

WARN[0000] /home/lullaby/course_labs/labs/lab05/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] Running 3/3
 ✔ Container lab05-client-1  Removed                                                    0.0s 
 ✔ Container lab05-server-1  Removed                                                    0.0s 
 ✔ Network lab05_app_net     Removed 
```
- [x] 14. Доработайте `docker-compose` и скрипт, который вы подготовили ранее, что бы вы смогли воспроизвести шаги п.11 по п.13 с демонстрацией. Сделайте `commit`.
```Dockerfile
networks:
  app_net:

services:
  server:
    build: ./server
    ports:
      - "8000:8000"
    networks:
      - app_net
    command: python app.py
    restart: unless-stopped

    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000"]
      interval: 10s
      timeout: 5s
      retries: 5

  client:
    build: ./client
    depends_on:
      server:
        condition: service_healthy
    networks:
      - app_net
    command: python client.py
    restart: on-failure
```
```bash

┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ curl http://localhost:8000


    <html>
    <head><title>Colorful Output</title></head>
    <body style="font-family: monospace; font-size: 24px;">
    <span style="color:red">h</span><span style="color:green">e</span><span style="color:yellow">l</span><span style="color:blue">l</span><span style="color:purple">o</span><span style="color:red"> </span><span style="color:green">a</span><span style="color:yellow">p</span><span style="color:blue">p</span><span style="color:purple">s</span><span style="color:red">e</span><span style="color:green">c</span><span style="color:yellow"> </span><span style="color:blue">w</span><span style="color:purple">o</span><span style="color:red">r</span><span style="color:green">l</span><span style="color:yellow">d</span>
    </body>
    </html>

```
- [x] 15. Залейте изменения в свой удаленный репозиторий, проверьте историю `commit`.
- [x] 16. Подготовьте отчет `gist`.
 
***
