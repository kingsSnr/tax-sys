from django.db import models

# Create your models here.
from django.db import models
from taxes.models import TaxRecord

class Report(models.Model):
    tax_record = models.ForeignKey(TaxRecord, on_delete=models.CASCADE)
    report_file = models.FileField(upload_to='reports/')
    date_generated = models.DateTimeField(auto_now_add=True)
