from django.contrib import admin

# Register your models here.
# admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile, Scholarship, Application, Document, FAQItem, Notification

# --- Profile modelini User Admin paneliga inline qo'shish ---
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profil Ma\'lumotlari'
    fk_name = 'user'
    # Profile'dagi ba'zi maydonlarni inline'da ko'rsatish
    fields = ('role', 'avatar', 'phone', 'birth_date', 'iin', 'address')

class CustomUserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_role') # Rolni qo'shish
    list_select_related = ('profile',) # So'rovlarni optimallashtirish

    def get_role(self, instance):
        # Foydalanuvchi rolini olish (agar profil mavjud bo'lsa)
        try:
            return instance.profile.get_role_display()
        except Profile.DoesNotExist:
            return "Profil yo'q"
    get_role.short_description = 'Rol' # Ustun nomi

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Standart UserAdmin ni o'chirib, o'zimiznikini ro'yxatdan o'tkazamiz
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# --- Scholarship Admin ---
@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ('name', 'provider', 'deadline', 'type', 'status', 'popular', 'created_at')
    list_filter = ('status', 'type', 'field', 'popular', 'deadline')
    search_fields = ('name', 'provider', 'description')
    list_editable = ('status', 'popular') # Tez o'zgartirish uchun
    date_hierarchy = 'deadline' # Sana bo'yicha iyerarxiya
    fieldsets = (
        (None, {
            'fields': ('name', 'provider', 'description')
        }),
        ('Asosiy Ma\'lumotlar', {
            'fields': ('amount', 'deadline', 'field', 'type', 'status', 'popular')
        }),
    )

# --- Document modelini Application Admin paneliga inline qo'shish ---
class DocumentInline(admin.TabularInline): # Yoki StackedInline
    model = Document
    extra = 1 # Sukut bo'yicha 1 ta qo'shimcha yuklash joyi
    fields = ('document_type', 'file')
    readonly_fields = ('uploaded_at',) # Yuklangan sanani o'zgartirib bo'lmaydi

# --- Application Admin ---
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'scholarship', 'submission_date', 'status', 'last_updated')
    list_filter = ('status', 'scholarship', 'submission_date')
    search_fields = ('applicant__username', 'scholarship__name', 'applicant_full_name', 'applicant_email', 'applicant_iin')
    readonly_fields = ('submission_date', 'last_updated', 'applicant', 'scholarship', 'confirm_accuracy', 'confirm_terms') # Odatda ariza yuborilgach o'zgarmaydigan maydonlar
    date_hierarchy = 'submission_date'
    inlines = [DocumentInline] # Hujjatlarni shu yerda boshqarish

    fieldsets = (
        ('Asosiy Ariza Ma\'lumotlari', {
            'fields': ('applicant', 'scholarship', 'status', 'review_notes')
        }),
        ('Ariza Beruvchi Ma\'lumotlari (Ariza paytidagi)', {
            'classes': ('collapse',), # Sukut bo'yicha yopiq turishi uchun
            'fields': (
                'applicant_full_name', 'applicant_birth_date', 'applicant_iin',
                'applicant_phone', 'applicant_email', 'applicant_address'
            )
        }),
        ('Ta\'lim Ma\'lumotlari (Ariza paytidagi)', {
            'classes': ('collapse',),
            'fields': ('university', 'faculty', 'course', 'gpa', 'achievements', 'essay')
        }),
         ('Tasdiqlash va Sanalar', {
            'fields': ('confirm_accuracy', 'confirm_terms', 'submission_date', 'last_updated')
        }),
    )

    # Statusni tez o'zgartirish uchun action qo'shish (ixtiyoriy)
    actions = ['mark_as_reviewing', 'mark_as_approved', 'mark_as_rejected']

    def mark_as_reviewing(self, request, queryset):
        queryset.update(status='reviewing')
    mark_as_reviewing.short_description = "Statusni 'Ko'rib chiqilmoqda' ga o'zgartirish"

    def mark_as_approved(self, request, queryset):
        queryset.update(status='approved')
    mark_as_approved.short_description = "Statusni 'Ma'qullangan' ga o'zgartirish"

    def mark_as_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_as_rejected.short_description = "Statusni 'Rad etilgan' ga o'zgartirish"


# --- FAQItem Admin ---
@admin.register(FAQItem)
class FAQItemAdmin(admin.ModelAdmin):
    list_display = ('question', 'is_active', 'order')
    list_filter = ('is_active',)
    search_fields = ('question', 'answer')
    list_editable = ('is_active', 'order')

# --- Notification Admin ---
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_short_message', 'is_read', 'created_at', 'link')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message')
    list_display_links = ('user', 'get_short_message') # Xabarga bosib kirish uchun
    readonly_fields = ('user', 'message', 'link', 'created_at') # Odatda bildirishnomalar tizim tomonidan yaratiladi

    def get_short_message(self, obj):
        # Xabarni qisqartirib ko'rsatish
        return obj.message[:70] + '...' if len(obj.message) > 70 else obj.message
    get_short_message.short_description = 'Xabar matni'