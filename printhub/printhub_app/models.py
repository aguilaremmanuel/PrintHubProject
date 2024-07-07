from django.db import models
from django.contrib.auth.hashers import make_password, check_password as check_password_hash
import random
import os
from django.utils.deconstruct import deconstructible
from django.conf import settings

@deconstructible
class UploadToUserFolder(object):
    def __call__(self, instance, filename):
        folder_name = f'{instance.file_parent.folder_parent.folder_id.shop_id}/{instance.file_parent.folder_parent.folder_no}/{instance.file_parent.user_folder_no}'
        
        temp = filename.replace(' ', '_')
        filename = temp

        # Ensure the directory exists
        full_path = os.path.join(settings.MEDIA_ROOT, folder_name)
        if not os.path.exists(full_path):
            os.makedirs(full_path)

        # Extract base name and extension without altering spaces
        base_name, extension = os.path.splitext(filename)
        #base_name = os.path.basename(base_name)  # Get just the filename part
        # Check for existing files with the same base name
        
        existing_files = [f for f in os.listdir(full_path) if os.path.isfile(os.path.join(full_path, f))]

        # Determine the new filename

        if filename in existing_files:
            count = 1
            filename = f"{base_name}{count}{extension}"

            print(filename)
            while filename in existing_files:
                count += 1
                filename = f"{base_name}{count}{extension}"
        else:
            # Check for existing files with similar names
            similar_names = [f for f in existing_files if f.startswith(base_name)]

            # If there are similar names with the same extension
            if any(name.endswith(extension) for name in similar_names):
                count = 1
                filename = f"{base_name}{count}{extension}"
                while filename in existing_files:
                    count += 1
                    filename = f"{base_name}{count}{extension}"

        return folder_name + '/'+ filename
        
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
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        db_table = 'user_folder'

class UserFile(models.Model):
    user_file_no = models.BigAutoField(primary_key=True)
    file = models.FileField(upload_to=UploadToUserFolder())
    file_parent = models.ForeignKey(UserFolder, on_delete=models.CASCADE)
    paper_color = models.CharField(max_length=10, null=True)
    page_number = models.CharField(max_length=10, null=True)
    custom_page_size = models.CharField(max_length=10, null=True)
    file_type = models.CharField(max_length=10, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    actual_page_size = models.CharField(max_length=10, null=True, blank=True)
    page_count = models.IntegerField(null=True, blank=True)

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