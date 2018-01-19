
* create index template

```

PUT _template/template_subnet
{
  "index_patterns": ["subnet"],
  "mappings": {
    "general": {
      "properties": {
        "router": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "subnet": {
          "type": "ip"
        }
      }
    }
  }
}

```


* create index with pre-defined field type

```
PUT subnet
{
  "mappings": {
    "general": {
      "properties": {
        "router": {
          "type": "text",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        },
        "subnet": {
          "type": "ip",
          "fields": {
            "keyword": {
              "type": "keyword",
              "ignore_above": 256
            }
          }
        }
      }
    } 
  }
}
```


