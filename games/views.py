from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from users.decorators import not_created_company
from django.http import JsonResponse
from .forms import GameAccountForm,CreateCompanyForm,CompanyAccountForm,EditGameAccountForm
from .models import GameAccount,GameAccountGallery,Category,Review
from basket.models import Basket
from companies.models import Company
from django.db.models import F,Q
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import When,Case,Value
from contacts.forms import ContactForm
import json
import ast
from services.choices import GAME_STATUS
from django.template.loader import render_to_string
from django.contrib import messages


# Create your views here.

def index_view(request):
    

    search = request.GET.get('search')
    if search:
        url = '/game-accounts-list/?search=' + search
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
    context['gameaccs']=gameaccs
    context['latest_games']=latest_games
    context['category']=Category.objects.all()
  
    return render(request,'games/index.html',context)

    

    
@login_required(login_url='/users/login/')
def create_company(request):
    context={}

    if request.method == 'POST':
        context['form']=CreateCompanyForm(data=request.POST,files=request.FILES,user=request.user)
        
        form = CreateCompanyForm(data=request.POST,files=request.FILES,user=request.user)
        if form.is_valid():
            form.save()
            
        else:
             
            return render(request, 'users/create_company.html', context)
    else:
        if request.GET.get('next'):
            return redirect('users:login')
       
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
            form.save(commit=False)
            message='Game account successfully added'
            return render(request, 'games/add_game_account.html', {f'form':GameAccountForm(user=request.user),'company':company,'messages':message})
            
        else:
            return render(request, 'games/add_game_account.html', {'form': form})
    else:
        form = GameAccountForm(user=request.user)
        return render(request, 'games/add_game_account.html', {'form': form,'company':company})
    

@not_created_company
def user_game_accounts(request):
    filter=''
    context={}
    search=request.GET.get('search')
    filter_cat=request.GET.get('query')
    
    company=Company.objects.get(user=request.user)
    gameacc=GameAccount.objects.filter(company=company)


  
    if search or  filter_cat:
        if filter_cat:
            search=filter_cat
        gameacc=gameacc.filter(category__name__exact=search)

        context['filter'] =f'&query={search}'


    latest_games=gameacc.order_by('-created_at')[:3]
    #Pagination
    paginator=Paginator(gameacc,1)
    page=request.GET.get('page',1)
    gameacc_list=paginator.get_page(page)
   
  
    context['paginator'] = paginator
    context['gameaccs'] = gameacc_list
    context['latest_games'] = latest_games

    return render(request,'games/self_game_accounts.html',context)



def list_view(request):
    context={}
    filter_dict={}
    query=request.GET.get('search')
    filter_cat=request.GET.get('query')
    cat=request.GET.get('category')
    type=request.GET.get('type')
   
    gameaccs=GameAccount.objects.all()
    latest_games=gameaccs.order_by('-created_at')[:3]
    random_gameaccs = gameaccs.order_by('?')[:4]



    
    if not filter_cat:
        filter_cat={}
    else:
        filter_cat=ast.literal_eval(filter_cat)


    if query or filter_cat.get('search'):
        if filter_cat.get('search'):
            query=filter_cat.get('search')

        gameaccs=gameaccs.filter(category__name__icontains=query)
        filter_dict['search']=query
        context['filter']=f'&query={filter_dict}'

    

    elif cat or filter_cat.get('cat'):
    
        print(filter_cat.get('cat'))
        if filter_cat.get('cat'):
            cat=filter_cat.get('cat')
            
        gameaccs=gameaccs.filter(category__name__icontains=cat)
        filter_dict['cat']=cat
        context['filter']=f'&query={filter_dict}'


    elif type or filter_cat.get('type'):
        if filter_cat.get('type'):
            type=filter_cat.get('type')

        gameaccs=gameaccs.filter(type=type)
        print(gameaccs)
        filter_dict['type']=type
        context['filter']=f'&query={filter_dict}'


    paginator=Paginator(gameaccs,1)
    page=request.GET.get('page',1)
    gameaccs_list=paginator.get_page(page)
    
   



         
    context['gameaccs']=gameaccs_list
    context['random_gameaccs']=random_gameaccs
    context['latest_games']=latest_games
    context['paginator']=paginator

    return render(request,"games/list.html",context)


