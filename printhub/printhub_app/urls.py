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
    
    path('user/signup/', views.user_signup, name='user_signup'),            # user signup page
    path('user/login/', views.user_login, name='user_login'),               # user login page
    path('user/logout/', views.user_logout, name='user_logout'),            # user logout page
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),   # user dashboard page
    path('user/dashboard/join-a-shop', views.user_join_shop, name="user_join_shop"),
    path('user/dashboard/redirecting', views.user_redirect_when_shop_clicked, name="user_redirect_when_shop_clicked"),
    path('user/dashboard/upload', views.user_upload_file, name="user_upload_file"),
    path('user/dashboard/upload-files', views.user_upload_files, name="user_upload_files"),
    path('user/dashboard/test-upload', views.user_test_upload, name="user_test_upload"),
    path('user/dashboard/uploadinggg', views.t_upload_files, name="t_upload_files"),
]
