from dotenv import load_dotenv
from typing import Dict, Any, List
from getToken import get_oauth_token
from fetchOdooData import fetch_odoo_data
from datetime import datetime, timedelta

def get_ecommerce_products(limit, order='name asc'):
    token = get_oauth_token()
    if token is None:
        return None

    domain = [
        ['sale_ok', '=', True],
        ['active', '=', True],
        ['type', '=', 'product'],
        ['price', '>', 0]
    ]
    fields = [
        'id',
        'name',
        'categ_id',
        'list_price',
        'description',
        'default_code'
    ]

    product_data = fetch_odoo_data(
        'product.template',
        domain,
        fields,
        token,
        None,  # No group by
        limit,
        order
    )

    return product_data


def get_product_name(name):
    token = get_oauth_token()
    domain = [['name', 'ilike', name]]
    fields = ['id', 'name', 'categ_id', 'list_price', 'description', 'weight', 'qty_available', 'sale_ok', 'type', 'image_1920', 'standard_price']
    group_by = ['id']
    limit = 10

    product_data = fetch_odoo_data(
        'product.template',
        domain,
        fields,
        token,
        group_by,
        limit
    )

    return product_data[0]


def get_sale_order(num_order):
    token = get_oauth_token()
    domain = [['name', '=', num_order]]
    fields = [
        'id',
        'name',
        'partner_id',
        'date_order',
        'amount_total',
        'state'
    ]
    sale_order = fetch_odoo_data('sale.order', domain, fields, token)
    return sale_order[0]

    
def get_sales_report(start_date: str, end_date: str) -> Dict[str, Any]:
    token = get_oauth_token()
    #end_date = datetime.now().strftime('%Y-%m-%d')

    domain = [
        ['invoice_date', '>=', start_date],
        ['invoice_date', '<=', end_date],
        ['move_type', '=', 'out_invoice'],
        ['state', '=', 'posted']
    ]

    fields = ['amount_total', 'partner_id']
    group_by = ['partner_id']

    invoice_data = fetch_odoo_data(
        'account.move',
        domain,
        fields,
        token,
        group_by,
        limit=None,
        order=None
    )

    if not invoice_data:
        return {
            'total_sales': 0,
            'total_invoices': 0,
            'average_sales_per_invoice': 0,
            'total_customers': 0,
            'highest_invoice_value': 0,
            'lowest_invoice_value': 0
        }

    total_sales = 0
    highest_invoice_value = 0
    lowest_invoice_value = float('inf')
    customer_set = set()

    for invoice in invoice_data:
        invoice_value = invoice['amount_total']
        total_sales += invoice_value
        if invoice_value > highest_invoice_value:
            highest_invoice_value = invoice_value
        if invoice_value < lowest_invoice_value:
            lowest_invoice_value = invoice_value
        customer_set.add(invoice['partner_id'][0])

    total_invoices = len(invoice_data)
    total_customers = len(customer_set)
    average_sales_per_invoice = total_sales / total_invoices

    return {
        'total_sales': total_sales,
        'total_invoices': total_invoices,
        'average_sales_per_invoice': average_sales_per_invoice,
        'total_customers': total_customers,
        'highest_invoice_value': highest_invoice_value,
        'lowest_invoice_value': 0 if lowest_invoice_value == float('inf') else lowest_invoice_value
    }
    
    
def get_top_customer_by_invoices(date: str) -> Dict[str, Any]:
    token = get_oauth_token()
    current = datetime.now().strftime('%Y-%m-%d')
    print(date)

    domain = [
        ['invoice_date', '>=', date],
        ['invoice_date', '<=', current],
        ['move_type', '=', 'out_invoice'],
        ['state', '=', 'posted']
    ]

    fields = ['partner_id', 'amount_total']
    group_by = ['partner_id']

    invoice_data = fetch_odoo_data(
        'account.move',
        domain,
        fields,
        token,
        group_by,
        limit=None,
        order=None
    )

    if not invoice_data:
        return None

    customer_data = {}
    for invoice in invoice_data:
        partner_id = invoice['partner_id'][0]
        amount_total = invoice['amount_total']

        if partner_id not in customer_data:
            customer_data[partner_id] = {'count': 0, 'totalAmount': 0}

        customer_data[partner_id]['count'] += 1
        customer_data[partner_id]['totalAmount'] += amount_total

    top_customer = None
    max_invoices = 0
    total_amount = 0
    for partner_id, data in customer_data.items():
        if data['count'] > max_invoices:
            max_invoices = data['count']
            top_customer = partner_id
            total_amount = data['totalAmount']

    if top_customer is None:
        return None

    customer = fetch_odoo_data(
        'res.partner',
        [['id', '=', top_customer]],
        ['name'],
        token
    )

    if not customer:
        return None

    response = {
        'customer_name': customer[0]['name'],
        'invoice_count': max_invoices,
        'total_amount': total_amount
    }

    return response


