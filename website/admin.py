from django.contrib import admin
#import from created Record db model
from .models import Record #import from created Record db model

admin.site.register(Record)
