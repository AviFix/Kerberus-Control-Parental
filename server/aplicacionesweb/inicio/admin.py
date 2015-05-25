from inicio.models import Anuncio
from django.contrib import admin

class AnuncioAdmin(admin.ModelAdmin):
    fields = ['descripcion', 'url','path_imagen']
    list_display = ('descripcion', 'url','path_imagen')
    search_fields = ['descripcion']

admin.site.register(Anuncio, AnuncioAdmin)