def topSellingProducts(startDate, sortBy):
    token = get_oauth_token()
    if token is None:
        return None
    
    current = datetime.now()
    current_date_str = current.strftime('%Y-%m-%d')

    domain = [
        ['invoice_date', '>=', startDate],
        ['invoice_date', '<=', current_date_str],
        ['product_id', '!=', False],
        ['quantity', '>', 0],
        ['price_subtotal', '>', 0]
    ]
    fields = ['product_id', 'quantity', 'price_subtotal']
    group_by = ['product_id']

    invoice_lines = fetch_odoo_data(
        'account.move.line',
        domain,
        fields,
        token,
        group_by,
        None, #No limit
        None #No order
    )

    if not invoice_lines or len(invoice_lines) == 0:
        return []

    # Agrupar por producto y sumar las cantidades e ingresos
    product_sales = {}
    for line in invoice_lines:
        if isinstance(line['product_id'], list) and line['quantity'] > 0:
            product_id, product_name = line['product_id']
            if product_id not in product_sales:
                product_sales[product_id] = {
                    'product_name': product_name,
                    'total_qty': 0,
                    'total_sales': 0
                }
            product_sales[product_id]['total_qty'] += line['quantity']
            product_sales[product_id]['total_sales'] += line['price_subtotal']

    # Encontrar el producto con la mayor cantidad vendida o el mayor total de ventas
    top_selling_product = {'total_qty': 0, 'total_sales': 0}
    for product in product_sales.values():
        if sortBy == 'qty' and product['total_qty'] > top_selling_product['total_qty']:
            top_selling_product = product
        elif sortBy == 'sale' and product['total_sales'] > top_selling_product['total_sales']:
            top_selling_product = product

    return top_selling_product


#pedidos en un dia
def get_orders_by_date(date):
    token = get_oauth_token()
    if token is None:
        return None

    model = 'sale.order'
    date_str = datetime.strptime(date, '%Y-%m-%d').strftime('%Y-%m-%d')
    domain = [('date_order', '>=', date_str + ' 00:00:00'), ('date_order', '<=', date_str + ' 23:59:59')]
    fields = ['id', 'name', 'partner_id', 'date_order', 'amount_total']
    orders = fetch_odoo_data(model, domain, fields, token)

    return orders


#Pedidos de mayor costo en un periodo
def get_top_orders_by_amount(fecha_inicio, fecha_fin, limit):
    token = get_oauth_token()
    if token is None:
        return None

    model = 'sale.order'
    domain = [('date_order', '>=', fecha_inicio + ' 00:00:00'), ('date_order', '<=', fecha_fin + ' 23:59:59')]
    fields = ['id', 'name', 'partner_id', 'date_order', 'amount_total']
    order = 'amount_total desc'
    orders = fetch_odoo_data(model, domain, fields, token, limit=limit, order=order)

    return orders


#Historial de Compras del Cliente
def get_purchase_history_by_customer_name(customer_name):
    token = get_oauth_token()
    
    # Buscar el cliente por nombre
    domain = [('name', '=', customer_name)]
    fields = ['id']
    customer = fetch_odoo_data('res.partner', domain, fields, token)
    
    if not customer:
        return f"No se encontró ningún cliente con el nombre {customer_name}."

    customer_id = customer[0]['id']
    
    # Obtener el historial de compras del cliente
    domain = [('partner_id', '=', customer_id), ('state', 'in', ['sale', 'done'])]
    fields = ['name', 'date_order', 'amount_total']
    orders = fetch_odoo_data('sale.order', domain, fields, token)

    return orders


