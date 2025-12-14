# Этап 1: сборка зависимостей
FROM python:3.11-slim AS builder
WORKDIR /hello

# Копируем файл с зависимостями
COPY requirements.txt .

xx# Устанавливаем зависимости в отдельную директорию wheelhouse для кеширования
RUN pip install --upgrade pip && pip wheel --wheel-dir=/wheels -r requirements.txt

# Этап 2: запускаемый образ
FROM python:3.11-slim
WORKDIR /hello

# Создаём непривилегированного пользователя
RUN useradd -m appuser

# Копируем файл с зависимостями
COPY --from=builder /wheels /wheels
COPY requirements.txt .

# Устанавливаем зависимости из wheel-пакетов и удаляем из финальной версии
RUN pip install --no-index --find-links=/wheels -r requirements.txt && rm -rf /wheels

# Копируем исходный код приложения
COPY new.py .

# Переменные окружения для улучшенной работы Python
ENV PYTHONUNBUFFERED=1
ENV SDL_VIDEODRIVER=dummy

# Запускаем приложение
USER appuser
CMD ["python", "new.py"]

#add USER, no-graphic mode and del /wheels in final image`s version
