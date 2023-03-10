---
title: Simplifying your Application Stack with NGINX Unit
author: ð¦ @liamcrilly  |  liam@nginx.com  |
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

# â â â â â â

* Rules of the game
* Unknown, random opponents
* Unpredictable delays
* Multiple moves at once
* Relaying for another player
* Opponent goes AWOL

---

## Being a web server
## is like playing chess

# â â â â â â

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
                                                  ââââââââââ
                                                  â server â
                                                  â ððð â
                                                  ââââââââââ

    ð¨ð¾âð» âââ¤GET /index.html HTTP/1.1âââââââââââââ>  [ ððð ]

    ð©ð¼âð» âââ¤GET /api/weather/v1/today HTTP/1.1âââ>  [ ððð ]

    ð©ð½âð» âââ¤POST /upload.php HTTP/1.1ââââââââââââ>  [ ððð ]

                                                  [ ððð ]

                                                  [ ððð ]
```

---

# How NGINX plays chess

```
                                                  ââââââââââ
                                                  â NGINX  â
                                                  â ð ð  â
                                                  â        â
                                                  â â­âââââ® â
    ð¨ð¾âð» âââ¤GET /index.html HTTP/1.1âââââââââââââ>  â ð   â â
                                                  â ^    â â
    ð©ð¼âð» âââ¤GET /api/weather/v1/today HTTP/1.1âââ>  â â    v â
                                                  â â   ð â
    ð©ð½âð» âââ¤POST /upload.php HTTP/1.1ââââââââââââ>  â â    â â
                                                  â â°ð<ââ¯ â
                                                  â        â
                                                  â        â
                                                  ââââââââââ
```

## ð Asynchronous event loop
* ð One copy of the rules
* ð One playing space (worker process)
* ð A board for each player, created/destroyed as needed

---

# How NGINX plays lots of chess

```
                                                  ââââââââââ
                                                  â NGINX  â
                                                  â ð ð  â
                                                  â        â
                                                  â â­âââââ® â
    ð¨ð¾âð» âââ¤GET /index.html HTTP/1.1âââââââââââââ>  â ð   v â
                                                  â ^    ðâââââ¼ CPU core 
    ð©ð¼âð» âââ¤GET /api/weather/v1/today HTTP/1.1âââ>  â â°ð<ââ¯ â
                                                  â        â
    ð©ð½âð» âââ¤POST /upload.php HTTP/1.1ââââââââââââ>  â â­âââââ® â
                                                  â ð   v â
                                                  â ^    ðâââââ¼ CPU core
                                                  â â°ð<ââ¯ â
                                                  ââââââââââ
