from background_task import background
from django.contrib.auth.models import User, Group
from datetime import datetime
from decimal import Decimal


@background(schedule=60)
def check_premium(owner_id):
    # lookup user by id and send them a message
    owner = User.objects.filter(pk=owner_id)[0]
    profile = owner.profile

    now = datetime.now()
    # we make the payment at 2AM  of the 2nd day to avoid 
    # timezone problems so no matter server location this always works.
    if(now.month == 12):
        next_payment = datetime(now.year+1, 1 , 2, 2)
    else:
        next_payment = datetime(now.year,now.month +1 , 2, 2)

    if(profile.funds < Decimal("15")):
        profile.renew_premium = False
        my_group = Group.objects.get(name='premium owner') 
        my_group.user_set.remove(owner)
        profile.save()

        #check_premium(owner_id, schedule=next_payment ,creator=owner)
        check_premium(owner_id, schedule=600, creator=owner)#every 60 seconds

    if(profile.funds >= Decimal("15") and profile.renew_premium):
        profile.funds -=  Decimal("15")
        profile.save()
        
        check_premium(owner_id, schedule=600, creator=owner)#every 60 seconds
        # check_premium(owner_id, schedule=next_payment ,creator=owner) 
