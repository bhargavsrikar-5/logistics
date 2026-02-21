import urllib.request, urllib.parse, json

API = 'http://127.0.0.1:8000'

def login(email, pw):
    data = urllib.parse.urlencode({'username': email, 'password': pw}).encode()
    return json.loads(urllib.request.urlopen(urllib.request.Request(API+'/token', data=data)).read())['access_token']

def post(url, data, token):
    body = json.dumps(data).encode()
    req = urllib.request.Request(API+url, data=body,
        headers={'Content-Type':'application/json','Authorization': 'Bearer '+token})
    try:
        resp = urllib.request.urlopen(req)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def get(url, token):
    req = urllib.request.Request(API+url, headers={'Authorization': 'Bearer '+token})
    return json.loads(urllib.request.urlopen(req).read())

tok = login('admin@example.com', 'password123')
s, r = post('/admin/create-user', {
    'name': 'Test MSME User',
    'email': 'testmsme_verify@demo.com',
    'password': 'pass123',
    'role': 'MSME'
}, tok)
print('Create MSME via admin: status=' + str(s) + ' email=' + str(r.get('email')) + ' role=' + str(r.get('role')) + ' status_field=' + str(r.get('status')))

users = get('/users', tok)
print('Demo company active users: ' + str(len(users)))
for u in users:
    print('  ' + u['email'] + ' - ' + u['role'])
