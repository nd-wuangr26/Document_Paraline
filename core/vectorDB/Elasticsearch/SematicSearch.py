from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os
load_dotenv()
from core.embedding.openai_embedding import OpenAIEmbedding

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL")
ELASTICSEARCH_API_KEY = os.getenv("ELASTICSEARCH_API_KEY")
# Initialize the Elasticsearch client

client = Elasticsearch(
    ELASTICSEARCH_URL,
  api_key=ELASTICSEARCH_API_KEY
)
# client.indices.create(
#   index="my-index",
#   mappings={
#         "properties": {
#             "text": {"type": "semantic_text"}
#         }
#     }
# )
retriever_object = {
    "rrf": {
        "retrievers": [
            {
                "standard": {
                    "query": {
                        "semantic": {
                            "field": "ai_questions_answered",
                            "query": "What is the Query API key information API in Elasticsearch?"
                        }
                    }
                }
            }
        ]
    }
}
# {
#   "ai_questions_answered": [
#     "What is the Query API key information API in Elasticsearch?",
#     "How can users retrieve all API keys using the Query API?",
#     "What methods are available to group API keys by owner and expiration?",
#     "How can invalidated API keys be managed in Elasticsearch?",
#     "What are the best practices for using the Query API key information API?"
#   ],
#   "ai_subtitle": [
#     "Guide to Query API Key Management in Elasticsearch"
#   ],
#   "ai_summary": [
#     "The document titled 'Docs / Reference / Elasticsearch / Rest Apis / Query Api Keys' serves as a comprehensive guide for users interested in understanding the Query API key information API within Elasticsearch. It provides detailed usage examples for retrieving API key metadata in a paginated manner, including methods to filter, sort, and aggregate API key data using query DSL and aggregation features. The document outlines how to retrieve all API keys, group them by owner and expiration, and manage invalidated API keys. Additionally, it emphasizes the importance of managing API keys effectively to ensure secure access and efficient operations within Elasticsearch. This guide is essential for users looking to optimize their API key management strategies and enhance their overall Elasticsearch experience."
#   ],
#   "ai_tags": [
#     "Elasticsearch",
#     "API Keys",
#     "Query API",
#     "Management"
#   ],
#   "content_body": [
#     "# Query API key information examples\n\nThis page provides usage examples for the [Query API key information API](https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-security-query-api-keys), which retrieves API key metadata in a paginated fashion. These examples demonstrate how to retrieve, filter, sort, and aggregate API key data using query DSL and aggregation features.\nYou can learn how to:\n- [Retrieve all API keys](#retrieve-all-api-keys)\n- [Group API keys by owner and expiration](#group-api-keys-by-owner-and-expiration)\n- [Group invalidated API keys by owner and name](#group-invalidated-api-keys-by-owner-and-name)\n\n## Retrieve all API keys\n\nThe following request lists all API keys, assuming you have the `manage_api_key` privilege:\n```json\n```\n\nA successful call returns a JSON structure that contains the information retrieved from one or more API keys:\n```js\n{\n  \"total\": 3,\n  \"count\": 3,\n  \"api_keys\": [ \n    {\n      \"id\": \"nkvrGXsB8w290t56q3Rg\",\n      \"name\": \"my-api-key-1\",\n      \"creation\": 1628227480421,\n      \"expiration\": 1629091480421,\n      \"invalidated\": false,\n      \"username\": \"elastic\",\n      \"realm\": \"reserved\",\n      \"realm_type\": \"reserved\",\n      \"metadata\": {\n        \"letter\": \"a\"\n      },\n      \"role_descriptors\": { \n        \"role-a\": {\n          \"cluster\": [\n            \"monitor\"\n          ],\n          \"indices\": [\n            {\n              \"names\": [\n                \"index-a\"\n              ],\n              \"privileges\": [\n                \"read\"\n              ],\n              \"allow_restricted_indices\": false\n            }\n          ],\n          \"applications\": [ ],\n          \"run_as\": [ ],\n          \"metadata\": { },\n          \"transient_metadata\": {\n            \"enabled\": true\n          }\n        }\n      }\n    },\n    {\n      \"id\": \"oEvrGXsB8w290t5683TI\",\n      \"name\": \"my-api-key-2\",\n      \"creation\": 1628227498953,\n      \"expiration\": 1628313898953,\n      \"invalidated\": false,\n      \"username\": \"elastic\",\n      \"realm\": \"reserved\",\n      \"metadata\": {\n        \"letter\": \"b\"\n      },\n      \"role_descriptors\": { } \n    }\n  ]\n}\n```\n\nIf you create an API key with the following details:\n```json\n\n{\n  \"name\": \"application-key-1\",\n  \"metadata\": { \"application\": \"my-application\"}\n}\n```\n\nA successful call returns a JSON structure that provides API key information. For example:\n```json\n  \"id\": \"VuaCfGcBCdbkQm-e5aOx\",\n  \"name\": \"application-key-1\",\n  \"api_key\": \"ui2lp2axTNmsyakw9tvNnw\",\n  \"encoded\": \"VnVhQ2ZHY0JDZGJrUW0tZTVhT3g6dWkybHAyYXhUTm1zeWFrdzl0dk5udw==\"\n```\n\nUse the information from the response to retrieve the API key by ID:\n```json\n\n{\n  \"query\": {\n    \"ids\": {\n      \"values\": [\n        \"VuaCfGcBCdbkQm-e5aOx\"\n      ]\n    }\n  }\n}\n```\n\nA successful call returns a JSON structure for API key information including its limited-by role descriptors:\n```js\n{\n  \"api_keys\": [\n    {\n      \"id\": \"VuaCfGcBCdbkQm-e5aOx\",\n      \"name\": \"application-key-1\",\n      \"creation\": 1548550550158,\n      \"expiration\": 1548551550158,\n      \"invalidated\": false,\n      \"username\": \"myuser\",\n      \"realm\": \"native1\",\n      \"realm_type\": \"native\",\n      \"metadata\": {\n        \"application\": \"my-application\"\n      },\n      \"role_descriptors\": { },\n      \"limited_by\": [ \n        {\n          \"role-power-user\": {\n            \"cluster\": [\n              \"monitor\"\n            ],\n            \"indices\": [\n              {\n                \"names\": [\n                  \"*\"\n                ],\n                \"privileges\": [\n                  \"read\"\n                ],\n                \"allow_restricted_indices\": false\n              }\n            ],\n            \"applications\": [ ],\n            \"run_as\": [ ],\n            \"metadata\": { },\n            \"transient_metadata\": {\n              \"enabled\": true\n            }\n          }\n        }\n      ]\n    }\n  ]\n}\n```\n\nYou can also retrieve the API key by name:\n```json\n\n{\n  \"query\": {\n    \"term\": {\n      \"name\": {\n        \"value\": \"application-key-1\"\n      }\n    }\n  }\n}\n```\n\nUse a `bool` query to issue complex logical conditions and use `from`, `size`, `sort` to help paginate the result:\n```js\nGET /_security/_query/api_key\n{\n  \"query\": {\n    \"bool\": {\n      \"must\": [\n        {\n          \"prefix\": {\n            \"name\": \"app1-key-\" \n          }\n        },\n        {\n          \"term\": {\n            \"invalidated\": \"false\" \n          }\n        }\n      ],\n      \"must_not\": [\n        {\n          \"term\": {\n            \"name\": \"app1-key-01\" \n          }\n        }\n      ],\n      \"filter\": [\n        {\n          \"wildcard\": {\n            \"username\": \"org-*-user\" \n          }\n        },\n        {\n          \"term\": {\n            \"metadata.environment\": \"production\" \n          }\n        }\n      ]\n    }\n  },\n  \"from\": 20, \n  \"size\": 10, \n  \"sort\": [ \n    { \"creation\": { \"order\": \"desc\", \"format\": \"date_time\" } },\n    \"name\"\n  ]\n}\n```\n\nThe response contains a list of matched API keys along with their sort values:\n```js\n{\n  \"total\": 100,\n  \"count\": 10,\n  \"api_keys\": [\n    {\n      \"id\": \"CLXgVnsBOGkf8IyjcXU7\",\n      \"name\": \"app1-key-79\",\n      \"creation\": 1629250154811,\n      \"invalidated\": false,\n      \"username\": \"org-admin-user\",\n      \"realm\": \"native1\",\n      \"metadata\": {\n        \"environment\": \"production\"\n      },\n      \"role_descriptors\": { },\n      \"_sort\": [\n        \"2021-08-18T01:29:14.811Z\",  \n        \"app1-key-79\"  \n      ]\n    },\n    {\n      \"id\": \"BrXgVnsBOGkf8IyjbXVB\",\n      \"name\": \"app1-key-78\",\n      \"creation\": 1629250153794,\n      \"invalidated\": false,\n      \"username\": \"org-admin-user\",\n      \"realm\": \"native1\",\n      \"metadata\": {\n        \"environment\": \"production\"\n      },\n      \"role_descriptors\": { },\n      \"_sort\": [\n        \"2021-08-18T01:29:13.794Z\",\n        \"app1-key-78\"\n      ]\n    },\n    ...\n  ]\n}\n```\n\n## Group API keys by owner and expiration\n\nFor example, given 2 users \"june\" and \"king\", each owning 3 API keys:\n- one that never expires (invalidated for user \"king\")\n- one that expires in 10 days\n- and one that expires in 100 day (invalidated for user \"june\")\n\nThe following request returns the names of valid (not expired and not invalidated) API keys that expire soon (in 30 days time), grouped by owner username.\n\n### Request\n\n```json\n\n{\n  \"size\": 0,\n  \"query\": {\n    \"bool\": {\n      \"must\": {\n        \"term\": {\n          \"invalidated\": false  \n        }\n      },\n      \"should\": [  \n        {\n          \"range\": { \"expiration\": { \"gte\": \"now\" } }\n        },\n        {\n          \"bool\": { \"must_not\": { \"exists\": { \"field\": \"expiration\" } } }\n        }\n      ],\n      \"minimum_should_match\": 1\n    }\n  },\n  \"aggs\": {\n    \"keys_by_username\": {\n      \"composite\": {\n        \"sources\": [ { \"usernames\": { \"terms\": { \"field\": \"username\" } } } ]  \n      },\n      \"aggs\": {\n        \"expires_soon\": {\n          \"filter\": {\n            \"range\": { \"expiration\": { \"lte\": \"now+30d/d\" } }  \n          },\n          \"aggs\": {\n            \"key_names\": { \"terms\": { \"field\": \"name\" } }\n          }\n        }\n      }\n    }\n  }\n}\n```\n\n### Response\n\n```json\n{\n  \"total\" : 4,  \n  \"count\" : 0,\n  \"api_keys\" : [ ],\n  \"aggregations\" : {\n    \"keys_by_username\" : {\n      \"after_key\" : {\n        \"usernames\" : \"king\"\n      },\n      \"buckets\" : [\n        {\n          \"key\" : {\n            \"usernames\" : \"june\"\n          },\n          \"doc_count\" : 2,  \n          \"expires_soon\" : {\n            \"doc_count\" : 1,\n            \"key_names\" : {\n              \"doc_count_error_upper_bound\" : 0,\n              \"sum_other_doc_count\" : 0,\n              \"buckets\" : [\n                {\n                  \"key\" : \"june-key-10\",\n                  \"doc_count\" : 1\n                }\n              ]\n            }\n          }\n        },\n        {\n          \"key\" : {\n            \"usernames\" : \"king\"\n          },\n          \"doc_count\" : 2,\n          \"expires_soon\" : {\n            \"doc_count\" : 1,  \n            \"key_names\" : {\n              \"doc_count_error_upper_bound\" : 0,\n              \"sum_other_doc_count\" : 0,\n              \"buckets\" : [  \n                {\n                  \"key\" : \"king-key-10\",\n                  \"doc_count\" : 1\n                }\n              ]\n            }\n          }\n        }\n      ]\n    }\n  }\n}\n```\n\n## Group invalidated API keys by owner and name\n\nTo retrieve the invalidated (but not yet deleted) API keys, grouped by owner username and API key name, issue the following request:\n\n### Request\n\n```json\n\n{\n  \"size\": 0,\n  \"query\": {\n    \"bool\": {\n      \"filter\": {\n        \"term\": {\n          \"invalidated\": true\n        }\n      }\n    }\n  },\n  \"aggs\": {\n    \"invalidated_keys\": {\n      \"composite\": {\n        \"sources\": [\n          { \"username\": { \"terms\": { \"field\": \"username\" } } },\n          { \"key_name\": { \"terms\": { \"field\": \"name\" } } }\n        ]\n      }\n    }\n  }\n}\n```\n\n### Response\n\n```json\n{\n  \"total\" : 2,\n  \"count\" : 0,\n  \"api_keys\" : [ ],\n  \"aggregations\" : {\n    \"invalidated_keys\" : {\n      \"after_key\" : {\n        \"username\" : \"king\",\n        \"key_name\" : \"king-key-no-expire\"\n      },\n      \"buckets\" : [\n        {\n          \"key\" : {\n            \"username\" : \"june\",\n            \"key_name\" : \"june-key-100\"\n          },\n          \"doc_count\" : 1\n        },\n        {\n          \"key\" : {\n            \"username\" : \"king\",\n            \"key_name\" : \"king-key-no-expire\"\n          },\n          \"doc_count\" : 1\n        }\n      ]\n    }\n  }\n}\n```"
#   ],
#   "content_title": [
#     "Docs / Reference / Elasticsearch / Rest Apis / Query Api Keys"
#   ],
#   "product_name": [
#     "elasticsearch"
#   ],
#   "root_type": [
#     "documentation"
#   ],
#   "slug": [
#     "docs-reference-elasticsearch-rest-apis-query-api-keys.md"
#   ],
#   "url": [
#     "https://www.elastic.co/docs/reference/elasticsearch/rest-apis/query-api-keys/"
#   ],
#   "_id": "5I69YJkBwq66Rn7JYcfQ",
#   "_index": "kibana_sample_data_elasticsearch_documentation",
#   "_score": 1
# }
search_response = client.search(
    index="kibana_sample_data_elasticsearch_documentation",
    retriever=retriever_object,
)
print(search_response)