import graphene

import articles.schema
import providers.schema
import services.schema


class Query(
    articles.schema.Query,
    providers.schema.Query,
    services.schema.Query,
    graphene.ObjectType
):
    pass


# class Mutation(graphene.ObjectType):
#     pass


schema = graphene.Schema(query=Query)
