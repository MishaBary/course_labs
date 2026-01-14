<div align="center">
<h1><a id="intro">Лабораторная работа №7</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> 
<img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> 
<img src="https://img.shields.io/badge/Contributor-Барышев_М._С.-8b9aff" alt="Contributor Badge"></a>

<img src="https://img.shields.io/badge/Semgrep-220000?logo=semgrep&logoColor=white" alt="Semgrep">
<img src="https://img.shields.io/badge/Checkov-000000?logo=checkov&logoColor=white" alt="Checkov">
<img src="https://img.shields.io/badge/OWASP-Dependency--Check-000000?logo=owasp&logoColor=white" alt="OWASP">
<img src="https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white" alt="Python">
<img src="https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white" alt="Docker">

</div>

***

Данная лабораторная работа посвещена изучению аудита безопасности исходного кода приложения на статический анализ, включая првоерки зависимости. Мы рассмотрим как работать с `Semgrep`, `Checkov`, `Dependency Check` и правилами для них. Аналогично познакомися с `maven`. Мы разберем как проверить конфигурации безопасности и выявить их не корректность, как произвести чекап.


***

## Задание

- [x] 1. Разверните и подготовьте окружение для уязвимого приложения

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r vulnerable-app/requirements.txt
```

- [x] 2. Запустите уязвимое приложение

```bash
$ docker-compose -f docker-compose.yml up -d --build # http://localhost:8080

--build пересобирает образ приложения из vulnerable-app/Dockerfile.

-d запускает в фоне.
```

- [x] 3. Запустите SAST Semgrep и проанализируйте выведенный лог в консоли и опишите логику правил для `semgrep-rules.yml` исходя из паттернов, которые используются. Отчет будет в директории SAST

```bash
$ semgrep --config sast/semgrep-rules.yml \
  --json \
  --output sast/semgrep-report.json \
  vulnerable-app/

Semgrep — это инструмент статического анализа исходного кода (SAST), который работает по принципу поиска шаблонов (patterns) в AST (Abstract Syntax Tree) программы.

```
**Логика правил sast/semgrep-rules.yml**


Основные группы проверок:

1) SQL Injection

    Поиск динамической сборки SQL-строки `("...'"+ user + "...", f-string и т.д.)`

    Смысл: если пользовательский ввод попадает в SQL без параметров → возможна SQLi.

2) Command Injection / RCE

  `os.system(...)` и опасные subprocess вызовы `(["sh","-c", ...])`

  Смысл: попадание пользовательских параметров в shell-команду → выполнение произвольных команд.

3) LFI / Path Traversal

  `open(path, "r")` где path берётся из query params

  Смысл: чтение /etc/passwd, приватных ключей, конфигов и т.д.

4) Unsafe deserialization

  `pickle.loads(...)`

  Смысл: pickle небезопасен для недоверенных данных → возможен RCE.

5) Eval

  `eval(...)` на пользовательском вводе

  Смысл: выполнение произвольного Python-кода.

6) Reflected XSS

  Вставка q напрямую в HTML `(f"<h1>{q}</h1>")`

  Смысл: XSS через параметры запроса.

7) Hardcoded secrets

  Поиск паттернов вида DB_PASSWORD = "..." и секретов в YAML

  Смысл: утечка секретов, компрометация БД/сервисов.

8) Debug / Verbose logging

  `app.run(..., debug=True), logging.basicConfig(level=logging.DEBUG)`

  Смысл: раскрытие внутренней информации, трассировки, окружения.


- [x] 4. Запустите SAST Checkov по Dockerfile, compose и проанализируйте выведенный лог в консоли и опишите логику правил для `checkov-config.yaml` по `Docker`. Отчет будет в директории SAST

```bash
$ checkov \
  --framework dockerfile \
  --file vulnerable-app/Dockerfile docker-compose.yml \
  --output json \
  --output-file-path sast/checkov-report.json \
  --soft-fail


Checkov сканирует IaC/Docker на небезопасные конфигурации.

