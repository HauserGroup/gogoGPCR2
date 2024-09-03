from packaging import version

def fields_for_id(field_id, participant):
    """
    Retrieve and sort fields associated with the given fields
    
    Input(s):
    - field_id: List of phenotypes IDs
    - participant: UKB spark dk

    Output(s):
    - Sorted list of fields
    """

    field_id = str(field_id)
    # Updated regex to handle the specific format like 21000_i0
    fields = participant.find_fields(
        name_regex=r"^p{}(_i\d+)?(_a\d+)?$".format(field_id)
    )
    
    def extract_version(field_name):
        # Remove the prefix and extract the part after "_i" or return a default version
        parts = field_name.split('_i')
        if len(parts) > 1:
            # If there's an '_i' part, try to parse the version after it
            return version.parse(parts[1])
        else:
            # If no '_i' part, return a default low version to sort these first
            return version.parse("0")
    
    # Sort the fields using the custom key that handles both cases
    return sorted(fields, key=lambda f: extract_version(f.name))