#Total de Ventas Generadas por un cliente
def get_total_sales_by_customer(customer_name, start_date, end_date):
    token = get_oauth_token()
    
    # Buscar el cliente por nombre
    domain = [('name', '=', customer_name)]
    fields = ['id']
    customer = fetch_odoo_data('res.partner', domain, fields, token)
    
    if not customer:
        return f"No se encontró ningún cliente con el nombre {customer_name}."

    customer_id = customer[0]['id']
    
    domain = [('partner_id', '=', customer_id), ('date_order', '>=', start_date), ('date_order', '<=', end_date), ('state', 'in', ['sale', 'done'])]
    fields = ['amount_total']
    orders = fetch_odoo_data('sale.order', domain, fields, token)
    
    total_sales = sum(order['amount_total'] for order in orders)

    return [total_sales, len(orders)]


#Clientes con facturas pendientes de pago
def get_customers_with_pending_invoices():
    token = get_oauth_token()
    domain = [('payment_state', '=', 'not_paid')]
    fields = ['partner_id', 'amount_total', 'invoice_date']
    invoices = fetch_odoo_data('account.move', domain, fields, token)
    
    pending_invoices = set()
    
    for invoice in invoices:
        #partner_id = invoice['partner_id'][0]
        partner_name = invoice['partner_id'][1]
        pending_invoices.add(partner_name)
        
    return len(pending_invoices)


#facturas pendientes a pagar
def get_pending_invoices_to_pay():
    token = get_oauth_token()
    domain = [('payment_state', '=', 'not_paid')]
    fields = ['partner_id', 'amount_total', 'invoice_date']
    invoices = fetch_odoo_data("account.move", domain, fields, token)

    return len(invoices)


#producto más vendido
def get_top_selling_product(start_date, end_date):
    token = get_oauth_token()
    print(start_date)
    print(end_date)
    
    domain = [['order_id.date_order', '>=', start_date],
              ['order_id.date_order', '<=', end_date],
              ['order_id.state', 'in', ['sale', 'done']]
             ]
    
    fields = ['product_id', 'product_uom_qty']
    
    sale_order_lines = fetch_odoo_data('sale.order.line', domain, fields, token)
    
    sales_by_product = {}
    for line in sale_order_lines:
        product_id = line['product_id'][0]
        product_qty = line['product_uom_qty']
        if product_id in sales_by_product:
            sales_by_product[product_id] += product_qty
        else:
            sales_by_product[product_id] = product_qty
    
    top_product_id = max(sales_by_product, key=sales_by_product.get)
    top_product_name = fetch_odoo_data('product.product', [['id', '=', top_product_id]], ['name'], token)[0]['name']
    
    return {'product_id': top_product_id, 'product_name': top_product_name, 'quantity_sold': sales_by_product[top_product_id]}


#Pedidos pendientes de envio
def get_pending_shipments():
    try:
        token = get_oauth_token()
        domain = [('state', '=', "sent")]
        fields = ['name', 'date_order', 'partner_id']
        result = fetch_odoo_data('sale.order', domain, fields, token)
        
        if not isinstance(result, list):
            raise ValueError("Unexpected result format")
        
        pending_shipments = []
        for order in result:
            pending_shipments.append({
                'name': order['name'],
                'date_order': order['date_order'],
                'customer': order['partner_id'][1] if order['partner_id'] else 'Unknown'
            })
        
        return pending_shipments
    
    except Exception as e:
        return {'error': str(e)}
    

#número de pedidos cancelados este mes
def get_canceled_orders_this_month():
    token = get_oauth_token()
    
    now = datetime.now()
    first_day_of_month = now.replace(day=1)
    domain = [['state', '=', 'cancel'], ['date_order', '>=', first_day_of_month.strftime('%Y-%m-%d %H:%M:%S')]]
    fields = ['name']
    result = fetch_odoo_data('sale.order', domain, fields, token)
    
    return len(result)


#stock del producto
def get_product_stock_level(product_name):
    token = get_oauth_token()
    domain = [('name', '=', product_name)]
    fields = ['qty_available']
    result = fetch_odoo_data('product.product', domain, fields, token)
    
    if result and result[0]:
        return f"El nivel actual de stock del producto '{product_name}' es {result[0]['qty_available']} unidades."
    else:
        return f"No se encontró el producto '{product_name}'."


