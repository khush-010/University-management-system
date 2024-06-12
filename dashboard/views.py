from django.shortcuts import render, redirect
from django.http import HttpResponse,JsonResponse
from .models import Users,Application
from django.shortcuts import render,HttpResponseRedirect
from .forms import loginForm,RegForm,ApplicationForm,ChangePassForm
from university.authenticate import Auth
from django.contrib.auth import login
from django.conf import settings
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import random
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect


# Create your views here.

def start(request):
    return redirect('home/')

def home(request):
    if 'user' in request.session:
        current_user = request.session['user']
        user = Users.objects.get(email=current_user)
        if user is not None:
            if user.role == 'S':
                return render(request,'dashboard/stu-dashboard.html',{'user':user})
            elif user.role == 'F':
                return render(request,'dashboard/fac-dashboard.html',{'user':user})
       
    else:
        return login(request)
    
    

def login(request):
    if request.method == "POST":
        fm = loginForm(request.POST)
        if fm.is_valid():
            uname=fm.cleaned_data['user_id']
            upass=fm.cleaned_data['password']
            user = Auth.authentication(request=request,username=uname,password=upass)
            if user is not None:
                backend_path = settings.AUTHENTICATION_BACKENDS[1]
                user.backend = backend_path
                user=Auth.get_user(user.id)
                request.session['user'] = uname
                request.session.set_expiry(6000)
                if user.role == 'S':
                    return render(request,'dashboard/stu-dashboard.html',{'user':user})
                elif user.role == 'F':
                    return render(request,'dashboard/fac-dashboard.html',{'user':user})
            else:
                return render(request, 'dashboard/login.html', {'form': fm, 'error': 'Invalid username or password'})

    else:
        fm = loginForm()
    return render(request, 'dashboard/login.html', {'form': fm})

def signup(request):
    if request.method == "POST":
        fm = RegForm(request.POST)
        if fm.is_valid():
            
            user = fm.save(commit=False)
            upass=fm.cleaned_data['password']
            try:
                validate_password(upass)
                user.password = make_password(upass)
                user.save()
                login_url = reverse('login')
                messages.success(request,f'Your Application is Successfully Submitted. Click here to <a href="{login_url}">Login</a>')
            
            except ValidationError as e:
                for error in e:
                    messages.warning(request, error)
            
            fm=RegForm()
            return render(request, 'dashboard/signup.html', {'form': fm})

    else:
        fm = RegForm()

    return render(request,'dashboard/signup.html',{'form':fm})

def application(request):
    if request.method == "POST":
        uname = request.session['user']
        if not uname:
            return redirect('login')
        try:
            user = Users.objects.get(email=uname)

        except Users.DoesNotExist:
            return redirect('login')
        
        form=ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.user_name = user
            application.save()
            
            messages.success(request,f'Your Application is Successfully Submitted.')
            form = ApplicationForm()
            return render(request, 'dashboard/application.html', {'form': form})
    else:
        form=ApplicationForm()

    return render(request,'dashboard/application.html',{'form':form})

def pen_app(request):
    applications= Application.objects.all()
    
    # for application in Application.objects.all():
    #     if application.status == 'Pending':
            
    #         applications.append(application)
            
    
    context = {
        'applications': applications,
    }

    return render(request,'dashboard/pen-app.html',context)

def accept(request):
    if request.method == "POST":
        sid=request.POST.get('sid')
        pi = Application.objects.get(id=sid)
        pi.status = "Accepted"
        pi.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})


def reject(request):
    if request.method == "POST":
        sid=request.POST.get('sid')
        pi = Application.objects.get(id=sid)
        pi.status = "Rejected"
        pi.save()
        return JsonResponse({'status':1})
    else:
        return JsonResponse({'status':0})
    

def app_status(request):
    uname = request.session['user']
    if not uname:
        return redirect('login')
    try:
        user = Users.objects.get(email=uname)

    except Users.DoesNotExist:
        return redirect('login')
    
    applications=[]
    for application in Application.objects.all():
        if application.user_name.id == user.id:
            applications.append(application)

    return render(request,'dashboard/app-status.html',{'applications':applications})

def change_pass(request):
    uname = request.session['user']
    if not uname:
        return redirect('login')
    try:
        user = Users.objects.get(email=uname)

    except Users.DoesNotExist:
        return redirect('login')
    
    if request.method == 'POST':
        form = ChangePassForm(request.POST)
        
        
        if form.is_valid():
            curr_pass=form.cleaned_data['current_password']
            new_pass=form.cleaned_data['new_password']
            con_pass=form.cleaned_data['confirm_password']
            if check_password(curr_pass,user.password):
                try:
                    validate_password(new_pass)
                    if new_pass == con_pass:
                        user.password = make_password(new_pass)
                        user.save()
                        messages.success(request,'You password is changed successfully.')
                        form=ChangePassForm()
                        
                    else :
                        messages.error(request,'Your new password does not matches confirm password field.')
                        form=ChangePassForm()
                except ValidationError as e:
                    for error in e:
                        messages.warning(request, error)

            else:
                messages.error(request,'You have enterred incorrect current password.')
                form=ChangePassForm()
                
            
    else:
        
        form=ChangePassForm()
    context = {'form':form,'user':user}
    return render(request,'dashboard/change-pass.html',context)


def forget_pass(request):
    if request.method == 'POST':
        email = request.POST.get('user')
        user = Users.objects.filter(email=email).first()
        if user is not None:
            otp = random.randint(100000,999999)
            user.otp = otp
            user.save()
            send_mail(
                "OTP for reseting your password ",
                f"Your OTP is {otp}",
                "khushdhameliya007@gmail.com",
                [user.email],
                fail_silently=False,
            )
            return JsonResponse({'status':1})
        else :
            return JsonResponse({'status':0})
    else:
        return render(request,'dashboard/forget-pass.html')

@csrf_protect
def confirm_otp(request):
    if request.method == "POST":
        otp =  request.POST.get('otp')
        uname = request.POST.get('user')
        user =  Users.objects.get(email=uname)
        if str(user.otp) == otp:
            user.otp = None
            return JsonResponse({'status':1})
        else:
            return JsonResponse({'status':0})
    
@csrf_protect
def new_pass(request):
    if request.method == 'POST':
        new_pass = request.POST.get('npass')
        
        uname = request.POST.get('user')
        user = Users.objects.get(email=uname)
        try:
            validate_password(new_pass)
            
            user.password = make_password(new_pass)
            user.save()
            print("done")
            return JsonResponse({'status':1})
        
                
        except ValidationError as e:
            return JsonResponse({'status':0})
    else:
        return JsonResponse({'status':0})

def logout(request):
    try:
        del request.session['user']
    except:
        return login(request)
    return login(request)
