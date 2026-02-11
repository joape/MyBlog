from django.contrib import admin
from .models import Post

# Register your models here.
#admin.site.register(Post) 
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    show_facets = admin.ShowFacets.ALWAYS #muestra los filtros en la barra lateral del panel de administración, incluso si no hay resultados para esos filtros. Esto puede ser útil para mantener la consistencia en la interfaz de administración y permitir a los administradores ver todas las opciones de filtrado disponibles, incluso si no hay datos que coincidan con esos filtros en ese momento.
    