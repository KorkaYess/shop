from django.views.decorators.http import require_POST
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render
from django.urls import reverse

from .serilizers import ProductSerializer, CategorySerializer, \
    SubcategorySerializer
from .models import Product, Category, Subcategory, CartItem


def home(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'home.html', context={
        'categories': categories,
        'products': products
    })


@require_POST
def cart_add(request, product_id):
    if not Product.objects.filter(id=product_id).exists():
        raise Http404
    cart = request.session.get('cart')
    if cart:
        product = Product.objects.get(id=product_id)
        if CartItem.objects.filter(product=product, id__in=cart).count() > 0:
            item = CartItem.objects.get(product=product, id__in=cart)
            item.quant += 1
            item.save()
            request.session['cart'] = cart
        else:
            item = CartItem.objects.create(product=product, quant=1)
            cart.append(item.id)
            request.session['cart'] = cart
    else:
        product = Product.objects.get(id=product_id)
        item = CartItem.objects.create(product=product, quant=1)
        request.session['cart'] = [item.id]
    return HttpResponseRedirect(reverse('cart_list'))


def cart_list(request):
    cart = request.session.get('cart')
    if cart:
        items = []
        for item in cart:
            try:
                item = CartItem.objects.get(id=item)
                items.append(item)
            except Product.DoesNotExist:
                pass
    else:
        items = []

    total_price = 0
    for item in items:
        total_price += item.product.price * item.quant
    request.session['total_price'] = str(total_price)
    return TemplateResponse(
        request, 'cart.html',
        {'cart': items, 'total_price': total_price}
    )


@require_POST
def cart_delete(request, product_id):
    cart = request.session.get('cart')
    if cart:
        filtered = []
        for product in cart:
            if product != product_id:
                filtered.append(product)
        request.session['cart'] = filtered
    return HttpResponseRedirect(reverse('cart_list'))


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    class Meta:
        model = Product


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    class Meta:
        model = Category


class SubcategoryViewSet(ModelViewSet):
    serializer_class = SubcategorySerializer
    queryset = Subcategory.objects.all()

    class Meta:
        model = SubcategorySerializer
