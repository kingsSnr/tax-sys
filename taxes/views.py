from django.shortcuts import render, redirect
from .models import TaxRecord
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from .models import TaxRecord

def calculate_tax_view(request):
    if request.method == 'POST':
        tax_type = request.POST['tax_type']
        amount = float(request.POST['amount'])
        tax_year = int(request.POST['tax_year'])

        # Calculate tax based on type
        if tax_type == 'VAT':
            vat = amount * 0.16
            income = 0
            other_taxes = 0
        elif tax_type == 'Income':
            income = amount * 0.30
            vat = 0
            other_taxes = 0
        else:
            other_taxes = amount
            vat = 0
            income = 0

        tax_record = TaxRecord.objects.create(
            user=request.user,
            income=income,
            vat=vat,
            other_taxes=other_taxes,
            tax_year=tax_year
        )

        messages.success(request, 'Tax record added successfully.')
        return redirect('tax_list')

    return render(request, 'taxes.html')




def tax_list_view(request):
    search_query = request.GET.get('q', '')

    # Build query for filtering tax records
    tax_records = TaxRecord.objects.filter(user=request.user)

    if search_query.isdigit():
        tax_records = tax_records.filter(tax_year__exact=search_query)
    else:
        tax_records = tax_records.filter(
            Q(income__icontains=search_query) |
            Q(vat__icontains=search_query) |
            Q(other_taxes__icontains=search_query)
        )

    # Pagination
    paginator = Paginator(tax_records, 10)  # 10 records per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }

    return render(request, 'taxes.html', context)



def delete_tax_view(request, tax_id):
    tax_record = TaxRecord.objects.get(id=tax_id, user=request.user)
    tax_record.delete()
    messages.success(request, 'Tax record deleted successfully.')
    return redirect('tax_list')

