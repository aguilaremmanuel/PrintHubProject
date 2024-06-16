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

def main_page (request):
    return render(request, 'main-page.html')

def shop_dashboard(request):
    shop_id = request.session.get('shop_id')
    if shop_id:

        folders = ShopFolder.objects.filter(folder_id=shop_id) 

        return render(request, 'shop/shop-dashboard.html', {'folders': folders})
    else:
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
        ShopFolder.objects.create(name=folder_name, folder_id=shop)

    return redirect('shop_dashboard')

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
            folder = UserFolder.objects.get(user=user_id)
        except User.DoesNotExist:
            UserFolder.objects.create(folder_parent=shop_folder, user=user)

        if shop_folder:
            folder_no = shop_folder.folder_no
        else:
            folder_no = None

        return render(request, 'user/user-upload-files.html')
    elif int(shop_folder_count) > 1:
        return render(request, 'user/shop-multiple-folder.html', shop_info)

    return redirect('user_dashboard')