import asyncio, asyncpg

async def fix():
    conn = await asyncpg.connect('postgresql://postgres:harihyma@127.0.0.1/logistics_db')
    
    # Get old company id
    old_co = await conn.fetchrow("SELECT id FROM companies WHERE name = 'Demo Logistics Co.'")
    if old_co:
        old_id = old_co['id']
        await conn.execute("UPDATE zones SET company_id = NULL WHERE company_id = $1", old_id)
        await conn.execute("UPDATE vehicles SET company_id = NULL WHERE company_id = $1", old_id)
        await conn.execute("DELETE FROM companies WHERE id = $1", old_id)
        print("Demo Logistics Co. removed.")
    else:
        print("Demo Logistics Co. not found (already removed).")
    
    remaining = await conn.fetch('SELECT email, role FROM users ORDER BY id')
    print('Remaining users:')
    for r in remaining:
        print(f"  {r['email']} - {r['role']}")
    
    cos = await conn.fetch('SELECT name FROM companies')
    print('Companies:', [c['name'] for c in cos])
    await conn.close()

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(fix())
