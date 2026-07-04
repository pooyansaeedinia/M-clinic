from django.contrib import admin

from .models import GallerySection, Procedure, SectionImage


class SectionImageInline(admin.TabularInline):
    model = SectionImage
    extra = 1
    fields = ('title_en', 'title_tr', 'image_type', 'image')


class GallerySectionInline(admin.TabularInline):
    model = GallerySection
    extra = 1
    show_change_link = True


@admin.register(Procedure)
class ProcedureAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name_en',)}
    inlines = [GallerySectionInline]


@admin.register(GallerySection)
class GallerySectionAdmin(admin.ModelAdmin):
    list_display = ('procedure', 'created_at')
    list_filter = ('procedure',)
    inlines = [SectionImageInline]


@admin.register(SectionImage)
class SectionImageAdmin(admin.ModelAdmin):
    list_display = ('section', 'title_en', 'image_type', 'created_at')
    list_filter = ('image_type', 'section__procedure')
