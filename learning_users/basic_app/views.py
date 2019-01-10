from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm


#
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("you are logged in")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))



def register(request):

    #we assume that user is not registered
    registered = False #will tell if some1 is registered or not

    #jesli zapostowano
    if request.method == "POST":
        #lapiemy formsy
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        #sprawdzamy czy obydwa formsy sa valid
        if user_form.is_valid() and profile_form.is_valid():

                #jezeli sa - lapiemy wszystko z user form
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                #potem lapiemy wszystko z profile form
                profile = profile_form.save(commit=False)
                profile.user = user

                #sprawdzamy x2 czy jest obraz do zapisania
                if 'profile_pic' in request.FILES:
                    profile.profile_pic = request.FILES['profile_pic']

                profile.save()

                registered = True
        else:#jezeli był post ale znalezopno blad to print error
            print(user_form.errors,profile_form.errors)
    else:#jesli nie bylo jeszcze request postujemy forms do wypelnienia
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render (request,'basic_app/registration.html',
                            {'user_form':user_form,
                             'profile_form':profile_form,
                             'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account not active")
        else:
            print ('Someone tried to login and failed')
            print('Username {} and password {}'.format(username,password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request,'basic_app/login.html',{})
