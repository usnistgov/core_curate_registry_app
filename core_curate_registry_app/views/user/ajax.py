"""Curate registry app user ajax
"""
from django.utils.decorators import method_decorator
from django.views.generic import View

from core_curate_app.permissions import rights
from core_main_app.utils import decorators
from core_curate_app.views.user import ajax as curate_ajax


class StartCurate(View):
    """Start Curate Ajax"""

    @method_decorator(
        decorators.permission_required(
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_ACCESS,
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
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_ACCESS,
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
            response_content = response.content.decode("utf-8")
            if "enter-data" in response_content:
                role = request.GET.get("role", None)
                response.content = f"{response_content}?role={role}"
        return response
