from django.contrib import admin

# this adds to the admin dashboard the operation to manipulate question objects.
# you can add any object to the list and manipulate it directly.
# this can be improved upon by following this tutorial:
# https://docs.djangoproject.com/en/3.0/intro/tutorial07/


from .models import Profile,Club,Event,Rating,Receipt,Reservation,Ticket,Hookah,Product
admin.site.register(Profile)
admin.site.register(Club)
admin.site.register(Event)
admin.site.register(Rating)
admin.site.register(Receipt)
admin.site.register(Reservation)
admin.site.register(Ticket)
admin.site.register(Hookah)
admin.site.register(Product)


