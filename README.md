# 5gcity-infrastructure-abstraction

5GCity-Infrastructure-Abstraction between Slice Manager and RAN Controllers (i2CAT RAN Controller &amp; Ruckus Controller)

## Installing RAN Proxy and its requirements

```sh
$ git clone https://github.com/5GCity/5GCity-infrastructure-abstraction.git
$ cd 5GCity-infrastructure-abstraction
$ pip3 install -r requirements.txt
```

## Setting the configuration

For setting the controllers use the file ``conf/config.py`` and set as follows:

```python
CONTROLLERS = [
    {
    'id': 0,
    'type': 'ruckus',
    'ip': '127.0.0.1',
    'port': 8080,
    'url': 'http://{}:{}/',
    'topology': RUCKUS_TOPOLOGY
    },
    {
    'id': 1,
    'type': 'i2cat',
    'ip': '84.88.34.20',
    'port': 8008,
    'url': 'http://{}:{}/' 
    }
]
```

## Running and stopping the proxy server

```sh
$ cd proxy/web/
$ bash init.sh start
Starting Agnostic Wireless Proxy......  OK
$ bash init.sh stop
Stopping Agnostic Wireless Proxy......  OK
```

## Restarting the proxy server

```sh
$ cd proxy/web/
$ bash init.sh restart
Stopping Agnostic Wireless Proxy......  OK
Starting Agnostic Wireless Proxy......  OK
```

## Checking the proxy server status

```sh
$ cd proxy/web/
$ bash init.sh status
Agnostic Wireless Proxy......  RUNNING
```
