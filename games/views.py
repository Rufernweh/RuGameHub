from django.shortcuts import render,redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.decorators import not_created_company
from django.http import JsonResponse
from .forms import GameAccountForm,CreateCompanyForm,CompanyAccountForm
from .models import GameAccount,Category
from companies.models import Company
from django.db.models import F,Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import When,Case,Value

# Create your views here.

def index_view(request):
    search = request.GET.get('search')
    if search:
        #***************************************************
        # bura list seyfesini qoyacaqsan asagidaki mirtadi
        url = '/your-game-accounts/?search=' + search
        return redirect(url)
    

    gameaccss = GameAccount.objects.annotate(type_color=Case(When(type='MOBA',then=Value('#1464d2')),
        When(type='FPS',then=Value('#a714b9')),
        When(type='Racing',then=Value('#ef9e2b')),
        When(type='RPG',then=Value('#2bef46')),
        When(type='Simulation and sports',then=Value('#ef2beb')),
        ))
    
    gameaccs = gameaccss.order_by('?')[:4]
     
    latest_games=gameaccss.order_by('-created_at')[:3]
    
    context={}
    context['user']=''
    context['gameaccs']=gameaccs
    context['latest_games']=latest_games
    if not  request.user.is_anonymous and  Company.objects.filter(user=request.user):
        context['company']=Company.objects.get(user=request.user)
        context['category']=Category.objects.all()
        context['user']=request.user
    return render(request,'games/index.html',context)

    

    
@login_required(login_url='/users/login/')
def create_company(request):
    context={}

    if request.method == 'POST':
        context['form']=CreateCompanyForm(data=request.POST,files=request.FILES,user=request.user)
        if Company.objects.filter(user=request.user):
            context['company']=Company.objects.get(user=request.user)
        form = CreateCompanyForm(data=request.POST,files=request.FILES,user=request.user)
        if form.is_valid():
            form.save()
            
        else:
             
            return render(request, 'users/create_company.html', context)
    else:
        if request.GET.get('next'):
            return redirect('users:login')
        if Company.objects.filter(user=request.user):
            context['company']=Company.objects.get(user=request.user)
        context['form']=CreateCompanyForm(user=request.user)
    return render(request, 'users/create_company.html', context)


@not_created_company
def company_account(request):
    check_icon=False
    message=''
    context={}

    company=Company.objects.get(user=request.user)
    form=CompanyAccountForm(instance=company,user=request.user)
    icon=Company.objects.get(user=request.user).icon
    icon_url=icon.url
    check_icon=True
    
    context['check_icon']=check_icon
   
    

    if request.method == 'POST':
        form=CompanyAccountForm(data=request.POST,instance=company,user=request.user,files=request.FILES)
        if form.is_valid():
            form.save()
            message=True
            icon_url=Company.objects.get(user=request.user).icon.url
    context['form']=form
    context['messages']=message
    context['icon_url']=icon_url
    
    return render(request,'users/company_account.html',context)




@not_created_company
def add_game_account(request):
    company=Company.objects.get(user=request.user)
    
    if request.method == 'POST':
        images=request.FILES.getlist('image')
        print(images)
    
        form = GameAccountForm(user=request.user,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            
        else:
            return render(request, 'games/add_game_account.html', {'form': form})
    else:
        form = GameAccountForm(user=request.user)
        return render(request, 'games/add_game_account.html', {'form': form,'company':company})
    

@not_created_company
def user_game_accounts(request):
    search=request.GET.get('search')
    print(search)
    query=request.GET.get('q')
    context={}
    company=Company.objects.get(user=request.user)
    gameacc=GameAccount.objects.filter(company=company)
    if query:
        gameacc=gameacc.filter(name__icontains=query)
    latest_games=gameacc.order_by('-created_at')[:3]
    #Pagination
    paginator=Paginator(gameacc,3)
    page=request.GET.get('page',1)
    gameacc_list=paginator.get_page(page)
   
  
    context['company'] = company
    context['paginator'] = paginator
    context['gameaccs'] = gameacc_list
    context['latest_games'] = latest_games
    return render(request,'games/self_game_accounts.html',context)



def list_view(request):
    return render(request,"games/list.html",{})