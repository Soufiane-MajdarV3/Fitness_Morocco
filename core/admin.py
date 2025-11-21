from django.contrib import admin
from .models import SiteConfig, ContactMessage


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'commission_percentage')
    fields = ('site_name', 'tagline', 'contact_email', 'contact_phone', 'address', 'about_us',
              'facebook_url', 'twitter_url', 'instagram_url', 'commission_percentage')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
    actions = ['mark_as_read']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"
