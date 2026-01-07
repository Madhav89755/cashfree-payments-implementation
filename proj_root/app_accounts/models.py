import random
import string
from functools import partial
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.


class CommonModel(models.Model):
    created_on = models.DateTimeField(_("Created On"), auto_now_add=True)
    updated_on = models.DateTimeField(_("Updated On"), auto_now=True)

    class Meta:
        abstract = True


class UserProfile(CommonModel):
    user = models.OneToOneField(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="user_profile",
    )
    phone_number = models.CharField(_("Phone Number"), max_length=15)
    cashfree_customer_id = models.CharField(_("Cashfree Customer Id"), max_length=100)

    def __str__(self):
        return f"{self.user} - {self.cashfree_customer_id}"


class UserOrder(CommonModel):
    order_id = models.CharField(_("Order Id"), max_length=20, primary_key=True)
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="user_orders",
    )
    currency = models.CharField(_("Currency"), max_length=5, default="INR")
    order_amount = models.PositiveBigIntegerField(default=0)
    is_payment_done = models.BooleanField(_("Payment Done"), default=False)

    def __str__(self):
        return f"{self.user} - {self.order_id}"


class TransactionStatus(models.TextChoices):
    STARTED = ("started", "started")
    FAILED = ("failed", "failed")
    DONE = ("done", "done")


class UserTransactions(CommonModel):
    user = models.OneToOneField(
        User,
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="user_transactions",
    )
    order = models.ForeignKey(
        UserOrder,
        verbose_name=_("User Order"),
        on_delete=models.CASCADE,
        related_name="order_transaction",
    )
    amount = models.PositiveBigIntegerField(default=0)
    status = models.CharField(
        _("Transaction Status"), max_length=7, choices=TransactionStatus.choices
    )

    def __str__(self):
        return f"{self.user} - {self.order_id} - {self.pk}"


def random_string(length=6):
    chars = string.ascii_letters + string.digits
    return "".join(random.choice(chars) for _ in range(length))


class OtpModel(CommonModel):
    user = models.OneToOneField(
        User, verbose_name=_("User"), on_delete=models.CASCADE, related_name="user_otp"
    )
    otp = models.CharField(
        _("OTP"),
        default=partial(random_string),
        max_length=6,
    )
    def __str__(self):
        return f'{self.user} - {self.otp}'
