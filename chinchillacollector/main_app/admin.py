from django.contrib import admin

# Register your models here.
from .models import Chinchilla, Feeding, Toy, Photo

admin.site.register(Chinchilla)
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)