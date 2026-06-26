from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required # <-- Untuk mengunci halaman
from .models import JadwalMakan
import requests

def beranda(request):
    return render(request, 'nutriscan/beranda.html')

def ai_rekomendasi(request):
    rekomendasi = None
    if request.method == 'POST':
        keluhan = request.POST.get('keluhan')
        target_diet = request.POST.get('target_diet')
        
        # Integrasi API DeepSeek dari dosen
        headers = {
            "Authorization": "Bearer sk-dfc7dbd65214845ab245d78cf684cb8",
            "Content-Type": "application/json"
        }
        
        prompt = f"Saya memiliki kondisi/keluhan: {keluhan} dan target diet: {target_diet}. Berikan saya rekomendasi menu makanan harian yang sehat dan analisis nutrisi singkat."
        
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "stream": False
        }
        
        try:
            response = requests.post("https://api.deepseek.com/chat/completions", headers=headers, json=payload)
            if response.status_code == 200:
                rekomendasi = response.json()['choices'][0]['message']['content']
            else:
                rekomendasi = "Maaf, terjadi kesalahan saat menghubungi AI."
        except Exception as e:
            rekomendasi = f"Error jaringan: {str(e)}"
            
    return render(request, 'nutriscan/ai_rekomendasi.html', {'rekomendasi': rekomendasi})

def rekomendasi_tempat(request):
    # Fitur 2: Rekomendasi tempat makan menggunakan Google Maps/Places API
    # Implementasi utama akan berada di bagian frontend (JavaScript) pada template
    return render(request, 'nutriscan/tempat_makan.html')

def jadwal_makan(request):
    # Fitur 3: Manajemen jadwal makan online
    jadwal = JadwalMakan.objects.all().order_by('-tanggal')
    if request.method == 'POST':
        JadwalMakan.objects.create(
            tanggal=request.POST.get('tanggal'),
            waktu=request.POST.get('waktu'),
            menu=request.POST.get('menu'),
            kalori=request.POST.get('kalori')
        )
        return redirect('jadwal_makan')
        
    return render(request, 'nutriscan/jadwal_makan.html', {'jadwal': jadwal})

# FITUR DAFTAR AKUN
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Otomatis login setelah daftar
            return redirect('beranda')
    else:
        form = UserCreationForm()
    return render(request, 'nutriscan/register.html', {'form': form})

# FITUR MASUK
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('beranda')
    else:
        form = AuthenticationForm()
    return render(request, 'nutriscan/login.html', {'form': form})

# FITUR KELUAR
def logout_view(request):
    logout(request)
    return redirect('beranda')

# UPDATE FITUR JADWAL MAKAN (Hanya untuk user yang login)
@login_required(login_url='login') # Menolak akses jika belum login
def jadwal_makan(request):
    # Hanya mengambil jadwal milik user yang sedang login
    jadwal = JadwalMakan.objects.filter(user=request.user).order_by('-tanggal')
    
    if request.method == 'POST':
        JadwalMakan.objects.create(
            user=request.user, # Pasangkan dengan user yang aktif
            tanggal=request.POST.get('tanggal'),
            waktu=request.POST.get('waktu'),
            menu=request.POST.get('menu'),
            kalori=request.POST.get('kalori')
        )
        return redirect('jadwal_makan')
        
    return render(request, 'nutriscan/jadwal_makan.html', {'jadwal': jadwal})