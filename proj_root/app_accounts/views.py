from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from .models import UserProfile, UserOrder
from .paymentService import CashfreePaymentService
from .otpService import OTPService

# Create your views here.


def home(request):
    return render(request, 'home.html')

def login_user(request):
    method=request.method
    context={}
    match method:
        case 'GET':
            return render(request, 'login.html', context)
        case 'POST':
            email=request.POST.get('emailid')

            if not email:
                messages.error(request, "All Fields are required.")
            else:
                try:
                    context['email']=email
                    OTPService(email=email).create_otp()
                    messages.success(request, "OTP Sent Successfully.")
                    return render(request, 'otp_verification.html', context)
                except User.DoesNotExist as e:
                    messages.error(request, "User with this email does not exists.")
                except Exception as e:
                    print(str(e))
                    messages.error(request, "An unknown error Occurred.")

            return render(request, 'login.html', context)
        case _:
            return render(request, 'login.html', context)

def register(request):
    method=request.method
    context={}
    match method:
        case 'GET':
            return render(request, 'register.html', context)
        case 'POST':
            first_name=request.POST.get('first_name')
            last_name=request.POST.get('last_name')
            email=request.POST.get('emailid')
            phone_no=request.POST.get('phone_no')

            if not first_name or not last_name or not email or not phone_no:
                messages.error(request, "All Fields are required.")
            else:
                try:
                    resp=CashfreePaymentService().create_customer(email=email,
                                                                phone_number=phone_no,
                                                                first_name=first_name,
                                                                last_name=last_name)
                    
                    print('response', resp)
                    with transaction.atomic():
                        user_obj=User.objects.create(first_name=first_name, last_name=last_name, email=email, username=email)
                        user_profile_obj=UserProfile.objects.create(
                            user=user_obj,
                            phone_number=phone_no,
                            cashfree_customer_id=resp.get('customer_uid')
                        )

                        messages.success(request, "User Registered Success.")
                        context['message']="User Created Successfully"
                except Exception as e:
                    messages.error(request, "An unknown error Occurred.")

            return render(request, 'register.html', context)
        case _:
            return render(request, 'register.html', context)


def verify_otp(request):
    if request.method=='POST':
        email=request.POST.get('email')
        otp=request.POST.get('otp')

        otp_valid=OTPService(email=email).validate_otp(otp)
        if not otp_valid:
            messages.error(request, "OTP is not valid.")
            return redirect("/login")
        messages.success(request, "OTP Verified Successfully.")
        user = User.objects.get(email=email)
        if user is not None:
            login(request, user)
            return redirect("dashboard")

        return redirect("/dashboard")
    return redirect("/")

@login_required(login_url='/login')
def dashboard(request):
    if request.method=='POST':
        context={}
        customer=UserProfile.objects.get(user=request.user)
        customer_id=customer.cashfree_customer_id
        ph_no=customer.phone_number
        amount=request.POST.get("amount")
        description=request.POST.get("description")
        try:
            resp=CashfreePaymentService().create_order(customer_id=customer_id, customer_phone=ph_no, amount=amount, description=description)
            if "cf_order_id" in resp:
                UserOrder.objects.create(
                    order_id=resp['cf_order_id'],
                    user=request.user,
                    order_amount=amount
                )

                context['payment_session_id']=resp['payment_session_id']
                return render(request, 'checkout.html', context)
        except Exception as e:
            print("Error Occurred", str(e))
    return render(request, 'dashboard.html')

@login_required(login_url='/login')
def logout_user(request):
    logout(request)
    return redirect("/")