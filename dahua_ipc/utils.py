import re
from typing import Any, Union

def set_nested_value(container: Union[dict, list], keys: list, value: Any):
    """Set a nested value in a mixed dict/list structure."""
    for i, key in enumerate(keys):
        is_last = i == len(keys) - 1

        # Handle list indexing
        if isinstance(container, list):
            # Ensure the list is long enough
            while len(container) <= key:
                container.append({} if not is_last else None)
            if is_last:
                container[key] = value
                return
            if not isinstance(container[key], (dict, list)):
                # Replace with proper structure
                next_key = keys[i + 1]
                container[key] = [] if isinstance(next_key, int) else {}
            container = container[key]

        # Handle dict key
        elif isinstance(container, dict):
            if key not in container:
                next_key = keys[i + 1] if not is_last else None
                container[key] = [] if isinstance(next_key, int) else {}
            if is_last:
                container[key] = value
                return
            container = container[key]

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
                    pass  # Keep as string

        # Parse dotted keys with [index]
        key_parts = []
        for part in key.split('.'):
            matches = re.findall(r'([^\[\]]+)|\[(\d+)\]', part)
            for name, index in matches:
                if name:
                    key_parts.append(name)
                if index:
                    key_parts.append(int(index))

        # Assign value into nested structure
        set_nested_value(data, key_parts, val)

    return data
