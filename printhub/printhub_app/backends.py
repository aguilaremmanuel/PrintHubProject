from django.contrib.auth.backends import BaseBackend
from .models import Shop, User

class ShopBackend(BaseBackend):
    
    def authenticate(request, email=None, password=None):
        try:
            shop = Shop.objects.get(email=email)
            if shop.check_password(password):
                return shop
        except Shop.DoesNotExist:
            return None

class UserBackend(BaseBackend):

    def authenticate(request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

