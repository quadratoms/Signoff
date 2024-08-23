from django.contrib import admin

from client_app.models import DynamicFormField, DynamicFormFieldValue, FormType, UserRequest




admin.site.register(FormType)
admin.site.register(DynamicFormField)
admin.site.register(DynamicFormFieldValue)


class DynamicFormFieldInline(admin.TabularInline):
    model = DynamicFormFieldValue
    extra = 1

class UserRequestAdmin(admin.ModelAdmin):
    inlines = [DynamicFormFieldInline]

admin.site.register(UserRequest, UserRequestAdmin)
# Register your models here.
