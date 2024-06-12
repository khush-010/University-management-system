from django.contrib.auth.backends import BaseBackend
from dashboard.models import Users
from django.contrib.auth.hashers import check_password

class Auth(BaseBackend):
    def authentication(request,username=None,password=None):
        try:
            user = Users.objects.get(email=username)
            if check_password(password, user.password):
                return user
            return None
        except Users.DoesNotExist:
            return None
        
    def get_user(user_id):
        try:
            return Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            return None