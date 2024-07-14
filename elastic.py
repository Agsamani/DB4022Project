from elasticsearch import Elasticsearch
from Wol import settings

def get_es_client():
    es_config = settings.ELASTICSEARCH_DSL['default']
    return Elasticsearch(
        [es_config['hosts']],
        http_auth=es_config['http_auth']
    )

def create_index(index_name):
    es_client = get_es_client()

    # Define the mapping for your index
    mapping = {
        "mappings": {
            "properties": {
                "Title": {"type": "text"},
                "Price": {"type": "float"},
                "CreationDate": {"type": "date"},
                "IsActive": {"type": "boolean"}
            }
        }
    }

    if es_client.indices.exists(index=index_name):
        print(f'Index "{index_name}" already exists')
    else:
        es_client.indices.create(index=index_name, body=mapping)
        print(f'Successfully created index "{index_name}"')

if __name__ == '__main__':
    if get_es_client().indices.exists(index='advertisements'):
        get_es_client().indices.delete(index='advertisements')
    create_index('advertisements')


