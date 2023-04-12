from django import forms
from .models import GameAccount,GameAccountGallery
from companies.models import Company
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField
from phonenumbers import parse, is_valid_number, NumberParseException
from django.core.validators import RegexValidator, ValidationError
from django.forms.widgets import ClearableFileInput
from PIL import Image
from django.utils.safestring import mark_safe



    


class GameAccountForm(forms.ModelForm):
    image=forms.FileField()
    mobile=forms.CharField(max_length=13,widget=forms.TextInput(attrs={'placeholder':'Mobile'}))
    class Meta:
        model = GameAccount
        fields = '__all__'

   
    def __init__(self,user, *args, **kwargs):
        self.user=user
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label='-------Category'
        self.fields['type'].empty_label='-------Type'
        self.fields['description'].widget.attrs.update({'placeholder':'Description'})
        for field_name, field in self.fields.items():
            field.required = False
            field.errors=False

        for field in self.fields:
            self.fields[field].widget.attrs.update({
            "class": "form-control",
        })
        
      
            

    def clean(self):
        company=Company.objects.get(user=self.user)
        name=self.cleaned_data.get('name')
        description=self.cleaned_data.get('description')
        price=self.cleaned_data.get('price')
        category=self.cleaned_data.get('category')
        type=self.cleaned_data.get('type')
        mobile=self.cleaned_data.get('mobile')
        images = self.files.getlist('image')

        now = timezone.now()
        start_date = timezone.make_aware(timezone.datetime(now.year, now.month, 1), timezone.get_current_timezone())
        end_date = timezone.make_aware(timezone.datetime(now.year, now.month, 1) + timezone.timedelta(days=30), timezone.get_current_timezone())
        print(name,images,mobile,type,category)
        
    
        # Count the number of game accounts created by the company in the current month
        count = GameAccount.objects.filter(company=company, created_at__gte=start_date, created_at__lt=end_date).count()

        # Check if the limit has been reached
        if count >= 10:
            self.add_error('name',"You cannot add more than 10 game accounts in a month.")
        elif   name  and price and images and category and type and mobile:
                if name:
                    name=name.strip()
                    name_spaces = name.replace(" ", "")       
                    if  name_spaces.isdigit():
                        self.add_error('name','Please enter only letters in the name')

                elif mobile:
                    azerbaijan_mobile_regex = r'^\+994(?:50|51|55|70|77|99)\d{7}$'
                    azerbaijan_mobile_validator = RegexValidator(
                    regex=azerbaijan_mobile_regex)
                    if not mobile_number.startswith("+994"):
                        mobile_number = "+994" + mobile_number[1:]

                        try:
                            azerbaijan_mobile_validator(mobile_number)
                            print('Mobile number is valid')
                        except ValidationError:
                            self.add_error('mobile','Please enter the valid phone number')
        else:
             self.add_error('name','This * field is required')
                     

        

    def save(self,*args,**kwargs):
            company=Company.objects.get(user=self.user)
            
            name=self.cleaned_data.get('name')
            category=self.cleaned_data.get('category')
            price=self.cleaned_data.get('price')
            description=self.cleaned_data.get('description')
            image=self.files.getlist('image')
            type=self.cleaned_data.get('type')
            mobile=self.cleaned_data.get('mobile')

            if description:
                game_account=GameAccount.objects.create(
                    name=name,
                    company=company,
                    category=category,
                    description=description,
                    price=price,
                    mobile=mobile,
                    type=type
                )
            else:
                game_account=GameAccount.objects.create(
                    name=name,
                    category=category,
                    company=company,
                    price=price,
                    type=type,
                    mobile=mobile
                )
            for i in image:
                GameAccountGallery.objects.create(
                    game=game_account,
                    image=i
                )





