from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import GameAccountForm,CreateCompanyForm,CompanyAccountForm
from .models import GameAccount,Category
from companies.models import Company
from django.db.models import F,Q
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def index_view(request):
    context={}
    context['user']=''
    context['games']=GameAccount.objects.all()
    if not  request.user.is_anonymous and  Company.objects.filter(user=request.user):
        context['company']=Company.objects.get(user=request.user)
        context['category']=Category.objects.all()
        context['user']=request.user
        print(Company.objects.get(user=request.user))
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
        if Company.objects.filter(user=request.user):
            context['company']=Company.objects.get(user=request.user)
        context['form']=CreateCompanyForm(user=request.user)
    return render(request, 'users/create_company.html', context)


@login_required(login_url='/users/login/')
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




@login_required(login_url='/users/login/')
def add_game_account(request):
    
    if request.method == 'POST':
        print('*********8')
        images=request.FILES.getlist('image')
        print(images)
    
        form = GameAccountForm(user=request.user,data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('games:game-accounts')
            
        else:
            return render(request, 'games/add_game_account.html', {'form': form})
    else:
        form = GameAccountForm(user=request.user)
        return render(request, 'games/add_game_account.html', {'form': form})
    


def game_accounts(request):
    return render(request,'games/game_accounts.html',{})