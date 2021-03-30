import graphene
import sys
sys.path.append('../question')
import app.config.schema


class Query(app.config.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)