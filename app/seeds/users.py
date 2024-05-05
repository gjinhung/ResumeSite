from app.models import db, User, Resume, Section, Detail, Company, environment, SCHEMA
from sqlalchemy.sql import text
import datetime


# Adds a demo user, you can add other users here if you want
def seed_users():
    demo = User(
        username="Demo",
        email="demo@aa.io",
        password="password",
        first_name="Dem",
        last_name="Moe",
        joined_on=datetime.datetime.now(),
        profile_pic="https://publichealth.uga.edu/wp-content/uploads/2020/01/Thomas-Cameron_Student_Profile.jpg",
        phone="123-456-7890",
        location="New Jersey",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    marnie = User(
        username="marnie",
        email="marnie@aa.io",
        password="password",
        first_name="Mar",
        last_name="Nie",
        joined_on=datetime.datetime.now(),
        profile_pic="https://publichealth.uga.edu/wp-content/uploads/2020/01/Thomas-Cameron_Student_Profile.jpg",
        phone="123-456-7890",
        location="New Jersey",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    bobbie = User(
        username="bobbie",
        email="bobbie@aa.io",
        password="password",
        first_name="Bob",
        last_name="Bee",
        joined_on=datetime.datetime.now(),
        profile_pic="https://publichealth.uga.edu/wp-content/uploads/2020/01/Thomas-Cameron_Student_Profile.jpg",
        phone="123-456-7890",
        location="New Jersey",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    resume1 = Resume(
        user_id=1,
        name="Resume 1",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    projects = Section(
        title="Projects",
        resume=resume1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    experience = Section(
        title="Experience",
        resume=resume1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )
    education = Section(
        title="Education",
        resume=resume1,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    yelping = Company(
        organization="Yelping",
        title="Flask/React fullstack clone of Yelp with search, Google Maps, 3 CRUD features, and full user auth",
        user_id=1,
        section=projects,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    cityra = Company(
        organization="CityRa",
        title="Flask/React fullstack website for students to host tours with search, 3 CRUD and full user auth",
        user_id=1,
        section=projects,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    plumbing = Company(
        organization="LAB Plumbing",
        title="Apprentice",
        user_id=1,
        section=experience,
        start_date="August 2020",
        end_date="Present",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    analyst = Company(
        organization='Mayor"s Office of Criminal Justice',
        title="Budget Analyst",
        user_id=1,
        section=experience,
        start_date="July 2017",
        end_date="August 2020",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    aa = Company(
        organization="App Academy",
        title="Part-Time Student",
        user_id=1,
        section=education,
        start_date="December 2023",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    marist = Company(
        organization="Marist College",
        title="Student",
        user_id=1,
        section=education,
        start_date="August 2010",
        end_date="May 2014",
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    detail1 = Detail(
        description="Collaborated with two other developers using GitHub to manage code and collaborate on features",
        company=yelping,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    detail2 = Detail(
        description="Created a booking system using SQLAlchemy to set up a relational database to create, delete and update tour specific bookings",
        company=cityra,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    detail3 = Detail(
        description="Used critical thinking skills to troubleshoot and resolve complex issues when installing plumbing pipes and fixtures while both satisfying client's request at a timely manner and complying with New York plumbing code",
        company=plumbing,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    detail4 = Detail(
        description="Create and manage offline budget to actual report for MOCJ’s budget of over $400 million and used projections to help MOCJ predict potential surpluses/deficits to help plan for future programs",
        company=analyst,
        created_at=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )

    db.session.add_all(
        [
            demo,
            marnie,
            bobbie,
            resume1,
            projects,
            experience,
            education,
            yelping,
            cityra,
            plumbing,
            aa,
            analyst,
            marist,
            detail1,
            detail3,
            detail2,
            detail4,
        ]
    )
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
