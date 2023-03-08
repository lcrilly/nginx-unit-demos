---
title: Simplifying your Application Stack with NGINX Unit
author: 🐦 @liamcrilly  |  liam@nginx.com  |
date: Jan-2023
extensions: [terminal]
---

# Origins

> " _When I started NGINX, I focused on a_
> 
> _very specific problem - how to handle more_
> 
> _customers per a single server._ "

-- **Igor Sysoev**, NGINX creator and founder

---

## Being a web server
## is like playing chess

# ♞ ♘ ♜ ♖ ♛ ♕

* Rules of the game
* Unknown, random opponents
* Unpredictable delays
* Multiple moves at once
* Relaying for another player
* Opponent goes AWOL

---

## Being a web server
## is like playing chess

# ♞ ♘ ♜ ♖ ♛ ♕

* Rules of the game
* Unknown, random opponents
* Unpredictable delays
* Multiple moves at once
* Relaying for another player
* Opponent goes AWOL

> ## Most of the time spent playing chess is _waiting_!

---

# How webservers used to play chess

```
                                                  ┏━━━━━━━━┓
                                                  ┃ server ┃
                                                  ┃ 🏁👑📓 ┃
                                                  ┗━━━━━━━━┛

    👨🏾‍💻 ──┤GET /index.html HTTP/1.1├────────────>  [ 🏁👑📓 ]

    👩🏼‍💻 ──┤GET /api/weather/v1/today HTTP/1.1├──>  [ 🏁👑📓 ]

    👩🏽‍💻 ──┤POST /upload.php HTTP/1.1├───────────>  [ 🏁👑📓 ]

                                                  [ 🏁👑📓 ]

                                                  [ 🏁👑📓 ]
```

---

# How NGINX plays chess

```
                                                  ┏━━━━━━━━┓
                                                  ┃ NGINX  ┃
                                                  ┃ 👑 📓  ┃
                                                  ┃        ┃
                                                  ┃ ╭────╮ ┃
    👨🏾‍💻 ──┤GET /index.html HTTP/1.1├────────────>  ┃ 🏁   │ ┃
                                                  ┃ ^    │ ┃
    👩🏼‍💻 ──┤GET /api/weather/v1/today HTTP/1.1├──>  ┃ │    v ┃
                                                  ┃ │   🏁 ┃
    👩🏽‍💻 ──┤POST /upload.php HTTP/1.1├───────────>  ┃ │    │ ┃
                                                  ┃ ╰🏁<─╯ ┃
                                                  ┃        ┃
                                                  ┃        ┃
                                                  ┗━━━━━━━━┛
```

## 🔁 Asynchronous event loop
* 📓 One copy of the rules
* 🔘 One playing space (worker process)
* 🏁 A board for each player, created/destroyed as needed

---

# How NGINX plays lots of chess

```
                                                  ┏━━━━━━━━┓
                                                  ┃ NGINX  ┃
                                                  ┃ 👑 📓  ┃
                                                  ┃        ┃
                                                  ┃ ╭────╮ ┃
    👨🏾‍💻 ──┤GET /index.html HTTP/1.1├────────────>  ┃ 🏁   v ┃
                                                  ┃ ^    🏁╂───╼ CPU core 
    👩🏼‍💻 ──┤GET /api/weather/v1/today HTTP/1.1├──>  ┃ ╰🏁<─╯ ┃
                                                  ┃        ┃
    👩🏽‍💻 ──┤POST /upload.php HTTP/1.1├───────────>  ┃ ╭────╮ ┃
                                                  ┃ 🏁   v ┃
                                                  ┃ ^    🏁╂───╼ CPU core
                                                  ┃ ╰🏁<─╯ ┃
                                                  ┗━━━━━━━━┛
```

## 🔁 Asynchronous event loop
* 📓 One copy of the rules
* 🔘 One playing space (worker process)
* 🏁 A board for each player, created/destroyed as needed

## 💪 **Worker process per CPU core**

---

# NGINX innovations

 🔁 Asynchronous event loop - does more with less

 💪 Multi-process architecture - for near-linear CPU scaling

 🚦 Configuration reload without interruption

---

# NGINX timeline

* `2001` genesis
* `2004` nginx-0.1 (first open source release)
* `2011` nginx-1.0, founded NGINX, Inc. ⬡
* `2019` No.1 web server 📈
* `2023`
  - stats
    - 300M web sites [1]
    - 34% of all websites [2]
    - 45% of busiest 1000 sites [2]

> Sources: [1] Netcraft, [2] W3Techs

---

# Introducing NGINX Unit (an NGINX project)

## Universal web app server

* Started with experiments for NGINX v2
* Combined with idea to natively run applicatoin code without separate process managers
* Open source, Apache 2 license

### Timeline
  - `2016` initial prototype
  - `2017` unit-0.1 (first public release)
  - `2018` unit-1.0
    `┋`
  - `2023` unit-1.29

---

# Universal web app server

## Primary Capabilities
1. Serves static assets
2. Runs application code
3. Proxies to backends

…
### The only server component required to build web apps and APIs
  - Deliver complete web applications with fewer pieces
  - Homogenous benefits: consistency, configuration

…
### Evolved architecture from NGINX (no shared code)
  - Don't invent a new configuration language/syntax
  - Reconfiguration happens in-situ (no reloads)
  - Flexible request routing, decoupled from network ports

---

# Unit architecture

* **Main process** starts Unit and creates/destroys the other processes
* **Controller process** accepts new configuration and applies it to the router
* **Router process** (multi-threaded🧵) handles client requests in async event loop
…

