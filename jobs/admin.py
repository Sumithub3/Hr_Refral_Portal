from django.contrib import admin
from .models import job, post, apply, contact, profile
# Register your models here.
admin.site.register(job)
admin.site.register(post)
admin.site.register(apply)
admin.site.register(contact)
admin.site.register(profile)
