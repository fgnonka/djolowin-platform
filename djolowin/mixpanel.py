from account.models import CustomUser

from mixpanel import Mixpanel

mp = Mixpanel("266cebd9ca2e4a46b65f23e0926719a3")

# Note: you must supply the user_id who performed the event as the first parameter.
user = CustomUser.objects.get(username="usera")
user_id = user.id
mp.track(user_id, "Signed Up", {"Signup Type": "Referral"})
