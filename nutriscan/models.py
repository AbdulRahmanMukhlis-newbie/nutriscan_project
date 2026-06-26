from django.db import models
from django.contrib.auth.models import User # <-- Tambahkan ini

class JadwalMakan(models.Model):
    # Hubungkan jadwal dengan user yang sedang login
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='jadwal_makan') 
    
    WAKTU_CHOICES = [
        ('Sarapan', 'Sarapan'),
        ('Makan Siang', 'Makan Siang'),
        ('Makan Malam', 'Makan Malam'),
        ('Cemilan', 'Cemilan'),
    ]
    
    tanggal = models.DateField()
    waktu = models.CharField(max_length=20, choices=WAKTU_CHOICES)
    menu = models.CharField(max_length=200)
    kalori = models.IntegerField(help_text="Estimasi kalori")

    def __str__(self):
        return f"{self.user.username} - {self.tanggal} - {self.waktu}"