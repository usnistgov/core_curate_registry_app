"""Data util for curate_registry app
"""


def get_jquery_selector_from_data_structure(data_id_list):
    """Create a jquery_selector from xpath
    Args : List of ObjectId from data structure elements
    Returns: Jquery_selector from xpath (.ID1,.ID2,.ID3 ...)

    """

    jquery_selector = ""
    for data_id in data_id_list:
        jquery_selector = jquery_selector + ("." + str(data_id) + ",")
    jquery_selector = jquery_selector[:-1]
    return jquery_selector
