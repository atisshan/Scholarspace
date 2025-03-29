from django.contrib import admin
from .models import CustomUser, University, Program, ProgramType
from django.contrib.auth.admin import UserAdmin
# Register your models here.


@admin.register(CustomUser)

class CustomUserAdmin(admin.ModelAdmin):
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('citizenship',)}), 
    )


admin.site.register(University)
admin.site.register(Program)  
admin.site.register(ProgramType) 