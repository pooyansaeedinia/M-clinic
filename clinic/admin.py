from django.contrib import admin

from .models import Procedure, ProcedureImage


class ProcedureImageInline(admin.TabularInline):
    model = ProcedureImage
    extra = 1


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name_en',)}
    inlines = [ProcedureImageInline]


@admin.register(ProcedureImage)
class ProcedureImageAdmin(admin.ModelAdmin):
    list_display = ('procedure', 'created_at')
    list_filter = ('procedure',)
