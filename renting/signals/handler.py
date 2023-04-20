from django.db.models.signals import post_save, post_delete
from django.dispatch import  receiver

from django.contrib.auth import get_user_model
User = get_user_model()

from renting.models import Landlord, Manager, UserLocation

# @receiver(post_save,sender=User)
# def create_manager_or_landlord(sender,**kwargs):
#     if kwargs['created']:
#         user=kwargs['instance']
#         if user.is_manager==True:
#             Manager.objects.create(user=user,gender="",phone_number="",profile_image="")
#             UserLocation.objects.create(user=user,province=None,district=None,sector=None,cell=None)
#         elif user.is_landlord==True:
#             Landlord.objects.create(user=user,gender="",phone_number="",profile_image="")
#             UserLocation.objects.create(user=user,province=None,district=None,sector=None,cell=None)
