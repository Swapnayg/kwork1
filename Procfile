release: python manage.py makemigrations kworkapp && python manage.py makemigrations && python manage.py migrate
web: uvicorn mainKwork.asgi:application --port $PORT --host 0.0.0.0
worker: python manage.py runworker channel_layer