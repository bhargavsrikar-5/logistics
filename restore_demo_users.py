import asyncio, sys, os
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from models import User, UserRole, UserStatus, Company
from auth import get_password_hash
from database import DATABASE_URL

engine = create_async_engine(DATABASE_URL)
AsyncSession_ = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def restore():
    async with AsyncSession_() as db:
        # Create Demo Logistics Co. again
        existing_co = await db.execute(select(Company).where(Company.name == 'Demo Logistics Co.'))
        company = existing_co.scalars().first()
        if not company:
            company = Company(name='Demo Logistics Co.', description='Default demo company')
            db.add(company)
            await db.flush()
            print(f'Created Demo Logistics Co. id={company.id}')

        # Restore 3 users
        users = [
            {'email': 'admin@example.com',  'name': 'System Admin',       'role': UserRole.ADMIN,  'password': 'password123'},
            {'email': 'msme@example.com',   'name': 'MSME Business User', 'role': UserRole.MSME,   'password': 'password123'},
            {'email': 'driver@example.com', 'name': 'Driver Raj',         'role': UserRole.DRIVER, 'password': 'password123',
             'phone': '9876543210', 'license': 'DL-KA01-2023001'},
        ]
        for u in users:
            ex = await db.execute(select(User).where(User.email == u['email']))
            if not ex.scalars().first():
                new_user = User(
                    email=u['email'],
                    name=u['name'],
                    role=u['role'],
                    status=UserStatus.ACTIVE,
                    hashed_password=get_password_hash(u['password']),
                    company_id=company.id,
                    phone=u.get('phone'),
                    license_number=u.get('license'),
                )
                db.add(new_user)
                print(f"Restored: {u['email']}")

        await db.commit()
        print('Done.')

        # Show all users
        all_users = await db.execute(select(User))
        print('\nAll users in DB:')
        for u in all_users.scalars().all():
            print(f'  {u.email} | {u.role} | company_id={u.company_id}')

asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
asyncio.run(restore())
