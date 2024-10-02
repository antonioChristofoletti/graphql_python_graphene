from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base, Employer, Job, JobApplication, User

from app.config.config import DB_URL
from app.db.data import employers_data, jobs_data, users_data, job_applications


engine = create_engine(DB_URL)

Session = sessionmaker(bind=engine)


def prepare_database():
    from app.utils import hash_password
    
    Base.metadata.drop_all(engine)

    Base.metadata.create_all(engine)

    session = Session()

    for employer in employers_data:
        emp = Employer(**employer)
        session.add(emp)

    for job in jobs_data:
        session.add(Job(**job))

    for u in users_data:
        u["password_hash"] = hash_password(u["password"])

        del u["password"]

        session.add(User(**u))

    for ja in job_applications:
        session.add(JobApplication(**ja))

    session.commit()
