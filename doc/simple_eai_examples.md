# EAI REST handler examples: Simple handler

This EAI handler simply populates its confInfo object with two stanzas. The handler can be requested to produce Atom 
feed output:

```
$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/simple_eai
<?xml version="1.0" encoding="UTF-8"?>
<!--This is to override browser formatting; see server.conf[httpServer] to disable. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .-->
<?xml-stylesheet type="text/xml" href="/static/atom.xsl"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:s="http://dev.splunk.com/ns/rest">
  <title></title>
  <id>https://localhost:8089/servicesNS/admin/splunk-rest-examples/simple_eai</id>
  <updated>2016-09-29T10:10:12-04:00</updated>
  <generator build="2f8cf215be08" version="6.5.0"/>
  <author>
    <name>Splunk</name>
  </author>
  <s:messages/>
  <entry>
    <title>nonpersistent</title>
    <id>https://localhost:8089/servicesNS/admin/splunk-rest-examples/simple_eai/nonpersistent</id>
    <updated>2016-09-29T10:10:12-04:00</updated>
    <link href="/servicesNS/admin/splunk-rest-examples/simple_eai/nonpersistent" rel="alternate"/>
    <author>
      <name>system</name>
    </author>
    <link href="/servicesNS/admin/splunk-rest-examples/simple_eai/nonpersistent" rel="list"/>
    <link href="/servicesNS/admin/splunk-rest-examples/simple_eai/nonpersistent/_acl" rel="_acl"/>
    <content type="text/xml">
      <s:dict/>
    </content>
  </entry>
  <entry>
    <title>persistent</title>
    <id>https://localhost:8089/servicesNS/admin/splunk-rest-examples/simple_eai/persistent</id>
    <updated>2016-09-29T10:10:12-04:00</updated>
    <link href="/servicesNS/admin/splunk-rest-examples/simple_eai/persistent" rel="alternate"/>
    <author>
      <name>system</name>
    </author>
    <link href="/servicesNS/admin/splunk-rest-examples/simple_eai/persistent" rel="list"/>
    <link href="/servicesNS/admin/splunk-rest-examples/simple_eai/persistent/_acl" rel="_acl"/>
    <content type="text/xml">
      <s:dict/>
    </content>
  </entry>
</feed>
```

or as JSON:

```
$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/simple_eai?output_mode=json | python -m json.tool
{
    "entry": [
        {
            "acl": {
                "app": "",
                "can_list": true,
                "can_write": true,
                "modifiable": false,
                "owner": "system",
                "perms": null,
                "removable": false,
                "sharing": "system"
            },
            "author": "system",
            "content": {
                "eai:acl": null
            },
            "id": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/simple_eai/nonpersistent",
            "links": {
                "_acl": "/servicesNS/admin/splunk-rest-examples/simple_eai/nonpersistent/_acl",
                "alternate": "/servicesNS/admin/splunk-rest-examples/simple_eai/nonpersistent",
                "list": "/servicesNS/admin/splunk-rest-examples/simple_eai/nonpersistent"
            },
            "name": "nonpersistent",
            "updated": "2016-09-29T10:11:18-04:00"
        },
        {
            "acl": {
                "app": "",
                "can_list": true,
                "can_write": true,
                "modifiable": false,
                "owner": "system",
                "perms": null,
                "removable": false,
                "sharing": "system"
            },
            "author": "system",
            "content": {
                "eai:acl": null
            },
            "id": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/simple_eai/persistent",
            "links": {
                "_acl": "/servicesNS/admin/splunk-rest-examples/simple_eai/persistent/_acl",
                "alternate": "/servicesNS/admin/splunk-rest-examples/simple_eai/persistent",
                "list": "/servicesNS/admin/splunk-rest-examples/simple_eai/persistent"
            },
            "name": "persistent",
            "updated": "2016-09-29T10:11:18-04:00"
        }
    ],
    "generator": {
        "build": "2f8cf215be08",
        "version": "6.5.0"
    },
    "links": {},
    "messages": [],
    "origin": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/simple_eai",
    "updated": "2016-09-29T10:11:18-04:00"
}
```
