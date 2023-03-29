from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import UserCreationForm as BaseCreationForm
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from services.generator import CodeGenerator
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
User = get_user_model()

# -----------------------   Admin Forms  ---------------------------------------------------


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={'placeholder':"Password"}))
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput(attrs={'placeholder':"Password confirmation"}))
    email = forms.CharField(
        label="Email", widget=forms.TextInput(attrs={'placeholder':"Enter the email"}))
    full_name = forms.CharField(max_length=30,
        label="Password confirmation", widget=forms.TextInput(attrs={'placeholder':"Enter the Fullname "}))
    

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "password1",
            "password2",
        ]


    def clean(self):
        password1=self.cleaned_data.get('password1')
        password2=self.cleaned_data.get('password2')
        email = self.cleaned_data.get('email')
        full_name=self.cleaned_data.get('full_name').strip()
        full_name_spaces = full_name.replace(" ", "")
        if User.objects.filter(email=email):
            self.add_error('email',"This email already exists")
        else:
            if not full_name_spaces.isalpha():
                self.add_error('password1',"Please enter only letters in the full name")

            elif password1 and password2 and password1 != password2:
                self.add_error('password1',"Passwords don't match")
            elif password1:
                if len(password1) < 6:
                    self.add_error('password1','Password must minumum length 6')

                elif not  password1.strip()[0].isalpha():
                    self.add_error('password1','Password  must begin with letter')
            
                elif not any(char.isalpha() for char in password1) or not any(char.isdigit() for char in password1):
                    self.add_error('password1', 'The password must contain both letters and numbers')
                    
       
        return self.cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "is_active",
            "is_superuser",
            "password",
        ]

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}))

    class Meta:
        model = User
        fields = ("email", "password")

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        if User.objects.filter(email=email):
            user=User.objects.get(email=email)
            check_passwordr=check_password(password,user.password)
            if check_passwordr:
                if not user.is_active:
                    self.add_error('email', "This user is not active")
            else:
                self.add_error('email',"Email or password is wrong")
        else:
            self.add_error('email',"Email or password is wrong")
        return self.cleaned_data


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })


class RegisterForm(UserAdminCreationForm):

    def save(self):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save()
        user.set_password(self.cleaned_data.get("password1"))
        user.is_active = False
        user.activation_code = CodeGenerator.create_activation_link_code(
            size=4, model_=User
        )
        
        user.save()

        message = f"Please write code below: \n{user.activation_code}"

        # send mail
        send_mail(
            'Activate email', # subject
            message, # message
            settings.EMAIL_HOST_USER, # from email
            [user.email], # to mail list
            fail_silently=False,
        )
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                "class": "form-control",
            })



class ActivateForm(forms.ModelForm):
    activation_code = forms.CharField(max_length=4,widget=forms.TextInput(attrs={'placeholder': 'Enter the code'}))

    class Meta:
        model = User
        fields = ("activation_code", )

   

   
   



  



class CustomPasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True,'placeholder':'old password'}
        ),
    )
    new_password1 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True,'placeholder':'New password'}
        ),
    )

    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "autofocus": True,'placeholder':'New password confirm'}
        ),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)


    def clean(self):
        new_password1=self.cleaned_data.get('new_password1')
        new_password2=self.cleaned_data.get('new_password2')
        old_password = self.cleaned_data.get('old_password')
        if  not self.user.check_password(old_password):
            self.add_error('new_password1',"Your old password was entered incorrectly. Please enter it again")
        else:
            if new_password1 and new_password2 and new_password1 != new_password2:
                self.add_error('new_password1',"Passwords don't match")
            if new_password1:
                if len(new_password1) < 6:
                    self.add_error('new_password1','Password must minumum length 6')

                if not  new_password1.strip()[0].isalpha():
                    self.add_error('new_password1','Password  must begin with letter')
            
                if not any(char.isalpha() for char in new_password1) or not any(char.isdigit() for char in new_password1):
                    self.add_error('new_password1', 'The password must contain both letters and numbers')
    def save(self, commit=True):
        """Save the new password."""
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
                    
       
        return self.cleaned_data
  



class ResetPasswordForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Enter your email address'}))

    class Meta:
        model = User
        fields = ("email", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})

    def clean(self):
        email = self.cleaned_data.get("email")
        if not User.objects.filter(email=email).exists():
            self.add_error('email',"This email does not exist")
            

        return self.cleaned_data



class ResetPasswordCompleteForm(forms.ModelForm):
    
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter new password confirm'}))
    class Meta:
        model = User
        fields = ("password1", "password2")



    def clean(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
                self.add_error('password1',"Passwords don't match")
                if password1:
                    if len(password1) < 6:
                        self.add_error('password1','Password must minumum length 6')

                    if not  password1.strip()[0].isalpha():
                        self.add_error('password1','Password  must begin with letter')
                
                    if not any(char.isalpha() for char in password1) or not any(char.isdigit() for char in password1):
                        self.add_error('password1', 'The password must contain both letters and numbers')

        return self.cleaned_data


    def save(self):
        password1 = self.cleaned_data.get("password1")
        self.instance.set_password(password1)
        self.instance.save()
        return self.instance
    

class UserProfileForm(forms.ModelForm):
    full_name = forms.CharField(max_length=30)

    class Meta:
        fields=('email','full_name')
        model=User

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
    
    def clean(self):
        email=self.cleaned_data.get('email')
        full_name=self.cleaned_data.get('full_name').strip()
        full_name_spaces = full_name.replace(" ", "")
        if full_name == self.user.full_name:
            if email == self.user.email:
                self.add_error('email','The e-mail address is already in use')
                self.cleaned_data['check email']=False
            else:
                self.cleaned_data['check email']=True
        else:

            if not full_name_spaces.isalpha():
                self.add_error('email',"Please enter only letters in the full name")
            else:
                self.cleaned_data['check full_name']=True   
                if email == self.user.email:
                    self.cleaned_data['check email']=False
                elif  email != self.user.email:
                    self.cleaned_data['check email']=True

        return self.cleaned_data

            


    def save(self,commit=True,):
        user=self.user
        full_name=self.cleaned_data.get('full_name')
        email=self.cleaned_data.get('email')

        if self.cleaned_data.get('check full_name'):
            user.full_name=full_name
            user.save()
        if self.cleaned_data.get('check email'):
            user.email=email
            user.save()
        



        

        


