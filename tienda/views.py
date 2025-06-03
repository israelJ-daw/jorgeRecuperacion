from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from django.http import Http404

from .models import *
# Create your views here.

def index(request):
    return render(request, 'index.html', {})

@permission_required('tienda.view_cliente')
def lista_clientes(request):
    clientes = Cliente.objects.all()
    
    return render(request, 'clientes/lista_clientes.html', {'clientes': clientes})


def registrar_usuario(request):

    if request.method == 'POST':
        formulario = RegistroForm(request.POST)
        if formulario.is_valid():
            user = formulario.save()
            rol = int(formulario.cleaned_data.get('rol'))
            if (rol == Usuario.CLIENTE):
                grupo = Group.objects.get(name='clientes')
                grupo.user_set.add(user)
                cliente = Cliente.objects.create(Usuario=user)
                cliente.save()
            elif (rol == Usuario.VENDEDOR):
                grupo=Group.objects.get(name='vendedores')
                grupo.user_set.add(user)
                vendedor= Vendedor.objects.create(Usuario=user)
                vendedor.save()
                
            login(request,user)    
            return redirect('index')
        
    else:
        formulario = RegistroForm()   
    return render(request, 'registration/signup.html', {'formulario': formulario})


def lista_vendedores(request):
    vendedores = Vendedor.objects.all()

    return render (request, 'vendedores/lista_vendedores.html', {'vendedores': vendedores})


def lista_coches(request):
    coches = Coche.objects.all()

    return render (request, 'coches/lista_coche.html', {'coches': coches})

permission_required('tienda.add_coche')
def crear_coche(request):
    if request.method == 'POST':
        formulario = cocheModelForms(request.POST)
        if formulario.is_valid():
            print ("Es validoo!")
            formulario.save()
            messages.success(request, 'Se ha creado perfectamente')
            return redirect ("lista_coche")
    else:
        formulario = cocheModelForms()
    return render (request, 'coches/crear_coche.html', {'formulario': formulario})

    
def lista_tienda(request):
    tiendas = Tienda.objects.filter(vendedor=request.user.vendedor).all() 
    return render(request, 'tienda/lista_tienda.html', {'tiendas': tiendas})


def coche_detalle(request, id_coche):
    coche = Coche.objects.get(id=id_coche)
    return render (request, 'coches/coche_detalle.html',{'coche' : coche}) 

def coche_editar(request, id_coche):
    coche = Coche.objects.get(id = id_coche)
    
    if request.method == "POST": 
        formulario = cocheModelForms(request.POST, instance=coche)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, 'Se ha modificado perfectamente')            
            return redirect ('coche_detalle', id_coche = id_coche) 
    else:
        formulario = cocheModelForms(instance=coche)     
        
    return render (request, 'coches/coche_editar.html', {'formulario' : formulario, 'lola' : coche })   


def tienda_detalle(request, id_tienda):
    tienda = Tienda.objects.get(id=id_tienda)
    return render (request, 'tienda/tienda_detalle.html',{'tienda' : tienda}) 


def tienda_editar(request, id_tienda):
    tienda = Tienda.objects.get(id = id_tienda)
    
    if request.method == "POST": 
        formulario = TiendaModelForms(request.POST, instance=tienda)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, 'Se ha modificado perfectamente')            
            return redirect ('tienda_detalle', id_tienda = id_tienda) 
    else:
        formulario = TiendaModelForms(instance=tienda)     
        
    return render (request, 'tienda/tienda_editar.html', {'formulario' : formulario, 'tienda' : tienda })   

def coche_eliminar(request, id_coche):
    coche = Coche.objects.get(id=id_coche)
    
    try:
        coche.delete()
        messages.success(request, "se ha eliminado el coche " + coche.nombre  +"correctamente")
    except Exception as Error:
        print(Error)
    return redirect ('lista_coche')        

def detalle_cliente(request, id_cliente):
    if request.user.cliente.id == id_cliente:
        cliente = Cliente.objects.get(id = id_cliente)
        return render (request, 'clientes/detalles_cliente.html', {'cliente': cliente} )
    else:
        raise Http404()
 