--soft-fail = даже если найдены проблемы, exit code будет 0 (удобно для лабораторных/CI).
```
**Проблемы:**

- CKV_DOCKER_2 — HEALTHCHECK отсутствует
Checkov требует добавить HEALTHCHECK в Dockerfile, чтобы контейнер можно было мониторить (оркестратор/compose понимал состояние контейнера).

- CKV_DOCKER_3 — USER отсутствует (контейнер работает под root)
Требование: запускать приложение не от root, а от отдельного пользователя.

Чтобы закрыть обе проблемы, в Dockerfile:

- создание пользователя (например appuser)

- переход на него через USER appuser

- HEALTHCHECK (например через curl на http://localhost:8080/)


- [x] 5. Подготовка зависимостей Java и Maven‑скан для проведения SCA. Отчеты будут в директории SCA. Будет ошибка, которую надо поправить, что бы уязвимости определялись или добавить дополнительные уязвимости для их вывода в отчете

```bash
$ cd sca
$ ./dependency-check.sh --update # обновление и поставка базы NVD API
$ mvn dependency:resolve
$ mvn dependency:copy-dependencies -DoutputDirectory=./lib # зависимости из $ pom.xml как jar в ./lib
$ mvn org.owasp:dependency-check-maven:check || true # Maven-плагин OWASP
```

**На одном из этапов возникала типовая проблема**

Maven plugin не мог работать без локальной базы (NVD DB), когда autoupdate выключен, а базы ещё нет.
Решение:

  - выполнить предварительное обновление базы через ./dependency-check.sh --update

  - и/или включить autoUpdate=true и указать dataDirectory, nvdApiKey в pom.xml.

Найденные уязвимые зависимости: 

- commons-httpclient-3.1.jar
  CVE: CVE-2012-5783, CVE-2020-13956

- groovy-all-2.1.6.jar
  CVE: CVE-2015-3253, CVE-2016-6814, CVE-2020-17521
  (есть CVSS 9.8 — критично)

- jackson-annotations-2.4.0.jar
  CVE: CVE-2018-1000873

- jackson-core-2.4.6.jar
  CVE: CVE-2018-1000873

- jackson-databind-2.4.6.jar

Очень много CVE (включая критичные):

- CVE-2017-17485 (9.8)

- CVE-2020-9547 (9.8)

- CVE-2020-9548 (9.8)

- CVE-2020-8840 (9.8)


- [x] 6. Запустите SCA CLI OWASP Dependency-Check для уязвимого приложения. Отчеты будут в директории SCA. Опишите как работает сканирование SCA для `pom.xml` и `app.py`

**Как работает SCA для pom.xml**

Dependency-Check анализирует:

- зависимости, подтянутые Maven (.m2) или собранные в sca/lib/*.jar

- извлекает координаты пакетов (groupId/artifactId/version)

- сверяет версии с базами уязвимостей (NVD и др.)

- формирует отчёт по CVE и CVSS.

**Как работает сканирование “для app.py”**

Сканирует Python-зависимости из requirements.txt, проверяет версии пакетов на наличие известных уязвимостей

- [x] 7. Соберите единый отчет из всех сканирований в виде `html`, `csv`, `json`

```bash
$ bash sca/generate_unified_report.sh
```

- [x] 8. Проанализируйте все уязвимости и обьясните для SAST Checkov сработки статуса `Unknown`. Классифицируйте их и укажите какие не должны быть в отчетах. Внесите исправления и запустите повторное сканирование и убедитесь, что они устранены. Приложите исправленный файл и отчет без уязвимостей

В Checkov статус UNKNOWN появляется, когда проверка:

- требует рантайм-контекста, которого нет в статике (например, значения подставляются переменными окружения/внешним CI),

- или правило не применимо к текущему типу файла/ресурса,

- или Checkov не может корректно собрать граф/контекст (редко, но бывает на сложных IaC). 

Исправления под Checkov:

- Добавить пользователя и запуск не от root:

    ```bash
    RUN useradd -m appuser
    USER appuser
    ```

- Добавить HEALTHCHECK:

  ```bash
  HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1',8080)); s.close()"
  ```

- [x] 9. Опишите выведенные уязвимости для SAST Semgrep и принцип их работы. Поправьте скрипт `app.py`. Запустите повторное сканирование и убедитесь, что они устранены. Приложите исправленный файл `app.py` и отчет без уязвимостей.

  ### SQL Injection

  **Исходный код:**

  ```python
  query = f"SELECT id, name, email FROM users WHERE name = '{username}'"
  rows = cur.execute(query).fetchall()
  ```

  **Принцип уязвимости**

  SQL-инъекция возникает, когда пользовательский ввод напрямую включается в SQL-запрос. Злоумышленник может передать, например:

  ```
  ' OR 1=1 --
  ```

  и получить доступ ко всем записям БД.

  **Как это обнаруживает Semgrep**

  Правило ищет:
  - SQL-запросы, собранные через f-string или конкатенацию
  - отсутствие параметризованных плейсхолдеров (?, %s)

  **Исправление**

  Использование параметризованных запросов:

  ```python
  cur.execute(
      "SELECT id, name, email FROM users WHERE name = ?",
      (username,)
  )
  ```

  ### Reflected XSS

  **Исходный код (уязвимый):**

  ```python
  html = f"<h1>Results for: {q}</h1>"
  return make_response(html, 200)
  ```

  **Принцип уязвимости**

  Reflected XSS возникает, когда пользовательский ввод возвращается в HTML без экранирования. Злоумышленник может передать:

  ```html
  <script>alert(1)</script>
  ```

  и выполнить JavaScript в браузере жертвы.

  **Как это обнаруживает Semgrep**

  Правило ищет:
  - формирование HTML через f-string
  - вставку параметров запроса без экранирования

  **Исправление**

  Безопасные варианты:
  - экранирование (html.escape)
  - возврат JSON вместо HTML

  Пример:

  ```python
  from html import escape
  html = f"<h1>Results for: {escape(q)}</h1>"
  ```

  ### Command Injection (RCE)

  **Исходный код (уязвимый):**

  ```python
  cmd = f"ping -c 1 {host}"
  os.system(cmd)
  ```

  **Принцип уязвимости**

  Command Injection позволяет выполнить произвольные команды ОС, например:

  ```
  127.0.0.1; rm -rf /
  ```

  **Как это обнаруживает Semgrep**

  Правило реагирует на:
  - `os.system(...)`
  - передачу пользовательских данных в shell-команды

  **Исправление**

  Использование subprocess.run без shell и с валидацией:

  ```python
  subprocess.run(["ping", "-c", "1", host], check=True)
  ```

  ### Arbitrary File Read (LFI / Path Traversal)

  **Исходный код (уязвимый):**

  ```python
  path = request.args.get("path", "/etc/passwd")
  with open(path, "r") as f:
      data = f.read()
  ```

  **Принцип уязвимости**

  Позволяет читать произвольные файлы системы:
  - `/etc/passwd`
  - конфиги
  - ключи

  **Как это обнаруживает Semgrep**

  Правило ищет:
  - `open(...)`
  - путь, полученный из пользовательского ввода

  **Исправление**

  Ограничение директорией (allowlist):

  ```python
  BASE_DIR = "/app/files"
  safe_path = os.path.abspath(os.path.join(BASE_DIR, path))
  if not safe_path.startswith(BASE_DIR):
      abort(403)
  ```

  ### Unsafe Deserialization (pickle)

  **Исходный код (уязвимый):**

  ```python
  obj = pickle.loads(bytes.fromhex(data))
  ```

  **Принцип уязвимости**

  pickle выполняет код при десериализации. Передача специально сформированных данных → RCE.

  **Как это обнаруживает Semgrep**

  Прямой паттерн:

  ```
  pattern: pickle.loads(...)
  ```

  **Исправление**

  Полное удаление или замена на безопасный формат (JSON):

  ```python
  import json
  obj = json.loads(data)
  ```

  ### Использование eval на пользовательском вводе

  **Исходный код (уязвимый):**

  ```python
  result = eval(expr)
  ```

  **Принцип уязвимости**

  `eval()` выполняет любой Python-код:

  ```python
  __import__("os").system("id")
  ```

  **Как это обнаруживает Semgrep**

  Явный паттерн:

  ```
  pattern: eval(...)
  ```

  **Исправление**

  Удаление eval или строгое ограничение допустимых операций:

  ```python
  import ast
  node = ast.parse(expr, mode="eval")
  result = eval(compile(node, "<expr>", "eval"), {"__builtins__": {}})
  ```

  ### Hardcoded Secrets

  **Исходный код (уязвимый):**

  ```python
  DB_PASSWORD = "SuperSecret123"
  ```

  **Принцип уязвимости**

  Секреты в коде:
  - легко утекут в git
  - не подлежат ротации
  - компрометируют систему

  **Как это обнаруживает Semgrep**

  Правила ищут:
  - строки `PASSWORD = "..."`
  - secret, token, key

  **Исправление**

  Использование переменных окружения:

  ```python
  DB_PASSWORD = os.getenv("DB_PASSWORD")
  ```

  ### Debug Mode и утечка информации

  **Исходный код (уязвимый):**

  ```python
  app.config["DEBUG"] = True
  @app.route("/debug")
  def debug():
      return {"headers": headers, "env_sample": env}
  ```

  **Принцип уязвимости**

  - утечка переменных окружения
  - трассировки ошибок
  - конфигурации сервиса

  **Как это обнаруживает Semgrep**

  Проверки:
  - `DEBUG = True`
  - возврат `os.environ`

  **Исправление**

  - отключение debug
  - удаление debug-endpoint

- [x] 10. Доработайте SCA уязвимости, что бы они только остались в фиинальной версии отчетов.
- [x] 11. Проверьте себя по найденным сработкам анализаторов и так вы сможете помочь себе разобраться в ситуации, если возникнут сложности

```bash
$ bash cheat_check_yuorself.sh
```

- [x] 12. Делайте все коммиты на соответствующих шагах, далее заливайте изменения в удаленный репозиторий.
- [x] 13. Подготовьте отчет `gist`.
- [x] 14. Почистите кеш от `venv` и остановите уязвимое приложение

```bash
$ deactivate
$ rm -rf venv
$ docker-compose -f ххх down
$ docker-compose -f docker-compose.yml down
$ docker system prune -f
```

***

## Материал

- SAST Static Application Security Testing — это статический анализ исходного кода, шаблонов и конфигураций на наличие уязвимостей без выполнения приложения, где:

> - Проверяются исходники, конфиги, Dockerfile, IaC‑файлы, шаблоны, но код не запускается
> - Инструменты SAST ищут небезопасные конструкции SQL‑инъекции, XSS, небезопасное использование криптографии, жёстко заданные секреты и т.п., сравнивая код с набором правил и паттернов
> - Подходит на ранних стадиях разработки: ошибки находят до деплоя, прямо на этапе коммита или CI

- SCA Software Composition Analysis — анализ сторонних библиотек, зависимостей и компонентов, которые приложение использует, где:

> - Целью является поиск уязвимостей и проблем в сторонних пакетах
> - Инструменты строят «список компонентов» SBOM, сопоставляют версии библиотек с базами уязвимостей NVD, GitHub Advisories и др., а также показывают, какие зависимости нужно обновить

- Semgrep используется для анализа исходного кода и конфигураций по набору правил, где:

> - Работает по принципу «структурного grep»: ищет не просто строки, а языковые конструкции if, функции, вызовы библиотек, поэтому хорошо подходит для поиска уязвимых паттернов в Python, Java, JavaScript и т.д.
> - Поддерживает готовые правила, в том числе по OWASP Top 10, и кастомные, которые можно описать в YAML

- Checkov ориентирован на инфраструктуру как код (IaC) и Docker, где:

> - Анализирует Terraform, CloudFormation, Kubernetes‑манифесты, Dockerfile и другие инфраструктурные файлы на ошибки конфигурации, которые могут привести к уязвимостям, как открытые порты, небезопасные политики, отключённая проверка сертификатов и т.п.
> - Подходит для автоматической проверки Docker/IaC в пайплайнах, чтобы не пропускать небезопасные настройки в образах и инфраструктуре

- OWASP Dependency‑Check для поиска уязвимостей в зависимостях проекта, где

> - Анализирует используемые библиотеки Maven‑зависимости, JAR‑файлы, Python‑пакеты и др., сопоставляет их с базами уязвимостей и выдаёт список известных проблем для конкретных версий по CVE

***