
#!/bin/bash


# Activate your virtual environment
xterm -hold -e "cd /home/djolo/Documents/djolowin-platform; source ./djolowin-env/bin/activate; bash" &

# Start Redis server
# xterm -hold -e "cd /home/djolo/Documents/djolowin-platform; redis-server" &

# Start Celery worker
xterm -hold -e "cd /home/djolo/Documents/djolowin-platform; celery -A djolowin worker -l info" &

# Start Celery beat
xterm -hold -e "cd /home/djolo/Documents/djolowin-platform; celery -A djolowin beat -l info" &

# Start stripe webhook
xterm -hold -e "cd /home/djolo/Documents/djolowin-platform; stripe listen --forward-to localhost:8000/currency/stripe-webhook/" 

# # Start your Django server
# xterm -hold -e "cd /home/djolo/Documents/djolowin-platform; python manage.py runserver"
