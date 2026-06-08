import random
from django.core.management.base import BaseCommand
from faker import Faker
from main_app.models import Report # Sudah diperbaiki sesuai models.py

fake = Faker('id_ID')

class Command(BaseCommand):
    help = 'Generate contextual fake reports'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Jumlah data')

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        
        context_data = {
            'Jalan Rusak': {
                'titles': ['Lubang Besar di Tengah Jalan', 'Aspal Mengelupas Parah'],
                'desc': 'Ditemukan kerusakan jalan yang cukup dalam.'
            },
            'Sampah': {
                'titles': ['Tumpukan Sampah Liar', 'Bau Menyengat'],
                'desc': 'Warga mengeluhkan penumpukan sampah.'
            },
            'Lampu Mati': {
                'titles': ['Penerangan Jalan Umum Mati', 'Kabel Lampu Putus'],
                'desc': 'Lampu jalan di area ini mati total.'
            },
            'Drainase': {
                'titles': ['Saluran Air Mampet', 'Drainase Meluap'],
                'desc': 'Saluran air tersumbat sedimen.'
            },
            'Keamanan': {
                'titles': ['Vandalisme Fasilitas Umum', 'Pencurian Kabel'],
                'desc': 'Dibutuhkan patroli tambahan di area ini.'
            }
        }
        
        # Sesuaikan dengan STATUS_CHOICES di models.py Anda
        status_choices = ['REPORTED', 'VERIFIED', 'IN_PROGRESS', 'RESOLVED']

        for _ in range(total):
            category = random.choice(list(context_data.keys()))
            title_template = random.choice(context_data[category]['titles'])
            
            # Menggunakan model 'Report' sesuai isi models.py
            Report.objects.create(
                title=f"{title_template} - {fake.street_name()}",
                category=category,
                description=f"{context_data[category]['desc']} Lokasi: {fake.street_address()}",
                location=f"Kecamatan {fake.city()}", 
                status=random.choice(status_choices),
            )

        self.stdout.write(self.style.SUCCESS(f'Berhasil membuat {total} laporan!'))