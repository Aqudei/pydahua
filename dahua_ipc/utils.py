import re
from collections import defaultdict
from typing import Any

def set_nested_value(d: dict, keys: list, value: Any):
    """Recursively set nested keys in a dict/list structure safely."""
    for i, key in enumerate(keys):
        if isinstance(key, int):
            # Ensure list is long enough
            while len(d) <= key:
                d.append({})
            if i == len(keys) - 1:
                d[key] = value
            else:
                if not isinstance(d[key], (dict, list)):
                    d[key] = {}
                d = d[key]
        else:
            if i == len(keys) - 1:
                d[key] = value
            else:
                if key not in d:
                    # Decide if next is list or dict
                    next_key = keys[i + 1]
                    d[key] = [] if isinstance(next_key, int) else {}
                d = d[key]

def parse_response(text: str):
    data = {}
    lines = text.strip().splitlines()
    for line in lines:
        if not line.strip():
            continue
        key, val = line.split('=', 1)

        # Handle boolean, int, float, and string
        if val.lower() == 'true':
            val = True
        elif val.lower() == 'false':
            val = False
        else:
            try:
                val = int(val)
            except ValueError:
                try:
                    val = float(val)
                except ValueError:
                    val = val.strip()

        # Parse keys
        key_parts = []
        for part in key.split('.'):
            # e.g. FocusRect[2] → ("FocusRect", 2)
            matches = re.findall(r'([^\[\]]+)|\[(\d+)\]', part)
            for m in matches:
                if m[0]:
                    key_parts.append(m[0])
                if m[1]:
                    key_parts.append(int(m[1]))

        # Set the value safely
        set_nested_value(data, key_parts, val)

    return data
