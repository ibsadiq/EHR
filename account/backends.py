from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

user = get_user_model()


class UserBackend(ModelBackend):
    def authenticate(self, request, **kwargs):
        try:
            email = kwargs["email"]
        except:
            email = kwargs["username"]
        password = kwargs["password"]
        try:
            userobj = user.objects.get(Q(email__iexact=email))
            if userobj.check_password(password) is True:
                return userobj
        except:
            pass
