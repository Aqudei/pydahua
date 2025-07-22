from dahua_ipc import *
from dotenv import load_dotenv
import os
import argparse

load_dotenv()

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("key")
    # parser.add_argument("value")
    # args = parser.parse_args()

    dahua = DahuaIPC(
        os.environ.get("CAM_IP"),
        os.environ.get("CAM_USER"),
        os.environ.get("CAM_PASS"),
    )

    # response = dahua.GetVideoInOptionsConfig()
    # print("GetVideoInOptionsConfig() response:")
    # print(response)

    response = dahua.GetVideoInputCaps()
    print("GetVideoInputCaps() response:")
    print(response)

    # response = dahua.SetVideoInOptionsConfig(channel=0, key=args.key, value=args.value)
    # print("SetVideoInOptionsConfig() response:")
    # print(response)
