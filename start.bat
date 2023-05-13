call .\djolowin-env\Scripts\activate

start 

celery -A djolowin worker -l info
celery -A djolowin beat -l info
stripe listen --forward-to localhost:8000/currency/stripe-webhook/
```