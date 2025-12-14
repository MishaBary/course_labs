FROM python:3.11-slim AS builder
WORKDIR /hello
COPY requirements.txt .
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

FROM python:3.11-slim 
WORKDIR /hello
COPY --from=builder /wheels /wheels 
COPY requirements.txt .
RUN pip install --no-index --find-links=/wheels -r requirements.txt
COPY hello.py .

ENV PYTHONUNBUFFERED=1
CMD ["python", "hello.py"]
# -:
#  Контейнер запускается под пользователем root - надо добавить USER
#  python:3.11-slim может изменяться - digest
#  Каталог /wheels остаётся в финальном образе - много инфы о контейнере
# +:
#  Установка зависимостей из локальных wheel-пакетов
#  Разделение этапов сборки и исполнения
#  Минимальный базовый образ
