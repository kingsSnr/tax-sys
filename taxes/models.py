from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.db import models

class TaxRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    income = models.DecimalField(max_digits=10, decimal_places=2)
    vat = models.DecimalField(max_digits=10, decimal_places=2)
    other_taxes = models.DecimalField(max_digits=10, decimal_places=2)
    tax_year = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def calculate_total_tax(self):
        return self.income + self.vat + self.other_taxes
