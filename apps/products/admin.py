from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'name', 
        'marketplace', 
        'status', 
        'price_target', 
        'notify_whatsapp', 
        'notify_telegram', 
        'notify_promotion',
        'created_by',
        'created_at'
    ]
    list_filter = [
        'marketplace', 
        'status', 
        'notify_whatsapp', 
        'notify_telegram', 
        'notify_promotion',
        'created_at'
    ]
    search_fields = ['name', 'description', 'category', 'url']
    list_editable = ['status', 'notify_whatsapp', 'notify_telegram', 'notify_promotion']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'url', 'marketplace', 'category', 'status')
        }),
        ('Configurações de Notificação', {
            'fields': ('notify_whatsapp', 'notify_telegram', 'notify_promotion', 'price_target')
        }),
        ('Informações Adicionais', {
            'fields': ('description', 'created_by'),
            'classes': ('collapse',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(created_by=request.user)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
