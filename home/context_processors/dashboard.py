from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from datetime import datetime, date
from django.db.models.functions import ExtractMonth, ExtractWeekDay
from django.db.models import Sum, Avg
from solidPayApp.models import (
    USDPaymentRequest,
    nonEmptyWallets
)

# Create your views here.

def dashboard(request):

    current_year = timezone.now().year
    monthly_sales = USDPaymentRequest.objects.filter(fullfilled=True, requestDate__year=current_year)

    monthly_sales = monthly_sales.annotate(month=ExtractMonth('requestDate'))
    monthly_sales = monthly_sales.values('month').annotate(total_pending=Sum('pendingAmountUSD')).order_by('month')



    query = USDPaymentRequest.objects.filter(fullfilled=True, requestDate__year=current_year)

    weekly_sales = query.annotate(weekDay=ExtractWeekDay('requestDate'))
    weekly_sales = weekly_sales.values('weekDay').annotate(total_pending=Sum('pendingAmountUSD')).order_by('weekDay')

    total_revenue = USDPaymentRequest.objects.filter(fullfilled=True).aggregate(sum_pending=Sum('pendingAmountUSD'))['sum_pending']
    if total_revenue is None:
        total_revenue = 0

    today = timezone.now().date()
    sum_today = USDPaymentRequest.objects.filter(fullfilled=True, requestDate__date=today).aggregate(sum_pending=Sum('pendingAmountUSD'))['sum_pending']
    if sum_today is None:
        sum_today = 0

    failed_transactions = nonEmptyWallets.objects.filter(refunded=False).aggregate(sum_failed=Sum('balance'))['sum_failed']

    average_transaction = USDPaymentRequest.objects.filter(fullfilled=True).aggregate(average=Avg('pendingAmountUSD'))['average']

    recent_activity = query.order_by('-requestDate')[:8]

    current_month = timezone.now().month
    current_month_count = query.filter(requestDate__month=current_month).count()

    refunded_transactions = nonEmptyWallets.objects.filter(refunded=True, date__year=current_year)
    refunded_transactions = refunded_transactions.annotate(month=ExtractMonth('date'))
    refunded_transactions = refunded_transactions.values('month').annotate(total_refunded=Sum('balance')).order_by('month')

    context = {
        'monthly_sales': monthly_sales,
        'weekly_sales': weekly_sales,
        'total_revenue': total_revenue,
        'sum_today': sum_today,
        'failed_transactions': failed_transactions,
        'average_transaction': average_transaction,
        'recent_activity': recent_activity,
        'current_month_count': current_month_count,
        'refunded_transactions': refunded_transactions,
    }

    return context