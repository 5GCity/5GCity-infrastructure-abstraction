# Testing using curl command

### List tenants

```bash
curl -H "Content-Type: application/json" -X GET -d '{}' http://127.0.0.1:8080/{}
```

### Adding tenant 

```bash
curl -H "Content-Type: application/json" -X POST -d '{}' http://127.0.0.1:8080/{}
```

### Removing tenant 

```bash
curl -H "Content-Type: application/json" -X DELETE -d '{}' http://127.0.0.1:8080/{}
```

### Modifing tenant configuration

```bash
curl -H "Content-Type: application/json" -X PATCH -d '{}' http://127.0.0.1:8080/{}
```

### Python Example for adding a new tenant
```python
import json, requests

url = 'http://127.0.0.1:8080/{}'

data = {
    "token": "JCS39VlJ3ELIez2KBMMzS29YsYUdnrOWu"
}

resp = requests.post(url=url, json=data)
data = json.loads(resp.text)

print data

```