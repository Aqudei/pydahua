# dahua_ipc/__init__.py

import requests
from requests.auth import HTTPDigestAuth
from .logging_config import setup_logger

FOCUS_MODE_MAP = {"0": "Manual", "1": "Auto", "2": "SemiAuto", "3": "Infinity"}

FOCUS_MODE_REVERSE_MAP = {v: int(k) for k, v in FOCUS_MODE_MAP.items()}


class DahuaIPC:
    def __init__(self, ip, username, password, port=80):
        self.base_url = f"http://{ip}:{port}/cgi-bin"
        self.auth = HTTPDigestAuth(username, password)
        self.logger = setup_logger()

    def _get(self, path, params=None):
        url = f"{self.base_url}/{path}"
        try:
            self.logger.debug(f"GET {url} params={params}")
            response = requests.get(url, auth=self.auth, params=params, timeout=10)
            response.raise_for_status()
            self.logger.debug(f"Response: {response.status_code}")
            return response.text
        except requests.RequestException as e:
            self.logger.error(f"HTTP request failed: {e}")
            raise RuntimeError(f"Request failed: {e}")

    def SetVideoInOptionsConfig(self, channel=0, key=None, value=None):

        return self._get(
            "configManager.cgi",
            {"action": "setConfig", f"VideoInOptions[{channel}].{key}": value},
        )
        
    def GetVideoInOptionsConfig(self):

        return self._get(
            "configManager.cgi", {"action": "getConfig", "name": "VideoInOptions"}
        )

    def GetVideoInputCaps(self, channel=0):
        return self._get(
            "devVideoInput.cgi", {"action": "getCaps", "channel": channel}
        )

    def AutoFocus(self, channel=0):
        return self._get(
            "devVideoInput.cgi", {"action": "autoFocus", "channel": channel}
        )
        
    def GetVideoColorConfig(self):
        return self._get(
            "configManager.cgi", {"action": "getConfig", "name": "VideoColor"}
        )    
    
    def SetColorConfig(self, paramName, paramValue):
        return self._get(
            "configManager.cgi", {"action": "setConfig", f"{paramName}": paramValue}
        )    
    
    
    def ptz_control(self, action, channel=0, code="Left", arg1=0, arg2=1, arg3=0):
        """
        PTZ control example: code="Left", action="start"/"stop"
        """
        params = {
            "action": action,
            "channel": channel,
            "code": code,
            "arg1": arg1,
            "arg2": arg2,
            "arg3": arg3,
        }

        return self._get("ptz.cgi", params)

    def reboot(self):
        return self._get("reboot.cgi")

    def get_focus_mode(self, channel=0):
        """
        Get current focus mode for a given channel.
        """
        result = self._get(
            "configManager.cgi",
            {"action": "getConfig", "name": f"VideoInFocus[{channel}]"},
        )

        for line in result.splitlines():
            if "FocusMode=" in line or "Mode" in line:
                return line.split("=")[1].strip()
        return None

    def focus_near(self, action="start", channel=0):
        return self.ptz_control(action=action, code="FocusNear", channel=channel)

    def focus_far(self, action="start", channel=0):
        return self.ptz_control(action=action, code="FocusFar", channel=channel)

    def get_color_mode(self, channel=0):
        result = self._get(
            "configManager.cgi",
            {"action": "getConfig", "name": f"VideoInMode[{channel}]"},
        )
        for line in result.splitlines():
            if "ColorMode=" in line:
                return line.split("=")[1].strip()
        return None

    def set_color_mode(self, mode, channel=0):
        return self._get(
            "configManager.cgi",
            {"action": "setConfig", "VideoInMode[{}].ColorMode".format(channel): mode},
        )

    def get_zoom_level(self, channel=0):
        result = self._get("ptz.cgi", {"action": "query", "channel": channel})
        for line in result.splitlines():
            if "zoom=" in line:
                return float(line.split("=")[1].strip())
        return None

    def set_zoom_level(self, level, channel=0):
        return self._get(
            "ptz.cgi",
            {"action": "set", "channel": channel, "code": "Zoom", "value": level},
        )

    def get_focus_level(self, channel=0):
        result = self._get("ptz.cgi", {"action": "query", "channel": channel})
        for line in result.splitlines():
            if "focus=" in line:
                return float(line.split("=")[1].strip())
        return None

    def set_focus_level(self, level, channel=0):
        return self._get(
            "ptz.cgi",
            {"action": "set", "channel": channel, "code": "Focus", "value": level},
        )

    def get_exposure_settings(self, channel=0):
        result = self._get(
            "configManager.cgi",
            {"action": "getConfig", "name": f"VideoInExposure[{channel}]"},
        )
        settings = {}
        for line in result.splitlines():
            if "=" in line:
                k, v = line.strip().split("=", 1)
                settings[k.split(".")[-1]] = v
        return settings

    def set_exposure_settings(self, channel=0, **kwargs):
        """
        kwargs: Gain, Iris, ExposureCompensation, ExposureTime, etc.
        """
        config = {f"VideoInExposure[{channel}].{k}": v for k, v in kwargs.items()}
        return self._get("configManager.cgi", {"action": "setConfig", **config})

    def get_image_settings(self, channel=0):
        result = self._get(
            "configManager.cgi",
            {"action": "getConfig", "name": f"VideoInImage[{channel}]"},
        )
        settings = {}
        for line in result.splitlines():
            if "=" in line:
                k, v = line.strip().split("=", 1)
                settings[k.split(".")[-1]] = v
        return settings

    def set_image_settings(self, channel=0, **kwargs):
        config = {f"VideoInImage[{channel}].{k}": v for k, v in kwargs.items()}
        return self._get("configManager.cgi", {"action": "setConfig", **config})

    def get_available_channels(self):
        """
        Returns a list of available channel indices from the device.
        """
        result = self._get(
            "configManager.cgi", {"action": "getConfig", "name": "ChannelTitle"}
        )
        channels = []
        for line in result.splitlines():
            if "table.ChannelTitle[" in line:
                try:
                    idx = int(line.split("[")[1].split("]")[0])
                    channels.append(idx)
                except (IndexError, ValueError):
                    continue
        return sorted(set(channels))
