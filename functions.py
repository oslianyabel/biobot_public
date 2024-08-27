import odoo
from datetime import datetime
import utils

def sales_order(pedido):
    order_data = odoo.get_sale_order(pedido)
    ans = ""
    if order_data:
        for key, value in order_data.items():
            ans += f"{key}: {value} \n"
    else:
        ans += "No se encontró el pedido especificado."
    return ans


def devoluciones(pedido, motivo):
    order_data = odoo.get_sale_order(pedido)
    if not order_data:
        return "Pedido no encontrado"
    if motivo == "fallo":
        diff = utils.date_diff(order_data['date_order'], datetime.now().strftime('%Y-%m-%d')) / 365
        if int(order_data['date_order'][:4]) >= 2022:
            return "Explique en qué falla y envíe un video mostrando el fallo." if diff <= 3 else "El pedido está fuera de fecha de garantía."
        else:
            return "Explique en qué falla y envíe un video mostrando el fallo." if diff <= 2 else "El pedido está fuera de fecha de garantía."
    else:
        diff = utils.date_diff(order_data['date_order'], datetime.now().strftime('%Y-%m-%d'))
        return "En este caso al tratarse de un producto que está en perfectas condiciones pero ya no deseas, tendrías que hacerte cargo de los portes y enviarlo bien protegido a la siguiente dirección indicando el nombre al que se realizó la compra:\n\n- Biomag SL, (Mars Gaming)\n- C/ Barrachi 39, Local 3, 01013\n- Vitoria (Álava)\n- ATT. Javi\n\nY una vez lo recibamos procederemos con elreembolso del pedido" if diff <= 14 else "El pedido está fuera de fecha de garantía"
    
    
def repuestos(tipo_producto, modelo):
    return "Responde lo siguiente: Tool repuestos en desarrollo"


def compatibilidades(tipo_producto, producto):
    return "Responde lo siguiente: Tool compatibilidades en desarrollo"


def software(tipo_producto, producto):
    return "Responde lo siguiente: Tool software en desarrollo"


def stock(tipo_producto, producto):
    return "Responde lo siguiente: Tool stock en desarrollo"


def product_list(quantity):
    products = odoo.get_ecommerce_products(quantity)
    ans = ""
    for product in products:
        for key, value in product.items():
            ans += f"{key}: {value}"
        ans += "\n"
        
    return ans


def product_list_price():
    products = odoo.get_ecommerce_products(10, order='list_price desc')
    ans = "10 productos mas caros:\n"
    for product in products:
        for key, value in product.items():
            ans += f"{key}: {value}"
        ans += "\n"
        
    return ans


def product_detail(product_name):
    product = odoo.get_product_name(product_name)
    ans = ""
    ans += "Información del Producto: \n"
    for key, value in product.items():
        ans += f"{key}: {value} \n"
    return ans


#sin agregar a api pq falla
def topSellingProduct(date, sortBy):
    product = odoo.topSellingProduct(date, sortBy)
    ans = ""
    for key, value in product.items():
        ans += f"{key}: {value} \n"
    return ans


def top_customer(fecha):
    customer = odoo.get_top_customer_by_invoices(fecha)
    ans = ""
    for key, value in customer.items():
        ans += f"{key}: {value} \n"
    return ans
  
  
#Reporte de ventas  
def sales_report(fecha_inicio, fecha_fin = datetime.now().strftime('%Y-%m-%d')):
    report = odoo.get_sales_report(fecha_inicio, fecha_fin)
    ans = ""
    for key, value in report.items():
        ans += f"{key}: {value} \n"
    return ans


#Limpia chat
def clear_chat():
    return "Historial eliminado."


def orders_by_date(fecha):
    orders = odoo.get_orders_by_date(fecha)
    ans = ""
    for order in orders:
        for key, value in order.items():
            ans += f"{key}: {value}, "
        ans = ans[:-2]+".\n"
    return ans


#Pedidos de mayor costo en un periodo
def orders_by_amount(fecha_inicio = '2000-01-01', fecha_fin = datetime.now().strftime('%Y-%m-%d'), limit = 10):
    orders = odoo.get_top_orders_by_amount(fecha_inicio, fecha_fin, limit)
    ans = ""
    for order in orders:
        for key, value in order.items():
            ans += f"{key}: {value}, "
        ans = ans[:-2]+".\n"
    return ans


#Historial de Compras del Cliente
def customer_history(customer_name):
    purchase_history = odoo.get_purchase_history_by_customer_name(customer_name)
    sum_amount_total = 0
    date_min = datetime.now()
    date_max = datetime(2020, 1, 1, 0, 0, 0)
    for order in purchase_history:
        sum_amount_total += order["amount_total"]
        date = datetime.strptime(order["date_order"], "%Y-%m-%d %H:%M:%S")
        if date < date_min:
            date_min = date
        if date > date_max:
            date_max = date

    ans = ""
    ans += f"Total de compras:{len(purchase_history)} \n"
    ans += f"Importe Total:{sum_amount_total} \n"
    ans += f"Primera compra en: {date_min}, última compra en: {date_max}"
    return ans


#Total de Ventas Generadas por el Cliente en un periodo
def customer_amount_by_date(customer_name, start_date, end_date):
    data = odoo.get_total_sales_by_customer(customer_name, start_date, end_date)
    return f"El cliente ha realizado {data[1]} compras con un importe total de ${data[0]}"


