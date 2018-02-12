# Persistent REST handler examples

The persistent rest driver script distributed as part of the Splunk internal SDK simplifies marshaling of arguments. 
The handler receives all its arguments as a JSON string, which is convertible to a Python dictionary or a comparable 
map structure in other programming languages.

Depending on the restmap.conf parameters for the rest handler, however, certain attributes may be missing from the 
JSON. The user and app context used to invoke the handler will also affect the available attributes.

The following examples should mimic closely the behavior of the "echo_persistent" handler on a system where this
Splunk app is installed. This handler simply echoes the original input back as a JSON string; this is a good way to see
how the various calling conventions will affect the input your script receives.

## Contents
- [Basic usage](#basic)
- [Using data payloads](#payload)
- [Using query parameters](#query)
- [Using namespace context](#namespace)
- [Using user and namespace context](#user)
- [Invalid context errors](#invalid)
- [Persistent request payload format](#persistentrequest)
- [Persistent reply payload format](#persistentreply)
- [Multiformat requests](#rawrequests)

### <a name="basic"></a>Basic usage

Note that the "cookies" and "headers" attributes are enabled via the use of the "passCookies" and passHttpHeaders" 
restmap.conf parameters, respectively.

```
$ curl -s -k -u admin:changeme https://localhost:8089/services/echo_persistent | python -m json.tool
{
    "connection": {
        "listening_port": 8089,
        "src_ip": "127.0.0.1",
        "ssl": true
    },
    "cookies": [],
    "headers": [
        [
            "Authorization",
            "Basic NOTAREALTOKEN"
        ],
        [
            "User-Agent",
            "curl/7.29.0"
        ],
        [
            "Host",
            "localhost:8089"
        ],
        [
            "Accept",
            "*/*"
        ]
    ],
    "method": "GET",
    "output_mode": "xml",
    "output_mode_explicit": false,
    "query": [],
    "rest_path": "/echo_persistent",
    "restmap": {
        "conf": {
            "handler": "echo_persistent_handler.EchoHandler",
            "match": "/echo_persistent",
            "output_modes": "json",
            "passHttpCookies": "true",
            "passHttpHeaders": "true",
            "passPayload": "true",
            "requireAuthentication": "true",
            "script": "echo_persistent_handler.py",
            "scripttype": "persist"
        },
        "name": "script:echo"
    },
    "server": {
        "guid": "1B43291B-02C8-45C3-A9BD-72A9C9130EDD",
        "hostname": "host.domain.com",
        "rest_uri": "https://127.0.0.1:8089",
        "servername": "host.domain.com"
    },
    "session": {
        "authtoken": "NOTAREALTOKEN",
        "user": "admin"
    }
}
```

### <a name="payload"></a>Using data payloads

Passing a data argument converts the method to a HTTP POST, and adds the "form" attribute. Since we are also specifying 
"passPayload=true" in restmap.conf, the payload is also included in raw form in the "payload" attribute. Note that the 
contents of the "form" argument are passed as a list of pairs, and thus can be repeated, so it is important to account 
for repeated keys when converting the form arguments to a map or dictionary data structure.

```
$ curl -s -k -u admin:changeme https://localhost:8089/services/echo_persistent -d "abcd=EFGH" -d "ijkl=MNOP" | python -m json.tool
{
    "connection": {
        "listening_port": 8089,
        "src_ip": "127.0.0.1",
        "ssl": true
    },
    "cookies": [],
    "form": [
        [
            "abcd",
            "EFGH"
        ],
        [
            "ijkl",
            "MNOP"
        ]
    ],
    "headers": [
        [
            "Authorization",
            "Basic NOTAREALTOKEN"
        ],
        [
            "User-Agent",
            "curl/7.29.0"
        ],
        [
            "Host",
            "localhost:8089"
        ],
        [
            "Accept",
            "*/*"
        ],
        [
            "Content-Length",
            "19"
        ],
        [
            "Content-Type",
            "application/x-www-form-urlencoded"
        ]
    ],
    "method": "POST",
    "output_mode": "xml",
    "output_mode_explicit": false,
    "payload": "abcd=EFGH&ijkl=MNOP",
    "query": [],
    "rest_path": "/echo_persistent",
    "restmap": {
        "conf": {
            "handler": "echo_persistent_handler.EchoHandler",
            "match": "/echo_persistent",
            "output_modes": "json",
            "passHttpCookies": "true",
            "passHttpHeaders": "true",
            "passPayload": "true",
            "requireAuthentication": "true",
            "script": "echo_persistent_handler.py",
            "scripttype": "persist"
        },
        "name": "script:echo"
    },
    "server": {
        "guid": "1B43291B-02C8-45C3-A9BD-72A9C9130EDD",
        "hostname": "host.domain.com",
        "rest_uri": "https://127.0.0.1:8089",
        "servername": "host.domain.com"
    },
    "session": {
        "authtoken": "NOTAREALTOKEN",
        "user": "admin"
    }
}
```

### <a name="query"></a>Using query parameters
Key-value arguments in the HTTP query string will be passed as part of the "query" attribute. Like the "form" attribute,
"query" information is passed to the handler as a list of pairs. Thus it is possible for arguments to be repeated. 
This must be taken into account when crafting your REST handler: do  you prefer to receive multi-valued arguments in a 
special form such as comma-separated strings, or do you wish to allow the user to simply specify repeated arguments?

```
$ curl -s -k -u admin:changeme 'https://localhost:8089/services/echo_persistent?arg1=value1&arg2=value2&arg1=value1' | python -m json.tool
{
    "connection": {
        "listening_port": 8089,
        "src_ip": "127.0.0.1",
        "ssl": true
    },
    "cookies": [],
    "headers": [
        [
            "Authorization",
            "Basic NOTAREALTOKEN"
        ],
        [
            "User-Agent",
            "curl/7.29.0"
        ],
        [
            "Host",
            "localhost:8089"
        ],
        [
            "Accept",
            "*/*"
        ]
    ],
    "method": "GET",
    "output_mode": "xml",
    "output_mode_explicit": false,
    "query": [
        [
            "arg1",
            "value1"
        ],
        [
            "arg2",
            "value2"
        ],
        [
            "arg1",
            "value1"
        ]
    ],
    "rest_path": "/echo_persistent",
    "restmap": {
        "conf": {
            "handler": "echo_persistent_handler.EchoHandler",
            "match": "/echo_persistent",
            "output_modes": "json",
            "passHttpCookies": "true",
            "passHttpHeaders": "true",
            "passPayload": "true",
            "requireAuthentication": "true",
            "script": "echo_persistent_handler.py",
            "scripttype": "persist"
        },
        "name": "script:echo"
    },
    "server": {
        "guid": "1B43291B-02C8-45C3-A9BD-72A9C9130EDD",
        "hostname": "host.domain.com",
        "rest_uri": "https://127.0.0.1:8089",
        "servername": "host.domain.com"
    },
    "session": {
        "authtoken": "NOTAREALTOKEN",
        "user": "admin"
    }
}
```

### <a name="namespace"></a>Using namespace context

Making a request to the handler under a specific namespace context will result in the addition of the "ns" key to 
the argument dictionary. Note that the "user" is "-", which indicates the "wildcard" or "all apps" context.

```
$ curl -s -k -u admin:changeme https://localhost:8089/servicesNS/-/splunk-rest-examples/echo_persistent | python -m json.tool
{
    "connection": {
        "listening_port": 8089,
        "src_ip": "127.0.0.1",
        "ssl": true
    },
    "cookies": [],
    "headers": [
        [
            "Authorization",
            "Basic NOTAREALTOKEN"
        ],
        [
            "User-Agent",
            "curl/7.29.0"
        ],
        [
            "Host",
            "localhost:8089"
        ],
        [
            "Accept",
            "*/*"
        ]
    ],
    "method": "GET",
    "ns": {
        "app": "splunk-rest-examples"
    },
    "output_mode": "xml",
    "output_mode_explicit": false,
    "query": [],
    "rest_path": "/echo_persistent",
    "restmap": {
        "conf": {
            "handler": "echo_persistent_handler.EchoHandler",
            "match": "/echo_persistent",
            "output_modes": "json",
            "passHttpCookies": "true",
            "passHttpHeaders": "true",
            "passPayload": "true",
            "requireAuthentication": "true",
            "script": "echo_persistent_handler.py",
            "scripttype": "persist"
        },
        "name": "script:echo"
    },
    "server": {
        "guid": "1B43291B-02C8-45C3-A9BD-72A9C9130EDD",
        "hostname": "host.domain.com",
        "rest_uri": "https://127.0.0.1:8089",
        "servername": "host.domain.com"
    },
    "session": {
        "authtoken": "NOTAREALTOKEN",
        "user": "admin"
    }
}
```

### <a name="user"></a>Using user and namespace context

Adding a specific user to the context will result in the addition of the "user" to the ns" attribute of the argument 
dictionary.

```
$ curl -s -k -u admin:changeme https://localhost:8089/servicesNS/admin/splunk-rest-examples/echo_persistent | python -m json.tool
{
    "connection": {
        "listening_port": 8089,
        "src_ip": "127.0.0.1",
        "ssl": true
    },
    "cookies": [],
    "headers": [
        [
            "Authorization",
            "Basic NOTAREALTOKEN"
        ],
        [
            "User-Agent",
            "curl/7.29.0"
        ],
        [
            "Host",
            "localhost:8089"
        ],
        [
            "Accept",
            "*/*"
        ]
    ],
    "method": "GET",
    "ns": {
        "app": "splunk-rest-examples",
        "user": "admin"
    },
    "output_mode": "xml",
    "output_mode_explicit": false,
    "query": [],
    "rest_path": "/echo_persistent",
    "restmap": {
        "conf": {
            "handler": "echo_persistent_handler.EchoHandler",
            "match": "/echo_persistent",
            "output_modes": "json",
            "passHttpCookies": "true",
            "passHttpHeaders": "true",
            "passPayload": "true",
            "requireAuthentication": "true",
            "script": "echo_persistent_handler.py",
            "scripttype": "persist"
        },
        "name": "script:echo"
    },
    "server": {
        "guid": "1B43291B-02C8-45C3-A9BD-72A9C9130EDD",
        "hostname": "host.domain.com",
        "rest_uri": "https://127.0.0.1:8089",
        "servername": "host.domain.com"
    },
    "session": {
        "authtoken": "NOTAREALTOKEN",
        "user": "admin"
    }
}
```

### <a name="invalid"></a>Invalid context errors

However, trying to view objects in a nonexistent context will result in an error. Note that the error messages are NOT
JSON-formatted.

```
$ curl -s -k -u admin:changeme https://localhost:8089/servicesNS/NOSUCHUSER/splunk-rest-examples/echo_persistent
<?xml version="1.0" encoding="UTF-8"?>
<response>
  <messages>
    <msg type="ERROR">User does not exist: nosuchuser</msg>
  </messages>
</response>
```

HTTP status code should be used to determine whether or not a request succeeded:

```
$ curl -s -k -u admin:changeme -o /dev/null -w "%{http_code}\n" https://localhost:8089/servicesNS/NOSUCHUSER/splunk-rest-examples/echo_persistent
404
```


### <a name="persistentrequest"></a>Persistent Request Payload Format

The new-style persistent REST request format is documented below. This will be passed in to the handle() method's in_string 
parameter.

```
     {
       "output_mode" = "xml"|"json"|etc,
       "output_mode_explicit" = True/False,
       "server" = {
         "rest_uri" = "https://127.0.0.1:8089",
         "hostname" = "string",
         "servername" = "string",
         "guid" = "0000-...",
         "site" = "0"                 # only for multisite clustering
       },
       "system_authtoken" = "authtoken"       # missing if passSystemAuth=false
       "restmap" = { "name" = "...",  # missing if passConf=false
         "conf" = { "key": "value", ... }
       },
       "path_info": "part/after/match",       # Missing if there isn't any URL after restmap "match"
       "query" = [ [ "key", "value" ], ... ]  # "GET" args passed on the URL
       "connection" = {
         "src_ip" = "..."
         "ssl" = True/False
         "listening_port" = port#
         "listening_ip" = "..."     # missing if listening to all
       },
       "session" = {                  # missing if an un-authed call
         "user": "name",              # missing if no user context
         "authtoken": "token",        # missing if not logged in
         "tz": "US/Pacific",          # missing if user is in the system's default timezone
         "search_id": "search",       # present only if REST call from search process
         "embed": { "app": "X", "user": "Y", "object": "Z" }, # present only for anonymous embed requests
       },
       "rest_path" = "/...",          # part of the URI after the /services...
       "lang" = "en-US",              # for requests originating in the UI, the language from the URL
       "api_version" = "1.2.3",       # only present for REST requests that send an explicit version on URL
       "method" = "GET/etc",
       "ns" = {                       # missing if not namespaced (i.e. "/services" instead of "/servicesNS")
         "app": "search",             # missing if wildcarded app
         "user": "admin"              # missing if wildcarded user
       },
       "form" = [ [ "key", "value" ], ... ]   # POST args passed in the body (only if a POST/PUT)
       "headers" = [ [ "name", "value" ], ...]        # missing if passHttpHeaders=false
       "cookies" = [ [ "name", "value" ], ...]        # missing if passHttpCookies=false
       "payload" = "..."              # missing unless POST/PUT and non-empty
       "payload_base64" = "..."               # ...or if requested in restmap.conf we can send base64-encoded
     }
```

## <a name="persistentreply"></a>Persistent Request Reply Format

The new-style persistent REST reply format is documented below.

```
   {
      "status" = 200,         # Optional (200 is the default)
      "status" = [ 200, "Foo" ],      # ...or you can pass a status code and the explaination string
      "headers" = [           # Optional (add headers to result)
        [ "Name", "value" ]
      ],
      "headers" = { "Name": "value" } # ... or 'headers' can be an object
      "headers" = { "Name": [ "value1", "value2" ] } # ... and a single header can be set multiple times
      "cookies" = [           # Optional (send Add-Cookie headers)
        {
           "name": "foo",
           "value": "bar",
           "domain": domain,          # optional
           "path": path,              # optional
           "httponly": True/False,    # optional (defaults to true)
           "secure": True/False,      # optional (defaults to true if servicing an https request)
           "maxage": seconds,         # optional
        },
      ],
      "cookies" = { "foo": { ... } }  # ... or 'cookies' can be an object
      "cookies" = { "foo": "bar" }    # ... using a string instead of an object accepts all of the defaults
      "filename" = "foo.txt",         # Optional (send a Content-Disposition header to suggest browser should download)
      "log" = True/False,             # Optional (false will prevent transaction from going in splunkd_access.log)
      "payload" = "",                 # send the reply payload as a raw string
      "payload_base64" = "",          # ...or it's provided as a base64-encoded one
      "payload" = {obj} / [array],    # ...or it can be a JSON object (which implies that we should return a JSON content type)
      "payload" = Null,               # ...or we want to explicitly send nothing (implies status 204)
   }
```

## <a name="multiformatrequests"></a>Multiformat Requests

One of the key use cases of the persistent REST handler framework is to enable the Splunk REST API to return something
other than XML or JSON output. The "echo" handler in this app uses the "raw" format to return its arguments as they were
received. The "multiformat" handler included in this app provides a slightly more complex example, demonstrating the 
difference between raw and JSON formats. A URI query parameter is used to request a specific format as part of the 
request; if no specific format is requested, the request is regarded as invalid and a 204 is returned.

This is a "raw" request. Verbose output from the "curl" command is shown. Note that no content-type is returned. The
author of the REST handler script could at this point add a "headers" object to the reply to specify specific 
content handling. 
```
$  curl -v -k -u admin:changeme "https://localhost:8089/services/multiformat_persistent?format=raw&input=kilroy_was_here"
*   Trying ::1...
* TCP_NODELAY set
* Connection failed
* connect to ::1 port 8089 failed: Connection refused
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8089 (#0)
* ALPN, offering http/1.1
* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
* successfully set certificate verify locations:
*   CAfile: /opt/local/share/curl/curl-ca-bundle.crt
  CApath: none
* TLSv1.2 (OUT), TLS header, Certificate Status (22):
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
* TLSv1.2 (IN), TLS handshake, Server finished (14):
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
* TLSv1.2 (OUT), TLS change cipher, Client hello (1):
* TLSv1.2 (OUT), TLS handshake, Finished (20):
* TLSv1.2 (IN), TLS change cipher, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Finished (20):
* SSL connection using TLSv1.2 / ECDHE-RSA-AES256-GCM-SHA384
* ALPN, server did not agree to a protocol
* Server certificate:
*  subject: CN=SplunkServerDefaultCert; O=SplunkUser
*  start date: Feb 11 21:42:26 2018 GMT
*  expire date: Feb 10 21:42:26 2021 GMT
*  issuer: C=US; ST=CA; L=San Francisco; O=Splunk; CN=SplunkCommonCA; emailAddress=support@splunk.com
*  SSL certificate verify result: self signed certificate in certificate chain (19), continuing anyway.
* Server auth using Basic with user 'admin'
> GET /services/multiformat_persistent?format=raw&input=kilroy_was_here HTTP/1.1
> Host: localhost:8089
> Authorization: Basic NOT_A_REAL_TOKEN
> User-Agent: curl/7.57.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Mon, 12 Feb 2018 00:11:56 GMT
< Expires: Thu, 26 Oct 1978 00:00:00 GMT
< Cache-Control: no-store, no-cache, must-revalidate, max-age=0
< Content-Length: 15
< Vary: *
< Connection: Keep-Alive
< X-Frame-Options: SAMEORIGIN
< Server: Splunkd
<
* Connection #0 to host localhost left intact
ereh_saw_yorlik
```

This is a "json" request. By returning the output as an object (in this case, a simple list) that has a JSON 
representation, splunkd will return the output as JSON. Note the presence of the Content-type header in the output.

```
$  curl -v -k -u admin:changeme "https://localhost:8089/services/multiformat_persistent?format=json&input=kilroy_was_here"
*   Trying ::1...
* TCP_NODELAY set
* Connection failed
* connect to ::1 port 8089 failed: Connection refused
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to localhost (127.0.0.1) port 8089 (#0)
* ALPN, offering http/1.1
* Cipher selection: ALL:!EXPORT:!EXPORT40:!EXPORT56:!aNULL:!LOW:!RC4:@STRENGTH
* successfully set certificate verify locations:
*   CAfile: /opt/local/share/curl/curl-ca-bundle.crt
  CApath: none
* TLSv1.2 (OUT), TLS header, Certificate Status (22):
* TLSv1.2 (OUT), TLS handshake, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Server hello (2):
* TLSv1.2 (IN), TLS handshake, Certificate (11):
* TLSv1.2 (IN), TLS handshake, Server key exchange (12):
* TLSv1.2 (IN), TLS handshake, Server finished (14):
* TLSv1.2 (OUT), TLS handshake, Client key exchange (16):
* TLSv1.2 (OUT), TLS change cipher, Client hello (1):
* TLSv1.2 (OUT), TLS handshake, Finished (20):
* TLSv1.2 (IN), TLS change cipher, Client hello (1):
* TLSv1.2 (IN), TLS handshake, Finished (20):
* SSL connection using TLSv1.2 / ECDHE-RSA-AES256-GCM-SHA384
* ALPN, server did not agree to a protocol
* Server certificate:
*  subject: CN=SplunkServerDefaultCert; O=SplunkUser
*  start date: Feb 11 21:42:26 2018 GMT
*  expire date: Feb 10 21:42:26 2021 GMT
*  issuer: C=US; ST=CA; L=San Francisco; O=Splunk; CN=SplunkCommonCA; emailAddress=support@splunk.com
*  SSL certificate verify result: self signed certificate in certificate chain (19), continuing anyway.
* Server auth using Basic with user 'admin'
> GET /services/multiformat_persistent?format=json&input=kilroy_was_here HTTP/1.1
> Host: localhost:8089
> Authorization: Basic YWRtaW46Y2hhbmdlbWU=
> User-Agent: curl/7.57.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Date: Mon, 12 Feb 2018 00:13:30 GMT
< Expires: Thu, 26 Oct 1978 00:00:00 GMT
< Cache-Control: no-store, no-cache, must-revalidate, max-age=0
< Content-Type: application/json; charset=UTF-8
< X-Content-Type-Options: nosniff
< Content-Length: 19
< Vary: *
< Connection: Keep-Alive
< X-Frame-Options: SAMEORIGIN
< Server: Splunkd
<
* Connection #0 to host localhost left intact
["ereh_saw_yorlik"]
```