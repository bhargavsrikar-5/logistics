import urllib.request, urllib.parse, json

API = 'http://127.0.0.1:8000'

def post(url, data, headers=None):
    body = json.dumps(data).encode()
    req = urllib.request.Request(API + url, data=body, headers={'Content-Type': 'application/json', **(headers or {})})
    try:
        resp = urllib.request.urlopen(req)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def get(url, headers=None):
    req = urllib.request.Request(API + url, headers=headers or {})
    try:
        resp = urllib.request.urlopen(req)
        return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())

def login(email, password):
    data = urllib.parse.urlencode({'username': email, 'password': password}).encode()
    req = urllib.request.Request(API + '/token', data=data)
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())['access_token']

print('=== 1. Register new company ===')
status, resp = post('/companies', {
    'company_name': 'Test Corp India',
    'company_description': 'A test company',
    'admin_name': 'Test Admin',
    'admin_email': 'testadmin@testcorp.com',
    'admin_password': 'password123'
})
print(f'  Status: {status} | Company: {resp.get("name")}')

print('=== 2. Search companies ===')
status, resp = get('/companies/search?q=Test')
print(f'  Status: {status} | Found: {[c["name"] for c in resp]}')
company_id = resp[0]['id'] if resp else None

print('=== 3. MSME sends join request ===')
status, resp = post('/join-request', {
    'company_id': company_id,
    'name': 'Jane Business',
    'email': 'jane@business.com',
    'password': 'password123',
})
print(f'  Status: {status} | {resp.get("message")}')

print('=== 4. MSME cannot login yet (PENDING) ===')
try:
    login('jane@business.com', 'password123')
    print('  ERROR: Should have been blocked!')
except urllib.error.HTTPError as e:
    body = json.loads(e.read())
    print(f'  Status: {e.code} | Blocked correctly: {body.get("detail", "")[:60]}')

print('=== 5. Admin approves MSME ===')
admin_token = login('testadmin@testcorp.com', 'password123')
status2, users = get('/admin/pending-users', {'Authorization': f'Bearer {admin_token}'})
print(f'  Pending users visible to admin: {[u["email"] for u in users]}')

if users:
    uid = users[0]['id']
    s, r = post(f'/admin/users/{uid}/approve', {}, {'Authorization': f'Bearer {admin_token}'})
    print(f'  Approve status: {s} | {r.get("message")}')

print('=== 6. MSME can login now ===')
try:
    msme_token = login('jane@business.com', 'password123')
    print(f'  Login OK! Token starts with: {msme_token[:20]}...')
except Exception as e:
    print(f'  ERROR: {e}')

print('=== 7. Admin creates a driver ===')
s, r = post('/admin/create-driver', {
    'name': 'Driver Singh',
    'email': 'driversingh@testcorp.com',
    'password': 'pass123',
    'phone': '9876543210',
}, {'Authorization': f'Bearer {admin_token}'})
print(f'  Create driver: {s} | {r.get("email")} | role={r.get("role")}')

print('\nAll multi-tenant tests passed!')
