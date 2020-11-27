"""Curate registry app user views
"""
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View

import core_curate_app.permissions.rights as rights
import core_main_app.utils.decorators as decorators
from core_curate_app.views.user.views import EnterDataView
from core_curate_app.views.user.views import ViewDataView
from core_curate_registry_app.settings import REGISTRY_XSD_FILENAME
from core_curate_registry_app.settings import XPATH_TITLE
from core_curate_registry_app.utils import jquery as jquery_utils
from core_main_app.commons import exceptions
from core_main_app.components.version_manager import api as version_manager_api
from core_main_app.utils.rendering import render
from core_main_registry_app.components.custom_resource import api as custom_resource_api
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)


@decorators.permission_required(
    content_type=rights.curate_content_type,
    permission=rights.curate_access,
    login_url=reverse_lazy("core_main_app_login"),
)
def index(request):
    """Curate homepage for the registry.

    Args:
        request:

    Returns:

    """
    assets = {
        "css": [
            "core_curate_registry_app/user/css/index.css",
            "core_main_registry_app/user/css/resource_banner/selection.css",
            "core_main_registry_app/user/css/resource_banner/resource_banner.css",
        ],
        "js": [{"path": "core_curate_registry_app/user/js/banner.js", "is_raw": False}],
    }

    # Get custom resources for the current template
    custom_resources = custom_resource_api.get_all_of_current_template(
        request=request
    ).order_by("sort")

    return render(
        request,
        "core_curate_registry_app/user/index.html",
        assets=assets,
        context={
            "custom_resources": custom_resources,
            "display_not_resource": False,
            "type_resource": CUSTOM_RESOURCE_TYPE.RESOURCE.value,
        },
    )


class StartCurate(View):
    """Start curate."""

    def __init__(self):
        super(StartCurate, self).__init__()
        self.assets = {
            "js": [
                {"path": "core_curate_app/user/js/select_template.js", "is_raw": False},
                {
                    "path": "core_curate_registry_app/user/js/start_curate.js",
                    "is_raw": False,
                },
            ],
            "css": ["core_curate_app/user/css/style.css"],
        }
        self.modals = []

    @method_decorator(
        decorators.permission_required(
            content_type=rights.curate_content_type,
            permission=rights.curate_access,
            login_url=reverse_lazy("core_main_app_login"),
        )
    )
    def get(self, request, role):
        """Start curate with role parameter.
        Args:
            request:
            role:

        Returns:
        """
        try:
            # Get custom resources for the current template
            custom_resource = custom_resource_api.get_by_current_template_and_slug(
                role, request=request
            )
        except exceptions.DoesNotExist:
            custom_resource = None

        context = {
            "template_id": version_manager_api.get_active_global_version_manager_by_title(
                REGISTRY_XSD_FILENAME, request=request
            ).current,
            "role": role,
            "custom_resource": custom_resource,
        }
        return render(
            request,
            "core_curate_app/user/curate.html",
            assets=self.assets,
            modals=self.modals,
            context=context,
        )


class EnterDataRegistryView(EnterDataView):
    def __init__(self):
        super(EnterDataRegistryView, self).__init__()
        self.assets["js"].extend(
            (
                {"path": "core_curate_registry_app/user/js/role.js", "is_raw": False},
                {
                    "path": "core_curate_registry_app/user/js/enter_data_registry.js",
                    "is_raw": False,
                },
                {"path": "core_curate_registry_app/user/js/title.js", "is_raw": False},
                {
                    "path": "core_curate_registry_app/user/js/enter_data_registry.raw.js",
                    "is_raw": True,
                },
            )
        )
        self.modals.extend(
            ["core_curate_app/user/data-entry/modals/xml-valid-registry.html"]
        )

    def build_context(self, request, curate_data_structure, reload_unsaved_changes):
        # get the role before module initialization
        role = request.GET.get("role", None)
        # build context
        context = super(EnterDataRegistryView, self).build_context(
            request, curate_data_structure, reload_unsaved_changes
        )

        # init variables in context
        context["data_Elements"] = None
        context["role_choice"] = None
        context["role_type"] = None
        context["icon"]: None
        context["icon_color"]: None

        # don't give a role to select, if editing a form
        if not curate_data_structure.form_string:
            try:
                # Get custom resources for the current template
                custom_resource = custom_resource_api.get_by_current_template_and_slug(
                    role, request=request
                )
            except exceptions.DoesNotExist:
                custom_resource = None

            list_data_structure_element = data_structure_element_api.get_by_xpath(
                XPATH_TITLE, request
            )
            list_data_structure_element = list(list_data_structure_element)
            data_id_list = []
            for i in range(len(list_data_structure_element)):
                data_id_list.append(list_data_structure_element[i]["id"])
            jquery_selector = jquery_utils.get_jquery_selector_from_data_structure(
                data_id_list
            )
            context["data_Elements"] = jquery_selector

            # update context with role
            context["role_choice"] = (
                custom_resource.role_choice if custom_resource else None
            )
            context["role_type"] = (
                custom_resource.role_type if custom_resource else None
            )
            context["icon"] = custom_resource.icon if custom_resource else None
            context["icon_color"] = (
                custom_resource.icon_color if custom_resource else None
            )

        # return context
        return context


class ViewDataRegistryView(ViewDataView):
    def __init__(self):
        super(ViewDataRegistryView, self).__init__()
        self.assets["js"].append(
            {"path": "core_curate_app/user/js/view_data_registry.js", "is_raw": False}
        )

        self.modals = [
            "core_curate_app/user/data-review/modals/save-error.html",
            "core_curate_app/user/data-review/modals/save-form-registry.html",
        ]

    def build_context(self, request, curate_data_structure):

        context = super(ViewDataRegistryView, self).build_context(
            request, curate_data_structure
        )
        return context
