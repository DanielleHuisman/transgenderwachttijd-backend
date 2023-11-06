import strawberry
from strawberry.tools import merge_types

import transgenderwachttijd.articles.schema
import transgenderwachttijd.providers.schema
import transgenderwachttijd.services.schema

Query = merge_types('Query', (
    transgenderwachttijd.articles.schema.Query,
    transgenderwachttijd.providers.schema.Query,
    transgenderwachttijd.services.schema.Query,
))

schema = strawberry.Schema(query=Query)