class CreateCompanyForm(forms.ModelForm):
    name=forms.CharField(max_length=40,required=False)
    icon=forms.FileField(required=False)
    
    bio=forms.CharField(max_length=50,required=False)


    class Meta:
        fields = ('name','icon','bio')
        model=Company

    def __init__(self,user,*args,**kwargs):
       super().__init__(*args, **kwargs)
       self.user=user
       for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):
        name=self.cleaned_data.get('name')
        icon=self.cleaned_data.get('icon')
        bio=self.cleaned_data.get('bio')
        if  name:

            if name:
                name=name.strip()
                name_spaces = name.replace(" ", "")       
                if not name_spaces.isalpha():
                    self.add_error('name','Please enter only letters in the name')
            
                
                elif icon:
                        file = self.cleaned_data.get('icon')
                        try:
                            img = Image.open(file)
                            img.verify()
                        except:
                            self.add_error('icon','Please enter a valid image file')
        

        else:
            self.add_error('name','The * Fields is required')

        return self.cleaned_data
    

        
    def save(self,*args,**kwargs,):
            user=self.user
            name=self.cleaned_data.get('name')
            icon=self.cleaned_data.get('icon')
            bio=self.cleaned_data.get('bio')

            if bio :
                Company.objects.get_or_create(
                    user=user,
                    name=name,
                    bio=bio
                )
            if  icon :
                Company.objects.create(
                    user=user,
                    name=name,
                    icon=icon,
                    
                )
            else:
                Company.objects.create(
                    name=name,
                    icon='/companies/profile/Facebook-no-profile-picture-icon-620x389.jpg',
                    user=user,
                    )




class CompanyAccountForm(forms.ModelForm):
    name=forms.CharField(max_length=40,required=False)
    icon=forms.FileField(required=False)
    bio=forms.CharField(max_length=50,required=False)


    class Meta:
        fields = ('name','icon','bio')
        model=Company

    def __init__(self,user,*args,**kwargs):
       super().__init__(*args, **kwargs)
       self.user=user
       self.company=Company.objects.get(user=user)
       for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


    def clean(self):
        self.cleaned_data['check_name']=True
        self.cleaned_data['check_icon']=True
        self.cleaned_data['check_bio']=True
        self.cleaned_data['exists']=True
        name=self.cleaned_data.get('name')
        icon=self.cleaned_data.get('icon')
        bio=self.cleaned_data.get('bio')
        print(type(icon))
        if name ==  self.company.name  and icon == self.company.icon and bio == self.company.bio:
             self.cleaned_data['exists']=False
        elif   name:
            if name:
                name=name.strip()
                name_spaces = name.replace(" ", "")       
                if not name_spaces.isalpha():
                    self.add_error('name','Please enter only letters in the name')
                
               
                elif icon:
                        file = self.cleaned_data.get('icon')
                        try:
                            img = Image.open(file)
                            img.verify()
                        except:
                            self.add_error('icon','Please enter a valid image file')
        

        else:
            self.add_error('name','The * Fields is required')

        if name == self.company.name:
                     self.cleaned_data['check_name']=False
        if bio == self.company.name:
                     self.cleaned_data['check_bio']=False

        if icon == self.company.icon:
                     self.cleaned_data['check_icon']=False
        

        return self.cleaned_data
    

        
    def save(self,*args,**kwargs,):
            if self.cleaned_data.get('exists') == True:
                company=self.company
                user=self.user
                name=self.cleaned_data.get('name')
                icon=self.cleaned_data.get('icon')
                bio=self.cleaned_data.get('bio')

                if self.cleaned_data.get('check_name'):
                     company.name=name
                     company.save()

        
                if self.cleaned_data.get('check_icon'):
                     company.icon=icon
                     company.save()

                if self.cleaned_data.get('check_desc'):
                     company.bio=bio
                     company.save()
                
                    
              

        

    






