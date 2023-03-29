from django import forms
from .models import GameAccount,GameAccountGallery
from companies.models import Company
from django.utils import timezone
from phonenumber_field.formfields import PhoneNumberField
from phonenumbers import parse, is_valid_number, NumberParseException
from django.core.validators import RegexValidator, ValidationError
from django.forms.widgets import ClearableFileInput
from PIL import Image



    


class GameAccountForm(forms.ModelForm):
    image=forms.FileField()
    class Meta:
        model = GameAccount
        fields = '__all__'

   
    def __init__(self,user, *args, **kwargs):
        self.user=user
        super().__init__(*args, **kwargs)
        self.fields['company'].queryset = Company.objects.filter(user=user)
        self.fields['company'].empty_label='-------Company'
        self.fields['category'].empty_label='-------Category'
        self.fields['type'].empty_label='-------Type'
        self.fields['description'].widget.attrs.update({'placeholder':'Description'})
        for field_name, field in self.fields.items():
            field.required = False

        for field in self.fields:
            self.fields[field].widget.attrs.update({
            "class": "form-control",
        })
        
      
            

    def clean(self):
        company=self.cleaned_data.get('company')
        name=self.cleaned_data.get('name')
        description=self.cleaned_data.get('description')
        price=self.cleaned_data.get('price')
        company=self.cleaned_data.get('company')
        category=self.cleaned_data.get('category')
        type=self.cleaned_data.get('type')
        images = self.files.getlist('image')

        now = timezone.now()
        start_date = timezone.make_aware(timezone.datetime(now.year, now.month, 1), timezone.get_current_timezone())
        end_date = timezone.make_aware(timezone.datetime(now.year, now.month, 1) + timezone.timedelta(days=30), timezone.get_current_timezone())

        
    
        # Count the number of game accounts created by the company in the current month
        count = GameAccount.objects.filter(company=company, created_at__gte=start_date, created_at__lt=end_date).count()

        # Check if the limit has been reached
        if count >= 10:
            self.add_error('company',"You cannot add more than 10 game accounts in a month.")
        elif  company and name  and price and images and category and type:
                if name:
                    name=name.strip()
                    name_spaces = name.replace(" ", "")       
                    if not name_spaces.isalpha():
                        self.add_error('name','Please enter only letters in the name')
        else:
             self.add_error('name','This * field is required')
                     

        

    def save(self,*args,**kwargs):
            
            name=self.cleaned_data.get('name')
            company=self.cleaned_data.get('company')
            category=self.cleaned_data.get('category')
            price=self.cleaned_data.get('price')
            description=self.cleaned_data.get('description')
            image=self.files.getlist('image')
            type=self.cleaned_data.get('type')

            if description:
                game_account=GameAccount.objects.create(
                    name=name,
                    company=company,
                    category=category,
                    description=description,
                    price=price,
                    type=type
                )
            else:
                game_account=GameAccount.objects.create(
                    name=name,
                    category=category,
                    company=company,
                    price=price,
                    type=type
                )
            for i in image:
                print('esselee')
                print(i)
                GameAccountGallery.objects.create(
                    game=game_account,
                    image=i
                )





