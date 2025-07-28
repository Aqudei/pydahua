import re
from typing import Any, Union

def set_nested_value(container: Union[dict, list], keys: list, value: Any):
    """Set a nested value in a structure that can include dicts and lists."""
    for i, key in enumerate(keys):
        is_last = i == len(keys) - 1

        if isinstance(container, dict):
            if key not in container:
                # Peek ahead to decide list or dict
                next_key = keys[i + 1] if not is_last else None
                container[key] = [] if isinstance(next_key, int) else {}
            container = container[key]

        elif isinstance(container, list):
            # Ensure list is large enough
            while len(container) <= key:
                container.append({})

            if is_last:
                container[key] = value
                return
            if not isinstance(container[key], (dict, list)):
                # Decide what to overwrite with
                next_key = keys[i + 1]
                container[key] = [] if isinstance(next_key, int) else {}
            container = container[key]

    if isinstance(container, dict):
        container[keys[-1]] = value

def parse_response(text: str):
    data = {}
    lines = text.strip().splitlines()
    for line in lines:
        if '=' not in line:
            continue
        key, val = line.split('=', 1)

        # Convert value
        val = val.strip()
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
                    pass  # Leave as string

        # Parse key into parts
        key_parts = []
        for part in key.split('.'):
            matches = re.findall(r'([^\[\]]+)|\[(\d+)\]', part)
            for name, index in matches:
                if name:
                    key_parts.append(name)
                if index:
                    key_parts.append(int(index))

        set_nested_value(data, key_parts, val)

    return data
