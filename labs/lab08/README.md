<div align="center">
<h1><a id="intro">Лабораторная работа №8</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Baryshev_M._S.-8b9aff" alt="Contributor Badge"></a></div>

***

Данная лабораторная работа посвящена динамическому анализу безопасности web‑приложений DAST с использованием OWASP ZAP. Вы развернёте уязвимое приложение в Docker, проведете ручное тестирование по инструкции для понимания принципа и логики работы, далее выполните автоматическое сканирование, проанализируете отчёт и опишете уязвимости как и каким образом они реализуются. Аналогично вы проанализируете риски ИБ и предложите меры защиты, внесете необходимые исправления.

Для сдачи данной работы также будет требоваться ответить на дополнительыне вопросы по описанным темам.

***

## Структура репозитория лабораторной работы

```bash
lab08
├── dast
│   ├── convert_reports.py
│   ├── zap_scan.sh
│   └── zap-baseline.conf
├── docker-compose.yml
├── README.md
├── requirements.txt
└── vulnerable-app
    ├── app.py
    ├── Dockerfile
    ├── files
    │   └── secret.txt
    └── requirements.txt
```

***

## Материал

- DAST Dynamic Application Security Testing обеспечивает тестирование «чёрного ящика», когда сканер не знает исходного кода и взаимодействует с приложением как внешний клиент:
    -  Отправляет `HTTP`‑запросы 
    -  Анализирует ответы 
    -  Пытается воспроизвести реальные атаки `XSS`, `SQLi`, уязвимости в заголовках, слабую авторизацию и т.д. 

> В отличие от `SAST`/ `SCA`, здесь обязательно нужно живое, запущенное приложение (стенд), к которому есть сетевой доступ и разрешить доступ сканеру
> Инструмент ведёт себя как автоматизированный атакующий: обходит страницы, подставляет полезные нагрузки payloads и фиксирует подозрительные ответы

### OWASP ZAP

Особенности:
- Чёрный ящик: анализ идёт по внешнему интерфейсу `HTTP`/`HTTPS`
- Фокус на эксплуатацию: `SQLi`, `XSS`, `LFI`/ `RFI`, небезопасные заголовки, слабые cookies, открытые админки и т.д. Сканировать как простыми профилями baseline scan, так и агрессивными активными проверками

    > - Автоматически обходить сайт `spider`/ `crawler` и находить новые эндпоинты (входные точки)
    > - Выполнять пассивный анализ - заголовки, `cookies`, версии серверов, утечки данных и активные атаки `XSS`, `SQLi` и др.

- Формировать отчёты в форматах `HTML`, `JSON`, `XML` для дальнейшего анализа и интеграции в `CI/CD`

### Ремарка

Мы используем `owasp/zap2docker-stable` и CLI‑скрипт `zap_scan.sh` для сканирования по URL `http://localhost:8080/` уязвимого приложения Flask. Скрипт запускает `baseline‑скан`, сохраняет отчёты и передаёт JSON на генерацию `ODT/XLSX`.

***

## Задание

- [x] 1. Разверните и подготовьте окружение для уязвимого приложения

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt && vulnerable-app/requirements.txt 
```

- [x] 2. Запустите уязвимое приложение

```bash
$ docker-compose up -d --build  # http://localhost:8080
```

- [x] 3. Проверьте доступность приложения

```bash
$ curl -i http://localhost:8080
┌──(venv)─(lullaby㉿kali)-[~/course_labs/labs/lab08]
└─$ curl -i http://localhost:8080 
HTTP/1.1 200 OK
Server: Werkzeug/2.2.3 Python/3.11.14
Date: Tue, 13 Jan 2026 14:08:02 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 625
Set-Cookie: session=guest-session-id; Path=/
Connection: close
    <h1>Vulnerable DAST Demo App</h1>
    <p>Пример уязвимого приложения для лабораторной по DAST.</p>
    <ul>
      <li><a href="/echo?msg=Hello">Reflected XSS / echo</a></li>
      <li><a href="/search?username=admin">SQL Injection / search</a></li>
      <li><a href="/login">Небезопасный логин</a></li>
      <li><a href="/profile">Профиль (зависит от cookie)</a></li>
      <li><a href="/admin">«Админка» без нормальной авторизации</a></li>
      <li><a href="/files/">Directory listing</a></li>
    </ul>