class CreateCompanyForm(forms.ModelForm):
    name=forms.CharField(max_length=40,required=False)
    icon=forms.FileField(required=False)
    mobile=forms.CharField(max_length=20, required=False)
    bio=forms.CharField(max_length=50,required=False)


    class Meta:
        fields = ('mobile','name','icon','bio')
        model=Company

    def __init__(self,user,*args,**kwargs):
       super().__init__(*args, **kwargs)
       self.user=user
       for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):
        name=self.cleaned_data.get('name')
        mobile=self.cleaned_data.get('mobile')
        icon=self.cleaned_data.get('icon')
        bio=self.cleaned_data.get('bio')
        print(name,icon,mobile)
        print(type(icon))
        if  mobile and name:

            if name:
                name=name.strip()
                name_spaces = name.replace(" ", "")       
                if not name_spaces.isalpha():
                    self.add_error('name','Please enter only letters in the name')
            
                elif mobile:
                    check=True
                    mobile_regex = r'^\+?[0-9]{1,3}\s*\(?[0-9]{3}\)?[-.\s]*[0-9]{3}[-.\s]*[0-9]{4}$'
                    mobile_validator = RegexValidator(regex=mobile_regex)
                    try:
                        mobile_validator(mobile)
                    except ValidationError:
                        check=False
                        self.add_error('mobile','Invalid Phone number')
                    if Company.objects.filter(mobile=mobile).exists():
                         self.add_error('mobile','This mobile number is used by another company')


                    if check == True:
                            
                            try:
                                parsed_number = parse(mobile)
                                if not is_valid_number(parsed_number):
                                    self.add_error('mobile','Invalid Phone number')
                            except NumberParseException:
                                self.add_error("mobile",'Invalid Phone number')
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
            mobile=self.cleaned_data.get('mobile')
            icon=self.cleaned_data.get('icon')
            bio=self.cleaned_data.get('bio')

            if bio :
                Company.objects.create(
                    user=user,
                    name=name,
                    mobile=mobile,
                    bio=bio
                )
            if  icon :
                Company.objects.create(
                    user=user,
                    name=name,
                    mobile=mobile,
                    icon=icon,
                    
                )
            else:
                Company.objects.create(
                    name=name,
                    mobile=mobile,
                    icon='/companies/profile/Facebook-no-profile-picture-icon-620x389.jpg',
                    user=user,
                    )




class CompanyAccountForm(forms.ModelForm):
    name=forms.CharField(max_length=40,required=False)
    icon=forms.FileField(required=False)
    mobile=forms.CharField(max_length=20, required=False)
    bio=forms.CharField(max_length=50,required=False)


    class Meta:
        fields = ('mobile','name','icon','bio')
        model=Company

    def __init__(self,user,*args,**kwargs):
       super().__init__(*args, **kwargs)
       self.user=user
       self.company=Company.objects.get(user=user)
       for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})


    def clean(self):
        self.cleaned_data['check_name']=True
        self.cleaned_data['check_mobile']=True
        self.cleaned_data['check_icon']=True
        self.cleaned_data['check_bio']=True
        self.cleaned_data['exists']=True
        name=self.cleaned_data.get('name')
        mobile=self.cleaned_data.get('mobile')
        icon=self.cleaned_data.get('icon')
        bio=self.cleaned_data.get('bio')
        print(name,icon,mobile)
        print(type(icon))
        if name ==  self.company.name and self.company.name and mobile == self.company.mobile and icon == self.company.icon and bio == self.company.bio:
             self.cleaned_data['exists']=False
        elif mobile and name:
            if name:
                name=name.strip()
                name_spaces = name.replace(" ", "")       
                if not name_spaces.isalpha():
                    self.add_error('name','Please enter only letters in the name')
                
                elif mobile:
                    check=True
                    mobile_regex = r'^\+?[0-9]{1,3}\s*\(?[0-9]{3}\)?[-.\s]*[0-9]{3}[-.\s]*[0-9]{4}$'
                    mobile_validator = RegexValidator(regex=mobile_regex)
                    try:
                        mobile_validator(mobile)
                    except ValidationError:
                        
                        check=False
                        self.add_error('mobile','Invalid Phone number')


                    if Company.objects.filter(mobile=mobile).exists():
                         self.add_error('mobile','This mobile number is used by another company')

                    if check == True:
                            
                            try:
                                parsed_number = parse(mobile)
                                if not is_valid_number(parsed_number):
                                    self.cleaned_data['check_monile']=False
                                    self.add_error('mobile','Invalid Phone number')
                            except NumberParseException:
                                self.cleaned_data['check_monile']=False
                                self.add_error("mobile",'Invalid Phone number')
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

        if mobile == self.company.mobile:
                     self.cleaned_data['check_mobile']=False

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
                mobile=self.cleaned_data.get('mobile')
                icon=self.cleaned_data.get('icon')
                bio=self.cleaned_data.get('bio')

                if self.cleaned_data.get('check_name'):
                     company.name=name
                     company.save()

                if self.cleaned_data.get('check_mobile'):
                     company.mobile=mobile
                     company.save()
                if self.cleaned_data.get('check_icon'):
                     company.icon=icon
                     company.save()

                if self.cleaned_data.get('check_desc'):
                     company.bio=bio
                     company.save()
                
                    
              

        

    


