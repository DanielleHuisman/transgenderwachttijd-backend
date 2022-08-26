import strawberry
from strawberry.tools import merge_types

import articles.schema
import providers.schema
import services.schema

Query = merge_types('Query', (
    articles.schema.Query,
    providers.schema.Query,
    services.schema.Query,
))

schema = strawberry.Schema(query=Query)
