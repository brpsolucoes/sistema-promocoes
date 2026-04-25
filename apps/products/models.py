from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    MARKETPLACE_CHOICES = [
        ('amazon', 'Amazon'),
        ('mercadolivre', 'Mercado Livre'),
        ('americanas', 'Americanas'),
        ('magalu', 'Magazine Luiza'),
        ('casasbahia', 'Casas Bahia'),
        ('outro', 'Outro'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Ativo'),
        ('inactive', 'Inativo'),
    ]

    name = models.CharField(max_length=200, verbose_name="Nome do Produto")
    url = models.URLField(max_length=500, verbose_name="URL do Produto")
    marketplace = models.CharField(
        max_length=20, 
        choices=MARKETPLACE_CHOICES, 
        verbose_name="Marketplace"
    )
    notify_whatsapp = models.BooleanField(
        default=False, 
        verbose_name="Notificar no WhatsApp"
    )
    notify_telegram = models.BooleanField(
        default=False, 
        verbose_name="Notificar no Telegram"
    )
    notify_promotion = models.BooleanField(
        default=True, 
        verbose_name="Monitorar Promoções"
    )
    price_target = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True, 
        verbose_name="Preço Alvo"
    )
    description = models.TextField(
        blank=True, 
        verbose_name="Descrição"
    )
    category = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Categoria"
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='active',
        verbose_name="Status"
    )
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name="Cadastrado por"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Data de Cadastro"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Última Atualização"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