#productos con menos de 10 unidades en stock
def get_products_with_low_stock():
    token = get_oauth_token()
    domain = [('qty_available', '<', 10)]
    fields = ['name', 'qty_available']
    result = fetch_odoo_data('product.product', domain, fields, token)
    
    if result:
        low_stock_products = [f"{product['name']}: {product['qty_available']} unidades" for product in result]
        return f"Hay {len(low_stock_products)} productos con menos de 10 unidades en stock."
    else:
        return "No hay productos con menos de 10 unidades en stock."
    



#facturas pagadas en los últimos 7 días
def get_paid_invoices_last_7_days():
    token = get_oauth_token()

    # Calcular las fechas para los últimos 7 días
    today = datetime.today()
    start_date = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    end_date = today.strftime("%Y-%m-%d")

    # Definir la URL de la API y los parámetros
    endpoint = "account.move"
    domain = [
        ('move_type', '=', 'out_invoice'),
        ('payment_state', '=', 'paid'),
        ('invoice_date', '>=', start_date),
        ('invoice_date', '<=', end_date)
    ]
    fields = ['id', 'name', 'amount_total', 'date']
    # Fetch data from Odoo
    result = fetch_odoo_data(endpoint, domain, fields, token)

    return result


#Ventas por productos del último trimestre
def get_sales_by_product(start_date, end_date):
    token = get_oauth_token()
    endpoint = "sale.order.line"

    domain = [
        ('order_id.state', '=', 'sale'),
        ('order_id.date_order', '>=', start_date),
        ('order_id.date_order', '<=', end_date)
    ]

    fields = ['product_id', 'product_uom_qty', 'price_total']

    result = fetch_odoo_data(endpoint, domain, fields, token)
    
    # Agregar el código para agrupar y sumar ventas por producto aquí
    from collections import defaultdict
    sales_by_product = defaultdict(float)
    
    for line in result:
        product_name = line['product_id'][1]
        total_sales = line['price_total']
        sales_by_product[product_name] += total_sales
    
    return sales_by_product


#ventas por cliente
def get_sales_summary_by_customer(start_date, end_date):
    token = get_oauth_token()
    endpoint = "sale.order"

    domain = [
        ('state', '=', 'sale'),
        ('date_order', '>=', start_date),
        ('date_order', '<=', end_date)
    ]

    fields = ['partner_id', 'amount_total']

    result = fetch_odoo_data(endpoint, domain, fields, token)
    
    # Agregar el código para agrupar y sumar ventas por cliente aquí
    from collections import defaultdict
    sales_by_customer = defaultdict(float)
    
    for order in result:
        customer_name = order['partner_id'][1]
        total_sales = order['amount_total']
        sales_by_customer[customer_name] += total_sales
    
    return sales_by_customer


#productos con mayor margen beneficio
def get_products_highest_margin():
    token = get_oauth_token()
    
    domain = []
    fields = ['name', 'standard_price', 'list_price']
    
    products = fetch_odoo_data('product.product', domain, fields, token)
    
    margins = [{'name': product['name'], 'margin': product['list_price'] - product['standard_price']}
               for product in products]
    
    sorted_margins = sorted(margins, key=lambda x: x['margin'], reverse=True)
    
    return sorted_margins[:10]  # Top 10 products with highest margin


#devoluciones realizadas en un rango de fechas
def get_returns_processed(start_date, end_date):
    print(start_date)
    print(end_date)
    token = get_oauth_token()
    domain = [['state', 'in', ['done']], ['date', '>=', start_date], ['date', '<=', end_date]]
    fields = ['name']
    
    returns = fetch_odoo_data('stock.return.picking', domain, fields, token)
    
    return len(returns)


#clientes potenciales mas recientes
def get_recent_leads():
    token = get_oauth_token()
    
    domain = []
    fields = ['name', 'contact_name', 'email_from', 'create_date']
    order = 'create_date desc'
    
    leads = fetch_odoo_data('crm.lead', domain, fields, token, order=order, limit=10)
    
    return leads
