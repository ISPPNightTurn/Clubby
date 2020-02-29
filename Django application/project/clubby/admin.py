from django.contrib import admin

# this adds to the admin dashboard the operation to manipulate question objects.
# you can add any object to the list and manipulate it directly.
# this can be improved upon by following this tutorial:
# https://docs.djangoproject.com/en/3.0/intro/tutorial07/

# these models are here as an example:
from .models import Question,Choice
admin.site.register(Question)
admin.site.register(Choice)

from .models import Profile,Club,Event
admin.site.register(Profile)
admin.site.register(Club)
admin.site.register(Event)

