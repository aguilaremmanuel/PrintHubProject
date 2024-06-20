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

    @property
    def has_shop_rate(self):
        return self.shoprate_set.exists()

    @property
    def shop_rate_set(self):
        return self.shoprate_set

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

class UserFile(models.Model):
    user_file_no = models.BigAutoField(primary_key=True)
    file = models.FileField(upload_to='uploads/')
    file_parent = models.ForeignKey(UserFolder, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'user_file'

class ShopRate(models.Model):
    
    shop_rate_no = models.BigAutoField(primary_key=True)
    shop_id = models.ForeignKey(Shop, on_delete=models.CASCADE)
    long_colored_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_colored_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    a4_colored_low = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    long_colored_medium = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_colored_medium = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    a4_colored_medium = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    long_colored_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_colored_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    a4_colored_high = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    long_bw = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    short_bw = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    a4_bw= models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'shop_rate'

class TestFile(models.Model):
    test_file_no = models.BigAutoField(primary_key=True)
    file = models.FileField(upload_to='test_uploads/')

    class Meta:
        db_table = 'test_file'
