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

        return response.get("table.VideoInColor", {}).get(channel)

    def SetVideoInColor(self, name, value, channel=0, configNo=0):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {
                "action": "setConfig",
                f"VideoInColor[{channel}][{configNo}].{name}": value,
            },
        )

        return data  # OK OR ERROR

    def GetVideoInSharpness(self, channel=0):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {"action": "getConfig", "name": "VideoInSharpness"},
        )

        response = parse_table_like_response(data)

        return response.get("table.VideoInSharpness", {}).get(channel)

    def SetVideoInSharpness(self, name, value, channel=0, config_no=0):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {
                "action": "setConfig",
                f"VideoInSharpness[{channel}][{config_no}].{name}": value,
            },
        )

        return data

    def GetVideoInExposure(self, channel=0):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {"action": "getConfig", "name": "VideoInExposure"},
        )

        response = parse_table_like_response(data)

        return response.get("table.VideoInExposure", {}).get(channel)

    def GetVideoInOptionsConfig(self, channel=0):
        data = self._get(
            "cgi-bin/configManager.cgi",
            {"action": "getConfig", "name": "VideoInOptions"},
        )

        r = parse_table_like_response(data)
        return r.get("table.VideoInOptions", {}).get(channel)

    # 1 & 2: Color Mode
    def GetColorMode(self, channel=0):
        response = self.GetVideoInOptionsConfig(channel)
        if not response:
            return

        # return option code and description
        return response.get("DayNightColor", -1), DAY_NIGHT_COLOR_MAP.get(
            response.get("DayNightColor", -1)
        )

    # 3 & 4: Zoom Level
    def GetVideoInZoom(self, channel=0):
        response = self._get(
            "cgi-bin/configManager.cgi", {"action": "getConfig", "name": "VideoInZoom"}
        )

        parsed = parse_table_like_response(response)
        return parsed.get("table.VideoInZoom", {}).get(channel)

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

        r = parse_table_like_response(response)
        return r.get("status")

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

    def Command(self, cgi, params):
        cgi_path = cgi if cgi.endswith(".cgi") else f"{cgi}.cgi"
        return self._get(f"cgi-bin/{cgi_path}", params)