#Clientes con facturas pendientes de pago
def customer_with_pending_orders_to_pay():
    ans = odoo.get_customers_with_pending_invoices()
    return f"Hay {ans} vendedores con pedidos pendientes de pago."


#facturas pendientes a pagar
def pending_invoices_to_pay():
    invoices_total = odoo.get_pending_invoices_to_pay()
    return f"Hay {invoices_total} facturas pendientes por pagar."


#Producto más vendido del Trimestre
def top_product(start_date, end_date):
    product = odoo.get_top_selling_product(start_date, end_date)
    ans = ""
    for key, value in product.items():
        ans += f"{key}: {value}, "
    ans = ans[:-2]
    return ans


#Pedidos pendientes de envio
def pending_orders():
    orders = odoo.get_pending_shipments()
    ans = ""
    for order in orders:
        for key, value in order.items():
            ans += f"{key}: {value}, "
        ans = ans[:-2]+".\n"
    return ans


#número de pedidos cancelados este mes
def canceled_orders_this_month():
    total_orders = odoo.get_canceled_orders_this_month()
    return f"Este mes se han cancelado {total_orders} ordenes"


#stock del producto
def product_stock(product_name):
    return odoo.get_product_stock_level(product_name)


#productos con stock bajo
def products_low_stock():
    return odoo.get_products_with_low_stock()


#facturas pagadas en los últimos 7 días
def paid_invoices_last_7_days():
    invoices = odoo.get_paid_invoices_last_7_days()
    ans = ""
    for order in invoices:
        for key, value in order.items():
            ans += f"{key}: {value}, "
        ans = ans[:-2]+".\n"
    return ans


#Ventas por productos
def sales_by_product(start_date, end_date):
    data = odoo.get_sales_by_product(start_date, end_date)
    if len(data) > 50:
        sum = 0
        for key, value in data.items():
            sum += value
        
        prom = sum/len(data)
        return f"Hay demasiados productos({len(data)}) para escribirlos 1 por 1. El promedio de ingresos por producto es de ${prom}"
    else:
        ans = ""
        for key, value in data.items():
            ans += f"{key}: ${value}, "
        ans = ans[:-2]+".\n"
        return ans
    
    
#ventas por cliente
def sales_summary_by_customer(start_date, end_date):
    data = odoo.get_sales_summary_by_customer(start_date, end_date)
    if len(data) > 50:
        sum = 0
        for key, value in data.items():
            sum += value
        
        prom = sum/len(data)
        return f"Hay demasiados clientes({len(data)}) para escribirlos 1 por 1. El promedio de ingresos por clientes es de ${prom}"
    else:
        ans = ""
        for key, value in data.items():
            ans += f"{key}: ${value}, "
        ans = ans[:-2]+".\n"
        return ans
    

#productos con mayor margen beneficio
def products_highest_margin():
    products = odoo.get_products_highest_margin()
    ans = ""
    for product in products:
        for key, value in product.items():
            ans += f"{key}: {value}, "
        ans = ans[:-2]+".\n"
    return ans


#devoluciones realizadas en un rango de fechas
def returns_processed(start_date, end_date):
    ret_total = odoo.get_returns_processed(start_date, end_date)
    return f"Se efectuaron {ret_total} devoluciones en ese tiempo."


#clientes potenciales mas recientes
def recent_leads():
    customers = odoo.get_recent_leads()
    ans = ""
    for customer in customers:
        for key, value in customer.items():
            ans += f"{key}: {value}, "
        ans = ans[:-2]+".\n"
    return ans


def admin_actions():
    ans = "Estas son las acciones que puedes realizar: \n" \
        "- Consultar el historial de compras del cliente. \n" \
        "- Consultar el total de ventas generadas por un cliente. \n" \
        "- Consultar los clientes con facturas pendientes de pago. \n" \
        "- Consultar las ventas totales en un periodo de tiempo. \n" \
        "- Consultar el vendedor que ha generado más ventas en un periodo de tiempo. \n" \
        "- Consultar el producto más vendido en un periodo de tiempo. \n" \
        "- Consultar los pedidos de venta pendientes de envío. \n" \
        "- Consultar cuántos pedidos se han cancelado este mes. \n" \
        "- Consultar el nivel actual de stock de un producto. \n" \
        "- Consultar qué productos tienen menos de 10 unidades en stock. \n" \
        "- Consultar las facturas pendientes de pago. \n" \
        "- Consultar el monto total facturado en un periodo de tiempo. \n" \
        "- Consultar qué facturas han sido pagadas en los últimos 7 días. \n" \
        "- Consultar el informe de ventas de un periodo de tiempo. \n" \
        "- Consultar las ventas por producto en un periodo de tiempo. \n" \
        "- Consultar el resumen de ventas de un cliente para un periodo de tiempo. \n" \
        "- Consultar la información detallada de un producto. \n" \
        "- Consultar los productos con mayor margen de beneficio. \n" \
        "- Consultar las devoluciones que se han procesado en un periodo de tiempo. \n" \
        "- Consultar los clientes potenciales más recientes. \n"
            
    return ans

def user_actions():
    ans = "Estas son las acciones que puedes realizar: \n" \
        "- Consultar el estado de un pedido. \n" \
        "- Solicitar una devolución. \n" \
        "- Consultar los repuestos de un producto. \n" \
        "- Solicitar información de un producto. \n" \
        "- Consultar las compatibilidades de un producto. \n" \
        "- Consultar los software de un producto. \n" \
        "- Consultar la entrada en stock de un producto. \n"
    
    return ans