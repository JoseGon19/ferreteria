from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Producto, Factura, DetalleFactura
from django.contrib import messages
from .cart import Cart

def lista_productos(request):
    
    productos = Producto.objects.all()
    paginator = Paginator(productos, 8)  # 12 por página
    page = request.GET.get("page")
    productos_page = paginator.get_page(page)
    return render(request, "tienda/productos.html", {"productos": productos_page})

def agregar_carrito(request, producto_id):
    cart = Cart(request)
    producto = get_object_or_404(Producto, id=producto_id)
    cantidad = int(request.POST.get("cantidad", 1))
    cart.add(producto, cantidad)
    
    # Mensaje de éxito
    messages.success(request, f'Se agregaron {cantidad} unidad(es) de "{producto.nombre}" al carrito.')
    
    return redirect("lista_productos")

def ver_carrito(request):
    cart = Cart(request)
    return render(request, "tienda/carrito.html", {"cart": cart})

def finalizar_compra(request):
    cart = Cart(request)
    if not cart.cart:
        messages.error(request, "El carrito está vacío")
        return redirect("lista_productos")

    # Crear factura
    total = cart.get_total()
    factura = Factura.objects.create(total=total)

    # Crear detalle de factura y restar stock
    for item in cart.items():
        producto = item['producto']
        cantidad = item['cantidad']
        subtotal = item['total']

        # Restar del inventario
        if producto.stock >= cantidad:
            producto.stock -= cantidad
            producto.save()
        else:
            messages.error(request, f"No hay suficiente stock de {producto.nombre}")
            factura.delete()
            return redirect("ver_carrito")

        # Crear detalle
        DetalleFactura.objects.create(
            factura=factura,
            producto=producto,
            cantidad=cantidad,
            subtotal=subtotal
        )

    # Vaciar carrito
    cart.clear()
    messages.success(request, f"Compra realizada con éxito. Total: ${total:.2f}")
    return redirect("lista_productos")