from dotenv import load_dotenv
import os
import argparse

from dahua_ipc.dahua import DahuaCameraAPI

load_dotenv()

if __name__ == "__main__":
    dahua = DahuaCameraAPI(
        os.environ.get("CAM_IP"),
        os.environ.get("CAM_USER"),
        os.environ.get("CAM_PASS"),
    )

    
    
    