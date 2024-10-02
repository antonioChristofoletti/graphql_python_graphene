from graphene import Boolean, Field, Int, Mutation, String
from graphql import GraphQLError
from app.qql.types import JobApplicationObject, JobObject
from app.db.database import Session
from app.db.models import Job, JobApplication, User
from app.utils import is_admin


class AddJob(Mutation):
    class Arguments:
        title = String(required=True)
        description = String(required=True)
        employer_id = Int(required=True)

    job = Field(lambda: JobObject)

    @is_admin
    def mutate(root, info, title, description, employer_id):
        job = Job(title=title, description=description, employer_id=employer_id)
        session = Session()
        session.add(job)
        session.commit()
        session.refresh(job)
        return AddJob(job=job)


class UpdateJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        title = String()
        description = String()
        employer_id = Int()

    job = Field(lambda: JobObject)

    @is_admin
    def mutate(root, info, job_id, title=None, description=None, employer_id=None):
        session = Session()

        job = session.query(Job).filter(Job.id == job_id).first()

        if not job:
            raise Exception("Job not found")

        if title is not None:
            job.title = title

        if description is not None:
            job.description = description

        if employer_id is not None:
            job.employer_id = employer_id

        session.commit()
        session.refresh(job)
        session.close()

        return UpdateJob(job=job)


class DeleteJob(Mutation):
    class Arguments:
        id = Int(required=True)

    success = Boolean()

    @is_admin
    def mutate(root, info, id):
        session = Session()
        job = session.query(Job).filter(Job.id == id).first()

        if not job:
            raise Exception("Job not found")

        session.delete(job)
        session.commit()
        session.close()

        return DeleteJob(success=True)


class ApplyToJob(Mutation):
    class Arguments:
        job_id = Int(required=True)
        user_id = Int(required=True)

    job_application = Field(lambda: JobApplicationObject)

    @is_admin
    def mutate(root, info, job_id, user_id, logged_user):

        with Session() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise GraphQLError("The user id informed was not found")
            
            if logged_user.id != user_id:
                raise GraphQLError("You can only apply for jobs to the user informed in the token")

            job = session.query(Job).filter(Job.id == job_id).filter()
            if not job:
                raise GraphQLError("The job id informed was not found")

            job_application = (
                session.query(JobApplication)
                .filter(
                    JobApplication.job_id == job_id, JobApplication.user_id == user_id
                )
                .first()
            )
            if job_application:
                raise GraphQLError(
                    "The informed user is already associated to the informed job"
                )

            job_application = JobApplication(user_id=user_id, job_id=job_id)

            session.add(job_application)
            session.commit()
            session.refresh(job_application)

        return ApplyToJob(job_application=job_application)
