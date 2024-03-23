from app.models import db, User, Resume, Section, Detail, Company, environment, SCHEMA
from sqlalchemy.sql import text


# Adds a demo user, you can add other users here if you want
def seed_users():
    demo = User(username="Demo", email="demo@aa.io", password="password")
    marnie = User(username="marnie", email="marnie@aa.io", password="password")
    bobbie = User(username="bobbie", email="bobbie@aa.io", password="password")

    resume1 = Resume(user_id=1)

    projects = Section(title="Projects", resume=resume1)
    experience = Section(title="Experience", resume=resume1)
    education = Section(title="Education", resume=resume1)

    yelping = Company(
        organization="Yelping",
        title="Flask/React fullstack clone of Yelp with search, Google Maps, 3 CRUD features, and full user auth",
        user_id=1,
        section=projects,
    )

    cityra = Company(
        organization="CityRa",
        title="Flask/React fullstack website for students to host tours with search, 3 CRUD and full user auth",
        user_id=1,
        section=projects,
    )

    plumbing = Company(
        organization="LAB Plumbing",
        title="Apprentice",
        user_id=1,
        section=experience,
        start_date="August 2020",
        end_date="Present",
    )

    analyst = Company(
        organization='Mayor"s Office of Criminal Justice',
        title="Budget Analyst",
        user_id=1,
        section=experience,
        start_date="July 2017",
        end_date="August 2020",
    )

    aa = Company(
        organization="App Academy",
        title="Part-Time Student",
        user_id=1,
        section=education,
        start_date="December 2023",
    )

    marist = Company(
        organization="Marist College",
        title="Student",
        user_id=1,
        section=education,
        start_date="August 2010",
        end_date="May 2014",
    )

    db.session.add(demo)
    db.session.add(marnie)
    db.session.add(bobbie)
    db.session.commit()


# Uses a raw SQL query to TRUNCATE or DELETE the users table. SQLAlchemy doesn't
# have a built in function to do this. With postgres in production TRUNCATE
# removes all the data from the table, and RESET IDENTITY resets the auto
# incrementing primary key, CASCADE deletes any dependent entities.  With
# sqlite3 in development you need to instead use DELETE to remove all data and
# it will reset the primary keys for you as well.
def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))

    db.session.commit()
