<div align="center">
<h1><a id="intro">Лабораторная работа №6</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Барышев_М._С.-8b9aff" alt="Contributor Badge"></a></div>

***

Данная лабораторная работа посвещена изучению аудита безопасности `Docker` при использовании `Docker Bench Security`. Мы рассмотрим как с ним работать. Мы разберем как проверить конфигурации безопасности и выявить их не корректность, как произвести чекап с `CIS Docker Benchmark v1.6.0`.


***

## Задание

- [x] 1. Необходимо установить `Docker Engine` для Linux

```bash
$ sudo apt-get update
$ sudo apt-get install -y docker.io
$ sudo usermod -aG docker "$USER"

$ sudo systemctl start docker
$ docker pull docker/docker-bench-security
```

- [x] 2. Проверьте работу докера и сделать скрипт `audit.sh` исполняемым
```bash
┌──(venv)─(lullaby㉿kali)-[~/course_labs/labs/lab06]
└─$ ls -la audit.sh 
-rwxrwxr-x 1 lullaby lullaby 9701 Dec 15 14:37 audit.sh
```
- [x] 3. Развернуть уязвимое приложение как отдельные стенды

```bash
$ docker compose up -d # основной web, app, postgres
$ docker-compose -f dvulnerable-app.yml up -d # поверх для vulnerable-web, debug-shell
    -f # file
    up # создает и поднимает файлы из compose
    -d # фоновый режим
```

