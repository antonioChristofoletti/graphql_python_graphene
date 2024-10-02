from graphene import Field, Int, Schema, ObjectType, String, List, Mutation


class UserType(ObjectType):
    id = Int()
    name = String()
    age = Int()


class CreateUser(Mutation):
    class Arguments:
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, name, age):
        user = {"id": len(Query.users) + 1, "name": name, "age": age}

        Query.users.append(user)

        return CreateUser(user=user)


class UpdateUser(Mutation):
    class Arguments:
        user_id = Int(required=True)
        name = String()
        age = Int()

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id, name=None, age=None):
        user = None
        for u in Query.users:
            if u["id"] == user_id:
                user = u
                break

        if not user:
            return None

        if name is not None:
            user["name"] = name

        if age is not None:
            user["age"] = age

        return UpdateUser(user=user)


class DeleteUser(Mutation):
    class Arguments:
        user_id = Int(required=True)

    user = Field(UserType)

    @staticmethod
    def mutate(root, info, user_id):
        for idx, u in enumerate(Query.users):
            if u["id"] == user_id:
                user = Query.users.pop(idx)
                return DeleteUser(user=user)


class Query(ObjectType):
    user = Field(UserType, user_id=Int())
    users_by_min_age = Field(List(UserType), min_age=Int())

    # dummy data store
    users = [
        {"id": 1, "name": "Andy Doe", "age": 33},
        {"id": 2, "name": "Andia Doe", "age": 34},
        {"id": 3, "name": "Julie Sullivan", "age": 31},
        {"id": 4, "name": "John Barber", "age": 29},
    ]

    @staticmethod
    def resolve_user(root, info, user_id):
        matched_users = [user for user in Query.users if user["id"] == user_id]

        return matched_users[0] if matched_users else None

    @staticmethod
    def resolve_users_by_min_age(root, info, min_age):
        return [user for user in Query.users if user["age"] >= min_age]


class Mutation(ObjectType):
    create_user = CreateUser.Field()
    update_user = UpdateUser.Field()
    delete_user = DeleteUser.Field()


schema = Schema(query=Query, mutation=Mutation)

qql = """
query {
    user(userId: 2){
        id
        name
        age
    }
}
"""

qql = """
query {
    usersByMinAge(minAge: 33){
        id
        name
        age
    }
}
"""

qql = """
mutation {
    createUser(name: "New User", age: 25){
        user {
            id
            name
            age
        }
    }
}
"""

qql = """
mutation {
    updateUser(userId: 99, name: "Updated User", age: 26){
        user {
            id
            name
            age
        }
    }
}
"""

qql = """
mutation {
    deleteUser(userId: 1){
        user {
            id
            name
            age
        }
    }
}
"""

if __name__ == "__main__":
    result = schema.execute(qql)
    print(result)
