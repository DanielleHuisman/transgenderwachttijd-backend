import graphene

import providers.schema
import services.schema


class Query(
    providers.schema.Query,
    services.schema.Query,
    graphene.ObjectType
):
    pass


# class Mutation(graphene.ObjectType):
#     pass


schema = graphene.Schema(query=Query)
