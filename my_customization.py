
"""
- MODIFIED FROM BIBTEXPARSER'S BUILT-IN CUSTOMIZATIONS -

A set of functions useful for customizing bibtex fields.
You can find inspiration from these functions to design yours.
Each of them takes a record and return the modified record.
"""

import logging

logger = logging.getLogger(__name__)

__all__ = ['getnames', 'author', 'editor']


def getnames(names):
    """Make people names as surname, firstnames
    or surname, initials. Should eventually combine up the two.

    :param names: a list of names
    :type names: list
    :returns: list -- Correctly formated names
    """
    tidynames = []
    for namestring in names:
        namestring = namestring.strip()
        if len(namestring) < 1:
            continue
        if ',' in namestring:
            namesplit = namestring.split(',', 1)
            last = namesplit[0].strip()
            firsts = [i.strip() for i in namesplit[1].split()]
        else:
            namesplit = namestring.split()
            last = namesplit.pop()
            firsts = [i.replace('.', '. ').strip() for i in namesplit]
        if last in ['jnr', 'jr', 'junior']:
            last = firsts.pop()
        for item in firsts:
            if item in ['ben', 'van', 'der', 'de', 'la', 'le']:
                last = firsts.pop() + ' ' + last
        tidynames.append(last + ", " + ' '.join(firsts))
    return tidynames


def editor(record):
    """
    Turn the editor field into a dict composed of the original editor name
    and a editor id (without coma or blank).

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.

    """
    if "editor" in record:
        if record["editor"]:
            record["editor"] = getnames([i.strip() for i in record["editor"].replace('\n', ' ').split(" and ")])
        else:
            del record["editor"]
    return record
