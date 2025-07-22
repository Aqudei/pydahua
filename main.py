from dahua_ipc import *
from dotenv import load_dotenv
import os


load_dotenv()

if __name__ == "__main__":
    dahua = DahuaIPC(
        os.environ.get("CAM_IP"),
        os.environ.get("CAM_USER"),
        os.environ.get("CAM_PASS"),
    )

   
    response = dahua.focus_near()
    print("auto_focus() response:")
    print(response)