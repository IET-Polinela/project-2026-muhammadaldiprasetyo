from django.db import models

class Report(models.Model):
    # Definisi pilihan status untuk workflow [cite: 19, 20]
    STATUS_CHOICES = [
        ('REPORTED', 'Reported'),
        ('VERIFIED', 'Verified'),
        ('IN PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    ]
    
    title = models.CharField(max_length=200) # [cite: 27]
    category = models.CharField(max_length=100) # [cite: 28]
    description = models.TextField() # [cite: 29]
    location = models.CharField(max_length=200) # [cite: 31]
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES, # [cite: 34]
        default='REPORTED' # [cite: 35]
    )
    
    created_at = models.DateTimeField(auto_now_add=True) # [cite: 36]

    def __str__(self):
        return self.title # [cite: 36]