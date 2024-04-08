from django.urls import path
from .views import PrivateGraphQlView
from django.views.decorators.csrf import csrf_exempt
from blog.schema import schema
urlpatterns = [
    path('graphql', csrf_exempt(PrivateGraphQlView.as_view(graphiql=True, schema=schema))),
]
