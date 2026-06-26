from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required # <-- Untuk mengunci halaman
from .models import JadwalMakan
import requests
import os

def beranda(request):
    return render(request, 'nutriscan/beranda.html')

def ai_rekomendasi(request):
    rekomendasi = None
    if request.method == 'POST':
        keluhan = request.POST.get('keluhan')
        target_diet = request.POST.get('target_diet')
        
        # Mengambil API Key Gemini dari Render Environment
        api_key = os.environ.get("GEMINI_API_KEY")
        
        # Alamat endpoint resmi Gemini 1.5 Flash (Case-Sensitive)
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        
        headers = {"Content-Type": "application/json"}
        prompt = f"Keluhan: {keluhan}. Target diet: {target_diet}. Berikan rekomendasi menu makanan sehat harian secara singkat."
        
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=12)
            
            # Mencetak status kode ke log Render agar bisa dipantau jika error
            print(f"[LOG AI] Status Respon Server: {response.status_code}")
            
            if response.status_code == 200:
                rekomendasi = response.json()['candidates'][0]['content']['parts'][0]['text']
            else:
                # Menampilkan detail error dari Google jika bukan 200
                print(f"[LOG AI] Detail Error: {response.text}")
                rekomendasi = f"Gagal memuat rekomendasi dari AI (Status Error: {response.status_code})."
        except Exception as e:
            print(f"[LOG AI] Exception Terjadi: {str(e)}")
            rekomendasi = f"Masalah koneksi ke server AI: {str(e)}"
            
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