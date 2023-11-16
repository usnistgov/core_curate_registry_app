"""Curate registry app user views
"""
from django.utils.decorators import method_decorator
from django.views import View

from core_curate_app.permissions import rights
from core_curate_app.views.user.views import EnterDataView, ViewDataView
from core_curate_registry_app.settings import (
    REGISTRY_XSD_FILENAME,
    XPATH_TITLE,
    ALLOW_MULTIPLE_SCHEMAS,
)
from core_curate_registry_app.utils import jquery as jquery_utils
from core_main_app.commons import exceptions
from core_main_app.components.template_version_manager import (
    api as template_version_manager_api,
)
from core_main_app.utils import decorators
from core_main_app.utils.rendering import render
from core_main_registry_app.components.custom_resource import (
    api as custom_resource_api,
)
from core_main_registry_app.components.template import (
    api as template_registry_api,
)
from core_main_registry_app.constants import CUSTOM_RESOURCE_TYPE
from core_parser_app.components.data_structure_element import (
    api as data_structure_element_api,
)


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
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
        "js": [
            {
                "path": "core_curate_registry_app/user/js/banner.js",
                "is_raw": False,
            }
        ],
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
            "page_title": "Publish Resource",
            "ALLOW_MULTIPLE_SCHEMAS": ALLOW_MULTIPLE_SCHEMAS,
        },
    )


class StartCurate(View):
    """Start curate."""

    def __init__(self):
        super().__init__()
        self.assets = {
            "js": [
                {
                    "path": "core_curate_app/user/js/select_template.js",
                    "is_raw": False,
                },
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
            content_type=rights.CURATE_CONTENT_TYPE,
            permission=rights.CURATE_ACCESS,
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
            custom_resource = (
                custom_resource_api.get_by_current_template_and_slug(
                    role, request=request
                )
            )
        except exceptions.DoesNotExist:
            custom_resource = None

        context = {
            "template_id": template_version_manager_api.get_active_global_version_manager_by_title(
                REGISTRY_XSD_FILENAME, request=request
            ).current,
            "role": role,
            "custom_resource": custom_resource,
            "page_title": "Publish Resource",
        }
        return render(
            request,
            "core_curate_registry_app/user/curate.html",
            assets=self.assets,
            modals=self.modals,
            context=context,
        )


class EnterDataRegistryView(EnterDataView):
    """Enter Data Registry View."""

    def __init__(self):
        super().__init__()
        self.assets["js"].extend(
            (
                {
                    "path": "core_curate_registry_app/user/js/role.js",
                    "is_raw": False,
                },
                {
                    "path": "core_curate_registry_app/user/js/enter_data_registry.js",
                    "is_raw": False,
                },
                {
                    "path": "core_curate_registry_app/user/js/title.js",
                    "is_raw": False,
                },
                {
                    "path": "core_curate_registry_app/user/js/enter_data_registry.raw.js",
                    "is_raw": True,
                },
            )
        )
        self.modals.extend(
            ["core_curate_app/user/data-entry/modals/xml-valid-registry.html"]
        )

    def build_context(
        self, request, curate_data_structure, reload_unsaved_changes
    ):
        """Build the context of the view

        Args:
            request:
            curate_data_structure:
            reload_unsaved_changes:

        Returns:

        """
        # get the role before module initialization
        role = request.GET.get("role", None)
        # build context
        context = super().build_context(
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
                custom_resource = (
                    custom_resource_api.get_by_current_template_and_slug(
                        role, request=request
                    )
                )
            except exceptions.DoesNotExist:
                custom_resource = None

            list_data_structure_element = (
                data_structure_element_api.get_by_xpath(XPATH_TITLE, request)
            )
            list_data_structure_element = list(list_data_structure_element)
            data_id_list = []
            for i in range(len(list_data_structure_element)):
                data_id_list.append(str(list_data_structure_element[i].id))
            jquery_selector = (
                jquery_utils.get_jquery_selector_from_data_structure(
                    data_id_list
                )
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
    """View Data Registry."""

    def __init__(self):
        super().__init__()
        self.assets["js"].append(
            {
                "path": "core_curate_app/user/js/view_data_registry.js",
                "is_raw": False,
            }
        )

        self.modals = [
            "core_curate_app/user/data-review/modals/save-error.html",
            "core_curate_app/user/data-review/modals/save-form-registry.html",
            "core_main_app/common/modals/download-options.html",
        ]

    def build_context(self, request, curate_data_structure):
        """Build the context of the view

        Args:
            request:
            curate_data_structure:

        Returns:

        """

        context = super().build_context(request, curate_data_structure)
        return context


@decorators.permission_required(
    content_type=rights.CURATE_CONTENT_TYPE,
    permission=rights.CURATE_ACCESS,
)
def start_curate_other_resources(request):
    """Page that allows to select a template to start curating.

    Args:
        request:

    Returns:

    """
    assets = {
        "js": [
            {
                "path": "core_curate_app/user/js/select_template.js",
                "is_raw": False,
            },
            {
                "path": "core_curate_app/user/js/select_template.raw.js",
                "is_raw": True,
            },
            {
                "path": "core_curate_registry_app/user/js/start_curate.js",
                "is_raw": False,
            },
        ],
        "css": [
            "core_curate_app/user/css/common.css",
            "core_curate_app/user/css/style.css",
        ],
    }

    registry_template = template_registry_api.get_current_registry_template(
        request
    )
    global_active_template_list = (
        template_version_manager_api.get_active_global_version_manager(
            request=request
        )
    )
    other_templates = global_active_template_list.exclude(
        id=registry_template.id
    )

    context = {
        "templates_version_manager": other_templates,
    }

    # Set page title
    context.update({"page_title": "Curate"})

    return render(
        request,
        "core_curate_app/user/curate.html",
        assets=assets,
        context=context,
    )
