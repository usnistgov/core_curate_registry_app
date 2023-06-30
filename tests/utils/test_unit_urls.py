""" Urls test class
"""
from unittest import TestCase

from core_curate_app.rest.curate_data_structure.views import (
    CurateDataStructureDetail,
)

from django.urls import reverse, resolve


class TestUrls(TestCase):
    """TestUrls"""

    def test_url_curate_data_structure_detail(
        self,
    ):
        """test_url_curate_data_structure_detail

        Returns:

        """
        url = reverse("core_curate_app_rest_draft_detail", args=[1])
        self.assertEquals(
            resolve(url).func.view_class, CurateDataStructureDetail
        )
