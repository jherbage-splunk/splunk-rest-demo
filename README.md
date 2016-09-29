# Splunk REST endpoint examples

## Overview
This app contains several REST endpoints that can be used as a starting point for Splunk app developers.

## Installation

To install, clone the repository into the `$SPLUNK_HOME/etc/apps` directory and restart Splunk.

## Overview

A Splunk REST handler is a script that is invoked when a request is made to Splunk's REST API at a specific URI. 
By setting configurations in the `restmap.conf` file of your app, and writing the corresponding code, you can 
enable Splunk to execute code of your choice in response to an HTTP request.

REST handlers are a powerful method for executing processes under the control of the primary splunkd process. They 
complement the other mechanisms provided by Splunk for external process execution, which include: modular inputs, 
CherryPy controllers, and custom search commands.

## Interfaces

Splunk provides several interfaces that can be extended for custom REST API development.

- "Old-style" handlers derived from the `rest.BaseRestHandler` class
- EAI handlers derived from the `admin.MConfigHandler` class
- "New-style" handlers derived from the `PersistentServerConnectionApplication` class. These are often referred to as 
  "persistent" handlers; however this is slightly misleading, as noted below.

This app does NOT provide an example of a class derived from `rest.BaseRestHandler`; in nearly all cases, it is 
preferable to derive from `PersistentServerConnectionApplication` for non-EAI use cases.

## EAI (Extensible Administration Interface)
The Extensible Administration Interface is the interface used by Splunk Core developers to easily extend the user 
interface to accommodate new adminstrative capabilities. The saved searches administration UI is a (complex) example of 
an interface driven by an EAI handler. The EAI interface provides certain services such as pagination, role-based access 
control, and namespacing to the developer; however, for the developer, writing an EAI handler is generally more complex 
than writing a "new-style" handler. EAI handlers can provide output in Atom feed format or (in more recent Splunk versions)
as JSON.

## Persistence

Prior to the introduction of "persistent mode" handlers, an external process - usually a Python interpreter - would be 
instantiated for *every* REST API call.

In Splunk 6.4, a new *persistent mode* has been added to REST handler interfaces enabling them to serve multiple REST 
API calls in a single process execution. This vastly reduces the number of processes that must be created to handle 
API traffic, and brings REST handlers roughly in line with the performance of CherryPy controllers.

Note that a handler in persistent mode will exit after it has been completely idle for a period of 60 seconds. This 
timeout is not currently configurable.

While the "new-style" protocol is commonly referred to as the "persistent" protocol, EAI handlers can also be run in 
persistent mode. An important distinction is that while a persistent handler written using the new protocol cannot be 
trivially converted to a non-persistent handler, EAI handlers can be "toggled" between persistent and non-persistent 
mode transparently, with no code changes required.


## App Contents
1. Simple persistent handler: `echo_persistent_handler.py`

	This handler is the simplest possible demonstration of the new "raw" REST interface. It echoes all arguments passed
	into it as output. Usage examples may be found at [echo_persistent_examples.](doc/echo_persistent_examples.md)

2. Simple EAI handler: `simple_eai_handler.py`

	This handler is the simplest possible EAI handler, provided solely for the purpose of demonstrating the mechanism 
	for populating EAI output. It is unlikely to be useful for any serious purpose. Usage examples may be found at 
	[simple_eai_examples.](doc/simple_eai_examples.md)
	
###Usage via splunkd

Access to custom REST handlers via splunkd, which listens on port 8089, can be performed from localhost using the "curl"
utility, similar to any other Splunk REST endpoint.

```
curl -k -u admin:changeme https://localhost:8089/services/echo_persistent
```

###Usage via splunkweb

A REST endpoint can be made accessible on the Splunkweb port (8000) via use of an "expose" stanza in web.conf.

Requests to port 8000 must circumvent CSRF protection restriction. For command-line testing, the simplest way to obtain
a token is to log in to Splunk using Chrome and, using Chrome's developer tools, right-click on any request and select 
"Copy as cURL".

A new REST request to port 8000 can then be crafted by replacing the parameters shown in `<brackets>`:

```
curl -k https://localhost:8000/en-US/splunkd/__raw/services/echo_persistent \
     -H 'Cookie: session_id_8000=<session_id>; splunkd_8000=<splunkd_8000>; splunkweb_csrf_token_8000=<csrf_token>'
```

Note that the URL should be rooted at /splunkd/__raw as shown above.

###License

No license, warranty, or claim of correctness for this code is provided, promised, or implied. This code is provided solely
for educational purposes and may not reflect the actual state of Splunk's product line. Please direct all complaints to the
author.
