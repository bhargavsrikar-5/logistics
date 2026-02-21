import os

files_to_fix = {
    r'frontend\src\components\CreateDeliveryModal.jsx': [
        ("user?.role === 'SUPER_ADMIN'", "user?.role === 'ADMIN'"),
    ],
    r'frontend\src\components\EditDeliveryModal.jsx': [
        ("user?.role === 'SUPER_ADMIN'", "user?.role === 'ADMIN'"),
    ],
    r'frontend\src\pages\FleetDashboard.jsx': [
        ("user?.role === 'FLEET_MANAGER' ? '/fleet' : '/admin'", "'/admin'"),
    ],
}

for filepath, replacements in files_to_fix.items():
    if not os.path.exists(filepath):
        print(f'MISSING: {filepath}')
        continue
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    for old, new in replacements:
        content = content.replace(old, new)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'Fixed: {filepath}')

print('All done!')
