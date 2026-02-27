from django.contrib import admin
from .models import CustomUser,UserProfile
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    
    model=CustomUser
    list_display=("email","is_superuser",'is_staff',"is_verified")
    list_filter=("is_superuser","is_staff")
    search_fields=("email",)
    ordering=("email",)
    fieldsets = (
    (None, {"fields": ("email", "password")}),
    
    ("Permissions", {"fields": ("is_active", "is_staff",'is_verified', "is_superuser", "groups", "user_permissions")}),
    
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "password1", "password2", "is_staff", "is_superuser"),
        }),
        )

admin.site.register(CustomUser, CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    model=UserProfile
    list_display=("first_name","user","last_name")
    search_fields=("first_name","last_name","city","province")
    list_filter=("first_name","last_name","city","province")
    

admin.site.register(UserProfile,UserProfileAdmin)