```
 ┌───────────────────────────────────────────┐
 │                 Unit                      │
 │   ┏━━━━━━━━━━━━┓    ┏━━━━━━━━━━━━┓        │
 │   ┃    Main    ┃    ┃ Controller ┃        │
 │   ┗━━━━━━━━━━━━┛    ┗━━━━━━━━━━━━┛        │
 │   ┏━━━━━━━━━━━━┓                          │
 │   ┃   Router   ┃━┓                        │
 │   ┃   ╭────╮   ┃ ┃━┓                      │
 │   ┃   🏁   v   ┃ ┃ ┃                      │
 │   ┃   ^    🏁  ┃ ┃ ┃                      │
 │   ┃   ╰🏁<─╯   ┃ ┃ ┃                      │
 │   ┗━━━━━━━━━━━━┛ ┃ ┃                      │
 │     ┗━━━━━🧵━━━━━┛ ┃                      │
 │       ┗━━━━━🧵━━━━━┛                      │
 └───────────────────────────────────────────┘
 ```

---

# Unit architecture

* **Main process** starts Unit and creates/destroys the other processes
* **Controller process** accepts new configuration and applies it to the router
* **Router process** (multi-threaded🧵) handles client requests in async event loop
* **Application processes** managed by Router, scaled up/down as required

```
 ┌───────────────────────────────────────────┐
 │                 Unit                      │
 │   ┏━━━━━━━━━━━━┓    ┏━━━━━━━━━━━━┓        │
 │   ┃    Main    ┃    ┃ Controller ┃        │
 │   ┗━━━━━━━━━━━━┛    ┗━━━━━━━━━━━━┛        │
 │   ┏━━━━━━━━━━━━┓                          │
 │   ┃   Router   ┃━┓                        │
 │   ┃   ╭────╮   ┃ ┃━┓                      │
 │   ┃   🏁   v   ┃ ┃ ┠───[App: PHP]         │
 │   ┃   ^    🏁  ┃ ┃ ┃                      │
 │   ┃   ╰🏁<─╯   ┃ ┃ ┠───[App: Python]      │
 │   ┗━━━━━━━━━━━━┛ ┃ ┃                      │
 │     ┗━━━━━🧵━━━━━┛ ┠───(.html .js .css)   │
 │       ┗━━━━━🧵━━━━━┛                      │
 └───────────────────────────────────────────┘
```

---

# Unit runs apps across many languages and frameworks

## Languages
> ### PHP, Python, Ruby, Perl, Go, Node.JS, Java

## Frameworks
> Laravel        Koa        Flask        Quart         
>
>   Rails      Falcon     CakePHP     FastAPI    
>
>  Express          Django       YiiFramework
>
> Sanic     Catalyst      Bottle      Responder
>
>  Lumen         CodeIgniter          Spring
>
> Zope     Pyramid     Starlette     Guillotina   

---

# The problem with web frameworks

### 🚏 Split routing, and serving of static+dynamic content

### 🔐 TLS at the runtime is challenging

### 🔧 Configuring a web server and application process manager

### 🐳 Complex containers and the multi-daemon anti-pattern

---

# JSON configuration

```json
{

    "listeners": { },

    "routes": [ ],

    "applications": { }

}
```

---

# JSON configuration example

```json
{
  "listeners": {
    "*:8080": {                       // Listen for new TCP connections
      "pass": "routes"                // Send all HTTP requests to the router
    }
  },

  "routes": [
    {                                 // A single route to catch everything
      "action": {
        "share": "/var/www$uri",      // Serve the requested URI from disk,
        "fallback": {                 // but if that doesn't exist then,
          "pass": "applications/calc" // send the request to the app.
        }
      }
    }
  ],

  "applications": {
    "calc": {
      "type": "python",               // Specify the language module
      "path": "/var/www/apps/calc",   // Directory where the code is
      "module": "calculator"          // For Python, the module name
    }
  }
}
```

---

# Flexible configuration that spans network and runtime

## Infrastructure as code for the entire stack

```
┌──────────────────┐                                                           ┌───────────┐
│                  │ ───────────────────────────[pass]───────────────────────> │           │
│                  │             ┌────────────┐                                │ upstreams │
│                  │             │            │ ────────────[proxy]──────────> │           │
│     listeners    │ ──[pass]──> │            │                                └───────────┘
│                  │             │            │              ┌────────────────┐
│                  │             │   routes   │ ──[share]──> │ /files/on/disk │
│                  │             │            │              └────────────────┘
│                  │             │            │              ┌────────────────┐
│  ┏━━━━━━━━━━━━┓  │             │            │ ──[pass]───> │                │
│  ┃certificates┃  │             └────────────┘              │  applications  │
│  ┗━━━━━━━━━━━━┛  │ ────────────────[pass]────────────────> │                │
│                  │                                         └────────────────┘
└──────────────────┘
```
```
    LAYER 4-6                       LAYER 7                      USER SPACE         LAYER 7
  TCP/TLS/ports                  Headers, URIs                   Code/Files        IP/Ports
```

---

# Demo

```terminal22
zsh -i
```

---

# Why use NGINX Unit

### 🚀 Build applications
 * Simplify microservices
 * Modernize monoliths

…
### 🔒 Deploy to production
 * True end-to-end TLS
 * Isolate applications

---

# Get started with NGINX Unit

### 🔧 Installation, configuration, and how-to **docs**
 * https://unit.nginx.org/

…
### 🧑‍💻 Code, issues
 * https://github.com/nginx/unit

…
### 💬 Community, discussion
 * https://community.nginx.org/joinslack
 * unit@nginx.org (https://mailman.nginx.org/)

---

# _fin_

### ℹ️ This presentation and demos at https://github.com/lcrilly/nginx-unit-demos

> In-terminal presentation by [lookatme](https://lookatme.readthedocs.io/en/latest/index.html)
>
> https://github.com/d0c-s4vage/lookatme
