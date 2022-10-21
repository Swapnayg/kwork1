release: python manage.py makemigrations kworkapp && python manage.py makemigrations && python manage.py migrate
web: daphne mainKwork.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channel_layer --settings=mainKwork.settings -v2