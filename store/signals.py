from . models import Customer
from . models import SmsCode
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save,sender=Customer)
def post_save_generate_code(sender,instance,created,*args,**kwargs):
    if created:
        SmsCode.objects.create(customer=instance)