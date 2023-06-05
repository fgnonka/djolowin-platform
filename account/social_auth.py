from account.models import CustomUser

def create_user(backend, user, *args, **kwargs):
    if not user:
        email = kwargs['details']['email']
        user = CustomUser.objects.create_user(email=email)
    return {'user': user}