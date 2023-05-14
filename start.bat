call .\djolowin-env\Scripts\activate

# Start Redis server
redis-server

# Start Celery worker
celery -A djolowin worker -l info

# Start Celery beat
celery -A djolowin beat -l info

# Initiate stripe webhook listener
stripe listen --forward-to localhost:8000/currency/stripe-webhook/

# Start your Django server
python manage.py runserver
```