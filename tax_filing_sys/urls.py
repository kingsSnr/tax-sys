"""
URL configuration for tax_filing_sys project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path
from users import views as user_views
from taxes import views as tax_views
from compliance import views as compliance_views
from reports import views as report_views
from django.contrib.auth import views as auth_views

from django.urls import path, re_path
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', user_views.login_view, name='login'),
    path('logout/', user_views.logout_view, name='logout'),
    path('', user_views.index_view, name='index'),
    path('compliance-check/', compliance_views.check_compliance_view, name='compliance_check'),
    path('generate-report/<int:tax_record_id>/', report_views.generate_report_view, name='generate_report'),

    re_path(r'^accounts/login/$', lambda request: redirect('/')),

    path('calculate-tax/', tax_views.calculate_tax_view, name='calculate_tax'),
    path('tax-list/', tax_views.tax_list_view, name='tax_list'),
    path('delete-tax/<int:tax_id>/', tax_views.delete_tax_view, name='delete_tax'),
]