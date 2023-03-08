Simple add application demo
===========================

This directory contains several implementations of the same `add` demo.
The code and configuration for each supported programming language is
in the corresponding subdirectory.

Each implementation of the `add` application behaves the same way (more
or less). Requests to the **/add** URI expect a `POST` body with a JSON
payload. The JSON should have an array of numbers, which will be added
together.

**Sample request**
```json
{
    "operands": [33, 50]
}
```

**Sample response**
```json
{
    "result": 83
}
```

> **Note:** The configuration JSON uses relative paths so that you don't
> need to make local edits. Therefore you must start `unitd` from this
> directory.

Demo: Configuration
-------------------

1. Start Unit. The command line options provide a richer demo experience.
```shell
$ unitd --no-daemon --log /dev/stderr &
```

2. Select a programming language, then show the code and configuration
```shell
$ ls -l python
$ cat python/add.py
$ cat python/conf.json | jq
```

3. Apply the configuration using the `unitc` tool (installed with Unit Homebrew package)
```shell
$ cat python/conf.json | unitc /config
```

Demo: Application
-----------------

1. Show the HTML on disk, then serve it through Unit
```shell
$ cat html/index.html
$ curl localhost:9000
```

2. Create a JSON/POST request to the **/add** URI
```shell
echo '{"operands":[11,4]}' | curl -d@- localhost:9000/add
```

> **Note:** HTTPie can create JSON requests natively and set Content-Type
> headers correctly. The Java (Spring Boot) implementation requires this.
```shell
$ http -v localhost:9000/add operands:=\[11,4]
```

For fun with [floating point rounding errors](https://0.30000000000000004.com/), try
```json
{
    "operands": [0.1, 0.2]
}
```
