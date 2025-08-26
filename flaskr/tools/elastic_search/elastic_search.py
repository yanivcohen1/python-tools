from datetime import datetime, date
from math import ceil
from elasticsearch import Elasticsearch, ElasticsearchException
from elasticsearch_dsl import Search, Q

# Initialize Elasticsearch client
es = Elasticsearch( host='localhost', port=9200)
try:
    info = es.info()
    print("Elasticsearch Cluster Info:")
    # print(info)
except ElasticsearchException as e:
    print("Failed to connect to Elasticsearch.")
    print(f"Error: {e}")

# Check if the index exists
index_name="analitics"
if not es.indices.exists(index=index_name):
    print(f"Index '{index_name}' does not exist.")

def find_query(string_query, page_request, from_date, to_date, group_name, index_name="analitics"):

    # Build the date range filter
    date_range_filter = Q('range', **{
        '@timestamp': {
            'gte': from_date.isoformat(),
            'lte': to_date.isoformat()
        }
    })

    # Build the string query
    combined_query = Q('query_string', query=f'groupName:{group_name} AND {string_query}')

    # Combine filter and query
    s = Search(using=es, index=index_name).query(combined_query).filter(date_range_filter).sort({ 'buildName': { 'order': 'asc' } })

    # Apply pagination
    page_number = page_request["page"]
    page_size = page_request["size"]
    s = s[page_number * page_size : (page_number + 1) * page_size]

    # For debugging: print the generated query
    # query_body = s.to_dict()
    # print("Elasticsearch POST JSON body:")
    # print(json.dumps(query_body, indent=2))

    # Add pretty=true to the URL
    # s = s.params(pretty=True)

    # manually build & print the URL
    # host = es.transport.hosts[0].get('host', 'localhost')
    # port = es.transport.hosts[0].get('port', 9200)
    # path = f"/{index_name}/_search"
    # print("Full Elasticsearch request URL:")
    # print(f"http://{host}:{port}{path}?pretty=true")

    # Execute the search
    response = s.execute()

    # Calculate total pages
    total_hits = response.hits.total
    total_pages = ceil(float(total_hits) / page_size)
    print(f"Find total Pages: {total_pages}")

    # Return the results
    return response


if __name__ == '__main__':
    # Example usage
    from_date = date(2025, 1, 1)
    to_date = date(2025, 1, 31)
    page_request = {'page': 0, 'size': 10}
    group_name = 'group1_agrs2f5sa2'
    string_query = "productName:(*) AND stepUpdateStatus:('failed')" # test the query in Kibana before using it here
    results = find_query(string_query, page_request, from_date, to_date, group_name, index_name=index_name)
    build_name = ""
    for hit in results:
        if build_name != hit.buildName:
            build_name = hit.buildName
            print(f"\nBuild Name: {build_name}")
        # print(hit)  # Do something with the hit
        print(hit.stepName)  # Do something with the hit


# --- NEW: create index 'yaniv' with @timestamp in the mapping and insert two docs ---
    # --- NEW: create index 'yaniv' with a custom type and insert two docs ---
    index_to_create = 'yaniv'
    # Use a type name that doesn't begin with underscore for older clusters
    doc_type = 'doc'
    # Define only the properties mapping
    mapping_props = {
        "properties": {
            "buildName":   {"type": "string", "index": "not_analyzed"},
            "groupName":   {"type": "string", "index": "not_analyzed"},
            "@timestamp":  {"type": "date"}
        }
    }
    if not es.indices.exists(index=index_to_create):
        # Create the index with type-based mapping
        es.indices.create(
            index=index_to_create,
            body={"mappings": {doc_type: mapping_props}}
        )
        print(f"Index '{index_to_create}' created with mapping for type '{doc_type}'.")

    # Insert two sample documents, each with a timestamp
    docs = [
        {
            "buildName":  "build1",
            "groupName":  "groupA",
            "@timestamp": datetime.utcnow().isoformat()
        },
        {
            "buildName":  "build2",
            "groupName":  "groupB",
            "@timestamp": datetime.utcnow().isoformat()
        }
    ]
    for i, doc in enumerate(docs, start=1):
        es.index(index=index_to_create, doc_type=doc_type, body=doc)
        print(f"Inserted document {i}: {doc}")

    es.indices.refresh(index=index_to_create)
    print(f"Index '{index_to_create}' refreshed. Documents are now searchable.")

    # --- Example: search 'yaniv' between two datetimes ---
    from_dt = datetime(2025, 1, 1, 0, 0, 0)
    to_dt   = datetime(2025, 12, 31, 23, 59, 59)
    page_req = {'page': 0, 'size': 10}
    # use wildcard string_query if you just want all docs
    results = find_query("*", page_req, from_dt, to_dt, group_name="*", index_name=index_to_create)
    for hit in results:
        print(hit.buildName, hit.groupName, hit["@timestamp"])
# --- END NEW ---
