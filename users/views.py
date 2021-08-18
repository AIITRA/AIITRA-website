from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.forms import DisconnectForm

#All the data google oauth returns is sent to adapter.py/populate_users. You can apply conditionals and anything there


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        email = request.POST['email']
        username = request.POST['username']
        if form.is_valid():
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account made for {username}. Please check your mail to activate the account.')
            form.save()
            user = User.objects.filter(email=email)[0]
            user.is_active = False
            send_email(user)
            return redirect('AIITRA-home')

        elif User.objects.filter(email = email).exists():
            if User.objects.filter(email = email)[0].is_active:
                messages.info(request, f'Account already exists for {email}')
                return redirect('login')
            else:
                messages.info(request, f'You have already registered {username}. Please verify your email.')
                return redirect('verify-email')
    else:
        form = UserRegistrationForm()

        context = {
            'form': form
        }
        return render(request, 'users/register.html', context)

def home(request):
    return render(request, 'users/homepage.html')

def verify_email(request):
    if request.method=='POST':
        form=Email_verification_form(request.POST)
        email=request.POST['email']
        user=User.objects.get(email=email)
        if user.is_active:
            messages.info(request, f'You have already verified your email . Please login')
            return redirect('login')
        else:
            send_email(user)
            messages.success(request, f'An email has been sent to {email}. Please click on the link to verify')
            return redirect('login')
    else:
        form=Email_verification_form()
        context = {
            'form': form
        }
        return render(request,'users/email_verification.html',context)



@login_required
def profile(request):
    current_user = request.user
    img = request.user.profile.image.url

    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        username = request.POST['username']

        if User.objects.filter(username = username).exists() and User.objects.filter(username = username)[0] != current_user:
            messages.error(request, f'Profile not updated. Username already exists.')
            return redirect('profile')
        else:
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request, f'Profile updated succesfully!')
                return redirect('profile')
    else:
        password_change_form = PasswordChangeForm(current_user)
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm()
        # social_form=DisconnectForm(request)
        google_link = False
        github_link = False
        sociallink = SocialAccount.objects.filter(user = current_user)
        if sociallink.exists():
            if sociallink.all().filter(provider = "google").exists():
                google_link = True
            if sociallink.all().filter(provider = "github").exists():
                github_link = True

        context = {
            'img': img,
            'u_form': u_form,
            'p_form': p_form,
            # 'social_form': social_form,
            'password_change_form': password_change_form,

            "google_link": google_link,
            "github_link": github_link
        }
        return render(request, 'users/profile.html', context)
