import requests
import json
import os

def fetch_odoo_data(model, domain, fields, token, group_by=None, limit=None, order=None):
    headers = {
        'Authorization': f'Bearer {token["access_token"]}',
        'Cookie': 'frontend_lang=en_GB; session_id=7df5b2976443f90f77e7d609ebf6db57b2949651'
    }

    params = {
        'model': model,
        'domain': json.dumps(domain),
        'fields': json.dumps(fields)
    }

    if group_by is not None:
        params['group_by'] = json.dumps(group_by)
    
    if limit is not None:
        params['limit'] = str(limit)
    
    if order is not None:
        params['order'] = order

    response = requests.get(
        f'{os.getenv("PUBLIC_ODOO_URL")}{os.getenv("PUBLIC_SEARCH_PATH")}',
        headers=headers,
        params=params
    )

    return response.json()


def fetch_odoo_data_dev(model, domain, fields, token, group_by=None, limit=None, order=None):
    headers = {
        'Authorization': f'Bearer {token["access_token"]}',
        'Cookie': 'frontend_lang=en_GB; session_id=7df5b2976443f90f77e7d609ebf6db57b2949651'
    }

    params = {
        'model': model,
        'domain': json.dumps(domain),
        'fields': json.dumps(fields)
    }

    if group_by is not None:
        params['group_by'] = json.dumps(group_by)
    
    if limit is not None:
        params['limit'] = str(limit)
    
    if order is not None:
        params['order'] = order

    response = requests.get(
        f'{os.getenv("PUBLIC_ODOO_URL_DEV")}{os.getenv("PUBLIC_SEARCH_PATH")}',
        headers=headers,
        params=params
    )

    return response.json()