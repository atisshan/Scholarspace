from django.contrib import admin
from .models import CustomUser, University, Program, ProgramType
from django.contrib.auth.admin import UserAdmin
from django import forms
# Register your models here.


@admin.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('citizenship',)}), 
    )


admin.site.register(University)
admin.site.register(Program)  

class ProgramTypeAdminForm(forms.ModelForm):
    entry_requirements = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        help_text="Enter each requirement on a new line"
    )
admin.site.register(ProgramType) 
class ProgramTypeAdmin(admin.ModelAdmin):
    form = ProgramTypeAdminForm