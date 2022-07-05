from django.contrib import admin

from .models import Books, Payments

admin.site.register(Books)
admin.site.register(Payments)

