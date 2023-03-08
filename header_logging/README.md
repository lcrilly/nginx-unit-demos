Request headers logging with JavaScript
=======================================

This demo config illustrates how JavaScript template literals can be
used to create custom/complex access logs. The access log contains
the typical fields and also includes every request header that was
sent by the client. This is done by iterating over the `headers`
object.

> **Note:** Requires Unit 1.30.0 or later

Demo
----

1. Start Unit. The command line options provide a richer demo experience.
```shell
$ unitd --no-daemon --log /dev/stderr &
```

2.  Apply the configuration using the `unitc` tool (installed with Unit Homebrew package)
```shell
$ unitc /config < conf.json
```

3. Make a request to the listener port
```shell
$ curl -i localhost:9000
```

The access log will be printed to the terminal showing the standard
request headers sent by curl(1). Try different clients or use `curl -H`
to send different headers.
