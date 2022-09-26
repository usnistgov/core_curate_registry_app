""" Unit tests of curate_registry_utils
"""

from unittest.case import TestCase

from core_curate_registry_app.utils import jquery


class TestUtilsGetJqueryFromDataStructureElement(TestCase):
    """Test Utils Get Jquery From Data Structure Element."""

    def test_utils_get_jquery_from_data_structure_element_returns_data(self):
        """test_utils_get_jquery_from_data_structure_element_returns_data.

        Args:

        Returns:

        """
        # Arrange
        string_expected = ".element1,.element2,.element3"
        object1 = "element1"
        object2 = "element2"
        object3 = "element3"
        data_list = [object1, object2, object3]
        # Act
        result = jquery.get_jquery_selector_from_data_structure(data_list)
        # Assert
        self.assertEqual(string_expected, result)

    def test_utils_get_jquery_from_data_structure_element_returns_empty(self):
        """test_utils_get_jquery_from_data_structure_element_returns_empty.

        Args:

        Returns:

        """
        # Arrange
        data_list = []
        string_expected = ""
        # Act
        result = jquery.get_jquery_selector_from_data_structure(data_list)
        # Assert
        self.assertEqual(string_expected, result)

    def test_utils_get_jquery_from_data_structure_element_returns_one_element(
        self,
    ):
        """test_utils_get_jquery_from_data_structure_element_returns_one_element.

        Args:

        Returns:

        """
        # Arrange
        object1 = "element1"
        string_expected = ".element1"
        data_list = [object1]
        # Act
        result = jquery.get_jquery_selector_from_data_structure(data_list)
        # Assert
        self.assertEqual(string_expected, result)
