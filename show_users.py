import asyncio, asyncpg

async def show():
    conn = await asyncpg.connect('postgresql://postgres:harihyma@127.0.0.1/logistics_db')
    rows = await conn.fetch('''
        SELECT u.email, u.name, u.role, u.status, c.name as company
        FROM users u
        LEFT JOIN companies c ON u.company_id = c.id
        ORDER BY c.name, u.role, u.email
    ''')
    current_company = None
    for r in rows:
        if r['company'] != current_company:
            current_company = r['company']
            print(f"\n Company: {current_company}")
            print("-" * 55)
        print(f"  {r['email']:<35} {r['role']:<8} {r['status']}")
    await conn.close()

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(show())
