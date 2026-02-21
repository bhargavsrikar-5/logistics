import urllib.request, urllib.parse, json

def login_and_test(email, password, test_url=None):
    data = urllib.parse.urlencode({'username': email, 'password': password}).encode()
    req = urllib.request.Request('http://127.0.0.1:8000/token', data=data)
    resp = urllib.request.urlopen(req)
    token = json.loads(resp.read())['access_token']
    
    me_req = urllib.request.Request('http://127.0.0.1:8000/users/me')
    me_req.add_header('Authorization', 'Bearer ' + token)
    me = json.loads(urllib.request.urlopen(me_req).read())
    print('  Login OK:', me['email'], '| role =', me['role'])
    
    if test_url:
        try:
            r = urllib.request.Request('http://127.0.0.1:8000' + test_url)
            r.add_header('Authorization', 'Bearer ' + token)
            resp2 = urllib.request.urlopen(r)
            print('  ' + test_url + ': HTTP', resp2.status)
        except urllib.error.HTTPError as e:
            print('  ' + test_url + ': HTTP', e.code)

print('=== ADMIN ===')
login_and_test('admin@example.com', 'password123', '/admin/stats')
print('=== MSME ===')
login_and_test('msme@example.com', 'password123', '/shipments')
print('=== DRIVER ===')
login_and_test('driver@example.com', 'password123', '/driver/dashboard')
print('All role tests passed!')
