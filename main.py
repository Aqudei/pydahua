from dahua_ipc import *
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

if __name__ == "__main__":
    dahua = DahuaIPC(
        os.environ.get("CAM_IP"),
        os.environ.get("CAM_USER"),
        os.environ.get("CAM_PASS"),
    )

    # response = dahua.GetVideoInOptionsConfig()
    # print("GetVideoInOptionsConfig() response:")
    # print(response)
    
    
    response = dahua.SetVideoInOptionsConfig(channel=0,key="FocusMode",value=3)
    print("SetVideoInOptionsConfig() response:")
    print(response)