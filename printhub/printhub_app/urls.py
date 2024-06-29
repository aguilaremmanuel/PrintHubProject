from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main_page, name='main_page'),                               # Main page URL
    path('shop/signup/', views.shop_signup, name='shop_signup'),            # shop signup page
    path("shop/login/", views.shop_login, name='shop_login'),               # shop login page
    path("shops/logout/", views.shop_logout, name='shop_logout'),           # shop logout
    path('shop/dashboard/', views.shop_dashboard, name='shop_dashboard'),   # shop dashboard page
    path('shop/dashboard/create-folder/', views.shop_create_folder, name="shop_create_folder"),
    path('shop/dashboard/prices/', views.shop_prices, name="shop_prices"),
    path('shop/dashboard/editing-price', views.shop_edit_price, name="shop_edit_price"),
    path('shop/dashboard/payment', views.shop_payment, name='shop_payment'),
    path('shop/dashboard/printing', views.shop_printing, name='shop_printing'),
    path('shop/dashboard/claiming', views.shop_claiming, name='shop_claiming'),

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
]
