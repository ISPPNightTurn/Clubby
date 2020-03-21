from background_task import background
from django.contrib.auth.models import User

@background(schedule=60)
def check_premium():
    # lookup user by id and send them a message
    User.objects.filter(groups__name='premium owner')


    user = User.objects.get(pk=user_id)
    user.email_user('Here is a notification', 'You have been notified')