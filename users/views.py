
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required
from compliance.models import ComplianceCheck
from reports.models import Report
from taxes.models import TaxRecord

from django.shortcuts import render, redirect
from django.db.models import Sum

def index_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    total_income_tax = TaxRecord.objects.filter(user=request.user).aggregate(total_income=Sum('income'))['total_income'] or 0
    total_vat = TaxRecord.objects.filter(user=request.user).aggregate(total_vat=Sum('vat'))['total_vat'] or 0
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




def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = None

        # Fetch username associated with the email
        try:
            username = User.objects.get(email=email).username
            user = authenticate(request, username=username, password=password)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            print("Invalid email or password")

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'User does not exist')
            return redirect('index')


    return render(request, 'index.html')

def logout_view(request):
    logout(request)
    return redirect('index')


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_email = request.POST.get('new_email')
        new_password = request.POST.get('new_password')
        repeat_password = request.POST.get('repeat_password')

        user = request.user

        # Check if the new passwords match
        if new_password != repeat_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('change-password')

        # Check if the old password is correct
        if not user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('change-password')

        if new_email != user.email and User.objects.filter(email=new_email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('change-password')

        user.email = new_email
        user.set_password(new_password)
        user.save()

        update_session_auth_hash(request, user)

        messages.success(request, 'Your email and password were successfully updated!')
        return redirect('dashboard')

    else:
        return render(request, 'change_password.html')
