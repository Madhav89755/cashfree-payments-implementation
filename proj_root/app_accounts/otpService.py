from django.contrib.auth.models import User
from django.utils import timezone
from .models import OtpModel

class OTPService:

    def __init__(self, email):
        self.email=email
        self.user_obj=User.objects.get(username=email)

    def create_otp(self):
        OtpModel.objects.filter(user=self.user_obj).delete()
        otp_obj=OtpModel.objects.create(user=self.user_obj)
        print(f"===========Your OTP for {self.email} is {otp_obj.otp} is valid for 5 minutes.=========")
        return otp_obj.otp

    def validate_otp(self, otp):
        otp_obj=OtpModel.objects.get(user=self.user_obj, otp=otp)
        is_valid=False
        if ((timezone.now()-otp_obj.created_on).total_seconds() / 60)<5:
            is_valid=True
        OtpModel.objects.filter(user=self.user_obj).delete()
        return is_valid
