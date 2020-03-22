from background_task import background
from django.contrib.auth.models import User
from datetime import datetime

@background(schedule=60)
def check_premium(owner_id):
    # lookup user by id and send them a message
    owner = User.objects.filter(pk=owner_id)[0]
    
    user.email_user('Here is a notification', 'You have been notified')
    now = datetime.now()
    # we make the payment at 2AM  of the 2nd day to avoid 
    # timezone problems so no matter server location this always works.
    if(now.month == 12):
        next_payment = datetime(now.year+1,1,2,2)
    else:
        next_payment = datetime(now.year,now.month +1 ,2,2)



    check_premium(owner_id, schedule=next_payment)