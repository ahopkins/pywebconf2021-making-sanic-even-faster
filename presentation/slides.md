layout: true
class: typo, typo-selection

---

count: false
class: nord-dark, center, middle

.rect.height-35[
	.width-30[
		.center[
			![](assets/images/logo.png)
		]
	]
]

# Making .oc-pink-7[Sanic] Even *Faster*

#### What's in store for v21

Adam Hopkins
.left.font-sm[
```python
start = datetime(2021, 3, 24, 12, 0, 0, tzinfo=ZoneInfo(key="America/New_York"))
end = start + timedelta(minutes=45)
```
]
---

class: border-layout, nord-dark

.east.height-100.width-65.p-xxs.ml-m[
	.card.noborder.noround.m-0.width-100.height-100[
.font-sm[
```python
class Adam:

	def __init__(self):
		self.work = PacketFabric("Sr. Software Engineer")
		self.oss = Sanic("Core Maintainer")
		self.home = Israel("Negev")

	async def run(self, inputs: Union[Pretzels, Coffee]) -> None:
		while True:
			await self.work.do(inputs)
			await self.oss.do(inputs)
		
	def sleep(self):
		raise NotImplemented
```
]
.left[

- [PacketFabric](https://packetfabric.com/) - .font-sm[Network-as-a-Service platform; private access to the cloud; secure connectivity between data centers ]
- [Sanic Framework](https://sanicframework.org/) - .font-sm[ Python 3.7+ `asyncio` enabled framework and server. Build fast. Run fast. ]
- [GitHub - /ahopkins](https://github.com/ahopkins)
- [Twitter - @admhpkns](https://twitter/admhpkns)
		]
	]
]
.west.width-30[
	.pt-xxl.ml-xxl[
		.width-100[
			.center[
				.width-80[
					![](assets/images/profile.png)
				]
				.width-80[
					![](assets/images/packetfabric.png)
				]
				.width-80[
					![](assets/images/sanic.png)
				]
			]
		]
	]
]

???

PacketFabric’s Network-as-a-Service platform weaves together a perfect solution for networking. It provides private
access to the cloud, secure connectivity between data centers, an easy on ramp to the secure internet all coupled with
network automation. It's built for the way we do business today. Plus, we were just named one of the Top Ten Hottest
Networking Startups by CRN Magazine,

---

class: nord-dark

# What is .oc-pink-7[Sanic]?

--

##### Framework

```python
from sanic import Sanic, text

app = Sanic("My Hello, world app")

@app.get("/")
async def hello_world(request):
    return text("Hello, world.")
```

--

##### Web server .font-md.oc-yellow-7[(production ready)]

```bash
$ sanic server.app
$ python -m sanic server.app
$ python server.py
```


---

class: nord-dark, middle, center

| | Framework | Server | ASGI ready |
|:-|:-:|:-:|:-:|
| Django | ✅ | ⛔ | ⛔ |
| Flask | ✅ | ⛔ | ⛔ |
| Starlette | ✅ | ⛔ |✅ |
| Gunicorn | ⛔ | ✅ | ✔️ |
| Hypercorn | ⛔ | ✅ | ✅ |
| Nginx | ⛔ | ✅ | - |
| .oc-pink-7[Sanic] | ✅ | ✅ | ✅ |


---

class: nord-dark, center, middle

# Hot off the press!
.block-middle.width-80[
	![](/assets/images/pypi.png)
]

---

class: nord-dark

# Quick Overview

1. What's new in 21.3
   - A lot!
   - Optimized routing
   - Stream everything
   - Signals
2. .oc-pink-7[Why] these changes were made
2. .oc-pink-7[How] these changes were made

---

class: nord-dark, center, middle

.block-middle.width-60[
	![](/assets/images/benchmarks_lousy.jpg)
]

???

About to show you some benchmarks, hesitant because

1. People put too much stock in them
2. Highly susceptible to changes in environment
3. Contextual and subjective

But ...

**relational**


---

class: nord-dark

# How does .oc-pink-7[Sanic] 20.12 stack up?

.block-middle.width-80[
	![](/assets/images/chart_1.svg)
	.oc-gray-6[Higher is better]
]

???

*What are we looking at here?*

- two requests, one static one dynamic
- key take away is the dynamic requests tend to be a little slower

---

class: nord-dark

# ... and v21.3?

.block-middle.width-80[
	![](/assets/images/chart_2.svg)
	.oc-gray-6[Higher is better]
]

???

See the improvement

Focus of 2021 is on performance optimization

LTS at end of year to hit *STABLE* API
  - means different things to different people
  - to us, it means that ther API is not going to change dramatically

---

class: nord-dark

# Why is it faster?

???

Asyncio frameworks faster than counterparts
Why async enabled frameworks are faster

	io bound
	not cpu bound

NOT a magic bullet, and they can be made to dun slowly

But why is Sanic faster? And, how are we making it more fast?

--

## ... *.oc-gray-6[Efficiency]*

.block-middle.width-50[
	![](/assets/images/efficiency.jpg)
]

???

- better routing
- streaming all responses to make more streamlined response


---


class: nord-dark

# Router efficiency

.block-middle.width-80[
	![](/assets/images/chart_3.svg)
	.oc-gray-6[Lower is better]
]

---

class: nord-dark

# What is a router?

.column-2.pt-l.mr-s.ml-s[
	.block-middle.width-100[
		.font-xl[From this...]
.left.font-sm[
- `/login`
- `/profile/<username>`
- `/orders`
- `/orders/<order_id:int>`

	]

	]
	.block-middle.width-100[
	.font-xl[... to this ...]
.left.font-sm[
```python
def login(request): ...
def view_profile(request): ...
def view_all_orders(request): ...
def view_single_order(request): ...
```
]
	]
]
<br />
.font-xl[... using this:]

```bash
GET /v4 HTTP/1.1
Host: localhost:8181
User-Agent: curl/7.75.0
Accept: */*
```

???

Part of a framework that is in charge of fetching the right handler toi execute

all frameworks need on, and they are also applicable in other situations outside of HTTP requests

Static v dynamic routes

---

class: nord-dark

# .oc-gray-6[Old] .oc-pink-7[Sanic] Router 🕰️

From this:

```bash
/foo/<bar:int>/<fuzz:alpha>/<buzz:number>
```

To this:

```python
r"/foo/(-?\d+)/([A-Za-z]+)/(-?(?:\d+(?:\.\d*)?|\.\d+))"
```

???

Like Django... bottom looks like what you used to do in old Django

--

Using this:

```python
for route in routes:
	match = route.pattern.match(url)
	if match and method in route.methods:
		break
```

???

Highly inefficient
regex is slow
about 20 other issues with old router

---

class: nord-dark, middle, center

# There must be a better way 🤯

---

class: nord-dark

# Runtime optimized router 🆕

- AST style compiled
- Route matching does not exist *.oc-gray-6[until]* startup
- Analyze declared routes into a 🌲
- Build matching function using the 🌲

---

class: nord-dark

.font-xxs[
```vash
/a/much/longer/item/<id>
/a/much/<longer>/item/<id>
/a/thing/<id>
/a/thing/<id>/and/doit
/a/<banana>
/<foo>
/<foo>/bar
/<foo>/buzz
/<foo>/fuzz
/<foo:int>
```
]

???

We have a number of dynamic routes

Some similar parts of their path

Old style would convert these all to regex and loop through them

--

.font-xxs[
```vash
Node(level=0)
     Node(part=a, level=1)
         Node(part=much, level=2)
             Node(part=longer, level=3)
                 Node(part=item, level=4)
                     Node(part=<id>, level=5, route=<Route: /a/much/longer/item/<id>>, dynamic=True)
             Node(part=<longer>, level=3, dynamic=True)
                 Node(part=item, level=4)
                     Node(part=<id>, level=5, route=<Route: /a/much/<longer>/item/<id>>, dynamic=True)
         Node(part=thing, level=2)
             Node(part=<id>, level=3, route=<Route: /a/thing/<id>>, dynamic=True)
                 Node(part=and, level=4)
                     Node(part=doit, level=5, route=<Route: /a/thing/<id>/and/doit>)
         Node(part=<banana>, level=2, route=<Route: /a/<banana>>, dynamic=True)
     Node(part=<foo>, level=1, route=<Route: /<foo>>, dynamic=True)
         Node(part=bar, level=2, route=<Route: /<foo>/bar>)
         Node(part=buzz, level=2, route=<Route: /<foo>/buzz>)
         Node(part=fuzz, level=2, route=<Route: /<foo>/fuzz>)
     Node(part=<foo:int>, level=1, route=<Route: /<foo:int>>, dynamic=True)
```
]

---

class: nord-dark, middle

# Is this better?

v20.12

.font-sm[
```bash
-----------------------------------------------------------------------------------------
Name (time in ns)   Min               Max               Mean               StdDev        
-----------------------------------------------------------------------------------------
static_route        183.5220 (1.0)    260.4150 (1.0)    193.0517 (1.0)     6.9385 (1.0)  
dynamic_route       184.8240 (1.01)   590.3360 (2.27)   201.4882 (1.04)   30.8262 (4.44) 
-----------------------------------------------------------------------------------------
```
]

v21.3

.font-sm[
```bash
------------------------------------------------------------------------------------------
Name (time in ns)   Min               Max                Mean              StdDev         
------------------------------------------------------------------------------------------
static_route        104.7200 (1.0)    192.7400 (1.0)     109.5443 (1.0)    7.1217 (2.22)  
dynamic_route       117.8700 (1.13)   193.0490 (1.00)    126.3849 (1.15)   3.2035 (1.0)   
------------------------------------------------------------------------------------------
```
]

???

Talk about approach to adding features

-- go to sidetrack

Compare means, stddev

Best part is no more wild swings. It is much more consistent than regex matching

---

class: nord-dark

# *.oc-yellow-6[SIDETRACK]*

.font-sm[
```python
def if_else(path):
    parts = path.split("/")
    if parts[0] == "":
        if parts[1] == "foo":
            if len(parts) == 2:
                return ROUTES[(parts[0], parts[1], None)]
    return False

def and_parts(path):
    parts = path.split("/")
    if parts[0] == "" and parts[1] == "foo" and len(parts) == 2:
        return ROUTES[(parts[0], parts[1], None)]
    return False

def path_grab(path):
    parts = path.split("/")
    return ROUTES[(parts[0], parts[1], None)]
```
]

???

Benchmarking can be good

Building out router and there are three different ways to get the same result

Which one is fastest? Enter timy

---

class: nord-dark

# *.oc-yellow-6[SIDETRACK]*

.font-sm[
```python

@timy.timer(loops=LOOPS)
def do_if_else():
    if_else(PATH)

@timy.timer(loops=LOOPS)
def do_and_parts():
    and_parts(PATH)

@timy.timer(loops=LOOPS)
def do_path_grab():
    path_grab(PATH)

do_if_else()
do_and_parts()
do_path_grab()
```
]

---

class: nord-dark

# *.oc-yellow-6[SIDETRACK]*

```q
Timy executed (do_if_else) for 500000 times in 0.254344 seconds
Timy best time was 0.000000 seconds
*Timy executed (do_and_parts) for 500000 times in 0.196365 seconds
Timy best time was 0.000000 seconds
Timy executed (do_path_grab) for 500000 times in 0.221170 seconds
Timy best time was 0.000000 seconds
```

---

class: nord-dark, middle

```python
compiled_src = compile(find_route_src, "", "exec")
ctx = {}
exec(compiled_src, None, ctx)
find_route = ctx["find_route"]
```

---

class: nord-dark, middle

```python
*compiled_src = compile(find_route_src, "", "exec")
ctx = {}
exec(compiled_src, None, ctx)
find_route = ctx["find_route"]
```

---

class: nord-dark, middle

```python
compile(src, filename, mode)
```

- `src`: the source that will be compiled, `str`, `bytes`, or AST object
- `filename`: from where source came from
- `mode`:
  - `"eval"`: single expression
  - `"exec"`: .oc-bg-yellow-4[.oc-gray-7[block of statements]]
  - `"single"`: single interactive statement

---

class: nord-dark, middle

```python
src = [
    Line("def find_route(path, router, basket, extra):", 0),
    Line("parts = tuple(path[1:].split(router.delimiter))", 1),
    Line("try:", 1),
    Line("route = router.static_routes[parts]", 2),
    Line("basket['__raw_path__'] = path", 2),
    Line("return route, basket", 2),
    Line("except KeyError:", 1),
    Line("pass", 2),
]
```

???

How do we generate the source? 

Remember compile is running at startup time.

---

class: nord-dark, middle

```python
def find_route(path, router, basket, extra):
	parts = tuple(path[1:].split(router.delimiter))
	try:
		route = router.static_routes[parts]
		basket['__raw_path__'] = path
		return route, basket
	except KeyError:
		pass
```

--

```python
find_route_src = """<see above>"""
```

???

Remember, at this point this is JUST text

---

class: nord-dark, middle

```python
compiled_src = compile(find_route_src, "", "exec")
ctx = {}
*exec(compiled_src, None, ctx)
find_route = ctx["find_route"]
```

???

compiled source code does us no good.

Those `.pyc` files don't do anything on your computer. You need the the Python
interpreter to run them.

That is what exec does.

`exec` performs dynamic execution of a code object

---

class: nord-dark, middle

```python
exec(object[, globals[, locals]])
```

- `object`: the code object to be executed
- `globals`: the global context to be applied, ie `globals()`
- `locals`: the local context to be applied, ie `locals()`

???

`globals()` and `locals()` provide all the variables in that scope

This is SUPER handy for us because if we pass in an object, any local variables in that scope will be bound to it

---

class: nord-dark, middle

```python
compiled_src = compile(find_route_src, "", "exec")
ctx = {}
*exec(compiled_src, None, ctx)
find_route = ctx["find_route"]
```

```python
def find_route(path, router, basket, extra):
	...

find_route(...)
```

---

class: nord-dark, center, middle

.block-middle.width-80[
	![](/assets/images/mindblown.webp)
]

???

Mindblowing stuff, opens huge possibilities

We just:

	1. ran some Python script
	2. that wrote some Python code
	3. compiled it
	4. executed it
	5. and spit out a new function that can be called

Self-writing code

you need try it

---

class: nord-dark

# Potential applications in .oc-pink-7[Sanic]

- 🚀 Optimizing request/response cycle
- 🕵 Minimizing middleware lookups
- 🧮 Streamlining HTTP and WS response logic
- 💡 Smarter error response handling
- 🔮 Predictive caching

???

In Sanic we built a router, but what else?

v21.3 proved this as a viable concept

Plan to expand upon this in 2021 to other areas 

=========

Touch ever part of the cycle
We know what middleware runs on what route at startup, so why not figure it out early
Lots of logic that can be compartmentalized and not sharing same factories/funcitons
error response handling
help dev cache (and prebuild) responses

---

class: nord-dark, middle

```python

@app.post("/login")
def login(request):
	...

@app.get("/profile/<username>")
def view_profile(request):
	...

@app.get("/orders")
def view_all_orders(request):
	...

@app.get("/orders/<order_id:int>")
def view_single_order(request):
	...

@app.put("/orders/<order_id:int>")
def update_single_order(request):
	...
```

---

class: nord-dark, middle, .font-sm
.column-2.pt-l.mr-s.ml-s[
	.block-middle.width-100[
Static routes
- `/login`
  - `POST` handler
- `/orders`
  - `GET` handler<br /><br />
	]
	.block-middle.width-100[
Dynamic routes
- `/profile/<username>`
  - `GET` handler
- `/orders/<order_id:int>`
  - `GET` handler
  - `PUT` handler
	]
]

---

class: nord-dark, middle, font-xxs

```python
def find_route(path, router, basket, extra):
    parts = tuple(path[1:].split(router.delimiter))
    try:
        route = router.static_routes[parts]
        basket['__raw_path__'] = path
        return route, basket
    except KeyError:
        pass
    num = len(parts)
    if num > 0:
        if parts[0] == "orders":
            if num == 2:
                basket[1] = parts[1]
                try:
                    basket['__params__']['order_id'] = int(basket[1])
                except ValueError:
                    ...
                else:
                    basket['__raw_path__'] = 'orders/<order_id:int>'
                    return router.dynamic_routes[('orders', '<order_id:int>')], basket
            raise NotFound
        elif parts[0] == "profile":
            if num == 2:
                basket[1] = parts[1]
                try:
                    basket['__params__']['username'] = str(basket[1])
                except ValueError:
                    ...
                else:
                    basket['__raw_path__'] = 'profile/<username>'
                    return router.dynamic_routes[('profile', '<username>')], basket
            raise NotFound
        raise NotFound
    raise NotFound

```

???

As you can see our original example super simple

The runtime built router allows us to have as great the level of complexity that we need for the applicaiton, but no more.

It is a shame to penalize simple apps for the edge case complex apps.

==========

Router is done

We have our handler

---

class: nord-dark

# Stream *.oc-gray-6[EVERYTHING]* 🌀

- Unify **all** response types:
  - .font-sm[`text()`, `json()`, `html()`, `file()`, `stream()`, `file_stream()`]
- Lighten the path to HTTP/2 server push
- Remove callbacks
- Side benefit: *.oc-gray-6[SPEED]*

???

Correct an API quirk

working on HTTP2 for a while, but every implementation struggled to maintain
- backwards compat
- speed
- complexity



---

class: nord-dark

# .oc-gray-6[Old] .oc-pink-7[Sanic] Request/Response 🕰️

```python
handler = router.get(request)
response = await handler(request)
*if stream_callback:
	await stream_callback(response)
else:
	write_callback(response)
```

???

This divergence is what we no longer are doing in 21.3

---

class: nord-dark, middle

```python
@app.route("/")
async def index(request):
    async def stream_from_db(response):
        conn = await asyncpg.connect(database='test')
        async with conn.transaction():
            async for record in conn.cursor('SELECT generate_series(0, 10)'):
                await response.write(record[0])

    return stream(stream_from_db)
```

???

Old style, return function that passes another function
Confusing, not obvious to beginners, and shouldn't be a part of asyncio
should be able to yield to the loop whenever we want

--

```python
@app.route("/")
async def test(request):
    response = await request.respond(content_type="text/csv")
    await response.send("foo,")
    await response.send("bar")
    await response.send("", True)
    return response

```



---

class: nord-dark,font-xxs

### Version 20.12

```bash
Running 30s test @ http://127.0.0.1:3333
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     4.48ms    5.95ms 131.35ms   91.06%
    Req/Sec    10.21k     1.94k   56.63k    76.23%
  3659132 requests in 30.09s, 411.78MB read
*Requests/sec: 121614.26
Transfer/sec:     13.69MB
```

### With new streaming internals

```bash
Running 30s test @ http://127.0.0.1:3333
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     3.81ms    4.55ms 107.27ms   90.82%
    Req/Sec    11.22k     2.29k   36.57k    74.27%
  4014399 requests in 30.09s, 394.33MB read
*Requests/sec: 133394.06
Transfer/sec:     13.10MB
```


### With new AST router

```bash
Running 30s test @ http://127.0.0.1:3333
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     3.74ms    4.60ms 102.41ms   90.73%
    Req/Sec    11.60k     2.61k   46.51k    75.23%
  4148337 requests in 30.08s, 407.48MB read
*Requests/sec: 137923.77
Transfer/sec:     13.55MB
```

---

class: nord-dark

# Introducing signals 🆕

```python
@app.signal("foo.bar.baz")
async def handler():
	...
```

- Convenient method to push work to the event loop
- Can be dispatched from anywhere in your application 🌐
- Familiar API resembling route handlers 👋
- *.oc-gray-6[BETA]* in 21.3 🎉
  - Intended to replace listeners and middleware in future
- Built using the new router

---

class: nord-dark, middle

### Dispatch with context

```python
@app.signal("user.registration.created")
async def send_registration_email(context):
    await send_email(context["email"], template="registration")

@app.post("/register")
async def handle_registration(request):
    await do_registration(request)

    await request.app.dispatch(
        "user.registration.created",
        context={"email": request.json.email}
    )
	return redirect(request.app.url_for("profile"))
```

---

class: nord-dark, middle

### Dynamic paths

```python
@app.signal("foo.bar.<thing>")
async def signal_handler(thing):
    print(f"[signal_handler] {thing=}")

@app.post("/trigger")
async def trigger(request):
    await app.dispatch("foo.bar.baz")
    return text("Done.")
```

---

class: nord-dark, middle

### Internal messaging

```python
@app.signal("do.something.expensive")
async def signal_handler(thing):
    await do_something()
	await app.dispatch("do.something.complete")

@app.post("/trigger")
async def trigger(request):
    await app.dispatch("do.something.expensive")

*   await app.event("do.something.complete")

    return text("Done.")
``` 


---

class: nord-dark

# What else?

- NEW docs 🎆
- Drop Python 3.6
- Expanded and consistent route naming
- New convenience decorators
- Alterable route `match_info`
- New version types allowd in routes (int, float, str)
- App, Blueprint, and Blueprint group parity
- Removed testing client to standalone package
- .oc-bg-yellow-6.oc-gray-8[Application and connection level context objects]

---

class: nord-dark, middle, center

# Questions?

GitHub - [/ahopkins]()<br />
Twitter - [@admhpkns]()<br />
PacketFabric - [packetfabric.com](https://packetfabric.com/)<br />
.oc-pink-7[Sanic] homepage - [sanicframework.org](https://sanicframework.org)<br />
.oc-pink-7[Sanic] repo - [/sanic-org/sanic](https://github.com/sanic-org/sanic)
