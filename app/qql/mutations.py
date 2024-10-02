from graphene import ObjectType
from app.qql.employer.mutations import AddEmployer, DeleteEmployer, UpdateEmployer
from app.qql.job.mutations import AddJob, ApplyToJob, DeleteJob, UpdateJob
from app.qql.user.mutations import CreateUser, LoginUser


class Mutation(ObjectType):
    add_job = AddJob.Field()
    update_job = UpdateJob.Field()
    delete_job = DeleteJob.Field()
    apply_job = ApplyToJob.Field()
    add_employer = AddEmployer.Field()
    update_employer = UpdateEmployer.Field()
    delete_employer = DeleteEmployer.Field()
    login_user = LoginUser.Field()
    create_user = CreateUser.Field()
