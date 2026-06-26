# nutriscan/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('ai-rekomendasi/', views.ai_rekomendasi, name='ai_rekomendasi'),
    path('tempat-makan/', views.rekomendasi_tempat, name='tempat_makan'),
    path('jadwal/', views.jadwal_makan, name='jadwal_makan'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]