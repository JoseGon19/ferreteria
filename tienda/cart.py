from decimal import Decimal
from tienda.models import Producto

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart

    def add(self, producto, cantidad=1):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            self.cart[producto_id]['cantidad'] += cantidad
            self.cart[producto_id]['total'] = self.cart[producto_id]['cantidad'] * float(producto.precio)
        else:
            self.cart[producto_id] = {
                'cantidad': cantidad,
                'precio': float(producto.precio),
                'total': float(producto.precio) * cantidad
            }
        self.save()

    def remove(self, producto):
        producto_id = str(producto.id)
        if producto_id in self.cart:
            del self.cart[producto_id]
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.session.modified = True

    def save(self):
        self.session.modified = True

    def __iter__(self):
        productos_ids = self.cart.keys()
        productos = Producto.objects.filter(id__in=productos_ids)
        for producto in productos:
            item = self.cart[str(producto.id)]
            item["producto"] = producto
            item["precio"] = Decimal(item["precio"])
            item["total"] = item["precio"] * item["cantidad"]
            yield item

    def get_total(self):
        return sum(Decimal(item["precio"]) * item["cantidad"] for item in self.cart.values())
    
    def items(self):
        for producto_id, item in self.cart.items():
            producto = Producto.objects.get(id=producto_id)
            yield {
                'producto': producto,
                'cantidad': item['cantidad'],
                'precio': item['precio'],
                'total': item['total']
            }