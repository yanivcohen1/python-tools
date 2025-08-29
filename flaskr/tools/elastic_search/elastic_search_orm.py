# ES 2.4.6 compatibility: use direct client and DocType
from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, String  # pylint: disable=import-error,no-name-in-module
from elasticsearch_dsl.field import Integer  # pylint: disable=import-error,no-name-in-module
from elasticsearch_dsl.field import Date     # add timestamp field support
from datetime import datetime, timezone

# 1. Establish a connection to your Elasticsearch cluster
es = Elasticsearch(hosts=['localhost:9200'], port=9200)

# 2. Define your document mapping using DocType
class Product(DocType):
    # ES 2.x uses 'string' type via DSL String field
    name = String()
    price = Integer()
    # add timestamp field for filtering
    timestamp = Date(name='@timestamp')

    class Meta:
        index = 'products'
        doc_type = 'product'

# 3. Create the index in ES (if not already created)
if not es.indices.exists(index='products'):
    Product.init(using=es)

# 4. INSERT (save) an instance with timestamp
prod = Product(name='Pear', price=4, timestamp=datetime.now(timezone.utc))  # meta={'id': 1}
prod.save(using=es)                   # performs an upsert

# 5. update by instance
prod.price = 5
prod.save(using=es)                   # performs an upsert
prod.delete(using=es)                 # deletes doc with id=1 from 'products' index

# 6. Bulk insert multiple products using the Product class
product_objs = [
    Product(name='Apple',  price=3, timestamp=datetime.now(timezone.utc)),
    Product(name='Banana', price=2, timestamp=datetime.now(timezone.utc)),
    Product(name='Cherry', price=5, timestamp=datetime.now(timezone.utc)),
]
for prod in product_objs:
    prod.save(using=es)

# Refresh the index so newly saved docs are searchable
es.indices.refresh(index='products')

# 7. Delete products by name using DSL delete (with timestamp range filter)
delete_name = 'Banana'
# Define date range for filtering
from_date = datetime(2025, 1, 1)
to_date   = datetime(2025, 12, 31)
# Build search with timestamp range filter and name match
delete_search = Product.search(using=es) \
    .filter('range', timestamp={'gte': from_date, 'lte': to_date}) \
    .query('match', name=delete_name)
# Execute search to preview hits
hits: list[Product] = delete_search.execute()
print(f"Products to delete: {[(hit.name, hit.meta.id) for hit in hits]}")
# Perform deletion by query
hits[0].delete(using=es)
