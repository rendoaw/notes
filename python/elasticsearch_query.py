#!/usr/bin/env python

import json
import argparse
from elasticsearch import Elasticsearch,helpers


def jsonpretty(text):
    return json.dumps(text, indent=4, sort_keys=True)

def arguments_parser():
    parser = argparse.ArgumentParser(description="Options:")
    parser.add_argument('--host', help='hostname', default='127.0.0.1')
    parser.add_argument('--port', help='hostname', default='9200')
    parser.add_argument('--key', help='show this key for output', default='hostname' )
    parser.add_argument('--query', help='query string' )
    parser.add_argument('--index', help='query index', default='myindex' )
    args = parser.parse_args()
    return args


def es_query(host, port=9200, q_key="content", q_val="", index="myindex"):
    es = Elasticsearch([{'host': host, 'port': 9200}])
    res = es.search(index=index,
            body={ "query" :
                    { "query_string" : {
                            "query" : q_val
                        }
                    }
                 }
            )
    return res


if __name__ == "__main__":
    args = arguments_parser()
    res = es_query(host=args.host, port=args.port, q_val=args.query, index=args.index)
    output = []
    for doc in res['hits']['hits']:
        entry = {}
        keys = args.key.split(',')
        for key in keys:
            if key in doc['_source']:
                entry[key] = doc['_source'][key]
        output.append(entry)
    print jsonpretty(output)
