import re
from collections import defaultdict
from typing import Any, Dict

def parse_table_like_response(response: str) -> Dict[str, Any]:
    """
    Parses key-value lines with structure like:
    table.SomeName[0][1].Field=Value
    into a nested dictionary.

    Supports:
    - Any table name (e.g., table.VideoInColor)
    - Multiple numeric index levels (e.g., [0][1][2])
    - Any field name and value

    :param response: Multiline string of response entries
    :return: Nested dictionary
    """

    def nested_dict():
        return defaultdict(nested_dict)

    def to_regular_dict(d):
        if isinstance(d, defaultdict):
            return {k: to_regular_dict(v) for k, v in d.items()}
        return d

    # Match: table.Name[0][1]...[n].Field=Value
    pattern = re.compile(
        r'table\.([a-zA-Z_][\w]*)((?:\[\d+\])+)\.([a-zA-Z_][\w]*)=([^\n\r]+)'
    )

    data = nested_dict()

    for line in response.strip().splitlines():
        line = line.strip()
        match = pattern.match(line)
        if not match:
            continue

        table_name, indices_str, field, value = match.groups()

        # Extract index values
        indices = list(map(int, re.findall(r'\[(\d+)\]', indices_str)))

        # Attempt to convert value to int if possible
        try:
            value = int(value)
        except ValueError:
            pass  # leave as string

        # Walk through nested levels
        ref = data[table_name]
        for idx in indices[:-1]:
            ref = ref[idx]
        ref[indices[-1]][field] = value

    return to_regular_dict(data)
