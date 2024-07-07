from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from .forms import *
from django.utils import timezone
from .backends import *
from django.contrib import messages
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, FileResponse, Http404
import json
from django.urls import reverse
import os
from django.core.files.storage import default_storage
from django.conf import settings
from pdf2image import convert_from_path
import cv2
import numpy as np
from docx import Document
import fitz
from PIL import Image, ImageFilter, ImageOps
import pytesseract
import io
import comtypes.client
import pythoncom
from django.template.loader import render_to_string
from django.db.models import Q
import shutil

def main_page (request):
    return render(request, 'main-page.html')

def shop_dashboard(request):
    shop_id = request.session.get('shop_id')
    if shop_id:

        folder_details = []

        folders = ShopFolder.objects.filter(folder_id=shop_id) 
        
        hasNoShopRate = request.session.get('raise_no_shop_rate')

        for folder in folders:

            for_payment = 0
            for_printing = 0
            for_claiming = 0
            
            user_folders = UserFolder.objects.filter(folder_parent=folder)

            for user_folder in user_folders:
                if user_folder.status == 'for payment':
                    for_payment = for_payment + 1
                elif user_folder.status == 'for printing':
                    for_printing = for_printing + 1
                elif user_folder.status == 'for claiming':
                    for_claiming = for_claiming + 1
            

            folder_detail = {
                'folder_no' : folder.folder_no,
                'folder_name' : folder.name,
                'for_payment' : for_payment,
                'for_printing' : for_printing,
                'for_claiming' : for_claiming
            }

            folder_details.append(folder_detail)

        if hasNoShopRate:
            del request.session['raise_no_shop_rate']
            return render(request, 'shop/shop-dashboard.html', {'folder_details': folder_details, 'raiseNoShopRate': True})
        
        return render(request, 'shop/shop-dashboard.html', {'folder_details': folder_details})
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

def shop_payment(request, folder_name, folder_no):

    context = {
        'folder_name' : folder_name,
        'folder_no' : folder_no,
    }

    return render(request, 'shop/shop-payment.html', context)

def update_folders_for_payment(request, folder_name, folder_no):
    user_folders_payment = UserFolder.objects.filter(status='for payment', folder_parent_id=folder_no).order_by('time_upload')
    context = {
        'user_folders_payment': user_folders_payment,
        'folder_name' : folder_name,
        'folder_no': folder_no,
    }
    html = render_to_string('partials/for_payment_folders.html', context)
    return JsonResponse({'html': html})

def update_folders_for_printing(request, folder_name, folder_no):
    user_folders_printing = UserFolder.objects.filter(
        Q(status='for printing') | Q(status='printing'), 
        folder_parent_id=folder_no).order_by('time_upload')
    
    context = {
            'user_folders_printing': user_folders_printing,
            'folder_name': folder_name,
            'folder_no': folder_no,
        }
    html = render_to_string('partials/for_printing_folders.html', context)
    return JsonResponse({'html': html})

def shop_customer_paid(request, folder_name, folder_no, user_folder_no):
    user_folder = UserFolder.objects.get(user_folder_no=user_folder_no)
    setattr(user_folder, "status", "for printing")
    user_folder.save()

    return redirect('shop_payment', folder_name=folder_name, folder_no=folder_no)

def shop_printing(request, folder_name, folder_no):
    context = {
        'folder_name': folder_name,
        'folder_no': folder_no,
    }
    return render(request, 'shop/shop-printing.html', context)

def shop_mark_as_done(request, folder_name, folder_no, user_folder_no):

    user_folder = UserFolder.objects.get(user_folder_no=user_folder_no)
    setattr(user_folder, "status", "for claiming")
    user_folder.save()

    return redirect('shop_printing', folder_name=folder_name, folder_no=folder_no)

