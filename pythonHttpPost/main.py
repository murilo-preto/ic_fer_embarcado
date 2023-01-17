import requests

fex = 'happy'

r = requests.post(
    'http://localhost:3000/api/facialexpressions', json={"fex": fex})
print(r.status_code)

print(requests.get('http://localhost:3000/api/facialexpressions/').text)
