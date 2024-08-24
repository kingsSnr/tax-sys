from django.db import models

# Create your models here.
from django.db import models

class ComplianceRule(models.Model):
    description = models.TextField()
    is_active = models.BooleanField(default=True)

class ComplianceCheck(models.Model):
    tax_record = models.ForeignKey('taxes.TaxRecord', on_delete=models.CASCADE)
    rule = models.ForeignKey(ComplianceRule, on_delete=models.CASCADE, null=True, blank=True) 
    is_compliant = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)