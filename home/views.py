from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.db.models.functions import ExtractMonth, ExtractWeekDay
from django.db.models import Sum, Avg
from solidPayApp.models import (
    USDPaymentRequest,
    nonEmptyWallets
)

# Create your views here.

def index(request):

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

    failed_transactions = nonEmptyWallets.objects.aggregate(sum_failed=Sum('balance'))['sum_failed']

    average_transaction = USDPaymentRequest.objects.filter(fullfilled=True).aggregate(average=Avg('pendingAmountUSD'))['average']

    print(average_transaction)


    context = {
        'monthly_sales': monthly_sales,
        'weekly_sales': weekly_sales,
        'total_revenue': total_revenue,
        'sum_today': sum_today,
        'failed_transactions': failed_transactions,
        'average_transaction': average_transaction
    }

    # Page from the theme 
    return render(request, 'pages/index.html', context)
