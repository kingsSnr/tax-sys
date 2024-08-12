from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from compliance.models import ComplianceCheck
from reports.models import Report
from taxes.models import TaxRecord
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ComplianceCheck, ComplianceRule
from taxes.models import TaxRecord

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import ComplianceCheck
from taxes.models import TaxRecord

@login_required
def index_view(request):
    total_income_tax = TaxRecord.objects.filter(user=request.user).aggregate(total_income=models.Sum('income'))['total_income'] or 0
    total_vat = TaxRecord.objects.filter(user=request.user).aggregate(total_vat=models.Sum('vat'))['total_vat'] or 0
    compliance_issues_count = ComplianceCheck.objects.filter(tax_record__user=request.user, is_compliant=False).count()
    total_reports = Report.objects.filter(tax_record__user=request.user).count()

    recent_tax_records = TaxRecord.objects.filter(user=request.user).order_by('-date_created')[:5]

    context = {
        'total_income_tax': total_income_tax,
        'total_vat': total_vat,
        'compliance_issues_count': compliance_issues_count,
        'total_reports': total_reports,
        'recent_tax_records': recent_tax_records,
    }

    return render(request, 'index.html', context)


from decimal import Decimal

def check_compliance_view(request):
    if request.method == 'POST':
        tax_record_id = request.POST.get('tax_record_id')

        try:
            tax_record = TaxRecord.objects.get(id=tax_record_id, user=request.user)
        except TaxRecord.DoesNotExist:
            messages.error(request, 'No TaxRecord matches the given ID.')
            return redirect('compliance_check')

        if tax_record.vat > 0:
            expected_vat = tax_record.income * Decimal('0.16')
            if tax_record.vat == expected_vat:
                compliant = True
                message = 'VAT is compliant'
                messages.success(request, message)
            else:
                compliant = False
                message = f'VAT is not compliant. Expected {expected_vat}, but got {tax_record.vat}.'
                messages.error(request, message)

        elif tax_record.income > 0:
            expected_income_tax = tax_record.income * Decimal('0.30')
            if tax_record.income == expected_income_tax:
                compliant = True
                message = 'Income tax is compliant'
                messages.success(request, message)
            else:
                compliant = False
                message = f'Income tax is not compliant. Expected {expected_income_tax}, but got {tax_record.income}.'
                messages.error(request, message)

        else:
            compliant = False
            message = 'No valid tax type found for compliance check.'
            messages.error(request, message)

        ComplianceCheck.objects.create(
            tax_record=tax_record,
            rule=None,
            is_compliant=compliant,
            notes=message
        )

        return redirect('compliance_check')

    return render(request, 'compliance_check.html')
