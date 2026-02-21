import urllib.request, urllib.parse, json

API = 'http://127.0.0.1:8000'

def login(email, password):
    data = urllib.parse.urlencode({'username': email, 'password': password}).encode()
    req = urllib.request.Request(API + '/token', data=data)
    return json.loads(urllib.request.urlopen(req).read())['access_token']

def get(url, token):
    req = urllib.request.Request(API + url, headers={'Authorization': f'Bearer {token}'})
    return json.loads(urllib.request.urlopen(req).read())

# Test isolation: Demo admin vs Test Corp admin
demo_token = login('admin@example.com', 'password123')
test_token = login('testadmin@testcorp.com', 'password123')

demo_users = get('/users', demo_token)
test_users = get('/users', test_token)

demo_emails = [u['email'] for u in demo_users]
test_emails = [u['email'] for u in test_users]

print('=== Demo Logistics Co. Admin sees: ===')
for e in demo_emails:
    print(' ', e)

print('\n=== Test Corp India Admin sees: ===')
for e in test_emails:
    print(' ', e)

# Cross-contamination check
cross = set(demo_emails) & set(test_emails)
if cross:
    print(f'\n❌ ISOLATION FAILED - both see: {cross}')
else:
    print('\n✅ ISOLATION CONFIRMED - zero overlap between companies!')

# Check vehicles
demo_vehicles = get('/vehicles', demo_token)
test_vehicles = get('/vehicles', test_token)
print(f'\nDemo company vehicles: {[v["name"] for v in demo_vehicles]}')
print(f'Test Corp vehicles: {[v["name"] for v in test_vehicles]} (should be empty)')