def ver_cuenta(request, id_cliente):
    cuenta = CuentaBancaria.objects.filter(cliente_id=id_cliente).first()
    
    return render (request, 'clientes/cuenta.html', {'cuenta' : cuenta} )

def crear_tienda(request):
    if request.method == 'POST':
        formulario = TiendaModelForms(request.POST)
        if formulario.is_valid():
            tienda = Tienda.objects.create(
                nombre = formulario.cleaned_data.get("nombre"),
                direccion = formulario.cleaned_data.get("direccion"),
                telefono = formulario.cleaned_data.get("telefono"),
                vendedor = request.user.vendedor,
            )   
            tienda.save()
            return redirect ("lista_tienda")
    else:
        formulario = TiendaModelForms()

    return render (request, 'tienda/crear_tienda.html', {'formulario': formulario})

def crear_cuenta(request):
    if request.method == 'POST':
        formulario = CuentaModelForms(request.POST)
        if formulario.is_valid():
            cuenta = CuentaBancaria.objects.create(
                iban = formulario.cleaned_data.get("iban"),
                banco = formulario.cleaned_data.get("banco"),
                tipo = formulario.cleaned_data.get("tipo"),
                cliente = request.user.cliente,  
            )
            cuenta.save()
            messages.success(request, 'Se ha Creado Su cuenta')  
            return redirect ("detalle_cliente", id_cliente=request.user.cliente.id)
    else:
        formulario = CuentaModelForms()

    return render (request, 'clientes/crear_cuenta.html', {'formulario': formulario})

def eliminar_cuenta(request, id_cuenta):
    cuenta = CuentaBancaria.objects.get(id=id_cuenta)

    try:
        cuenta.delete()  
        messages.success(request, "Se ha eliminado la cuenta bancaria correctamente.")
    except Exception as error:
        print(error)

    return redirect('ver_cuenta', id_cliente=cuenta.cliente.id) 

def cuenta_editar(request, id_cuenta):
    cuenta = CuentaBancaria.objects.get(id = id_cuenta)
    
    if request.method == "POST": 
        formulario = CuentaModelForms(request.POST, instance=cuenta)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, 'Se ha modificado perfectamente')            
        return redirect('ver_cuenta', id_cliente=cuenta.cliente.id) 
    else:
        formulario = CuentaModelForms(instance=cuenta)     
        
    return render (request, 'clientes/cuenta_editar.html', {'formulario' : formulario, 'cuenta' : cuenta })   


def detalle_vendedor(request, id_vendedor):
 
    if request.user.vendedor.id == id_vendedor:
        vendedor = Vendedor.objects.get(id = id_vendedor)
        return render (request, 'vendedores/detalle_vendedor.html', {'vendedor': vendedor} )
    else:
        raise Http404()


def ver_datos(request, id_vendedor):
    vendedor = DatosVendedor.objects.filter(vendedor_id=id_vendedor).first()
    
    return render (request, 'vendedores/datos_vendedor.html', {'vendedor' : vendedor} )

def crear_datos(request):
    if request.method == 'POST':
        formulario = DatosModelForms(request.POST)
        if formulario.is_valid():
            datos = DatosVendedor.objects.create(
                direccion = formulario.cleaned_data.get("direccion"),
                facturacion = formulario.cleaned_data.get("facturacion"),
                vendedor = request.user.vendedor,  
            )
            datos.save()
            messages.success(request, 'Se ha Creado Sus Datos')  
            return redirect ("detalle_vendedor", id_vendedor=request.user.vendedor.id)
    else:
        formulario = DatosModelForms()

    return render (request, 'vendedores/crear_datos.html', {'formulario': formulario})

def eliminar_datos (request, id_vendedor):
    vendedor = DatosVendedor.objects.get(id=id_vendedor)

    try:
        vendedor.delete()  
        messages.success(request, "Se han eliminado los datos Correctamente.")
    except Exception as error:
        print(error)

    return redirect('ver_datos', id_vendedor=vendedor.vendedor.id) 

