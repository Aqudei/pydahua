# dahua_ipc/cli.py

import argparse
import sys
import os
from dahua_ipc import DahuaIPC
from dotenv import load_dotenv
load_dotenv()

def parse_args():
    parser = argparse.ArgumentParser(description="Dahua IPC Command Line Interface")
    
    def env_or_arg(key, env, default=None):
        val = os.getenv(env)
        if val is not None:
            # Use env var + mark as optional
            return {"default": val, "help": f"{key} (env: {env}, default from env)"}
        else:
            # No env: must be provided as *positional* (so remove `required`)
            return {"help": f"{key} (env: {env})"}


    parser.add_argument("--ip", **env_or_arg("Camera IP", "CAM_IP"))
    parser.add_argument("--username", **env_or_arg("Username", "CAM_USER"))
    parser.add_argument("--password", **env_or_arg("Password", "CAM_PASS"))

    parser.add_argument("--port", type=int, default=int(os.getenv("CAM_PORT", 80)), help="HTTP port (env: DAHUA_PORT, default: 80)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("device-info", help="Get device information")
    subparsers.add_parser("channels", help="List available channels")

    snapshot_parser = subparsers.add_parser("snapshot", help="Take a snapshot")
    snapshot_parser.add_argument("--channel", type=int, default=0)
    snapshot_parser.add_argument("--output", help="Output file", required=True)

    subparsers.add_parser("reboot", help="Reboot the device")

    focus_mode = subparsers.add_parser("set-focus-mode", help="Set focus mode")
    focus_mode.add_argument("mode", choices=["Auto", "Manual", "SemiAuto", "Infinity"])
    focus_mode.add_argument("--channel", type=int, default=0)

    subparsers.add_parser("get-focus-mode", help="Get current focus mode")

    autofocus_parser = subparsers.add_parser("autofocus", help="Trigger auto focus")
    focusnear_parser = subparsers.add_parser("focus-near", help="Trigger focusnear")
    focusfar = subparsers.add_parser("focus-far", help="Trigger focusfar")

    autofocus_parser.add_argument("--channel", type=int, default=0)
    focusnear_parser.add_argument("--channel", type=int, default=0)
    focusfar.add_argument("--channel", type=int, default=0)

    return parser.parse_args()


def main():
    args = parse_args()
    cam = DahuaIPC(args.ip, args.username, args.password, port=args.port)

    if args.command == "device-info":
        print(cam.get_device_info())

    elif args.command == "channels":
        print("Available channels:", cam.get_available_channels())

    elif args.command == "snapshot":
        data = cam.take_snapshot(channel=args.channel)
        with open(args.output, "wb") as f:
            f.write(data)
        print(f"Snapshot saved to {args.output}")

    elif args.command == "reboot":
        print("Rebooting...")
        print(cam.reboot())

    elif args.command == "set-focus-mode":
        print(f"Setting focus mode to {args.mode}...")
        print(cam.set_focus_mode(mode=args.mode, channel=args.channel))

    elif args.command == "get-focus-mode":
        print("Current focus mode:", cam.get_focus_mode())

    elif args.command == "autofocus":
        print("Triggering autofocus...")
        print(cam.AutoFocus(channel=args.channel))
        
    elif args.command == "focus-near":
        print("Triggering focusnear...")
        print(cam.focus_near(channel=args.channel))
    
    elif args.command == "focus-far":
        print("Triggering focus-far...")
        print(cam.focus_far(channel=args.channel))
    else:
        print("Unknown command")
        sys.exit(1)
        
        
if __name__ == "__main__":
    main()