```

- [x] 4. Проведите ручное исследование уязвимостей и опишите почему такое происходит, каким образом реализуются уязвимости и дайте им определение
- [x] 4.1. `/echo` - проверить отражение параметра  `msg`  в `HTML` и использовать `payload` вида  `<script>alert('XSS')</script>` зафиксировав его поведение

```bash
http://localhost:8080/echo?msg=<script>alert('hack with XSS')</script>

```

- [x] 4.2. `/search` - проверить обычный запрос  `?username=admin` и использовать строку  `?username=admin' OR '1'='1` зафиксировав его поведение описав признак SQLi

```bash
http://localhost:8080/search?username=admin
Поиск пользователя

Запрос: SELECT id, username, role FROM users WHERE username = 'admin'

    3 – admin (admin)

http://localhost:8080/search?username=admin' OR '1'='1

Запрос: SELECT id, username, role FROM users WHERE username = 'admin' OR '1'='1'

    3 – admin (admin)
    4 – user (user)

```

- [x] 4.3. `/login` - войти под  `admin`  и  `user` проверив логику на открытые пароли и простые SQL‑запросы
- [x] 4.4. `/profile` - изменить `cookie  role`  на  `admin`  через `DevTools` → `Application` → `Cookies` и обновить  `/profile` (возможно создать `cookie`
- [x] 4.5. `/admin` -  проверить, что доступ запрещён без `cookie  role=admin` и далее подделать `cookie`, что «админка» открывается путем изменения через `DevTools`. **Подсказка:** доступ завязан на значение cookie, без подписи/ токена/ серверной проверки.

```bash
Admin panel

Секретные настройки приложения (демо).

    DEBUG: true
    FEATURE_FLAG: experimental_mode

```
- [x] 4.6. `/files/` - просмотрите `directory listing` и откройте один из файлов убедившись, что оно выводится

```bash
http://localhost:8080/files/secret.txt

SECRET_TOKEN=123456
```

- [x] 5. Доработайте по пп 4 лабораторную работу развив их содержимое, которое может выводиться (мин 1 пример)

```bash
Поиск пользователя

Ввод: admin' OR '1'='1

SQL-запрос: SELECT id, username, role FROM users WHERE username = 'admin' OR '1'='1'

Найдено записей: 2
⚠ Возможный признак SQL Injection: возвращено более одной записи

    3 — admin (admin)
    4 — user (user)

