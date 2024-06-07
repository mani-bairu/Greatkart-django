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

from cart.models import Cart,Cart_items
from cart.views import _cart_id

import requests

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

            try:
                cart=Cart.objects.get(cart_id=_cart_id(request))
                cart_items_exist = Cart_items.objects.filter(cart=cart).exists()
                if cart_items_exist:
                    #geting product variations by cart id
                    cart_items = Cart_items.objects.filter(cart=cart)
                    product_variations=[]
                    for items in cart_items:
                        variations= items.variation.all()
                        product_variations.append(list(variations))

                    print(product_variations)

                    # get the cart item from the user to access his product variations
                    cart_items = Cart_items.objects.filter(user=user)
                    ex_var_list=[]
                    id=[]
                    for items in cart_items:
                        variations= items.variation.all()
                        ex_var_list.append(list(variations))
                        id.append(items.id)
                    print(ex_var_list)

                    for pr in product_variations:
                        if pr in ex_var_list:
                            print('enter in pr in ex_var_list')
                            index= ex_var_list.index(pr)
                            item_id= id[index]
                            print('id:',item_id)
                            item = Cart_items.objects.get(id=item_id)
                            print(item.user)
                            print(item.quantity)
                            print(item.cart)
                            item.quantity += 1
                            item.user=user
                            item.save()
                            print(item.quantity)
                        else:
                            cart_items = Cart_items.objects.filter(cart=cart)
                            for items in cart_items:
                                items.user=user
                                items.save()
                else:
                    cart_items = Cart_items.objects.filter(cart=cart)
                    for items in cart_items:
                        items.user=user
                        items.save()


            except Exception as e:
                print(e)
                
            auth.login(request,user)
            messages.success(request,"you are now logged in ")
            url=request.META.get('HTTP_REFERER')
            try:
                query=requests.utils.urlparse(url).query
                # it gives next=/cart/checkout/
                parms=dict(x.split('=') for x in query.split('&') )
                print('this is dict',parms)
                #it gives dictionry value {'next':'/cart/checkout,'}
                for next in parms:
                    nextpage=parms[next]
                    print("this will redirect to next page",nextpage)
                    return redirect(nextpage)
            except:
                return redirect('home')

        else:
           
            messages.error(request,"invalid credentials")
            return redirect('signin')


    return render(request,'accounts/signin.html')


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
