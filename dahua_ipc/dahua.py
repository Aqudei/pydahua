import requests
from requests.auth import HTTPDigestAuth


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

    # 1 & 2: Color Mode
    def get_color_mode(self, channel=0):
        data = self._get("cgi-bin/configManager.cgi", {
            "action": "getConfig",
            "name": f"VideoInMode[{channel}]"
        })
        return data

    def set_color_mode(self, mode, channel=0):
        # mode: 0 = Auto, 1 = Color, 2 = B/W
        return self._set("cgi-bin/configManager.cgi", {
            "action": "setConfig",
            f"VideoInMode[{channel}].Mode": mode
        })

    # 3 & 4: Zoom Level
    def get_zoom_level(self, channel=0):
        return self._get("cgi-bin/devVideoInput.cgi", {
            "action": "getZoom",
            "channel": channel
        })

    def set_zoom_level(self, zoom, channel=0):
        return self._set("cgi-bin/devVideoInput.cgi", {
            "action": "setZoom",
            "channel": channel,
            "zoom": zoom
        })

    # 5 & 6: Focus
    def get_focus(self, channel=0):
        return self._get("cgi-bin/devVideoInput.cgi", {
            "action": "getFocus",
            "channel": channel
        })

    def set_focus(self, focus, channel=0):
        return self._set("cgi-bin/devVideoInput.cgi", {
            "action": "setFocus",
            "channel": channel,
            "focus": focus
        })

    # 7: Autofocus
    def autofocus(self, channel=0):
        return self._set("cgi-bin/devVideoInput.cgi", {
            "action": "autoFocus",
            "channel": channel
        })

    # 8a-d: Exposure Settings
    def get_exposure(self, channel=0):
        return self._get("cgi-bin/configManager.cgi", {
            "action": "getConfig",
            f"name": f"VideoInExposure[{channel}]"
        })

    def set_exposure(self, channel=0, gain=None, exposure=None, iris=None, shutter=None):
        params = {
            "action": "setConfig",
        }
        if gain is not None:
            params[f"VideoInExposure[{channel}].Gain"] = gain
        if exposure is not None:
            params[f"VideoInExposure[{channel}].ExposureCompensation"] = exposure
        if iris is not None:
            params[f"VideoInExposure[{channel}].Iris"] = iris
        if shutter is not None:
            params[f"VideoInExposure[{channel}].Shutter"] = shutter

        return self._set("cgi-bin/configManager.cgi", params)

    # 9a-e: Image Settings
    def get_image_settings(self, channel=0):
        return self._get("cgi-bin/configManager.cgi", {
            "action": "getConfig",
            f"name": f"VideoInImage[{channel}]"
        })

    def set_image_settings(self, channel=0, brightness=None, contrast=None, saturation=None, sharpness=None, gamma=None):
        params = {
            "action": "setConfig",
        }
        if brightness is not None:
            params[f"VideoInImage[{channel}].Brightness"] = brightness
        if contrast is not None:
            params[f"VideoInImage[{channel}].Contrast"] = contrast
        if saturation is not None:
            params[f"VideoInImage[{channel}].Saturation"] = saturation
        if sharpness is not None:
            params[f"VideoInImage[{channel}].Sharpness"] = sharpness
        if gamma is not None:
            params[f"VideoInImage[{channel}].Gamma"] = gamma

        return self._set("cgi-bin/configManager.cgi", params)
