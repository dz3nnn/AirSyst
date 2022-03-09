from dataclasses import field
from django.contrib import admin
from django.apps import apps
from .models import *

models = apps.get_models()

admin.site.site_header = "AirSyst"

# Custom

# Project Image


class ProjectImageInline(admin.StackedInline):
    model = Project_Image
    extra = 1


class ProjectAdmin(admin.ModelAdmin):
    inlines = [ProjectImageInline]

# Options


class OptionRelationInline(admin.StackedInline):
    model = OptionRelation
    extra = 1


class EquipImageInline(admin.StackedInline):
    model = Equipment_Image
    extra = 1


class EquipmentItemAdmin(admin.ModelAdmin):
    inlines = [OptionRelationInline, EquipImageInline]
    search_fields = ['article']

# Subcategories


class SubCategoryInline(admin.StackedInline):
    model = EquipmentSubCategory
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]


# Info admin

class InfoAdmin(admin.ModelAdmin):
    search_fields = ['name', 'content']


admin.site.register(Project, ProjectAdmin)
admin.site.register(Equipment_Item, EquipmentItemAdmin)
admin.site.register(EquipmentCategory, CategoryAdmin)
admin.site.register(Info, InfoAdmin)

# Register all other models

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
