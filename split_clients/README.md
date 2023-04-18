Split clients using JavaScript
==============================

This directory demonstrates how JavaScript modules can be used to implement
sophisticated routing decisions. A JavaScript function creates a hash of
the `User-Agent` request field and returns the name of the route that will
be used to process the request (`blue` or `green`).

The proportion of the hash numberspace that will return `green` is defined
in the `entry` route.

> **Note:** The configuration JSON uses relative paths so that you don't
> need to make local edits. Therefore you must start `unitd` from this
> directory.

Demo: Configuration
-------------------

1. Start Unit. The command line options provide a richer demo experience.
```shell
unitd --no-daemon --log /dev/stderr &
```

2. Upload the JavaScript module
```shell
cat split.js
cat split.js | unitc /js_modules
```

3. Apply the configuration using the `unitc` tool. Note that router logging
   and access logging will be displayed in the console.
```shell
cat conf.json
cat conf.json | unitc /config
```

Demo: Application (CLI)
-----------------------

1. Check the response with curl(1)
```shell
curl localhost:9000
```

2. Check the response with wget(1)
```shell
wget -O- localhost:9000
``` 

3. Set the proportion of User-Agents that will receive the green response to 25%
```shell
echo "\"\`routes/\${split.clients(0.25, headers['User-Agent'])}\`\"" | unitc /config/routes/entry/0/action/pass
```

4. Use other HTTP clients (e.g. HTTPie) to demonstrate the effect of User Agent
   string on routing. Or manipulate the User Agent header directly.
```shell
curl -H "User-Agent: foo" localhost:9000
```

> **Note:** this demo serves a static file to illustrate the blue/green
> routing decision. However, remark how this can be used to serve different
> versions of an application from the same Unit instance (or container)
> without the need for complex reverse proxy or Ingress configurations.
