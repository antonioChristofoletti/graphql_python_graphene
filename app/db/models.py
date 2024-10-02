from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class Employer(Base):
    __tablename__ = "employers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    contact_email = Column(String)
    industry = Column(String)
    jobs = relationship("Job", back_populates="employer", lazy="joined", join_depth=3)


class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    employer_id = Column(Integer, ForeignKey("employers.id"))
    employer = relationship(
        "Employer", back_populates="jobs", lazy="joined", join_depth=2
    )
    applications = relationship(
        "JobApplication", back_populates="job", lazy="joined", join_depth=2
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(String)
    role = Column(String)
    applications = relationship("JobApplication", back_populates="user", lazy="joined", join_depth=2)


class JobApplication(Base):
    __tablename__ = "job_applications"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    job_id = Column(Integer, ForeignKey("jobs.id"))
    user = relationship("User", lazy="joined", join_depth=2)
    job = relationship("Job", lazy="joined", join_depth=2)
