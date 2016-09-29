# EAI REST handler examples: Simple handler

This EAI handler simply populates its confInfo object with two stanzas. The handler can be requested to produce Atom 
feed output:

```
$ curl -s -k -u admin:changeme https://localhost:8089/servicesNS/admin/rest_examples/simple_eai
<?xml version="1.0" encoding="UTF-8"?>
<!--This is to override browser formatting; see server.conf[httpServer] to disable. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .-->
<?xml-stylesheet type="text/xml" href="/static/atom.xsl"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:s="http://dev.splunk.com/ns/rest" xmlns:opensearch="http://a9.com/-/spec/opensearch/1.1/">
  <title></title>
  <id>https://localhost:8089/servicesNS/admin/rest_examples/simple_eai</id>
  <updated>2016-09-29T00:02:56-04:00</updated>
  <generator build="2f8cf215be08" version="6.5.0"/>
  <author>
    <name>Splunk</name>
  </author>
  <link href="/servicesNS/admin/rest_examples/simple_eai/_acl" rel="_acl"/>
  <opensearch:totalResults>1</opensearch:totalResults>
  <opensearch:itemsPerPage>30</opensearch:itemsPerPage>
  <opensearch:startIndex>0</opensearch:startIndex>
  <s:messages/>
  <entry>
    <title>stanza1</title>
    <id>https://localhost:8089/servicesNS/admin/rest_examples/simple_eai/stanza1</id>
    <updated>2016-09-29T00:02:56-04:00</updated>
    <link href="/servicesNS/admin/rest_examples/simple_eai/stanza1" rel="alternate"/>
    <author>
      <name>system</name>
    </author>
    <link href="/servicesNS/admin/rest_examples/simple_eai/stanza1" rel="list"/>
    <content type="text/xml">
      <s:dict>
        <s:key name="attr">abcd</s:key>
        <s:key name="eai:acl">
          <s:dict>
            <s:key name="app"></s:key>
            <s:key name="can_list">1</s:key>
            <s:key name="can_write">1</s:key>
            <s:key name="modifiable">0</s:key>
            <s:key name="owner">system</s:key>
            <s:key name="perms">
              <s:dict>
                <s:key name="read">
                  <s:list>
                    <s:item>*</s:item>
                  </s:list>
                </s:key>
                <s:key name="write">
                  <s:list>
                    <s:item>*</s:item>
                  </s:list>
                </s:key>
              </s:dict>
            </s:key>
            <s:key name="removable">0</s:key>
            <s:key name="sharing">system</s:key>
          </s:dict>
        </s:key>
      </s:dict>
    </content>
  </entry>
</feed>
```

or as JSON:

```
$ curl -s -k -u admin:changeme https://localhost:8089/services/simple_eai?output_mode=json | python -m json.tool
{
    "entry": [
        {
            "acl": {
                "app": "",
                "can_list": true,
                "can_write": true,
                "modifiable": false,
                "owner": "system",
                "perms": {
                    "read": [
                        "*"
                    ],
                    "write": [
                        "*"
                    ]
                },
                "removable": false,
                "sharing": "system"
            },
            "author": "system",
            "content": {
                "attr": "abcd",
                "eai:acl": null
            },
            "id": "https://localhost:8089/services/simple_eai/stanza1",
            "links": {
                "alternate": "/services/simple_eai/stanza1",
                "list": "/services/simple_eai/stanza1"
            },
            "name": "stanza1",
            "updated": "2016-09-29T00:03:48-04:00"
        }
    ],
    "generator": {
        "build": "2f8cf215be08",
        "version": "6.5.0"
    },
    "links": {
        "_acl": "/services/simple_eai/_acl"
    },
    "messages": [],
    "origin": "https://localhost:8089/services/simple_eai",
    "paging": {
        "offset": 0,
        "perPage": 30,
        "total": 1
    },
    "updated": "2016-09-29T00:03:48-04:00"
}
```