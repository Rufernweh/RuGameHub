
from companies.models import Company
from basket.models import Basket

def my_context_processor(request):
    context={}
    if not  request.user.is_anonymous and  Company.objects.filter(user=request.user):
        context['company']=Company.objects.get(user=request.user)
    if not request.user.is_anonymous:
        context['basket']=Basket.objects.filter(user=request.user)
            


    return context