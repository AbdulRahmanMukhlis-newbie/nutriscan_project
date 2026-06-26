from django.db import models

class JadwalMakan(models.Model):
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
        return f"{self.tanggal} - {self.waktu}: {self.menu}"