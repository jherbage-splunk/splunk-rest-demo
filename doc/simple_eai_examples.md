# EAI REST handler examples: Simple handler

We have mapped two EAI handlers under a common root, `/examples`.
Requesting this root will populate two entries in the output showing
both handlers. By default, XML output is returned:

```
$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples
<?xml version="1.0" encoding="UTF-8"?>
<!--This is to override browser formatting; see server.conf[httpServer] to disable. . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .-->
<?xml-stylesheet type="text/xml" href="/static/atom.xsl"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:s="http://dev.splunk.com/ns/rest">
  <title></title>
  <id>https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples</id>
  <updated>2018-05-18T13:54:26-04:00</updated>
  <generator build="95d592afb9fd4598f6949922834483a7c9191e58" version="20180516"/>
  <author>
    <name>Splunk</name>
  </author>
  <s:messages/>
  <entry>
    <title>simple_eai_nonpersistent</title>
    <id>https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent</id>
    <updated>1969-12-31T19:00:00-05:00</updated>
    <link href="/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent" rel="alternate"/>
    <author>
      <name>system</name>
    </author>
    <link href="/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent" rel="list"/>
    <link href="/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent/_acl" rel="_acl"/>
    <content type="text/xml">
      <s:dict/>
    </content>
  </entry>
  <entry>
    <title>simple_eai_persistent</title>
    <id>https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent</id>
    <updated>1969-12-31T19:00:00-05:00</updated>
    <link href="/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent" rel="alternate"/>
    <author>
      <name>system</name>
    </author>
    <link href="/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent" rel="list"/>
    <link href="/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent/_acl" rel="_acl"/>
    <content type="text/xml">
      <s:dict/>
    </content>
  </entry>
</feed>
```

JSON output can be requested via the addition of the `output_mode=json`
parameter:

```
$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples?output_mode=json | python -m json.tool
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
            "id": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent",
            "links": {
                "_acl": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent/_acl",
                "alternate": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent",
                "list": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent"
            },
            "name": "simple_eai_nonpersistent",
            "updated": "1969-12-31T19:00:00-05:00"
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
            "id": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent",
            "links": {
                "_acl": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent/_acl",
                "alternate": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent",
                "list": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent"
            },
            "name": "simple_eai_persistent",
            "updated": "1969-12-31T19:00:00-05:00"
        }
    ],
    "generator": {
        "build": "95d592afb9fd4598f6949922834483a7c9191e58",
        "version": "20180516"
    },
    "links": {},
    "messages": [],
    "origin": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples",
    "updated": "2018-05-18T13:55:44-04:00"
}
```

Requesting either of the entries mapped below this handler will return
the entries associated with that handler. Since we are using a single
REST handler to serve in both persistent and non-persistent mode, the
output has the same number of stanzas. However, notice that we have
added the PID of the REST handler process to the output, in the `content`
object:

```
$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent?output_mode=json | python -m json.tool
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
                "eai:acl": null,
                "pid": 97339
            },
            "id": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent/stanza1",
            "links": {
                "alternate": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent/stanza1",
                "list": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent/stanza1"
            },
            "name": "stanza1",
            "updated": "1969-12-31T19:00:00-05:00"
        }
    ],
    "generator": {
        "build": "95d592afb9fd4598f6949922834483a7c9191e58",
        "version": "20180516"
    },
    "links": {
        "_acl": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent/_acl"
    },
    "messages": [],
    "origin": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent",
    "paging": {
        "offset": 0,
        "perPage": 30,
        "total": 1
    },
    "updated": "2018-05-18T14:53:42-04:00"
}
```

In the persistent case, we can use the `ps` utility on this PID on the
system after making our request. This demonstrated that the REST handler
process is still running, and will continue to do so until it is idle
for 60 seconds:

```
$ ps 97339
       PID   TT  STAT      TIME COMMAND
     97339   ??  Ss     0:00.09 /opt/splunk/bin/python /opt/splunk/etc/apps/splunk-rest-examples/bin/simple_eai_handler.py persistent
```

In the non-persistent case, the output is the same:

```
$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent?output_mode=json | python -m json.tool
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
                "eai:acl": null,
                "pid": 97382
            },
            "id": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent/stanza1",
            "links": {
                "alternate": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent/stanza1",
                "list": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent/stanza1"
            },
            "name": "stanza1",
            "updated": "1969-12-31T19:00:00-05:00"
        }
    ],
    "generator": {
        "build": "95d592afb9fd4598f6949922834483a7c9191e58",
        "version": "20180516"
    },
    "links": {
        "_acl": "/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent/_acl"
    },
    "messages": [],
    "origin": "https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_nonpersistent",
    "paging": {
        "offset": 0,
        "perPage": 30,
        "total": 1
    },
    "updated": "2018-05-18T14:58:38-04:00"
}
```

... but our `ps` output indicates that the process exited immediately
after serving the request:

```
$ ps 97382
  PID   TT  STAT      TIME COMMAND
```

## Mapping Using Distinct Roots

We have also mapped the handlers under distinct roots, to demonstrate
the necessary restmap.conf and web.conf entries for this usage. These
would be called via:

```
$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/nonpersistent/simple_eai_nonpersistent?output_mode=json | python -m json.tool

$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/persistent/simple_eai_persistent?output_mode=json | python -m json.tool
```

Note that if you map the same REST handler to two different paths using
two different restmap.conf stanzas, successive requests to either path
will use the same process!

```
[15:23:18]$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/examples/simple_eai_persistent?output_mode=json | python -m json.tool | grep "pid" | awk -F: '{print $2}'
 98188
[15:23:22]$ curl -s -k -u admin:changed https://localhost:8089/servicesNS/admin/splunk-rest-examples/persistent/simple_eai_persistent?output_mode=json | python -m json.tool | grep "pid" | awk -F: '{print $2}'
 98188
```

## Development Notes

EAI handlers can be toggled between persistent and non-persistent modes
simply via the addition of the `handlerpersistentmode = true` attribute
in `restmap.conf`. This makes for easier development as each new
request to the handler is independent; no "hacks" such as killing the
REST handler process are necessary.

However, EAI handlers and the EAI framework are designed to simplify
development for particular cases: specifically, managing Splunk custom
configuration files in an app. The EAI framework lacks many
capabilities that one would expect. For instance, there is no (simple)
way within a custom EAI REST handler to determine whether or not a
handler has been called in persistent mode, as the handler does not even
have access to the path it was called from!

For this reason, among many others, we encourage the use of the script-
based handler mechanisms described elsewhere in this repository.