# models.py
from elastic import get_es_client

def index_advertisement(ad_data):
    es_client = get_es_client()
    es_client.index(
        index='advertisements',
        id=ad_data['AdvertisementID'],
        document={
            'Title': ad_data['Title'],
            'Price': float(ad_data['Price']) if ad_data.get('Price') is not None else None,
            'CreationDate': ad_data['CreationDate'],
            'IsActive': ad_data['IsActive'],
        }
    )

def deactivate_advertisement(ad_id, active):
    es_client = get_es_client()
    es_client.update(
        index='advertisements',
        id=ad_id,
        doc={
            'IsActive': active,
        }
    )

def delete_advertisement(ad_id):
    es_client = get_es_client()
    es_client.delete(index='advertisements', id=ad_id)