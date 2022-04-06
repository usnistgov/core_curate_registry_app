""" Curate Data Structure registry api
"""
from core_main_app.settings import XML_POST_PROCESSOR, XML_FORCE_LIST
from core_main_app.utils import xml as xml_utils

from core_main_registry_app.utils.role.extraction import role_extraction


def get_role(curate_data_structure):
    """Get the role saved in the curate_data_structure's form string

    Args:
        curate_data_structure:

    Returns:

    """
    return role_extraction(
        xml_utils.raw_xml_to_dict(
            curate_data_structure.form_string,
            postprocessor=XML_POST_PROCESSOR,
            force_list=XML_FORCE_LIST,
        )
    )
