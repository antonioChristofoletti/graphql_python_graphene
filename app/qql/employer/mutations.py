from graphene import Field, Int, Mutation, String
from app.qql.types import EmployerObject
from app.db.database import Session
from app.db.models import Employer
from app.utils import is_admin, get_authenticated_user


class AddEmployer(Mutation):
    class Arguments:
        name = String(required=True)
        contact_email = String(required=True)
        industry = String(required=True)

    employer = Field(lambda: EmployerObject)

    authenticated_as = Field(String)

    @is_admin
    def mutate(root, info, name, contact_email, industry):
        user = get_authenticated_user(info.context)

        session = Session()
        employer = Employer(name=name, contact_email=contact_email, industry=industry)

        session.add(employer)
        session.commit()
        session.refresh(employer)

        return AddEmployer(employer=employer, authenticated_as=user.email)


class UpdateEmployer(Mutation):
    class Arguments:
        id = Int(required=True)
        name = String()
        contract_email = String()
        industry = String()

    employer = Field(lambda: EmployerObject)

    @is_admin
    def mutate(root, info, id, **kwargs):
        with Session() as session:
            e = session.query(Employer).filter(Employer.id == id).first()

            if not e:
                raise Exception("Employer not found")

            for k, v in kwargs.items():
                setattr(e, k, v)

            session.commit()
            session.refresh(e)

        return UpdateEmployer(employer=e)


class DeleteEmployer(Mutation):
    class Arguments:
        id = Int(required=True)

    employer = Field(lambda: EmployerObject)

    @is_admin
    def mutate(root, info, id):
        with Session() as session:
            e = session.query(Employer).filter(Employer.id == id).first()

            if not e:
                raise Exception("Employer not found")

            session.delete(e)
            session.commit()

        return DeleteEmployer(employer=e)
