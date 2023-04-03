from .models import Contact
from django import  forms


class ContactForm(forms.ModelForm):
    
    class Meta:
        model=Contact
        fields='__all__'

    def clean(self):
        name=self.cleaned_data.get('name')
        email=self.cleaned_data.get('email')
        message=self.cleaned_data.get('message')
        print(name,email,message)


    def save(self,*args,**kwargs):
        name=self.cleaned_data.get('name')
        email=self.cleaned_data.get('email')
        message=self.cleaned_data.get('message')

        Contact.objects.create(
            name=name,
            email=email,
            message=message
        )
        
