from packaging import version

def fields_for_id(field_id, participant):
    """[summary]

    Parameters
    ----------
    field_id : [type]
        [description]
    participant : [type]
        [description]

    Returns
    -------
    [type]
        [description]
    """

    field_id = str(field_id)
    fields = participant.find_fields(
        name_regex=r"^p{}(_i\d+)?(_a\d+)?$".format(field_id)
    )
    
    return sorted(fields, key=lambda f: version.parse(f.name.replace("p", "")))
