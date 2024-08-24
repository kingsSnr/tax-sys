# reports/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from .models import Report
from taxes.models import TaxRecord
from django.db.models import Sum
from django.utils.dateparse import parse_date

def tax_summary_view(request):
    if request.method == 'POST':
        from_date = request.POST.get('from_date')
        to_date = request.POST.get('to_date')

        if from_date and to_date:
            return redirect('generate_tax_report', from_date=from_date, to_date=to_date)

    return render(request, 'tax_summary_selection.html')

def generate_tax_report_view(request, from_date, to_date):
    from_date = parse_date(from_date)
    to_date = parse_date(to_date)

    tax_records = TaxRecord.objects.filter(
        user=request.user,
        date_created__range=[from_date, to_date]
    ).order_by('date_created')

    total_tax = tax_records.aggregate(
        total_income=Sum('income'),
        total_vat=Sum('vat'),
        total_other_taxes=Sum('other_taxes'),
    )

    context = {
        'tax_records': tax_records,
        'total_income': total_tax['total_income'] or 0,
        'total_vat': total_tax['total_vat'] or 0,
        'total_other_taxes': total_tax['total_other_taxes'] or 0,
        'from_date': from_date,
        'to_date': to_date,
    }

    if request.GET.get('download') == 'pdf':
        return download_tax_report_pdf(request, context)

    return render(request, 'tax_summary.html', context)

def download_tax_report_pdf(request, context):
    template_path = 'pdf_tax_summary.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="tax_summary_{context["from_date"]}_{context["to_date"]}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