def detail_view(request,code):
    gameaccss = GameAccount.objects.annotate(type_color=Case(When(type='MOBA',then=Value('#1464d2')),
        When(type='FPS',then=Value('#a714b9')),
        When(type='Racing',then=Value('#ef9e2b')),
        When(type='RPG',then=Value('#2bef46')),
        When(type='Simulation and sports',then=Value('#ef2beb')),
        ))
    gameacc=gameaccss.get(code=code)
    related_games=gameaccss.filter(type=gameacc.type)
    random_gameaccs = gameaccss.order_by('?')[:4]
    reviews=Review.objects.all()
    context={}
    context['types']=GAME_STATUS
    context['gameacc']=gameacc
    context['related_games']=related_games
    context['random_accs']=random_gameaccs
    context['reviews']=reviews
    context['basket']=Basket.objects.all()



    

    return render(request,'games/detail.html',context)



def add_comment(request):

    if request.method == 'POST':
        company=Company.objects.get(user=request.user)
        message = request.POST.get('message')
        review = Review.objects.create(name=request.user.full_name, message=message,user=request.user)
        

        # Get all reviews, including the newly added one
        reviews = Review.objects.all()

        # Render the reviews list template with the updated reviews
        reviews_html = render_to_string('games/detail.html', {'reviews': reviews})

        data = {
            'success': True,
            'name': review.name,
            'message': review.message,
            'created_date': review.created_at.strftime('%D, %B, %Y'),
            'reviews_html': reviews_html,
            'img':company.icon.url,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'success': False})
    

def check_login_status(request):
    if request.user.is_authenticated:
        logged_in = True
    else:
        logged_in = False

    # Yanıtı JSON formatında döndür
    response_data = {'logged_in': logged_in}
    return JsonResponse(response_data)






def remove_gameacc(request):
    if request.method == 'POST':
       
        product_id = request.POST.get('product_id')
        try:
            basket = Basket.objects.get(user=request.user, gameacc__id=product_id)
            basket.delete()
            return JsonResponse({'success': True})
        except Basket.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Sepetinizde bu ürün bulunamadı.'})
    else:
        return JsonResponse({'success': False, 'error': 'Geçersiz istek.'})
    

@not_created_company
def edit_adding_account(request,code):
    context={}
    company=Company.objects.get(user=request.user)
   
    removed_acc=request.GET.get('removed-acc')

    if removed_acc:
        GameAccount.objects.filter(code=removed_acc).delete()
        return redirect('games:user-game-accounts')
         
       
    
    if GameAccount.objects.filter(code=code,company=company):
        gameacc=GameAccount.objects.get(code=code,company=company)
        form=EditGameAccountForm(instance=gameacc,user=request.user,gameacc=gameacc,remove_img_list=[])
        images=gameacc.gameaccountgallery_set.all()
        

        if request.method == "POST":
            remove_img_list=request.POST.getlist('remove_image_list')
            form=EditGameAccountForm(data=request.POST,instance=gameacc,user=request.user,gameacc=gameacc,files=request.FILES,remove_img_list=remove_img_list)
            if form.is_valid():
                gameacc=form.save()
                
                code=form.instance.code
                response = redirect('games:edit-game-account', code=code)
                if form.cleaned_data.get('exists') == True:
                    message='Successfully update game account'
                    messages.add_message(request, messages.INFO, message)
                return response
        
                
                


        
    else:
        return redirect('games:index')
    
    context['form']=form
    context['images']=images
    context['code']=code
    context['gameacc']=gameacc



    return render(request,'games/edit_adding_account.html',context)





def remove_comment(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        comment_id = data.get('comment_id')
        review = get_object_or_404(Review, id=comment_id)
        review.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})


def remove_game_account(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        gameacc_id = data.get('Gameacc_id')
        object = get_object_or_404(GameAccount, id=gameacc_id)
        object.delete()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})