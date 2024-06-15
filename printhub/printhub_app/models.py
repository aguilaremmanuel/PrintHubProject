from django.db import models
from django.contrib.auth.hashers import make_password, check_password as check_password_hash
import random


class Shop(models.Model):
    shop_id = models.CharField(max_length=6, primary_key=True)
    shop_name = models.CharField(max_length=15)
    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=15)
    date_registered = models.DateTimeField(null=True, blank=True)
    last_login = models.DateTimeField(null=True, blank=True)
    shop_status = models.CharField(max_length=15, default="open")

    def check_password(self, raw_password):
        return check_password_hash(raw_password, self.password)
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)
    
    def save(self, *args, **kwargs):
        if not self.shop_id:
            # Generate a unique 6-digit shop_id
            while True:
                shop_id = ''.join([str(random.randint(0, 9)) for _ in range(6)])
                if not Shop.objects.filter(shop_id=shop_id).exists():
                    self.shop_id = shop_id
                    break
        
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'shop_account'

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    date_registered = models.DateTimeField(null=True, blank=True)

    def check_password(self, raw_password):
        return check_password_hash(raw_password, self.password)
    
    class Meta:
        db_table = 'user_account'

class FolderAccessUser(models.Model):
    folder_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'folder_access_user'

class ShopFolder(models.Model):
    folder_no = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    folder_id = models.ForeignKey(Shop, on_delete=models.CASCADE, null=True, blank=True)
    state = models.CharField(max_length=10, null=True, blank=True, default='hidden')

    class Meta:
        db_table = 'shop_folder'

class UserFolder(models.Model):
    user_folder_no = models.BigAutoField(primary_key=True)
    status = models.CharField(max_length=20, default='for uploading')
    folder_parent = models.ForeignKey(ShopFolder, on_delete=models.CASCADE)
    time_upload = models.DateTimeField(null=True, blank=True)
    time_paid = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'user_folder'

