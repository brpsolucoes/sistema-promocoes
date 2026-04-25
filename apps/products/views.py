from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Product
from .forms import ProductForm


@login_required
def product_list(request):
    query = request.GET.get('q', '')
    marketplace_filter = request.GET.get('marketplace', '')
    status_filter = request.GET.get('status', '')
    
    products = Product.objects.filter(created_by=request.user)
    
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )
    
    if marketplace_filter:
        products = products.filter(marketplace=marketplace_filter)
    
    if status_filter:
        products = products.filter(status=status_filter)
    
    context = {
        'products': products.order_by('-created_at'),
        'query': query,
        'marketplace_filter': marketplace_filter,
        'status_filter': status_filter,
        'marketplace_choices': Product.MARKETPLACE_CHOICES,
        'status_choices': Product.STATUS_CHOICES,
    }
    return render(request, 'products/product_list.html', context)


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm()
    
    context = {
        'form': form,
        'title': 'Cadastrar Produto',
        'button_text': 'Cadastrar'
    }
    return render(request, 'products/product_form.html', context)


@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    
    context = {
        'form': form,
        'product': product,
        'title': 'Editar Produto',
        'button_text': 'Atualizar'
    }
    return render(request, 'products/product_form.html', context)


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk, created_by=request.user)
    
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Produto excluído com sucesso!')
        return redirect('products:list')
    
    context = {
        'product': product
    }
    return render(request, 'products/product_confirm_delete.html', context)
