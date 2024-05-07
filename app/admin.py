from django.contrib import admin
from .models import Profile, Pet, User, MedicalRecord, VaccinationRecord
from django.conf import settings
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html

admin.site.register(Profile)

class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'breed', 'age', 'color', 'formatted_weight')
    list_filter = ('owner', 'breed')
    search_fields = ('name', 'breed', 'owner__username')

    def formatted_weight(self, obj):
        return f"{obj.weight} lbs"
    formatted_weight.admin_order_field = 'weight'  # Allows column order sorting
    formatted_weight.short_description = 'Weight (lbs)'  # Column header

    # if admin clicks 'other' in the color field, a text box will appear and they can enter a custom color
    def formfield_for_choice_field(self, db_field, request, **kwargs):
        if db_field.name == 'color':
            kwargs['choices'] = settings.COLOR_CHOICES
        return super().formfield_for_choice_field(db_field, request, **kwargs)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.color == 'other':
            form.base_fields['custom_color'].widget = forms.TextInput()
        return form

    def save_model(self, request, obj, form, change):
        if obj.color != 'other':
            obj.custom_color = ''
        super().save_model(request, obj, form, change)

    fieldsets = (
        (None, {
            'fields': ('name', 'owner', 'breed', 'age', 'color', 'weight')
        }),
        ('Custom Color', {
            'fields': ('custom_color',),
            'description': 'Specify custom color if "Other" is selected',
        }),
    )

admin.site.register(Pet, PetAdmin)

COLOR_CHOICES = getattr(settings, 'COLOR_CHOICES', [])

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

class MedicalRecordAdmin(admin.ModelAdmin):
    # Ensure 'list_display' only contains fields or methods that are defined
    list_display = ['display_user']  # Example fields

    def display_user(self, obj):
        return obj.pet.owner  # Assuming 'pet' is related to 'MedicalRecord' and has an 'owner' attribute
    display_user.short_description = 'User'

admin.site.register(MedicalRecord, MedicalRecordAdmin)

class VaccinationRecordAdmin(admin.ModelAdmin):
    list_display = ['pet', 'uploaded_date', 'document_link']
    list_filter = ['pet']
    search_fields = ['pet__name']

    def document_link(self, obj):
        return format_html("<a href='{}'>View Document</a>", obj.document.url)
    document_link.short_description = 'Document'

admin.site.register(VaccinationRecord, VaccinationRecordAdmin)