- [x] 4. Запустите скрипт из `venv` и проанализируйте то, что вывело на терминале и что вывело при конвертировании

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install openpyxl odfpy
$ ./audit.sh
$ deactivate # или $ deactivate 2>/dev/null || true
```
 
- [x] 5. Проведите анализ уязвимостей, опишите их причину возникновения

    ### Уязвимости уровня Docker Host / Docker Daemon (CIS отчёт)

    - Нет отдельного раздела (partition) под контейнеры -> риск смешивания данных ОС и Docker-данных, сложнее контролировать заполнение диска.
    В отчёте: 1.1 WARN 

    - Не настроен аудит (auditd) для Docker daemon и критичных директорий/юнитов -> события управления контейнерами и изменения конфигов не попадают в аудит (сложно расследовать инциденты).
    В отчёте: 1.5–1.10 WARN 

    - Нет ограничения сетевого трафика между контейнерами на дефолтном bridge -> лишняя связность, проще lateral movement внутри хоста.
    В отчёте: 2.1 WARN 

    - User namespace remap не включён -> root в контейнере ближе к root на хосте, хуже изоляция.
    В отчёте: 2.8 WARN 

    - Не включены механизмы авторизации для Docker client команд (authorization plugin) -> любой, кто получил доступ к Docker API/сокету, фактически управляет хостом.
    В отчёте: 2.11 WARN 

    - Не настроено централизованное удалённое логирование -> логи можно потерять/подменить, сложнее расследование.
    В отчёте: 2.12 WARN 

    - Content Trust выключен -> можно случайно стянуть/запустить “подменённый” образ.
    В отчёте: 4.5 WARN 

    ### Уязвимости уровня контейнеров runtime (самое критичное)

    Тут пункты отностятся к небезопасному уязвимому контейнеру vulnerable-app:

    - cap_add: ALL -> контейнер получает максимально возможные capabilities ядра.
    В отчёте: 5.3 WARN (CapAdd=[ALL]) 

    - privileged: true -> почти “как root на хосте”.
    В отчёте: 5.4 WARN 

    - network_mode: host -> контейнер в сетевом пространстве хоста (сложнее фильтровать, проще перехватывать/слушать).
    В отчёте: 5.9 WARN 

    - pid: host -> контейнер видит процессы хоста (база для атак/разведки).
    В отчёте: 5.15 WARN 

    - seccomp отключён (seccomp:unconfined) -> сняты syscall-ограничения, больше поверхность атаки.
    В отчёте: 5.21 WARN 

    - “no-new-privileges” не ограничивает привилегии (в целом привилегии не зажаты) -> выше шанс эскалации.
    В отчёте: 5.25 WARN 

    - docker.sock смонтирован в контейнер -> это прямой “root-доступ” к Docker daemon (а значит и к хосту).
    В отчёте: 5.31 WARN (Docker socket shared) 

    - Нет лимитов CPU/RAM/PIDs -> DoS хоста ресурсами контейнера.
    В отчёте: 5.10, 5.11, 5.28 WARN 

    - root FS контейнера R/W -> проще закрепиться (dropper, webshell, подмена конфигов).
    В отчёте: 5.12 WARN 

    - Нет healthcheck -> деградация/компрометация может быть незаметной.
    В отчёте: 4.6 WARN + 5.26 WARN

- [x] 6. Опишите влияния уязвимостей, их сценарий атаки

    #### Компрометация хоста через docker.sock

    Атакующий получает RCE внутри vulnerable-web (например, через уязвимый веб/конфиг/внешний доступ) -> в контейнере есть /var/run/docker.sock -> через Docker API атакующий запускает новый контейнер с монтированием / и --privileged, читает /etc/shadow, подменяет файлы, добавляет SSH ключи и т.п -> **Итог: полный захват хоста.**

    #### Container escape из-за privileged + cap_add=ALL + seccomp unconfined

    Контейнер почти без ограничений (privileged), capabilities ALL, seccomp отключён -> атакующий использует kernel-эксплойты/опасные syscalls/доступ к устройствам -> **Итог: выход в хост / выполнение действий на уровне хоста.**

    #### DoS хоста ресурсами

    Нет ограничений CPU/RAM/PIDs, контейнер может переполнять память/процессы -> **Итог: отказ в обслуживании (доступность падает).**


- [x] 7. Оцените риски ИБ и предложите меры для их снижения: 

    ### Риски docker-compose.yml

    1. insecure-db (PostgreSQL)

        environment: POSTGRES_PASSWORD=root (пароль в открытом виде и слишком простой, следовательно легко утечёт/подберётся).

        ports: "5432:5432" (база доступна с хоста/сети (в зависимости от окружения) -> увеличивает поверхность атаки).

        POSTGRES_USER=vulnuser (слабые учётки + явные креды).

        Риск:

            DL (Data Leak): высокий, если БД доступна извне или утекут креды.

            CR (Critical Risk): средний (обычно БД сама по себе хост не ломает, но может стать точкой входа в приложение/данные).

    2. app (python)

        APP_SECRET_KEY=hardcoded-in-env (секрет хранится в compose -> утечка)

        DB_URL=postgresql://vulnuser:root@insecure-db...(пароль прямо в строке подключения)

        volumes: ./app:/app:rw (контейнер может менять файлы приложения на хосте)

        Риск:

            DL: высокий (секреты и дебаг-данные).

            CR: средний, но могу предположить, что и высоким является (если через уязвимость в app получить управление контейнером, можно развивать атаку дальше).

    ### Риски vulnerable-app.yml
    
    1. vulnerable-web

        privileged: true (контейнер получает расширенный доступ к хосту -> резко растёт шанс компрометации)

        cap_add: [ALL] (максимальные capabilities -> больше возможностей атаковать ядро/хост)

        network_mode: host (сеть контейнера тут является сетью хоста -> легче перехватывать/слушать сервисы, обходить изоляцию)

        pid: host (контейнер видит процессы хоста)

        security_opt: apparmor:unconfined и seccomp:unconfined (отключаются защитные профили)

        volumes: /:/hostroot:rw (полный доступ к ФС хоста на запись -> можно читать или изменять системные файлы)

        volumes: /var/run/docker.sock:/var/run/docker.sock (доступ к Docker API, можно запускать любые контейнеры, монтировать, и т.д.)

        секреты в environment (ADMIN_PASSWORD, DB_PASSWORD, FLAG) - утечка секретов

        image: nginx:latest (тут лучше фиксировать дайджест)

        Риск:

            CR: очень высокий (компрометация хоста максимально вероятна при успешной атаке на контейнер).

            DL: очень высокий (секреты и доступ к хостовой файловой системе).

    2. debug-shell
        
        privileged: true, network_mode: host, pid: host, user: "0:0"

        ports: "22:22" и включён root login по паролю

        пароль (SSH_PASSWORD=password) и chpasswd в команде

        /:/hostroot:rw

        Риск:

            CR: очень высокий (по факту закрепление в хосте, можно назвать бэкдором).

            DL: очень высокий (доступ к данным хоста).

    ### Меры снижения рисков

        Какие меры можно применить:

            1. Секреты вынести из compose, например в .env. 

            2. Убрать privileged и cap_add: ALL. Использовать cap_drop: [ALL] и добавлять только нужные.

            3. Запускать процессы не от root.

            4. Не монтировать корень хоста (/:/hostroot) и любые системные директории хоста.

            5. Запретить docker.sock внутри контейнеров (не монтировать /var/run/docker.sock).

            6. Ограничить ресурсы: память/CPU/pids.

            7. Сделать FS read-only, использовать tmpfs для /tmp и runtime-каталогов.

            8. Запретить host namespaces (network_mode: host, pid: host — убрать).

            9. Фиксировать версии образов, а не latest.

- [x] 8. Сделайте анализ уязвимостей из сгенерированных файлов .odt, .xslx и опишите их в отчете. Файлы конвертируются в эти директории

    - **docker/docker-bench-security:latest:** 
        3 Critical уязвимости (пакеты musl, musl-utils, libseccomp) — признак устаревшей базы в образе bench (сканер тоже контейнер). Инструменты аудита надо периодически обновлять/пересобирать, иначе они сами несут CVE.

    - **postgres:16-alpine:** 
        4 High + 8 Medium (по stdlib v1.24.6 и т.п.). Базовый образ содержит пакеты/компоненты, требующие обновления (правильно: pin версии, регулярный rebuild, использовать патченные теги, CI-скан).

    - **nginx:alpine:** 1 Medium (пакет c-ares). "c-ares: c-ares: Denial of Service due to query termination after maximum attempts"

    - **python:3.11-alpine:** 1 Medium (уязвимость в pip). "Title": "pip: pip missing checks on symbolic link extraction"

- [x] 9. Подготовьте отчет `gist`.
- [x] 10. Почистите кеш от `venv` и остановите уязвимостей приложение, почистите контейнера

```bash
$ rm -rf venv
$ docker-compose -f demo-vulnerable-app.yml down
$ docker system prune -f
```

***
