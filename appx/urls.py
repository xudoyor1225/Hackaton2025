# appx/urls.py # Ilovangiz nomi 'appx' deb taxmin qilinadi

from django.urls import path
from . import views


urlpatterns = [
    # Autentifikatsiya
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # Asosiy sahifalar
    path('', views.dashboard, name='dashboard'),
    path('analytics/', views.analytics, name='analytics'),
    path('scholarships/find/', views.find_scholarships, name='find_scholarships'),
    path('help-center/', views.help_center, name='help_center'),
    path('apply/', views.submit_application, name='submit_application'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('settings/profile/', views.profile_settings, name='profile_settings'),
    path('settings/security/', views.security, name='security'),

    # Admin sahifalari
    path('applications/all/', views.all_applications, name='all_applications'),
    path('manage/scholarships/', views.manage_scholarships, name='manage_scholarships'),
    path('manage/users/', views.users, name='users'),

    # API/AJAX endpointlari
    path('api/applications/<int:pk>/details/', views.application_details_api, name='application_details_api'),
    path('api/applications/<int:pk>/change-status/', views.application_change_status_api, name='application_change_status_api'),

    path('api/scholarships/create/', views.scholarship_create, name='scholarship_create'),
    path('api/scholarships/update/<int:pk>/', views.scholarship_update, name='scholarship_update'),
    path('api/scholarships/toggle-status/<int:pk>/', views.scholarship_toggle_status, name='scholarship_toggle_status'),

    path('api/users/create-update/', views.user_create_or_update, name='user_create_update'),
    path('api/users/details/<int:pk>/', views.user_get_details, name='user_get_details'),
    path('api/users/toggle-status/<int:pk>/', views.user_toggle_status, name='user_toggle_status'),

]