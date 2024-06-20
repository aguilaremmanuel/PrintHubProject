from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import *
from django.utils import timezone
from .backends import *
from django.contrib import messages
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from django.urls import reverse
import os
from django.core.files.storage import default_storage
import fitz

def main_page (request):
    return render(request, 'main-page.html')

def shop_dashboard(request):
    shop_id = request.session.get('shop_id')
    if shop_id:
        folders = ShopFolder.objects.filter(folder_id=shop_id) 
        
        hasNoShopRate = request.session.get('raise_no_shop_rate')
        if hasNoShopRate:
            del request.session['raise_no_shop_rate']
            return render(request, 'shop/shop-dashboard.html', {'folders': folders, 'raiseNoShopRate': True})
        return render(request, 'shop/shop-dashboard.html', {'folders': folders})
    return redirect('shop_login')  

def shop_login(request):
    shop_id = request.session.get('shop_id')
    if shop_id:
        return redirect('shop_dashboard')  
    if request.method == 'POST':
        form = ShopLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            shop = ShopBackend.authenticate(request, email=email, password=password)
            #shop.last_login = timezone.now()
            if shop is not None:
                request.session['shop_id'] = shop.shop_id
                shop.save()
                return redirect('shop_dashboard')  
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = ShopLoginForm()
    return render(request, 'shop/shop-login.html', {'form': form})

def shop_signup(request):
    if request.method == 'POST':
        form = ShopSignupForm(request.POST)
        if form.is_valid():
            shop = form.save(commit=False)
            shop.set_password(form.cleaned_data['password'])
            shop.date_registered = timezone.now()
            shop.save()
            ShopRate.objects.create(shop_id=shop)
            return redirect('shop_login')  # Redirect to shop login page after successful signup
    else:
        form = ShopSignupForm()
    return render(request, 'shop/shop-signup.html', {'form': form})

def shop_create_folder(request):
    shop_id = request.session.get('shop_id')

    if request.method == 'POST':
        folder_name = request.POST.get('name')
        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            messages.error(request, 'Shop not found.')
            return redirect('shop_dashboard')
        
            
        
        if shop.has_shop_rate:

            shop_rate = shop.shop_rate_set.first()

            null_attributes = {
            'long_colored_low': shop_rate.long_colored_low is None,
            'short_colored_low': shop_rate.short_colored_low is None,
            'a4_colored_low': shop_rate.a4_colored_low is None,
            'long_colored_medium': shop_rate.long_colored_medium is None,
            'short_colored_medium': shop_rate.short_colored_medium is None,
            'a4_colored_medium': shop_rate.a4_colored_medium is None,
            'long_colored_high': shop_rate.long_colored_high is None,
            'short_colored_high': shop_rate.short_colored_high is None,
            'a4_colored_high': shop_rate.a4_colored_high is None,
            'long_bw': shop_rate.long_bw is None,
            'short_bw': shop_rate.short_bw is None,
            'a4_bw': shop_rate.a4_bw is None,
            }

            # Check if any attribute is null
            has_nulls = any(null_attributes.values())
            print(null_attributes)

            if has_nulls:
                request.session['raise_no_shop_rate'] = True
                return redirect('shop_dashboard')
            else:
                ShopFolder.objects.create(name=folder_name, folder_id=shop)
        else:
            request.session['raise_no_shop_rate'] = True
            return redirect('shop_dashboard')

    return redirect('shop_dashboard')

def shop_prices(request):
    shop_id = request.session.get('shop_id')
    try:
        shop = Shop.objects.get(shop_id=shop_id)
    except Shop.DoesNotExist:
        messages.error(request, 'Shop not found.')

    shop_rate = shop.shop_rate_set.first()

    paper_rates = {
            'short_colored_high': shop_rate.short_colored_high,
            'a4_colored_high': shop_rate.a4_colored_high,
            'long_colored_high': shop_rate.long_colored_high,

            'short_colored_medium': shop_rate.short_colored_medium,
            'a4_colored_medium': shop_rate.a4_colored_medium,
            'long_colored_medium': shop_rate.long_colored_medium,

            'short_colored_low': shop_rate.short_colored_low,
            'a4_colored_low': shop_rate.a4_colored_low,
            'long_colored_low': shop_rate.long_colored_low,

            'short_bw': shop_rate.short_bw,
            'a4_bw': shop_rate.a4_bw,
            'long_bw': shop_rate.long_bw,
    }

    return render(request, 'shop/shop-prices.html', {'paper_rates': paper_rates})

def shop_edit_price(request):
    shop_id = request.session.get('shop_id')

    if request.method == 'POST':
        new_price = request.POST.get('new_price')
        paper_type = request.POST.get('paper_type')

        shop = Shop.objects.get(shop_id=shop_id)
        shop_rate = ShopRate.objects.get(shop_id=shop)

        setattr(shop_rate, paper_type, new_price)
        shop_rate.save()

        return redirect('shop_prices')


def shop_logout(request):
    if 'shop_id' in request.session:
        del request.session['shop_id']
    return redirect('shop_login')

