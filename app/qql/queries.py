from graphene import List, ObjectType, Field, Int

from app.db.database import Session
from app.db.models import Employer, Job, JobApplication, User
from app.qql.types import EmployerObject, JobApplicationObject, JobObject, UserObject


class Query(ObjectType):
    jobs = List(JobObject)
    job = Field(JobObject, id=Int(required=True))
    employers = List(EmployerObject)
    employer = Field(EmployerObject, id=Int(required=True))
    users = List(UserObject)
    job_applications = List(JobApplicationObject)

    @staticmethod
    def resolve_job(root, info, id):
        with Session() as session:
            job = session.query(Job).filter(Job.id == id).first()
            return job

    @staticmethod
    def resolve_employer(root, info, id):
        with Session() as session:
            e = session.query(Employer).filter(Employer.id == id).first()
            return e

    @staticmethod
    def resolve_jobs(root, info):
        with Session() as session:
            return session.query(Job).all()

    @staticmethod
    def resolve_employers(root, info):
        with Session() as session:
            return session.query(Employer).all()

    @staticmethod
    def resolve_users(root, info):
        with Session() as session:
            return session.query(User).all()
        
    @staticmethod
    def resolve_job_applications(root, info):
        with Session() as session:
            return session.query(JobApplication).all()
