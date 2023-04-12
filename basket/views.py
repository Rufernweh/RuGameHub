from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import Basket
from games.models import GameAccount
from django.shortcuts import render,redirect
from django.db.models import Sum
from companies.models import Company
# Create your views here.

def basket_view(request):
    
    gameacc=request.GET.get('gameacc')
    if not  request.user.is_anonymous and  Company.objects.filter(user=request.user):
        context['company']=Company.objects.get(user=request.user)
 
        if gameacc:
            gameacc=GameAccount.objects.get(name=gameacc)
            baskets = Basket.objects.filter(user=request.user)
            if not baskets.filter(gameacc=gameacc):
                Basket.objects.create(gameacc=gameacc,user=request.user)
            else:
                return redirect('basket:basket')
        total_price = baskets.aggregate(Sum('gameacc__price'))['gameacc__price__sum'] or 0
        context = {
            'basket': baskets,
            'total_price': total_price
        }
    else:
        return redirect('users:login')
        
    return render(request,'games/store-cart.html',context)


@login_required(login_url='/users/login/')
def remove_gameacc(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        print(product_id)
        try:
            basket = Basket.objects.get(user=request.user, gameacc__id=product_id).delete()
            total_price = Basket.objects.filter(user=request.user).aggregate(Sum('gameacc__price'))['gameacc__price__sum'] or 0
            return JsonResponse({'success': True,'total_price':total_price})
        except Basket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Sepetinizde bu ürün bulunamadı.'})
    else:
        return JsonResponse({'success': False, 'error': 'Geçersiz istek.'})