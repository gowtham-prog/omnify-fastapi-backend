# app/seed.py
import asyncio
from datetime import datetime, timedelta
from app.db import AsyncSessionLocal, engine, Base
from app.models import Event, Attendee
from sqlalchemy import text

async def seed():
    async with AsyncSessionLocal() as session:
        # Clear existing data
        await session.execute(text("DELETE FROM attendees"))
        await session.execute(text("DELETE FROM events"))

        # Create sample events
        now = datetime.utcnow()
        event1 = Event(
            name="Tech Conference 2025",
            location="Bangalore",
            start_time=now + timedelta(days=3),
            end_time=now + timedelta(days=3, hours=8),
            max_capacity=100
        )
        event2 = Event(
            name="Startup Meetup",
            location="Mumbai",
            start_time=now + timedelta(days=7),
            end_time=now + timedelta(days=7, hours=6),
            max_capacity=50
        )

        session.add_all([event1, event2])
        await session.flush()  # Get IDs

        # Add some attendees
        attendees = [
            Attendee(name="Alice", email="alice@example.com", event_id=event1.id),
            Attendee(name="Bob", email="bob@example.com", event_id=event1.id),
            Attendee(name="Charlie", email="charlie@example.com", event_id=event2.id),
        ]
        session.add_all(attendees)

        await session.commit()
        print("✅ Test data inserted successfully!")

async def main():
    async with engine.begin() as conn:
        # Make sure tables exist
        await conn.run_sync(Base.metadata.create_all)
    await seed()

if __name__ == "__main__":
    asyncio.run(main())
