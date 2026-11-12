from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Producto, Categoria
from .forms import ConsultaClienteForm
from .forms import ProductoForm
from django.db.models import Count, Avg, Sum

# 1. Landing Page + Catálogo (Pública)
def home(request):
    productos = Producto.objects.select_related('categoria').all()
    categorias = Categoria.objects.all()
    return render(request, 'home.html', {
        'productos': productos,
        'categorias': categorias
    })

# 2. Registro de Usuario (Pública)
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Cuenta creada exitosamente para {username}. ¡Ahora puedes iniciar sesión!')
            return redirect('login')  # Redirige a la pantalla de login tras registrarse
    else:
        form = UserCreationForm()
    
    return render(request, 'registro.html', {'form': form})

# 3. Lógica del Carrito (Requiere Autenticación)
@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, pk=producto_id)
    cantidad = int(request.POST.get('cantidad', 1))

    if cantidad > producto.stock:
        messages.error(request, f"No hay suficiente stock disponible ({producto.stock} unidades).")
        return redirect('home')

    carrito = request.session.get('carrito', {})
    str_id = str(producto_id)

    if str_id in carrito:
        nueva_cantidad = carrito[str_id]['cantidad'] + cantidad
        if nueva_cantidad > producto.stock:
            messages.error(request, f"Excedes el stock disponible ({producto.stock} unidades).")
            return redirect('ver_carrito')
        carrito[str_id]['cantidad'] = nueva_cantidad
    else:
        carrito[str_id] = {
            'nombre': producto.nombre,
            'precio': float(producto.precio),
            'cantidad': cantidad,
            'imagen': producto.imagen or ''
        }

    request.session['carrito'] = carrito
    messages.success(request, f"Se agregó '{producto.nombre}' al carrito.")
    return redirect('ver_carrito')

@login_required
def ver_carrito(request):
    carrito = request.session.get('carrito', {})
    for item in carrito.values():
        item['subtotal'] = item['precio'] * item['cantidad']
    total = sum(item['subtotal'] for item in carrito.values())
    request.session['carrito'] = carrito
    return render(request, 'carrito.html', {'carrito': carrito, 'total': total})

@login_required
def eliminar_del_carrito(request, producto_id):
    carrito = request.session.get('carrito', {})
    str_id = str(producto_id)
    if str_id in carrito:
        del carrito[str_id]
        request.session['carrito'] = carrito
        messages.info(request, "Producto eliminado del carrito.")
    return redirect('ver_carrito')

@login_required
def procesar_compra(request):
    carrito = request.session.get('carrito', {})
    if not carrito:
        messages.warning(request, "El carrito está vacío.")
        return redirect('home')

    # Verificar stock
    for item_id, item_data in carrito.items():
        producto = get_object_or_404(Producto, pk=item_id)
        if producto.stock < item_data['cantidad']:
            messages.error(request, f"Stock insuficiente para {producto.nombre}.")
            return redirect('ver_carrito')

    # Descontar stock
    for item_id, item_data in carrito.items():
        producto = Producto.objects.get(pk=item_id)
        producto.stock -= item_data['cantidad']
        producto.save()

    # Vaciar carrito
    request.session['carrito'] = {}
    messages.success(request, "¡Compra realizada con éxito! El stock ha sido actualizado.")
    return redirect('home')


# 1. CREAR REGISTRO
def producto_crear_web(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige al listado principal
    else:
        form = ProductoForm()
    return render(request, 'producto_form.html', {'form': form, 'accion': 'Crear'})

# 2. EDITAR REGISTRO EXISTENTE
def producto_editar_web(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('home')  # Redirige al listado principal
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'producto_form.html', {'form': form, 'accion': 'Editar'})

# 3. ELIMINAR CON CONFIRMACIÓN
def producto_eliminar_web(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('home')  # Redirige al listado principal
    return render(request, 'producto_confirm_delete.html', {'producto': producto})

def panel_administracion(request):
    productos = Producto.objects.all()
    return render(request, 'panel_admin.html', {'productos': productos})


def reporte_agrupacion(request):
    """Reporte 1: Resumen por categoría (cantidad, precio promedio y stock total)."""
    reporte_categorias = Producto.objects.values('categoria').annotate(
        total_productos=Count('id'),
        precio_promedio=Avg('precio'),
        stock_total=Sum('stock')
    )
    return render(request, 'reporte_agrupacion.html', {'reporte': reporte_categorias})

def reporte_umbral(request):
    """Reporte 2: Listado de productos bajo un umbral de stock crítico (ej. stock <= 5)."""
    stock_critico = Producto.objects.filter(stock__lte=5).order_by('stock')
    return render(request, 'reporte_umbral.html', {'productos': stock_critico})

def contacto_view(request):
    # Uso de sesiones: contar visitas del usuario a esta sección
    visitas = request.session.get('visitas_contacto', 0) + 1
    request.session['visitas_contacto'] = visitas

    if request.method == 'POST':
        form = ConsultaClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contacto_exito.html', {'visitas': visitas})
    else:
        form = ConsultaClienteForm()

    return render(request, 'contacto.html', {'form': form, 'visitas': visitas})