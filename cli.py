import json
from pprint import pprint
from dotenv import load_dotenv
import os
import argparse

from app.dahua_ipc.dahua import DahuaCameraAPI
from app.dahua_ipc.utils import parse_table_like_response

load_dotenv()

if __name__ == "__main__":
    dahua = DahuaCameraAPI(
        os.environ.get("CAMERA_IP"),
        os.environ.get("CAMERA_USER"),
        os.environ.get("CAMERA_PASS"),
    )

    # print("GetFocusStatus()\n",dahua.GetFocusStatus())

    # print("Perform AutoFocus:")
    # dahua.AutoFocus()

    # List of all Get methods and their optional arguments
    get_methods = [
        ("GetVideoInColor", {"channel": 0}),
        ("GetVideoInSharpness", {"channel": 0}),
        ("GetVideoInExposure", {"channel": 0}),
        ("GetVideoInOptionsConfig", {"channel": 0}),
        ("GetColorMode", {"channel": 0}),
        ("GetVideoInZoom", {}),
        ("GetFocusStatus", {"channel": 0}),
    ]

    for method_name, kwargs in get_methods:
        print(f"--- {method_name} ---")
        try:
            method = getattr(dahua, method_name)
            result = method(**kwargs) if kwargs else method()
            print(result)
        except Exception as e:
            print(f"Error calling {method_name}: {e}")
        print()

    # with open("./VideoCaps.txt",'rt') as target:
    #     r = parse_table_like_response(target.read())
    #     print(r)
