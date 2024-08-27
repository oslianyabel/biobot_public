from functions import *

clients_tools = [
    {
        "type": "function",
        "function": {
            "name": "customer_history",
            "description": "Consulta el historial de compras de un cliente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Nombre del cliente.",
                    },
                },
                "required": ["customer_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "customer_amount_by_date",
            "description": "Consulta el monto de compras realizadas por un cliente en un intervalo de fechas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Nombre del cliente.",
                    },
                    "start_date": {
                        "type": "string",
                        "description": "Fecha inicial del intervalo en formato YYYY-MM-DD.",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Fecha final del intervalo en formato YYYY-MM-DD.",
                    },
                },
                "required": ["customer_name", "start_date", "end_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "customer_with_pending_orders_to_pay",
            "description": "Consulta los clientes con pedidos pendientes de pago.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "top_customer",
            "description": "Obtiene el cliente con más facturas desde una fecha específica hasta el día de hoy.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fecha": {
                        "type": "string",
                        "description": "Fecha de inicio para las facturas en formato YYYY-MM-DD.",
                    },
                },
                "required": ["fecha"],
            },
        },
    },
]

orders_tools = [
    {
        "type": "function",
        "function": {
            "name": "canceled_orders_this_month",
            "description": "Consulta las ordenes canceladas este mes.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "pending_orders",
            "description": "Consulta los pedidos pendientes de envio.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "orders_by_date",
            "description": "Consulta los pedidos realizados en un día específico",
            "parameters": {
                "type": "object",
                "properties": {
                    "fecha": {
                        "type": "string",
                        "description": "Fecha de los pedidos a consultar en formato YYYY-MM-DD.",
                    },
                },
                "required": ["fecha"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "orders_by_amount",
            "description": "Consulta los 10 pedidos de mayor monto en un intervalo de tiempo dado, desde una fecha inicial hasta una fecha final. En caso de no proporcionar fecha inicial, no enviar el parámetro. En caso de no proporcionar fecha final, no enviar el parámetro.",
            "parameters": {
                "type": "object",
                "properties": {
                    "fecha_inicio": {
                        "type": "string",
                        "description": "Fecha inicial de los pedidos a consultar en formato YYYY-MM-DD.",
                    },
                    "fecha_fin": {
                        "type": "string",
                        "description": "Fecha final de los pedidos a consultar en formato YYYY-MM-DD.",
                    },
                },
            },
        },
    },
]

inventory_tools = [
    {
        "type": "function",
        "function": {
            "name": "products_low_stock",
            "description": "Consulta los productos con stock bajo.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "product_stock",
            "description": "Consulta el stock de un producto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Nombre del producto",
                    },
                },
                "required": ["product_name"],
            },
        },
    },
]

invoices_tools = [
    {
        "type": "function",
        "function": {
            "name": "sales_report",
            "description": "Obtener un reporte de ventas en un intervalo de tiempo dado, desde una fecha inicial hasta una fecha final. En caso de que la fecha final sea la actualidad solo pasar como parámetro la fecha inicial",
            "parameters": {
                "type": "object",
                "properties": {
                    "fecha_inicio": {
                        "type": "string",
                        "description": "Fecha de inicio para el reporte en formato YYYY-MM-DD.",
                    },
                    "fecha_fin": {
                        "type": "string",
                        "description": "Fecha final para el reporte en formato YYYY-MM-DD.",
                    },
                },
                "required": ["fecha_inicio"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "paid_invoices_last_7_days",
            "description": "Obtiene las facturas pagadas en los últimos 7 días.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "pending_invoices_to_pay",
            "description": "Obtiene las facturas pendientes por pagar.",
        },
    },
]

statistics_tools = [
    {
        "type": "function",
        "function": {
            "name": "sales_by_product",
            "description": "Consulta las ventas por producto en un rango de fechas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Fecha inicial del rango a consultar",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Fecha final del rango a consultar",
                    },
                },
                "required": ["start_date", "end_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sales_summary_by_customer",
            "description": "Consulta las ventas de cada cliente en un rango de fechas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Fecha inicial del rango a consultar",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Fecha final del rango a consultar",
                    },
                },
                "required": ["start_date", "end_date"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "products_highest_margin",
            "description": "Consulta los productos con mayor margen de beneficio.",
        },
    },
]

products_tools = [
    {
        "type": "function",
        "function": {
            "name": "product_list",
            "description": "Lista cierta cantidad de productos disponibles, ordenados alfabeticamente.",
            "parameters": {
                "type": "object",
                "properties": {
                    "quantity": {
                        "type": "string",
                        "description": "Número de productos a listar.",
                    },
                },
                "required": ["quantity"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "product_list_price",
            "description": "Lista cierta cantidad de productos disponibles, ordenados de mayor precio a menor precio.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "product_detail",
            "description": "Busca un producto por su nombre y muestra su información",
            "parameters": {
                "type": "object",
                "properties": {
                    "product_name": {
                        "type": "string",
                        "description": "Nombre del producto a buscar",
                    },
                },
                "required": ["product_name"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "top_product",
            "description": "Consulta el producto más vendido en un rango de fechas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Fecha inicial del rango a consultar",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Fecha final del rango a consultar",
                    },
                },
                "required": ["start_date", "end_date"],
            },
        },
    },
]

returns_tools = [
    {
        "type": "function",
        "function": {
            "name": "returns_processed",
            "description": "Consulta las devoluciones procesadas en un rango de fechas.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_date": {
                        "type": "string",
                        "description": "Fecha inicial del rango a consultar",
                    },
                    "end_date": {
                        "type": "string",
                        "description": "Fecha final del rango a consultar",
                    },
                },
                "required": ["start_date", "end_date"],
            },
        },
    },
]