def datos_editar(request, id_vendedor):
    vendedor = DatosVendedor.objects.get(id = id_vendedor)
    
    if request.method == "POST": 
        formulario = DatosModelForms(request.POST, instance=vendedor)
        if formulario.is_valid:
            formulario.save()
            messages.success(request, 'Se ha modificado perfectamente')            
        return redirect('ver_datos', id_vendedor=vendedor.vendedor.id) 
    else:
        formulario = DatosModelForms(instance=vendedor)     
        
    return render (request, 'vendedores/datos_editar.html', {'formulario' : formulario, 'vendedor' : vendedor })   


permission_required("tienda.add_inventario")
def crear_inventario(request):
    
    if request.method == 'POST':
        formulario = CrearInventarioForms(request.POST, request=request)
        if formulario.is_valid():
            inventario = Inventario.objects.filter(tienda = formulario.cleaned_data.get("tienda"), coches = formulario.cleaned_data.get("coches")).first()
            if (inventario is None):
                formulario.save()
            else: 
                inventario.cantidad += formulario.cleaned_data.get("cantidad")
                inventario.save()     
            messages.success(request, 'Se ha añadido Correctamente')
            return redirect ("lista_tienda")
    else:
        formulario = CrearInventarioForms(None, request=request)
    return render (request, 'inventario/crear_inventario.html', {'formulario': formulario})



def lista_productos(request, tienda_id):
    productos = Inventario.objects.filter(tienda_id=tienda_id)

    return render(request, 'inventario/lista_productos.html', {'productos': productos})


def productos_editar(request, id_producto):
    productos = Inventario.objects.get(id=id_producto)
    
    if request.method == "POST": 
        formulario = CrearInventarioForms(request.POST, request=request, instance=productos)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Se ha modificado correctamente.')
            return redirect('lista_productos', tienda_id=productos.tienda.id)
    else:
        formulario = CrearInventarioForms(request=request, instance=productos)
        
    return render(request, 'inventario/productos_editar.html', {'formulario': formulario, 'productos': productos})

    

def eliminar_productos (request, id_productos):
    productos = Inventario.objects.get(id=id_productos)

    try:
        productos.delete()  
        messages.success(request, "Se han eliminado El producto Correctamente.")
    except Exception as error:
        print(error)

    return redirect('lista_productos', tienda_id=productos.tienda.id) 


def ver_productos (request):
    if (len(request.GET)> 0):
        formulario = BusquedaInventario(request.GET)
        if formulario.is_valid():
            nombre = formulario.cleaned_data.get("nombre")
            productos = Inventario.objects.filter(coches__nombre__icontains=nombre)
    else: 
        productos = Inventario.objects.all()
        formulario = BusquedaInventario()

    
    return render(request, 'inventario/todos_productos.html', {'productos': productos, 'formulario' : formulario})


def crear_pedidos (request):

    if request.method == 'POST':
        formulario = CrearPedidoForms (request.POST)
        if formulario.is_valid():
            pedidos = Pedidos.objects.create(
                coche = formulario.cleaned_data.get("coche"),
                fecha_pedido = formulario.cleaned_data.get("fecha_pedido"),
                cantidad = formulario.cleaned_data.get("cantidad"),
                direccion = formulario.cleaned_data.get("direccion"),
                cliente = request.user.cliente,  
            )
            pedidos.save()
            messages.success(request, 'Se ha Creado Su Pedido')  
            return redirect ("index")
    else:
        formulario = CrearPedidoForms()

    return render (request, 'clientes/crear_pedidos.html', {'formulario': formulario})


def buscarProductos(request):
    
    if (len(request.GET)> 0):
        formulario = BusquedaInventario(request.GET)
        if formulario.is_valid():
            nombre = formulario.cleaned_data.get("nombre")
            productos = Inventario.objects.filter(coches__nombre__icontains=nombre)
    else: 
        productos = Inventario.objects.all()
        formulario = BusquedaInventario()

    
    return render(request, 'inventario/todos_productos.html', {'productos': productos, 'formulario' : formulario})



def lista_pedidos(request):
    producto = Inventario.objects.all()
    pedidos= Pedidos.objects.select_related("cliente").all()
    return render(request, "inventario/listar_pedidos.html", {'pedidos_mostrar': pedidos, 'productos':producto})