```

## ð Asynchronous event loop
* ð One copy of the rules
* ð One playing space (worker process)
* ð A board for each player, created/destroyed as needed

## ðª **Worker process per CPU core**

---

# NGINX innovations

 ð Asynchronous event loop - does more with less

 ðª Multi-process architecture - for near-linear CPU scaling

 ð¦ Configuration reload without interruption

---

# NGINX timeline

* `2001` genesis
* `2004` nginx-0.1 (first open source release)
* `2011` nginx-1.0, founded NGINX, Inc. â¬¡
* `2019` No.1 web server ð
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
    `â`
  - `2023` unit-1.29

---

# Universal web app server

## Primary Capabilities
1. Serves static assets
2. Runs application code
3. Proxies to backends

â¦
### The only server component required to build web apps and APIs
  - Deliver complete web applications with fewer pieces
  - Homogenous benefits: consistency, configuration

â¦
### Evolved architecture from NGINX (no shared code)
  - Don't invent a new configuration language/syntax
  - Reconfiguration happens in-situ (no reloads)
  - Flexible request routing, decoupled from network ports

---

# Unit architecture

* **Main process** starts Unit and creates/destroys the other processes
* **Controller process** accepts new configuration and applies it to the router
* **Router process** (multi-threadedð§µ) handles client requests in async event loop
â¦

```
 âââââââââââââââââââââââââââââââââââââââââââââ
 â                 Unit                      â
 â   ââââââââââââââ    ââââââââââââââ        â
 â   â    Main    â    â Controller â        â
 â   ââââââââââââââ    ââââââââââââââ        â
 â   ââââââââââââââ                          â
 â   â   Router   âââ                        â
 â   â   â­âââââ®   â âââ                      â
 â   â   ð   v   â â â                      â
 â   â   ^    ð  â â â                      â
 â   â   â°ð<ââ¯   â â â                      â
 â   ââââââââââââââ â â                      â
 â     ââââââð§µââââââ â                      â
 â       ââââââð§µââââââ                      â
 âââââââââââââââââââââââââââââââââââââââââââââ
 ```

---

# Unit architecture

* **Main process** starts Unit and creates/destroys the other processes
* **Controller process** accepts new configuration and applies it to the router
* **Router process** (multi-threadedð§µ) handles client requests in async event loop
* **Application processes** managed by Router, scaled up/down as required

```
 âââââââââââââââââââââââââââââââââââââââââââââ
 â                 Unit                      â
 â   ââââââââââââââ    ââââââââââââââ        â
 â   â    Main    â    â Controller â        â
 â   ââââââââââââââ    ââââââââââââââ        â
 â   ââââââââââââââ                          â
 â   â   Router   âââ                        â
 â   â   â­âââââ®   â âââ                      â
 â   â   ð   v   â â â âââ[App: PHP]         â
 â   â   ^    ð  â â â                      â
 â   â   â°ð<ââ¯   â â â âââ[App: Python]      â
 â   ââââââââââââââ â â                      â
 â     ââââââð§µââââââ â âââ(.html .js .css)   â
 â       ââââââð§µââââââ                      â
 âââââââââââââââââââââââââââââââââââââââââââââ
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

### ð Split routing, and serving of static+dynamic content

### ð TLS at the runtime is challenging

### ð§ Configuring a web server and application process manager

### ð³ Complex containers and the multi-daemon anti-pattern

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
ââââââââââââââââââââ                                                           âââââââââââââ
â                  â âââââââââââââââââââââââââââ[pass]âââââââââââââââââââââââ> â           â
â                  â             ââââââââââââââ                                â upstreams â
â                  â             â            â ââââââââââââ[proxy]ââââââââââ> â           â
â     listeners    â ââ[pass]ââ> â            â                                âââââââââââââ
â                  â             â            â              ââââââââââââââââââ
â                  â             â   routes   â ââ[share]ââ> â /files/on/disk â
â                  â             â            â              ââââââââââââââââââ
â                  â             â            â              ââââââââââââââââââ
â  ââââââââââââââ  â             â            â ââ[pass]âââ> â                â
â  âcertificatesâ  â             ââââââââââââââ              â  applications  â
â  ââââââââââââââ  â ââââââââââââââââ[pass]ââââââââââââââââ> â                â
â                  â                                         ââââââââââââââââââ
ââââââââââââââââââââ
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

### ð Build applications
 * Simplify microservices
 * Modernize monoliths

â¦
### ð Deploy to production
 * True end-to-end TLS
 * Isolate applications

---

# Get started with NGINX Unit

### ð§ Installation, configuration, and how-to **docs**
 * https://unit.nginx.org/

â¦
### ð§âð» Code, issues
 * https://github.com/nginx/unit

â¦
### ð¬ Community, discussion
 * https://community.nginx.org/joinslack
 * unit@nginx.org (https://mailman.nginx.org/)

---

# _fin_

### â¹ï¸ This presentation and demos at https://github.com/lcrilly/nginx-unit-demos

> In-terminal presentation by [lookatme](https://lookatme.readthedocs.io/en/latest/index.html)
>
> https://github.com/d0c-s4vage/lookatme
