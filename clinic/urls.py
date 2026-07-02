from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('manage/', views.manage_content, name='manage_content'),
    path('procedure/<slug:slug>/', views.procedure_detail, name='procedure_detail'),
    path('procedure/add/', views.add_procedure, name='add_procedure'),
    path('procedure/<slug:slug>/edit/', views.edit_procedure, name='edit_procedure'),
    path('procedure/<slug:slug>/delete/', views.delete_procedure, name='delete_procedure'),
    path('procedure/<slug:slug>/add-image/', views.add_procedure_image, name='add_procedure_image'),
    path('procedure/<slug:slug>/image/<int:image_id>/edit/', views.edit_procedure_image, name='edit_procedure_image'),
    path('procedure/<slug:slug>/image/<int:image_id>/delete/', views.delete_procedure_image, name='delete_procedure_image'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('set-language/<str:lang_code>/', views.set_language, name='set_language'),
]
