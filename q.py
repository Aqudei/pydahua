from onvif import ONVIFCamera
from zeep.exceptions import Fault

def check_onvif(ip, port, username, password):
    try:
        print(f"Connecting to {ip}:{port} using ONVIF...")

        # Create an ONVIF camera client
        camera = ONVIFCamera(ip, port, username, password)

        # Get basic device info
        device_info = camera.devicemgmt.GetDeviceInformation()

        print("\n✅ Connected successfully! Device info:")
        print(f"Manufacturer: {device_info.Manufacturer}")
        print(f"Model      : {device_info.Model}")
        print(f"Firmware   : {device_info.FirmwareVersion}")
        print(f"Serial No. : {device_info.SerialNumber}")
        print(f"Hardware ID: {device_info.HardwareId}")

        return camera

    except Fault as e:
        print(f"\n❌ ONVIF Fault: {e}")
    except Exception as e:
        print(f"\n❌ Error connecting to camera: {e}")
    return False

# Example usage
if __name__ == "__main__":
    ip = "127.0.0.1"
    port = 8000  # Change if needed (commonly 80, 8000, 8899)
    username = "admin"
    password = "Password1"

    camera = check_onvif(ip, port, username, password)
    
    if camera:
        # Get media and imaging services
        media_service = camera.create_media_service()
        imaging_service = camera.create_imaging_service()

        # Get the first video source token
        profile = media_service.GetProfiles()[0]
        video_source_token = profile.VideoSourceConfiguration.SourceToken

        # Get current imaging settings
        imaging_settings = imaging_service.GetImagingSettings({'VideoSourceToken': video_source_token})

        # Modify focus mode
        imaging_settings.Focus.AutoFocusMode = 'AUTO'  # or 'AUTO'

        # Apply the new settings
        imaging_service.SetImagingSettings({
            'VideoSourceToken': video_source_token,
            'ImagingSettings': imaging_settings,
            'ForcePersistence': True
        })

        print("Focus mode updated.")
