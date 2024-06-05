from django.shortcuts import render,redirect
from .forms import RegistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.

def register(request):

    if request.method == 'POST':
        form=RegistrationForm(request.POST)
        if form.is_valid():
            first_name   = form.cleaned_data['first_name']
            last_name    = form.cleaned_data['last_name']
            email        = form.cleaned_data['email']
            password     = form.cleaned_data['password']

            user = Account.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                email=email,
                username=email.split('@')[0],
                password=password,
                )
            user.save()

            current_site   = get_current_site(request)
            mail_subject   = 'please activate your account'
            message        = render_to_string('accounts/account_varification_email.html',{

                                'user'   : user,
                                'domain' : current_site,
                                'uidb64'    : urlsafe_base64_encode(force_bytes(user.pk)),
                                'token'  : default_token_generator.make_token(user),

                                })
            
            to_email       = email
            send_mail      = EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()


            # messages.success(request,'your Registration is successfull to ACTIVATE your account please click link sent to your {{email}}')
            return redirect('/account/signin/?command=varification&email='+email)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f": {error}")
            return redirect('register')
    else:

        form=RegistrationForm()
    context={
            'form':form
        }
    return render(request,'accounts/register.html',context)

def signin(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        password= request.POST.get('password')
        

        user= auth.authenticate(request,email=email,password=password)

        if user is not None: 
            auth.login(request,user)
            return redirect('home')

        else:
           
            messages.error(request,"invalid credentials")
            return redirect('signin')


    return render(request,'accounts/signin.html')
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    messages.success(request,'you are successfully logout!!')
    return redirect('signin')

def activate(request,uidb64,token):
    try:

        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        user.is_active= True
        user.save()
        messages.success(request,'Congratulations your account is activated!!')
        return redirect('signin')
    return redirect('signin')

def dashboard(request):
    return render(request,'accounts/dashboard.html')

def forgotpassword(request):
    if request.method == 'POST':
        email=request.POST['email']
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email=email)
            current_site   = get_current_site(request)
            mail_subject   = 'Reset your password'
            message        = render_to_string('accounts/resetpasswordmessage.html',{

                                'user'   : user,
                                'domain' : current_site,
                                'uidb64'    : urlsafe_base64_encode(force_bytes(user.pk)),
                                'token'  : default_token_generator.make_token(user),

                                })
            
            to_email       = email
            send_mail      = EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()

        else:
            messages.error(request,"Given email doesnot exit!")
    return render(request,'accounts/forgetpassword.html')

def resetpassword(request,uidb64,token):
    try:

        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None
    
    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid
        return redirect('resetnewpassword')
    else:
        messages.error(request,'link expired!!')

def resetnewpassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if password == confirm_password:
            uid=request.session['uid']
            user=Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request,'your reset successfully!')
            return redirect('signin')
        else:
            messages.error(request,'password doesnt matched!')
            return redirect('resetnewpassword')

    return render(request,'accounts/resetpasswordpage.html')
