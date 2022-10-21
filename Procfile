release: python manage.py migrate
web: uvicorn mainKwork.asgi:application --port $PORT --host 0.0.0.0
python manage.py collectstatic --noinput
worker: python manage.py runworker channel_layer