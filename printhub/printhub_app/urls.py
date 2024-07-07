from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),                            # Main page URL
    path('about/',views.about_page, name='about_page'),                     # About
    path('pricing/',views.pricing_page, name='pricing_page'),               # Pricing
    path('contact/',views.contact_page, name='contact_page'),               # Contact

    path('faqs/',views.faqs_page, name='faqs_page'),                        # FAQs
    path('shop/signup/', views.shop_signup, name='shop_signup'),            # shop signup page
    path("shop/login/", views.shop_login, name='shop_login'),               # shop login page
    path("shops/logout/", views.shop_logout, name='shop_logout'),           # shop logout
    path('shop/dashboard/', views.shop_dashboard, name='shop_dashboard'),   # shop dashboard page
    path('shop/dashboard/create-folder/', views.shop_create_folder, name="shop_create_folder"),
    path('shop/dashboard/prices/', views.shop_prices, name="shop_prices"),
    path('shop/dashboard/editing-price', views.shop_edit_price, name="shop_edit_price"),
    path('shop/dashboard/payment/<str:folder_name>/<int:folder_no>/', views.shop_payment, name='shop_payment'),
    path('shop/dashboard/update-payment-folders/<str:folder_name>/<int:folder_no>', views.update_folders_for_payment, name='update_folders_for_payment'),
    path('shop/dashboard/update-printing-folders/<str:folder_name>/<int:folder_no>/', views.update_folders_for_printing, name='update_folders_for_printing'),
    path('shop/dashboard/printing/<str:folder_name>/<int:folder_no>', views.shop_printing, name='shop_printing'),
    path('shop/dashboard/printing/mark-as-done/<str:folder_name>/<int:folder_no>/<int:user_folder_no>/', views.shop_mark_as_done, name='shop_mark_as_done'),             
    path('shop/dashboard/claiming/<str:folder_name>/<int:folder_no>/', views.shop_claiming, name='shop_claiming'),
    path('shop/dashboard/payment-paid/<str:folder_name>/<int:folder_no>/<int:user_folder_no>', views.shop_customer_paid, name='shop_customer_paid'),
    path('shop/dashboard/printing-files/<str:folder_name>/<int:folder_no>/<int:user_folder_no>/', views.shop_printing_user_files, name='shop_printing_user_files'),
    path('shop/dashboard/printing/view-file/<int:file_no>/', views.shop_view_file, name='shop_view_file'),
    path('shop/dashboard/download-file/<int:file_no>/', views.shop_download_file, name='shop_download_file'),
    path('shop/dashboard/mark-as-claimed/<str:folder_name>/<int:folder_no>/<int:user_folder_no>/', views.shop_mark_as_claimed, name='shop_mark_as_claimed'),
    path('shop/dashboard/subscriptions/', views.shop_subscription, name='shop_subscription'),

    path('user/signup/', views.user_signup, name='user_signup'),            # user signup page
    path('user/login/', views.user_login, name='user_login'),               # user login page
    path('user/logout/', views.user_logout, name='user_logout'),            # user logout page
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),   # user dashboard page
    path('user/dashboard/join-a-shop', views.user_join_shop, name="user_join_shop"),
    path('user/dashboard/redirecting', views.user_redirect_when_shop_clicked, name="user_redirect_when_shop_clicked"),
    path('user/dashboard/upload', views.user_upload_file, name="user_upload_file"),
    path('user/dashboard/upload-files', views.user_upload_files, name="user_upload_files"),
    path('delete/<int:user_file_no>/', views.delete_file, name='delete_file'),
    path('user/dashboard/payment', views.user_payment_page, name="user_payment_page"),
    path('user/dashboard/cash-payment', views.user_cash_payment, name="user_cash_payment"),
    path('check_payment_status/<int:user_folder_no>/', views.check_payment_status, name='check_payment_status'),
    path('user/dashboard/printing-status/<int:user_folder_no>', views.user_printing_status, name='user_printing_status'),
    path('check_printing_status/<int:user_folder_no>/', views.check_printing_status, name='check_printing_status'),
]