def shop_printing_user_files(request, folder_name, folder_no, user_folder_no):

    user_folder = UserFolder.objects.get(user_folder_no=user_folder_no)
    setattr(user_folder, 'status', 'printing')
    user_folder.save()
    user_files = UserFile.objects.filter(file_parent_id = user_folder_no)
    
    folder_path = ""
    folder_path += str(user_files[0].file_parent.folder_parent.folder_id_id) + '/'
    folder_path += str(user_files[0].file_parent.folder_parent_id) + '/'
    folder_path += str(user_files[0].file_parent_id) + '/'


    context = {
        'folder_name': folder_name,
        'folder_no': folder_no,
        'user_folder_no': user_folder_no,
        'file_details': [],
    }

    username = user_files[0].file_parent.user.username
    context['username'] = username

    for file in user_files:

        file_detail = {}

        temp = str(file.file)

        filename = temp.replace(folder_path, '')

        file_detail['file_no'] = file.user_file_no
        file_detail['filename'] = filename
        page_count = file.page_count
        file_detail['page_count'] = page_count

        base_name, extension = os.path.splitext(temp)
        file_detail['file_type'] = extension

        if file.custom_page_size == 'none':
            size = file.actual_page_size
            file_detail['file_size'] = size.upper()
        else:
            size = file.custom_page_size
            file_detail['file_size'] = size.upper()

        if file.paper_color == 'colored':
            file_detail['paper_color'] = 'Colored'
        else:
            file_detail['paper_color'] = 'Black & White'

        file_detail['file_permission'] = file.file_type

        context['file_details'].append(file_detail)

    return render(request, 'shop/shop-printing-user-files.html', context)

def shop_view_file(request, file_no):
    
    file = UserFile.objects.get(user_file_no = file_no)
    file_page_urls = []
    temp = file.file.name

    image_path = ""
    split_file_path = temp.split('/') 
    
    for folder in split_file_path[:-1]:
        image_path += folder + '/'
    
    image_path += str(file_no) + '/'

    page_count = file.page_count

    for page in range(1, page_count+1):
        temp = image_path + 'page_' + str(page) + '.png'
        file_page_urls.append(temp)

    file_page_urls = [settings.MEDIA_URL + url for url in file_page_urls]

    context = {
        'file_page_urls': file_page_urls
    }

    html = render_to_string('partials/for_viewing_file.html', context)
    filename = split_file_path[len(split_file_path)-1]
    base_name, extension = os.path.splitext(filename)
    print(extension)
    return JsonResponse({'html': html, 'filename': filename, 'extension': extension})

def shop_download_file(request, file_no):

    user_file = UserFile.objects.get(user_file_no = file_no)
    temp = str(user_file.file)
    split_file_path = temp.split('/')    
    filename = split_file_path[len(split_file_path)-1]

    file_path = os.path.join(settings.MEDIA_ROOT, temp)
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True, filename=filename)
    else:
        raise Http404("File does not exist")

def shop_claiming(request, folder_name, folder_no):

    user_folders_claiming = UserFolder.objects.filter(status='for claiming', folder_parent_id=folder_no)

    context = {
        'user_folders_claiming': user_folders_claiming,
        'folder_name': folder_name,
        'folder_no': folder_no
    }

    return render(request, 'shop/shop-claiming.html', context)

def shop_mark_as_claimed(request, folder_name, folder_no, user_folder_no):
    user_folder = UserFolder.objects.get(user_folder_no=user_folder_no)
    setattr(user_folder, 'status', 'finished')
    setattr(user_folder, 'total_price', None)
    setattr(user_folder, 'time_upload', None)
    user_folder.save()

    user_files = UserFile.objects.filter(file_parent_id=user_folder.user_folder_no)
    user_files.delete()

    user_folder_path = user_folder.folder_parent.folder_id_id + '/' + str(user_folder.folder_parent.folder_no) + '/' + str(user_folder.user_folder_no) + '/'
    user_folder_path = os.path.join(settings.MEDIA_ROOT, user_folder_path)
    if os.path.exists(user_folder_path) and os.path.isdir(user_folder_path):
        shutil.rmtree(user_folder_path)

    return redirect('shop_claiming', folder_name=folder_name, folder_no=folder_no)

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

        user_id = request.session.get('id') # request user id
        shop_folder = ShopFolder.objects.filter(folder_id=shop_id).first() # kuhain yung nag iisang shop folder
        
        try:
            user = User.objects.get(id=user_id) # kunin si user para gumawa ng folder nya sa shop folder
        except User.DoesNotExist:
            messages.error(request, 'User not found.')

        try:
            user_folder = UserFolder.objects.get(user=user) # if existing na folder ni user kay shop, kuhain

            if user_folder.status == 'for payment' or user_folder.status == 'for printing' or user_folder.status == 'for claiming':
                request.session['file_parent'] = user_folder.user_folder_no 
                return redirect('user_cash_payment')
            else:
                setattr(user_folder, 'status', 'for uploading')
                user_folder.save()
            
        except UserFolder.DoesNotExist:
            user_folder = UserFolder.objects.create(folder_parent=shop_folder, user=user) # gumawa ng bagong folder if wala pa folder kay shop

        request.session['file_parent'] = user_folder.user_folder_no 
        
        try:
            user_files = UserFile.objects.filter(file_parent=user_folder.user_folder_no)
            user_filenames = [{'user_file_no': file.user_file_no, 
                            'file_name': file.file.name.replace(str(file.file_parent.folder_parent.folder_id.shop_id)+'/'+str(file.file_parent.folder_parent.folder_no)+'/'+str(file.file_parent.user_folder_no)+'/', ''), 
                            'file_extension': file.file.name.split('.')[-1]} for file in user_files]
        except UserFile.DoesNotExist:
            messages.error(request, 'User not found.')
            user_filenames = []

        context = {
            'user_filenames': user_filenames,
        }

        return render(request, 'user/user-upload-files.html', context)
    
    elif int(shop_folder_count) > 1:
        return render(request, 'user/shop-multiple-folder.html', shop_info)

    return redirect('user_dashboard')

