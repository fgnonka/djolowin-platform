import datetime

# Define the time window and login threshold
window_duration = datetime.timedelta(hours=6)
login_threshold = 1

# Get the current time
now = datetime.datetime.now()

# Query the login history table for each user
for user in users:
    login_times = get_login_times_for_user(user)

    # Check if the user has logged in enough times
    num_logins = 0
    for login_time in login_times:
        if now - login_time <= window_duration:
            num_logins += 1

    if num_logins >= login_threshold:
        award_reward(user)