Payload: ?username=admin' OR '1'='1
```
- [x] 6. Поставьте `OWASP ZAP` и стяните образ конкртеной версии для него

```bash
$ brew install --cask zap
$ docker pull ghcr.io/zaproxy/zaproxy:stable
```

- [x] 7. Задайте переменные окружения для работы скриптов

```bash
$ export ZAP_IMAGE=ghcr.io/zaproxy/zaproxy:stable
$ TARGET_URL="${TARGET_URL:-http://host.docker.internal:8080}"
```

- [x] 8. Запустите скрипт автоматического сканирования DAST `OWASP ZAP`

```bash
$ ./zap_scan.sh
```

- [x] 9. Изучите сгенерированные отчеты в `dast/reports` и опишите риски ИБ для них, без сценариев, так как ранее вы видели часть из их реализации

### Medium

    Content Security Policy (CSP) Header Not Set (на /, /echo, /profile, /robots.txt, /sitemap.xml)
    Риск: без CSP браузер не ограничивает источники скриптов/контента → XSS и инъекции проще эксплуатировать.

    Missing Anti-clickjacking Header (на /, /echo, /login, /profile, /search)
    Риск: приложение можно встраивать в iframe и атаковать clickjacking (выманивание кликов).

    Source Code Disclosure – SQL (на /search?username=admin)
    Причина в твоём коде: ты показываешь сформированный SQL-запрос в HTML (<code>{{ query }}</code>). ZAP это трактует как утечку внутренней реализации/запросов к БД.

### Low

    Cookie No HttpOnly Flag (cookie session)
    Риск: если произойдёт XSS, JS сможет прочитать cookie (кража сессии).

    Cookie without SameSite Attribute (cookie session)
    Риск: проще CSRF/перенос сессии в кросс-сайтовых запросах.

    X-Content-Type-Options Header Missing
    Риск: MIME-sniffing, иногда ведёт к XSS при неправильной раздаче контента.

    Permissions Policy Header Not Set
    Риск: браузер не ограничивает доступ к сенсорам/фичам.

    Server Leaks Version Information via "Server" header
    Риск: раскрытие версий Werkzeug/Python - облегчает подбор эксплойтов.

    Insufficient Site Isolation Against Spectre Vulnerability
    Риск: отсутствие COOP/COEP/CORP заголовков (browser isolation hardening).

### Informational

    Authentication Request Identified (ZAP заметил страницу логина)

    Session Management Response Identified (заметил управление сессией/куки)

    Information Disclosure – Sensitive Information in URL (информативно — параметры в URL)

    Storable and Cacheable Content / Non-Storable Content (кеширование)

### Итог

    - Отсутствие security-headers (CSP, anti-clickjacking, X-Content-Type-Options, Permissions-Policy, COOP/COEP/CORP), что повышает шанс XSS, clickjacking и снижает изоляцию контента в браузере.

    - Утечка версий через Server, которая упрощает разведку и подбор уязвимостей под конкретные версии.

    - Cookie без HttpOnly/SameSite, которая повышает риск кражи сессии при XSS и CSRF-атак.

    - SQL Source Code Disclosure - раскрывает внутреннюю структуру SQL-запросов и БД (помогает атакующему точнее строить SQLi).

    - Кеширование - на приватных страницах желательно Cache-Control: no-store, чтобы данные не оставались в браузере/прокси.

- [x] 10. Внесите исправления по данному отчету `DAST` для `vulnerable-app/app.py`

**Что исправил:**

    - Реализованы параметризованные SQL-запросы, устранена SQL Injection

    - Убрано отображение SQL-запросов в ответе (устранено раскрытие кода)

    - Включено экранирование пользовательского ввода (устранён XSS)

    - Переведена авторизация на серверную сессию, устранена подделка cookie

    - Ограничен доступ к /admin и /files

    - Добавлены основные security-headers (CSP, X-Frame-Options, X-Content-Type-Options, Permissions-Policy)

    - Усилена политика cookies (HttpOnly, SameSite)

    - Для чувствительных страниц включён Cache-Control: no-store

    High: 0

    Medium: 0

    Low: 1

    Informational: 4

- [x] 11. Делайте все необходимые коммиты по шагам и отправляйте изменения в удалённый репозиторий
- [x] 12. Подготовьте отчет `gist`.
- [x] 14. Почистите кеш от `venv` и остановите уязвимое приложение

```bash
$ deactivate
$ rm -rf venv
$ docker-compose -f docker-compose.yml down
$ docker system prune -f
```

***

## Рекомендации

- `XSS` на `echo` — отражение входных данных без экранирования
>   Заменить прямую подстановку строки на безопасный рендер с автоматическим экранированием или ручной фильтрацией
- `SQL Injection` на `search` — небезопасная конкатенация строки запроса
>   Перейти на параметризованные запросы `sqlite` и передача параметров отдельным аргументом, включая отказа от конкатенации `SQL`‑строк с пользовательским вводом
- Небезопасные `cookies` (`session`, `user`, `role` ) — без  `Secure`,  `HttpOnly`, `SameSite`
>   Задать флаги  `HttpOnly`,  `Secure` (если `HTTPS`), `SameSite=Lax/ Strict`
- Отсутствие основных `security‑headers` (`X-Frame-Options`, `X-Content-Type-Options`, `Content-Security-Policy` и т.д.)
- Усилить авторизацию на  `admin`  из-за доступа по подделанному cookie
- `Directory listing` на  `files`
> Ограничить список отдаваемых ресурсов, либо скрыть `directory listing`, либо добавить проверки и фильтрацию путей.

***
