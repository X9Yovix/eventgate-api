from django.contrib import admin
from events.models import Event, EventImage, Tag

admin.site.register(Event)
admin.site.register(EventImage)
admin.site.register(Tag)
