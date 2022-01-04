from django.db import models
from authentication.models import User

class Income(models.Model):

    SALARY_OPTIONS = [
        ('SALARY','SALARY'),
        ('BUSINESS', 'BUSINESS'),
        ('SIDE-HUSTLE', 'SIDE-HUSTLE'),
        ('OTHERS', 'OTHERS')
    ]
   
    source = models.CharField( choices=SALARY_OPTIONS, max_length=255)
    amount = models.DecimalField(max_digits=6,decimal_places=2,max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Income'
        ordering = ['-date']
    
    def __str__(self):
        return str(self.owner) +'s income'
    