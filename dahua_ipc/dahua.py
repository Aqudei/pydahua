import requests
from requests.auth import HTTPDigestAuth

from dahua_ipc.utils import parse_table_like_response


DAY_NIGHT_COLOR_MAP = {
    0: "always multicolor",
    1: "autoswitch along with brightness",
    2: "always monochrome",
}

CONFIG_NO_MAP = {0: "normal", 1: "day", 2: "night"}


class DahuaCameraAPI:
    def __init__(self, host, username, password):
        self.base_url = f"http://{host}"  # e.g. 192.168.1.108
        self.auth = HTTPDigestAuth(username, password)

    def _get(self, path, params=None):
        url = f"{self.base_url}/{path}"
        response = requests.get(url, params=params, auth=self.auth)
        response.raise_for_status()
        return response.text

    def _set(self, path, params=None):
        url = f"{self.base_url}/{path}"
        response = requests.get(url, params=params, auth=self.auth)
        response.raise_for_status()
        return response.text

    def SetVideoInExposure(self, name, value, channel=0, configNo=0):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {
                "action": "setConfig",
                f"VideoInExposure[{channel}][{configNo}].{name}": value,
            },
        )

        return data

    def GetVideoInColor(self, channel=0):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {"action": "getConfig", "name": "VideoInColor"},
        )

        response = parse_table_like_response(data)
        return response.get("table", {}).get("VideoInColor", {}).get(f"{channel}")

    def SetVideoInColor(self, name, value, channel=0, configNo=0):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {
                "action": "setConfig",
                f"VideoInColor[{channel}][{configNo}].{name}": value,
            },
        )

        return data  # OK OR ERROR

    def GetVideoInSharpness(self):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {"action": "getConfig", "name": "VideoInSharpness"},
        )

        return parse_table_like_response(data)

    def SetVideoInSharpness(self, name, value, channel=0, config_no=0):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {
                "action": "setConfig",
                f"VideoInSharpness[{channel}][{config_no}].{name}": value,
            },
        )

        return data

    def GetVideoInExposure(self):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {"action": "getConfig", "name": "VideoInExposure"},
        )

        return parse_table_like_response(data)

    def GetVideoInOptionsConfig(self):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {"action": "getConfig", "name": "VideoInOptions"},
        )

        return parse_table_like_response(data)

    # 1 & 2: Color Mode
    def GetColorMode(self, channel=0):
        response = self.GetVideoInOptionsConfig()
        if not response:
            return

        j = parse_table_like_response(response)
        channel0_option = j.get("table", {}).get("VideoInOptions", [])[0]

        # return option code and description
        return channel0_option.get("DayNightColor", -1), DAY_NIGHT_COLOR_MAP.get(
            channel0_option.get("DayNightColor", -1)
        )

    def set_color_mode(self, mode, channel=0):
        # mode: 0 = Auto, 1 = Color, 2 = B/W
        return self._set(
            "cgi-bin/configManager.cgi",
            {"action": "setConfig", f"VideoInMode[{channel}].DayNightColor": mode},
        )

    # 3 & 4: Zoom Level
    def GetVideoInZoom(self):
        response = self._get(
            "cgi-bin/configManager.cgi", {"action": "getConfig", "name": "VideoInZoom"}
        )

        parsed = parse_table_like_response(response)
        return parsed

    def SetVideoInZoom(self, name, value, channel=0, config_no=0):
        return self._set(
            "cgi-bin/configManager.cgi",
            {
                "action": "setConfig",
                f"VideoInZoom[{channel}][{config_no}].{name}": value,
            },
        )

    # 5 & 6: Focus
    def GetFocusStatus(self, channel=0):
        response = self._get(
            "cgi-bin/devVideoInput.cgi",
            {"action": "getFocusStatus", "channel": channel},
        )

        return parse_table_like_response(response)

    def AdjustFocus(self, focus, zoom, channel=0):
        return self._set(
            "cgi-bin/devVideoInput.cgi",
            {"action": "adjustFocus", "channel": channel, "focus": focus, "zoom": zoom},
        )

    # 7: Autofocus
    def AutoFocus(self, channel=0):
        return self._set(
            "cgi-bin/devVideoInput.cgi", {"action": "autoFocus", "channel": channel}
        )

    def set_exposure(
        self,
        channel=0,
        config_no=0,
        gain=None,
        exposure=None,
        iris=None,
        shutter: bool = None,
    ):
        params = {
            "action": "setConfig",
        }
        if gain is not None:
            params[f"VideoInExposure[{channel}][{config_no}].Gain"] = gain
        if exposure is not None:
            params[f"VideoInExposure[{channel}][{config_no}].Compensation"] = exposure
        if iris is not None:
            params[f"VideoInExposure[{channel}][{config_no}].Iris"] = iris
        if shutter is not None:
            params[f"VideoInExposure[{channel}][{config_no}].SlowShutter"] = shutter

        return self._set("cgi-bin/configManager.cgi", params)
