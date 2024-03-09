from django.shortcuts import render, redirect
from .forms import RegistrationForm
from django.contrib import messages
from django.urls import reverse


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User registered successfully')
            return redirect('registration-url')
    else:
        form = RegistrationForm()
    return render(request, 'auth/register.html', {"form": form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        # Redirect to a success page or homepage
        return HttpResponseRedirect(reverse('home-url'))
    # If the request method is not POST, return a method not allowed response
    return HttpResponseNotAllowed(['POST'])
