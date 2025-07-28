import json
from pprint import pprint
from dotenv import load_dotenv
import os
import argparse

from dahua_ipc.dahua import DahuaCameraAPI
from dahua_ipc.utils import parse_response

load_dotenv()

if __name__ == "__main__":
    dahua = DahuaCameraAPI(
        os.environ.get("CAM_IP"),
        os.environ.get("CAM_USER"),
        os.environ.get("CAM_PASS"),
    )

    # print("GetFocusStatus()\n",dahua.GetFocusStatus())
    
    # print("Perform AutoFocus:")
    # dahua.AutoFocus()

    r = dahua.GetVideoInColor()
    print(r)