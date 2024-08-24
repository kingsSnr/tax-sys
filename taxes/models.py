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
    quarterly_payments = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    section_179_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_tax(self):
        total_tax = (self.income - self.section_179_deduction) + self.vat + self.other_taxes
        return max(total_tax, 0)  

    def check_quarterly_payments_compliance(self):
        estimated_annual_tax = self.calculate_total_tax() * 4  
        required_quarterly_payment = estimated_annual_tax * 0.25 * 0.9  # 90% of 25% of annual tax
        return self.quarterly_payments >= required_quarterly_payment