def user_upload_files(request):
    
    if request.method == 'POST' and request.FILES['file']:

        user_folder_no = request.session.get('file_parent')
        
        uploaded_file = request.FILES['file']
        paper_color = request.POST.get('paper-color')
        page_number = request.POST.get('page-number')
        if page_number == 'all-pages':
            pass
        else:
            selected_pages = request.POST.getlist('custom-page')
            page_number = ','.join(selected_pages)

        if 'file-type' in request.POST:
            file_type = 'private'
        else:
            file_type = 'regular'

        custom_page_size = request.POST.get('custom-page-size') # None if non custom
        
        if custom_page_size is None:
            custom_page_size = "none"

        file_parent = UserFolder.objects.get(user_folder_no=user_folder_no)
        new_file = UserFile(file=uploaded_file, custom_page_size=custom_page_size, file_type=file_type, page_number=page_number, paper_color=paper_color, file_parent=file_parent)
        new_file.save()

        return redirect('user_upload_files')
    
    user_folder_no = request.session.get('file_parent')

    try:
        user_files = UserFile.objects.filter(file_parent=user_folder_no)
        user_filenames = [{'user_file_no': file.user_file_no, 
                           'file_name': file.file.name.replace(str(file.file_parent.folder_parent.folder_id.shop_id)+'/'+str(file.file_parent.folder_parent.folder_no)+'/'+str(file.file_parent.user_folder_no)+'/', ''), 
                           'file_extension': file.file.name.split('.')[-1]} for file in user_files]
    except UserFile.DoesNotExist:
        messages.error(request, 'User not found.')
        user_filenames = []

    context = {
        'user_filenames': user_filenames,
    }

    return render(request, 'user/user-upload-files.html', context)

def user_payment_page(request):
    
    user_folder_no = request.session.get('file_parent')

    try:
        user_files = UserFile.objects.filter(file_parent=user_folder_no)
    except UserFile.DoesNotExist:
        messages.error(request, 'User not found.')

    totalBill = 0
    hasPrice = True

    for file in user_files:
        if file.price is None:
            hasPrice = False
            break
        else:
            totalBill += file.price

    if hasPrice:
        context = {
            'totalBill': totalBill,
        }
        return render(request, 'user/user-payment-page.html', context)

    for file in user_files:

        base_name, extension = os.path.splitext(str(file.file))
        file_path = os.path.join(settings.MEDIA_ROOT, str(file.file))

        if extension == '.pdf':
            price = process_pdf(file, file_path)
            totalBill += price
            setattr(file, "price", price)
            file.save()
        else:
            file_path = convert_to_pdf(file_path)
            price = process_pdf(file, file_path)
            totalBill += price
            setattr(file, "price", price)
            file.save()

    context = {
        'totalBill': totalBill,
    }

    return render(request, 'user/user-payment-page.html', context)

