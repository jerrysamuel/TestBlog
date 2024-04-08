from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from graphene_django.views import GraphQLView
from django.core.exceptions import ValidationError
from django.db import IntegrityError

class PrivateGraphQlView(LoginRequiredMixin, GraphQLView):
    def handle_query(self, request, data, query, variables, operation_name, show_graphiql=False):
        try:
            response = super().handle_query(request, data, query, variables, operation_name, show_graphiql)
            return self.handle_response(response)
        except ValidationError as e:
            return self.handle_validation_error(e)
        except IntegrityError as e:
            return self.handle_database_error(e)
        except Exception as e:
            return self.handle_internal_error(e)

    def handle_response(self, response):
        if response.status_code == 400:
            errors = response.json().get('errors')
            if errors:
                return JsonResponse({'errors': [error['message'] for error in errors]}, status=400)
        return response

    def handle_validation_error(self, error):
        return JsonResponse({'errors': [str(error)]}, status=400)

    def handle_database_error(self, error):
        return JsonResponse({'errors': ['Database error: {}'.format(error)]}, status=400)

    def handle_internal_error(self, error):
        return JsonResponse({'errors': ['Internal server error: {}'.format(error)]}, status=500)