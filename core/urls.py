
from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # Report items
    path('report/lost/', views.report_lost, name='report_lost'),
    path('report/found/', views.report_found, name='report_found'),

    # Item listing and details
    path('items/', views.item_list, name='item_list'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),

    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    # Edit and delete
    path('edit-item/<int:pk>/', views.edit_item, name='edit_item'),
    path('delete-item/<int:pk>/', views.delete_item, name='delete_item'),
]