def user_dashboard(request):
    username = request.session.get('username')
    if username:

        user_id = request.session.get('id')
        folder_access_users = FolderAccessUser.objects.filter(user=user_id)
        folder_access_data = []

        for access in folder_access_users:
            folder_id = access.folder_id_id
            shop_name = access.folder_id.shop_name
            shop_status = Shop.objects.get(shop_id=folder_id).shop_status
            folder_access_data.append({'shop_name': shop_name, 'folder_id': folder_id, 'shop_status': shop_status})

        return render(request, 'user/user-dashboard.html', {'folder_access_data': folder_access_data})
    
    else:
        return redirect('user_login')  

def user_signup(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data['password'])
            user.save()
            return redirect('user_login')  # Redirect to shop login page after successful signup
    else:
        form = UserSignupForm()
    return render(request, 'user/user-signup.html', {'form': form})

def user_login(request):
    username = request.session.get('username')
    if username:
        return redirect('user_dashboard')  
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = UserBackend.authenticate(request, email=email, password=password)
            if user is not None:
                request.session['username'] = user.username
                request.session['id'] = user.id
                print(request.session.get('id'))
                user.save()
                return redirect('user_dashboard')  
            else:
                form.add_error(None, 'Invalid username or password')
    else:
        form = UserLoginForm()
    return render(request, 'user/user-login.html', {'form': form})

def user_logout(request):
    if 'username' in request.session:
        del request.session['username']
        del request.session['id']
    return redirect('user_login')

def user_join_shop(request):
    if request.method == "POST":
        shop_code = request.POST.get('shop_id')
        user_id = request.session.get('id')

        try:
            shop = Shop.objects.get(shop_id=shop_code)
        except Shop.DoesNotExist:
            messages.error(request, 'The shop code you entered does not exist.')
            return redirect('user_dashboard')  
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('user_dashboard')

        if FolderAccessUser.objects.filter(folder_id=shop, user=user).exists():
            messages.info(request, 'You are already a member of this shop.')
        else:
            # Add the user to the FolderAccessUser model
            FolderAccessUser.objects.create(folder_id=shop, user=user)
            messages.success(request, 'You have successfully joined the shop.')

    return redirect('user_dashboard')

@csrf_exempt
def user_redirect_when_shop_clicked(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        shop_id = data.get('shop_id')

        try:
            shop = Shop.objects.get(shop_id=shop_id)
        except Shop.DoesNotExist:
            messages.error(request, 'The shop code you entered does not exist.')

        shop_folder_count = ShopFolder.objects.filter(folder_id=shop).count()

        

        redirect_url = reverse('user_upload_file') + f'?shop_folder_count={shop_folder_count}&shop_id={shop_id}'
        return JsonResponse({'redirect_url': redirect_url})

    return JsonResponse({'message': 'Success'})

def user_upload_file(request): 

    shop_folder_count = request.GET.get('shop_folder_count')
    shop_id = request.GET.get('shop_id')

    shop_info = {
        'shop_folder_count': shop_folder_count,
        'shop_id': shop_id,
    }

    if int(shop_folder_count) == 0:
        return render(request, 'user/shop-zero-folder.html', shop_info)
    elif int(shop_folder_count) == 1:

        user_id = request.session.get('id')
        shop_folder = ShopFolder.objects.filter(folder_id=shop_id).first()
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            messages.error(request, 'User not found.')

        try:
            user_folder = UserFolder.objects.get(user=user)
        except UserFolder.DoesNotExist:
            UserFolder.objects.create(folder_parent=shop_folder, user=user)

        file_parent = user_folder.user_folder_no

        try:
            user_files = UserFile.objects.filter(file_parent=file_parent)
        except UserFile.DoesNotExist:
            messages.error(request, 'User not found.')
            user_files = []

        user_filenames = [{'file_name': file.file.name} for file in user_files]

        context = {
            'user_folder_no': user_folder.user_folder_no,
            'user_filenames': user_filenames
        }

        return render(request, 'user/user-upload-files.html', context)
    
    elif int(shop_folder_count) > 1:
        return render(request, 'user/shop-multiple-folder.html', shop_info)

    return redirect('user_dashboard')

def user_upload_files(request):

    if request.method == 'POST':

        user_folder_no = request.POST.get('user_folder_no')

        try:
            file_parent = UserFolder.objects.get(user_folder_no=user_folder_no)
        except UserFolder.DoesNotExist:
            pass
            
        requested_files = request.FILES.getlist('files')

        for file in requested_files:
            new_file = UserFile(file=file, file_parent=file_parent)
            new_file.save()

            # Optionally, you may want to redirect to a different view after successful upload
        return render(request, 'user/user-upload-files.html', {'user_folder_no':user_folder_no})

def user_test_upload(request):
    return render (request, "user/test-upload.html")

def t_upload_files(request):
    if request.method == 'POST':

        g_file = request.FILES.getlist('user_file')
        for file in g_file:
            new_file = TestFile(file=file)
            new_file.save()
            
            file_path = os.path.join(default_storage.location, 'test_uploads', new_file.name)

    return redirect('user_test_upload')
