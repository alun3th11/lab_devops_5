FROM python:3.11

WORKDIR /app

# Устанавливаем зависимости напрямую
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.30.0 \
    httpx==0.27.0 \
    pydantic-settings==2.5.0

# Копируем исходный код
COPY ./src ./src

# Запускаем приложение
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
