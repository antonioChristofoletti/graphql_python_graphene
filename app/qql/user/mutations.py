from graphene import Field, Mutation, String
from graphql import GraphQLError

from app.db.database import Session
from app.db.models import User
from app.qql.types import UserObject
from app.utils import generate_token, get_authenticated_user, hash_password, is_authenticated, verify_password


class LoginUser(Mutation):
    class Arguments:
        email = String(required=True)
        password = String(required=True)

    token = String()

    @staticmethod
    def mutate(root, info, email, password):
        session = Session()

        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise GraphQLError("A user by that email does not exist")

        verify_password(user.password_hash, password)

        token = generate_token(email)

        return LoginUser(token=token)



class CreateUser(Mutation):
    class Arguments:
        username = String(required=True)
        email = String(required=True)
        password = String(required=True)
        role = String(required=True)

    user = Field(lambda: UserObject)

    @is_authenticated
    def mutate(root, info, username, email, password, role):
        try:
            with Session() as session:
                jwt_user = get_authenticated_user(info.context)

                user = session.query(User).filter(User.email == email).first()

                if user:
                    raise GraphQLError(f"The email account '{email}' is already in use")
                
                if role.lower() == "admin" and jwt_user.role.lower() != "admin":
                    raise GraphQLError("You are not allowed to create this user, because It has the role 'admin' and your user has not the role 'admin'")

                user = User(
                    username=username,
                    email=email,
                    role=role,
                    password_hash=hash_password(password),
                )

                session.add(user)
                session.commit()
                session.refresh(user)

                return CreateUser(user=user)
        except GraphQLError as ex:
            raise ex
        except Exception as ex:
            raise GraphQLError(f"Error creating user. Error: {ex}")
