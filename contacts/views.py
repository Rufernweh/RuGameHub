from django.shortcuts import render,redirect
from .forms import ContactForm

# Create your views here.

def contact_view(request):
    contact_form=ContactForm()

    # Gönderildiği sayfanın URL'sini alın
    referer = request.META.get('HTTP_REFERER')
    print(referer)
    

    if request.method == 'POST':
        contact_form=ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return redirect(referer)
    return redirect('games:index')