class EditGameAccountForm(forms.ModelForm):
    image=forms.FileField()
    mobile=forms.CharField(max_length=13)
    class Meta:
        model = GameAccount
        exclude=('company',)

   
    def __init__(self,user,gameacc,remove_img_list,*args, **kwargs):
        self.remove_img_list=remove_img_list
        self.user=user
        self.gameacc=gameacc
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label='-------Category'
        self.fields['type'].empty_label='-------Type'
        self.fields['description'].widget.attrs.update({'placeholder':'Description'})
        for field_name, field in self.fields.items():
            field.required = False

        for field in self.fields:
            self.fields[field].widget.attrs.update({
            "class": "form-control",'safe': True     
        })

        
      
            

    def clean(self):
        self.cleaned_data['check_name']=True
        self.cleaned_data['check_category']=True
        self.cleaned_data['check_mobile']=True
        self.cleaned_data['check_type']=True
        self.cleaned_data['check_description']=True
        self.cleaned_data['check_price']=True
        self.cleaned_data['exists']=True
        

        name=self.cleaned_data.get('name')
        description=self.cleaned_data.get('description')
        price=self.cleaned_data.get('price')
        category=self.cleaned_data.get('category')
        type=self.cleaned_data.get('type')
        mobile=self.cleaned_data.get('mobile')
        remove_img=self.remove_img_list 
        print(remove_img)  
   
    
                     

        if remove_img[0] == ""  and name ==  self.gameacc.name   and price == self.gameacc.price and description == self.gameacc.description and type == self.gameacc.type and mobile == self.gameacc.mobile and category == self.gameacc.category:
             self.cleaned_data['exists']=False
        elif    name  and price  and category and type and mobile :
                if name:
                    name=name.strip()
                    name_spaces = name.replace(" ", "")       
                    if  name_spaces.isdigit():
                        self.add_error('name','Please enter only letters in the name')
                elif mobile:
                    azerbaijan_mobile_regex = r'^\+994(?:50|51|55|70|77|99)\d{7}$'
                    azerbaijan_mobile_validator = RegexValidator(
                    regex=azerbaijan_mobile_regex)
                    if not mobile_number.startswith("+994"):
                        mobile_number = "+994" + mobile_number[1:]

                        try:
                            azerbaijan_mobile_validator(mobile_number)
                            print('Mobile number is valid')
                        except ValidationError:
                            self.add_error('mobile','Please enter the valid phone number')
        else:
             self.add_error('name','This * field is required')

        if name == self.gameacc.name:
                     self.cleaned_data['check_name']=False

        if category == self.gameacc.category:
                     self.cleaned_data['check_category']=False
        
        if mobile == self.gameacc.mobile:
                     self.cleaned_data['check_mobile']=False

        if price == self.gameacc.price:
                     self.cleaned_data['check_price']=False
        
        if type == self.gameacc.type:
                     self.cleaned_data['check_type']=False

        if description == self.gameacc.description:
                     self.cleaned_data['check_description']=False
                     

        

    def save(self, *args,**kwargs):            
            name=self.cleaned_data.get('name')
            category=self.cleaned_data.get('category')
            price=self.cleaned_data.get('price')
            description=self.cleaned_data.get('description')
            type=self.cleaned_data.get('type')
            mobile=self.cleaned_data.get('mobile')
            remove_img=self.remove_img_list
            
            
            if self.cleaned_data.get('exists'):

                if  not remove_img[0] == "":
                      for img_id in remove_img:
                            img_id=img_id.replace(",","")
                            GameAccountGallery.objects.filter(id=img_id).delete()

                if name:
                      self.gameacc.name=name
                      self.gameacc.save()

                if category:
                      self.gameacc.category=category
                      self.gameacc.save()


                if price:
                      self.gameacc.price=price
                      self.gameacc.save()


                if  description:
                      self.gameacc.description=description
                      self.gameacc.save()

                if type:
                      self.gameacc.type=type
                      self.gameacc.save()

                if mobile:
                      self.gameacc.mobile=mobile
                      self.gameacc.save()


                
