"""Curate registry app user ajax
"""
import core_curate_app.permissions.rights as rights
import core_main_app.utils.decorators as decorators
from core_curate_app.views.user import ajax as curate_ajax
from django.utils.decorators import method_decorator
from django.views.generic import View


class StartCurate(View):
    """Start Curate Ajax"""

    @method_decorator(
        decorators.permission_required(
            content_type=rights.curate_content_type,
            permission=rights.curate_access,
            raise_exception=True,
        )
    )
    def get(self, request):
        """Load forms to start curating.

        Args:
           request:

        Returns:

        """
        return curate_ajax.start_curate(request)

    @method_decorator(
        decorators.permission_required(
            content_type=rights.curate_content_type,
            permission=rights.curate_access,
            raise_exception=True,
        )
    )
    def post(self, request):
        """Load forms to start curating.
        Add role to response url.

        Args:
           request:

        Returns:

        """
        response = curate_ajax.start_curate(request)
        if response.status_code == 200:
            role = request.GET.get("role", None)
            response.content = "{0}?role={1}".format(
                response.content.decode("utf-8"), role
            )
        return response
