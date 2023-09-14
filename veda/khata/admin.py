from django.contrib import admin
from .models import User,openaccount,depositetype,applyloan

admin.site.register(User)
admin.site.register(openaccount)
admin.site.register(depositetype)
admin.site.register(applyloan)