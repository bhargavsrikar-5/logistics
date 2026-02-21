with open(r'backend\main.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

keywords = ['list_vehicles', 'list_zones', 'get_analytics', 'async def analytics',
            'async def get_vehicles', 'async def get_zones', '/vehicles', '/zones', '/analytics',
            'async def read_users', 'update_vehicle', 'create_vehicle']
for i, line in enumerate(lines):
    if any(k in line for k in keywords):
        print(f'{i+1}: {line.rstrip()}')