def process_pdf(file, file_path):

    if file.paper_color == 'colored':
        actual_page_size = get_pdf_page_size(file_path)
        setattr(file, "actual_page_size", actual_page_size)
        file.save()

        if file.page_number == 'all-pages':
            pages = analyze_pdf_with_all_pages(file_path, file)
        else:
            custom_pages = file.page_number
            custom_pages = [int(n) for n in custom_pages.split(',')]
            pages = analyze_pdf_with_custom_pages(file_path, custom_pages, file)

        price = 0

        for page_status in pages.values():
            
            if file.custom_page_size == 'none':
                file_rate_type = actual_page_size + "_"
            else:
                file_rate_type = file.custom_page_size + "_"

            if page_status == 'bw':
                file_rate_type += page_status
            else:
                file_rate_type += 'colored_' + page_status
            
            shop_id = file.file_parent.folder_parent.folder_id.shop_id
            shop = Shop.objects.get(shop_id=shop_id)
            shop_rate = ShopRate.objects.get(shop_id=shop)

            price += getattr(shop_rate, file_rate_type, None) 

        return price
            
    else:

        split_file_path = file_path.split('/')
        file_images_path = ""
        file_images_path += split_file_path[0] + '/'
        file_images_path += split_file_path[1] + '/'
        file_images_path += split_file_path[2] + '/'
        file_images_path += str(file.user_file_no)

        output_dir = os.path.join(settings.MEDIA_ROOT, file_images_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        doc = fitz.open(file_path)

        actual_page_size = get_pdf_page_size(file_path)
        setattr(file, "actual_page_size", actual_page_size)
        file.save()
        
        file_rate_type = "_bw"

        if file.custom_page_size == 'none':
            file_rate_type = actual_page_size + file_rate_type
        else:
            file_rate_type = file.custom_page_size + file_rate_type

        if file.page_number == 'all-pages':
            page_count = get_pdf_page_count(file_path)

            for page_num in range(len(doc)):
                page = doc.load_page(page_num)
                pix = page.get_pixmap()
                image = Image.open(io.BytesIO(pix.tobytes()))
                image = ImageOps.grayscale(image)
                if file.file_type == 'private':
                    image = image.filter(ImageFilter.GaussianBlur(radius=5))
                image_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
                image.save(image_path)

        else:

            custom_pages = file.page_number
            page_count = len((custom_pages).split(','))
            custom_pages = [int(n) for n in custom_pages.split(',')]

            for page_num in range(len(doc)):
                if (page_num+1) in custom_pages:
                    page = doc.load_page(page_num)
                    pix = page.get_pixmap()
                    image = Image.open(io.BytesIO(pix.tobytes()))
                    image = ImageOps.grayscale(image)
                    if file.file_type == 'private':
                        image = image.filter(ImageFilter.GaussianBlur(radius=5))
                    image_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
                    image.save(image_path)

        setattr(file, 'page_count', page_count)
        file.save()

        shop_id = file.file_parent.folder_parent.folder_id.shop_id
        shop = Shop.objects.get(shop_id=shop_id)
        shop_rate = ShopRate.objects.get(shop_id=shop)

        price = getattr(shop_rate, file_rate_type, None) * page_count
        return price
    
def user_cash_payment(request):

    user_folder_no = request.session.get('file_parent')
    files = UserFile.objects.filter(file_parent=user_folder_no)

    if files[0].file_parent.total_price:
        context = {
            'totalBill': files[0].file_parent.total_price,
            'user_folder_no': files[0].file_parent.user_folder_no
        }
    else:
        totalBill = 0
        for file in files:
            totalBill += file.price

        context = {
            'totalBill': totalBill,
            'user_folder_no' : files[0].file_parent.user_folder_no
        }

        user_folder = UserFolder.objects.get(user_folder_no = user_folder_no)
        setattr(user_folder, "status", "for payment")
        setattr(user_folder, "total_price", totalBill)
        setattr(user_folder, "time_upload", timezone.now())
        user_folder.save()

    return render(request, 'user/user-pay-at-counter.html', context)

def check_payment_status(request, user_folder_no):
    user_folder = UserFolder.objects.get(user_folder_no=user_folder_no)
    paid = "true" if user_folder.status == 'for printing' else "false"
    return JsonResponse({'paid': paid})

def analyze_pdf_with_custom_pages(file_path, custom_pages, file):

    split_file_path = file_path.split('/')
    file_images_path = ""
    file_images_path += split_file_path[0] + '/'
    file_images_path += split_file_path[1] + '/'
    file_images_path += split_file_path[2] + '/'
    file_images_path += str(file.user_file_no)

    output_dir = os.path.join(settings.MEDIA_ROOT, file_images_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    results = {}
    doc = fitz.open(file_path)
    page_count = 0
    for page_num in range(len(doc)):
        if (page_num+1) in custom_pages:
            page_count = page_count + 1
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            image = Image.open(io.BytesIO(pix.tobytes()))
            if file.file_type == 'private':
                image = image.filter(ImageFilter.GaussianBlur(radius=5))

            image_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
            image.save(image_path)
            page_data = count_colored_pixels(image)
            results[page_num+1] = get_page_status(page_data)

    setattr(file, "page_count", page_count)
    file.save()
    return results

def analyze_pdf_with_all_pages(file_path, file):

    split_file_path = file_path.split('/')
    file_images_path = ""
    file_images_path += split_file_path[0] + '/'
    file_images_path += split_file_path[1] + '/'
    file_images_path += split_file_path[2] + '/'
    file_images_path += str(file.user_file_no)

    output_dir = os.path.join(settings.MEDIA_ROOT, file_images_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    results = {}
    doc = fitz.open(file_path)
    page_count = 0
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        image = Image.open(io.BytesIO(pix.tobytes()))

        if file.file_type == 'private':
            image = image.filter(ImageFilter.GaussianBlur(radius=5))
    
        image_path = os.path.join(output_dir, f'page_{page_num + 1}.png')
        image.save(image_path)
        page_data = count_colored_pixels(image)

        results[page_num + 1] = get_page_status(page_data)
        page_count = page_count + 1
    
    setattr(file, "page_count", page_count)
    file.save()
    return results

def get_page_status(page_data):
    colored_pixels = page_data[0]
    total_pixels = page_data[1]

    percentage = round((colored_pixels / total_pixels) * 100)

    if colored_pixels == 0:
        return 'bw'
    elif percentage >= 41 and percentage <= 100:
        return 'high'
    elif percentage >= 21 and percentage <= 40:
        return 'medium'
    else:
        return 'low'

def count_colored_pixels(image):
    page_data = []
    colored_pixels = 0
    total_pixels = 0
    # Convert image to LAB color space
    image = image.convert('LAB')

    # Define thresholds
    L_threshold_black = 30  # Near-black luminance threshold
    L_threshold_white = 225  # Near-white luminance threshold
    A_threshold = 10  # Color component threshold for A
    B_threshold = 10

    for pixel in image.getdata():
        L, A, B = pixel
        # Check if pixel is not near white or black
        if not (L < L_threshold_black or L > L_threshold_white):
            # Ensure the pixel has significant color component
            if abs(A - 128) > A_threshold or abs(B - 128) > B_threshold:
                colored_pixels += 1
        total_pixels += 1

    page_data.append(colored_pixels)
    page_data.append(total_pixels)
    return page_data

def get_pdf_page_size(filepath):
    doc = fitz.open(filepath)
    page = doc[0]
    page_width = round(page.rect.width, 2)
    page_height = round(page.rect.height, 2)
    area = round((page_width * page_height), 2)

    if area == 484704.0:
        return "short"
    elif area == 501211.81:
        return "a4"
    else:
        return "long"

def get_pdf_page_count(file_path):
    doc = fitz.open(file_path)
    page_count = doc.page_count
    doc.close()
    return page_count

def convert_to_pdf(file_path):
    try:
        pythoncom.CoInitialize()  # Initialize COM
        
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False
        
        # Load the document
        doc = word.Documents.Open(file_path)
        
        # Construct the output file path
        pdf_path = os.path.splitext(file_path)[0] + ".pdf"
        
        # Save as PDF
        doc.SaveAs(pdf_path, FileFormat=17)
        doc.Close()
        word.Quit()
        
        pythoncom.CoUninitialize()  # Uninitialize COM
        
        return pdf_path
    
    except Exception as e:
        print(f"Error converting file: {e}")
        pythoncom.CoUninitialize()  # Ensure COM is properly uninitialized on error
        return None
    
def delete_file(request, user_file_no):

    try:
        file_to_delete = UserFile.objects.get(user_file_no=user_file_no)
        base_name, extension = os.path.splitext(file_to_delete.file.name)
        
        if extension == '.pdf':
            pass
        else:
            generated_pdf_file_path = os.path.join(settings.MEDIA_ROOT, base_name + ".pdf")
            if os.path.exists(generated_pdf_file_path):
                os.remove(generated_pdf_file_path)
        
        file_path = os.path.join(settings.MEDIA_ROOT, file_to_delete.file.name)

        images_path = ""
        split_file_path = base_name.split('/') 
        
        for folder in split_file_path[:-1]:
            images_path += folder + '/'

        images_path += str(file_to_delete.user_file_no) + '/'
        images_path = os.path.join(settings.MEDIA_ROOT, images_path)
        if os.path.exists(images_path) and os.path.isdir(images_path):
            shutil.rmtree(images_path)

        if os.path.exists(file_path):
            os.remove(file_path)
            
        file_to_delete.delete()

    except UserFile.DoesNotExist:
        messages.error(request, 'File not found.')
    return redirect('user_upload_files')

def user_printing_status(request, user_folder_no):
    return render(request, 'user/user-printing-status.html', {'user_folder_no': user_folder_no}) 

def check_printing_status(request, user_folder_no):
    user_folder = UserFolder.objects.get(user_folder_no=user_folder_no)

    if user_folder.status == 'for printing':
        status = 'for printing'
    elif user_folder.status == 'printing':
        status = 'printing'
    else:
        status = 'finished'

    return JsonResponse({'status': status})