def producto_comprar_antigua(request, id_inventario):
    productos = Inventario.objects.get(id = id_inventario)
    
    if request.method == 'POST':
        formulario = cantidadComprar(request.POST, inventario = productos)
        if formulario.is_valid():
            cantidad = formulario.cleaned_data.get("cantidad")
            direccion = formulario.cleaned_data.get("direccion")
            productos.cantidad -= cantidad
            productos.save()
            pedidos = Pedidos.objects.create(
                coche = productos.coches,
                cantidad = cantidad,
                direccion = direccion,
                precio = productos.precio,
                tienda = productos.tienda,
                cliente = request.user.cliente,  
            )
            
            pedidos.save()
            messages.success(request, 'Se ha realizado su compra')  
            return redirect('index')
        
    else:
        formulario = cantidadComprar(inventario = productos)
    
    return render(request, 'inventario/producto_comprar.html', {'productos': productos, 'formulario': formulario})


def producto_comprar_nueva(request, id_inventario):
    productos = Inventario.objects.get(id = id_inventario)
    
    if request.method == 'POST':
        formulario = cantidadComprar(request.POST, inventario = productos)
        if formulario.is_valid():
            cantidad = formulario.cleaned_data.get("cantidad")
            
            pedido = Pedidos.objects.filter(cliente = request.user.cliente, estado = "pen").first()
            
            
            if (pedido is None):
            
                pedido = Pedidos.objects.create(
                    
                    cliente = request.user.cliente,  
                )
                pedido.save()

            lineapedidos = LineaPedidos.objects.create(

                pedido = pedido,
                coche = productos.coches,
                tienda = productos.tienda,
                precio = productos.precio,
                cantidad = cantidad
                )
                
            
            lineapedidos.save()


            messages.success(request, 'Se ha realizado su pedido')  
            return redirect('index')
        
    else:
        formulario = cantidadComprar(inventario = productos)
    
    return render(request, 'inventario/producto_comprar.html', {'productos': productos, 'formulario': formulario})

def lista_linea_pedidos (request, id_cliente):
    pedidos = LineaPedidos.objects.filter(pedido__cliente_id=id_cliente) 

    return render(request, 'inventario/listar_linea_pedidos.html', {'pedidos': pedidos })


def eliminar_linea_pedidos (request, id_pedido):
    productos = LineaPedidos.objects.get(id=id_pedido)

    try:
        productos.delete()  
        messages.success(request, "Se han eliminado El pedido Correctamente.")
    except Exception as error:
        print(error)

    return redirect('lista_linea_pedidos', id_cliente=request.user.cliente.id)


def editar_linea_pedido(request, id_pedido):
    linea = LineaPedidos.objects.get(id=id_pedido)
    
    if request.method == 'POST':
        formulario = cantidadEditar(request.POST, instance=linea)
        if formulario.is_valid():

            linea.cantidad = formulario.cleaned_data.get("cantidad")
            linea.save()
            messages.success(request, "Cantidad actualizada correctamente.")
            return redirect("lista_linea_pedidos", id_cliente=request.user.cliente.id)
    else:
        formulario = cantidadEditar(instance=linea)

    return render(request, 'inventario/editar_linea_pedido.html', {'formulario': formulario, 'linea': linea})



def finalizar_pedido(request):
    pedido = Pedidos.objects.filter(cliente=request.user.cliente, estado='pen').first()

    if not pedido:
        messages.error(request, "No se ha encontrado el pedido o el estado no es el esperado.")
        return redirect("index") 

    if request.method == 'POST':    
        formulario = FinalizarCompra(request.POST)
        if formulario.is_valid():
            pedido.direccion = formulario.cleaned_data.get("direccion")
            pedido.estado = 'comp'

            lineas = LineaPedidos.objects.filter(pedido=pedido)
            for linea in lineas:
                inventario = Inventario.objects.get(
                tienda=linea.tienda,
                coches=linea.coche  )
        
            inventario.cantidad -= linea.cantidad
            inventario.save()


            pedido.save()

            LineaPedidos.objects.filter(pedido=pedido).delete()
        
            messages.success(request, "Tu compra se ha realizado con éxito.")
            return redirect("lista_pedidos")
    
    else:
        formulario = FinalizarCompra()
        
    return render(request, 'inventario/finalizar_pedido.html', {'formulario': formulario, 'pedido': pedido})


