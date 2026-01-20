from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('donate/', views.donate),
    path('login/', views.common_login),
    path('payment/update/', views.update_payment), 
    path('donations/<int:user_id>/', views.donation_history),
    path('admin/summary/', views.admin_summary),
    path('admin/donations/', views.admin_all_donations),
    path('admin/donations/user/<str:email>/', views.admin_user_donations),
    path('admin/users/', views.admin_users_list),
    path("payment/razorpay/create/", views.create_razorpay_order),
    path("admin/export/users/", views.export_users_csv),
    path("admin/export/donations/", views.export_donations_csv),

]
