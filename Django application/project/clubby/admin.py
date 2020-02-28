from django.contrib import admin

# this adds to the admin dashboard the operation to manipulate question objects.
# you can add any object to the list and manipulate it directly.
from .models import Question
from .models import Choice

admin.site.register(Question)
admin.site.register(Choice)

