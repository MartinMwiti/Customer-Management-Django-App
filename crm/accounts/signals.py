#NB: Don't forget to change settings.py file as well as the app.py file in order for this to work

from django.db.models.signals import post_save
#from django.dispatch import receiver

from django.contrib.auth.models import User, Group
from .models import Customer


# ASSIGNING NEW USERS TO A CUSTOMER PROFILE AND ASSIGNING THEM TO CUSTOMER GROUP. This removes the code from the registration func in views.py file
# @receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):

	# If a user has been created and saved(form.save() part), run below code. This is triggered by the 'post_save' i.e after saving, run 'customer_profile' func.
	if created:
            group = Group.objects.get(name='customer')
            instance.groups.add(group) # Associate a new user with the 'customer' account Group
            Customer.objects.create(
                user=instance,
                name = instance.username
            )  # make sure when a new user registers, he/she is linked to customer profile.
            # print('Profile created!')

post_save.connect(customer_profile, sender=User) # this line provide similar result to the receiver decorator. Can switch if you want





# @receiver(post_save, sender=User)
# def update_profile(sender, instance, created, **kwargs):

# 	if created == False:
#         instance.profile.save()
#         print('Profile updated!')


#post_save.connect(update_profile, sender=User)
