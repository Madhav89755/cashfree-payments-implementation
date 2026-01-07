from django.contrib import admin

# Register your models here.
from .models import UserProfile, UserOrder, UserTransactions, OtpModel

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display=['pk', 'user_id', 'phone_number']
    search_fields=['pk', 'user_id', 'cashfree_customer_id']

@admin.register(UserOrder)
class UserOrderAdmin(admin.ModelAdmin):
    list_display=['pk', 'order_id', 'currency', 'order_amount']
    search_fields=['pk', 'order_id', 'user']
    list_filter=['is_payment_done']

@admin.register(UserTransactions)
class UserTransactionsAdmin(admin.ModelAdmin):
    list_display=['pk', 'order', 'amount', 'status']
    search_fields=['pk', 'order']
    list_filter=['status']


@admin.register(OtpModel)
class OtpAdmin(admin.ModelAdmin):
    list_display=['pk', 'user', 'otp', 'created_on']