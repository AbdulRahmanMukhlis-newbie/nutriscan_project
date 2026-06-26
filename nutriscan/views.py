from django.shortcuts import render
import requests
from django.shortcuts import render, redirect
from .models import JadwalMakan

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