potential_customers = [
    {
        "type": "function",
        "function": {
            "name": "recent_leads",
            "description": "Consulta los clientes potenciales más recientes.",
        },
    },
]

user_tools = [
    *products_tools,
    { 
        "type": "function",
        "function": {
            "name": "devoluciones",
            "description": "Realiza la devolución de un pedido.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pedido": {
                        "type": "string",
                        "description": "Nombre del pedido a devolver.",
                    },
                    "motivo": {
                        "type": "string",
                        "description": "Motivo de la devolución",
                        "enum": ["fallo", "no lo quiero"],
                    },
                },
                "required": ["pedido", "motivo"],
            },
        },
    },
    { 
        "type": "function",
        "function": {
            "name": "repuestos",
            "description": "Solicita repuesto para un producto.",
            "parameters": {
                "type": "object",
                "properties": {
                    "tipo_producto": {
                        "type": "string",
                        "description": "Tipo de producto del que se necesita repuesto",
                    },
                    "modelo": {
                        "type": "string",
                        "description": "modelo del producto que se necesita repuesto",
                    },
                },
                "required": ["modelo", "tipo_producto"],
            },
        },
    },
    { 
        "type": "function",
        "function": {
            "name": "compatibilidades",
            "description": "Consulta las compatibilidades de un producto",
            "parameters": {
                "type": "object",
                "properties": {
                    "tipo_producto": {
                        "type": "string",
                        "description": "Tipo de producto del que se necesita saber sus compatibilidades",
                    },
                    "producto": {
                        "type": "string",
                        "description": "Nombre del producto sobre el que se necesita saber sus compatibilidades",
                    },
                },
                "required": ["producto", "tipo_producto"],
            },
        },
    },
    { 
        "type": "function",
        "function": {
            "name": "software",
            "description": "Consulta los software de un producto",
            "parameters": {
                "type": "object",
                "properties": {
                    "tipo_producto": {
                        "type": "string",
                        "description": "Tipo de producto del que se necesita saber su software",
                    },
                    "producto": {
                        "type": "string",
                        "description": "Nombre del producto sobre el que se necesita saber su software",
                    },
                },
                "required": ["producto", "tipo_producto"],
            },
        },
    },
    { 
        "type": "function",
        "function": {
            "name": "sales_order",
            "description": "Consulta el estado, importe y fecha de un pedido.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pedido": {
                        "type": "string",
                        "description": "Nombre del pedido",
                    },
                },
                "required": ["pedido"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "clear_chat",
            "description": "Elimina el historial de la conversación y comienza una nueva.",
        },
    },
    {
        "type": "function",
        "function": {
            "name": "available_actions",
            "description": "Lista las acciones que puedes realizar.",
        },
    },
]

admin_tools = [
    *user_tools,
    *clients_tools,
    *orders_tools,
    *inventory_tools,
    *invoices_tools,
    *statistics_tools,
    *returns_tools,
    *potential_customers,
]

user_available_functions = {
    "sales_order": sales_order,
    "devoluciones": devoluciones,
    "repuestos": repuestos,
    "compatibilidades": compatibilidades,
    "software": software,
    #productos
    "product_list": product_list,
    "product_list_price": product_list_price,
    "product_detail": product_detail,
    "top_product": top_product,
    #extras
    "clear_chat": clear_chat,
}

admin_available_functions = {
    **user_available_functions,
    #clientes
    "customer_history" : customer_history,
    "customer_amount_by_date" : customer_amount_by_date,
    "customer_with_pending_orders_to_pay": customer_with_pending_orders_to_pay,
    "top_customer": top_customer,
    #pedidos
    "pending_orders": pending_orders,
    "canceled_orders_this_month": canceled_orders_this_month,
    "orders_by_amount": orders_by_amount,
    "orders_by_date": orders_by_date,
    #inventario
    "products_low_stock": products_low_stock,
    "product_stock": product_stock,
    #facturas
    "sales_report": sales_report,
    "paid_invoices_last_7_days": paid_invoices_last_7_days,
    "pending_invoices_to_pay": pending_invoices_to_pay,
    #statistics
    "sales_by_product": sales_by_product,
    "sales_summary_by_customer": sales_summary_by_customer,
    "products_highest_margin": products_highest_margin,
    #devoluciones
    "returns_processed": returns_processed,
    #clientes potenciales
    "recent_leads": recent_leads,
    #extras
    "available_actions": admin_actions,
}

user_available_functions["available_actions"] = user_actions
