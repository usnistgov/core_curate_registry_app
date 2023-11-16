""" Unit test user views
"""
from unittest.mock import patch

from django.test import SimpleTestCase, RequestFactory

from core_curate_registry_app.views.user.views import (
    start_curate_other_resources,
)
from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestStartCurateOtherResources(SimpleTestCase):
    """TestStartCurateOtherResources"""

    def setUp(self):
        """setUp

        Returns:

        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(user_id="1", has_perm=True)

    @patch(
        "core_main_app.components.template_version_manager.api.get_active_global_version_manager"
    )
    @patch(
        "core_main_registry_app.components.template.api.get_current_registry_template"
    )
    def test_start_curate_other_resources_returns_http_200(
        self,
        mock_get_current_registry_template,
        mock_get_active_global_version_manager,
    ):
        """test_get_when_user_has_preferences_returns_form

        Returns:

        """
        # Arrange
        request = self.factory.get("start_curate_other_resources")
        request.user = self.user1

        # Act
        response = start_curate_other_resources(request)

        # Assert
        self.assertEqual(response.status_code, 200)
