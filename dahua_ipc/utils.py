import re
from collections import defaultdict
from typing import Any, Dict

def parse_table_like_response(response: str) -> Dict[str, Any]:
    """
    Parses lines like:
      - table.X[0][1].Key=Value
      - status.Key=Value
    into a nested dictionary structure.

    Returns:
      {
        "table.X": { "0": { "1": { "Key": Value } } },
        "status": { "Key": Value }
      }
    """

    def nested_dict():
        return defaultdict(nested_dict)

    def to_regular_dict(d):
        if isinstance(d, defaultdict):
            return {k: to_regular_dict(v) for k, v in d.items()}
        return d

    # Matches: prefix.TableName[indices].Field=Value
    pattern_indexed = re.compile(
        r'^([a-zA-Z_][\w]*)\.([a-zA-Z_][\w]*)((?:\[\d+\])+)\.([a-zA-Z_][\w]*)=([^\n\r]+)$'
    )

    # Matches: prefix.Field=Value
    pattern_flat = re.compile(
        r'^([a-zA-Z_][\w]*)\.([a-zA-Z_][\w]*)=([^\n\r]+)$'
    )

    data = nested_dict()

    for line in response.strip().splitlines():
        line = line.strip()

        if match := pattern_indexed.match(line):
            prefix, table_name, indices_str, field, value = match.groups()
            full_key = f"{prefix}.{table_name}"
            indices = list(map(int, re.findall(r'\[(\d+)\]', indices_str)))

            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Leave as string

            ref = data[full_key]
            for idx in indices[:-1]:
                ref = ref[idx]
            ref[indices[-1]][field] = value

        elif match := pattern_flat.match(line):
            prefix, field, value = match.groups()
            try:
                value = int(value)
            except ValueError:
                try:
                    value = float(value)
                except ValueError:
                    pass  # Leave as string

            data[prefix][field] = value

        else:
            # Line didn't match any pattern — optionally log or skip
            continue

    return to_regular_dict(data)