def eliminar_pedidos(request, id_pedido):
    pedido = Pedidos.objects.filter(id=id_pedido).first()

    if pedido:
        try:
            pedido.delete()  
            messages.success(request, "Se ha eliminado el pedido correctamente.")
        except Exception as error:
            print(error)
            messages.error(request, "Hubo un error al intentar eliminar el pedido.")
    else:
        messages.warning(request, "El pedido no existe.")

    return redirect('lista_pedidos')



def busqueda_inventario(request):
    form = BusquedaInventarioForm(request.GET)
    
    productos = Inventario.objects.all()

    if form.is_valid():
        tienda = form.cleaned_data.get('tienda')
        coche = form.cleaned_data.get('coche')
        cantidad_min = form.cleaned_data.get('cantidad_min')
        cantidad_max = form.cleaned_data.get('cantidad_max')
        precio_min = form.cleaned_data.get('precio_min')
        precio_max = form.cleaned_data.get('precio_max')

        if tienda:
            productos = productos.filter(tienda__nombre__icontains=tienda)
        if coche:
            productos = productos.filter(coches__nombre__icontains=coche)
        if cantidad_min:
            productos = productos.filter(cantidad__gte=cantidad_min)
        if cantidad_max:
            productos = productos.filter(cantidad__lte=cantidad_max)
        if precio_min:
            productos = productos.filter(precio__gte=precio_min)
        if precio_max:
            productos = productos.filter(precio__lte=precio_max)

    return render(request, 'inventario/buscar_inventario.html', {
        'form': form,
        'productos': productos
    })


def detalles_pago(request, id_clientes):
    pedidos = Pedidos.objects.filter(cliente__id=id_clientes)
    
    tienda = Tienda.objects.all()
    try:
        cuenta_bancaria = CuentaBancaria.objects.get(cliente__id=id_clientes)
    except CuentaBancaria.DoesNotExist:
        cuenta_bancaria = None
    
    # Inicializar el total pagado
    total_pagado = 0 

    # Calcular el total pagado por todos los pedidos
    for pedido in pedidos:
        for linea in pedido.lineapedidos_set.all():
            total_pagado += linea.precio * linea.cantidad

    # Pasar los pedidos, el total pagado y la cuenta bancaria a la plantilla
    return render(request, 'pago/detalles_pago.html', {
        'total_pagado': total_pagado,
        'pedidos': pedidos,
        'cuenta_bancaria': cuenta_bancaria,
        'tiendas' : tienda
    })


def devolver_pedido(request, pedido_id):
    # Obtener el pedido
    pedido = Pedidos.objects.filter(id=pedido_id, cliente=request.user.cliente).first()

    # Verificar si el pedido existe y si pertenece al cliente
    if not pedido:
        return render(request, 'errores/404.html', {'message': 'El pedido no existe o no pertenece a tu cuenta.'})

    # Cambiar el estado del pedido a 'devuelto'
    pedido.estado = 'dev'
    pedido.save()

    # Recorrer los productos del pedido y actualizar el inventario
    for linea in pedido.lineapedidos_set.all():
        coche = linea.coche
        tienda = linea.tienda
        cantidad_devuelta = linea.cantidad

        # Actualizar el inventario de la tienda
        inventario = Inventario.objects.get(tienda=tienda, coches=coche)
        inventario.cantidad += cantidad_devuelta  # Aumentamos el stock con la cantidad devuelta
        inventario.save()

    # Redirigir a la página de éxito o detalles del pedido
    return render(request, 'pago/devolver.html', {'pedido': pedido})



#Paginas de error 
def mi_error_404(request, exception=None):
    return render (request, 'errores/404.html',None, None,404)

def mi_error_500(request, exception=None):
    return render (request, 'errores/500.html',None, None,500)