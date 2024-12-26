from NetSDK.NetSDK import NetClient
from services.callbacks import Callbacks
from NetSDK.SDK_Enum import EM_LOGIN_SPAC_CAP_TYPE, EM_EVENT_IVS_TYPE
from NetSDK.SDK_Callback import (
    NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY,
    NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY,
)
from ctypes import sizeof
import time
from logger import get_logger

logger = get_logger("TRAFFIC MONITOR")


def start_traffic_monitor(
    camera_ip: str,
    camera_port: int,
    camera_username: str,
    camera_password: str,
    camera_code: str,
    camera_id: int,
) -> None:
    sdk = NetClient()
    sdk.InitEx(None)
    sdk.SetAutoReconnect(None)

    stuInParam = NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY()
    stuInParam.dwSize = sizeof(NET_IN_LOGIN_WITH_HIGHLEVEL_SECURITY)
    stuInParam.szIP = camera_ip.encode()
    stuInParam.nPort = camera_port
    stuInParam.szUserName = camera_username.encode()
    stuInParam.szPassword = camera_password.encode()
    stuInParam.emSpecCap = EM_LOGIN_SPAC_CAP_TYPE.TCP
    stuInParam.pCapParam = None

    stuOutParam = NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY()
    stuOutParam.dwSize = sizeof(NET_OUT_LOGIN_WITH_HIGHLEVEL_SECURITY)

    loginID, device_info, error_msg = sdk.LoginWithHighLevelSecurity(
        stuInParam, stuOutParam
    )

    if not loginID:
        logger.error(f"Login failed: {error_msg}")
        return

    logger.info(f"Login successful. Channels available: {device_info.nChanNum}")
    callbacks = Callbacks()
    callbacks.set_camera_info(camera_code=camera_code, camera_id=camera_id)
    channel = 0
    attachID = sdk.RealLoadPictureEx(
        loginID,
        channel,
        EM_EVENT_IVS_TYPE.TRAFFICJUNCTION,
        1,
        callbacks.AnalyzerDataCallBack,
        0,
        None,
    )

    if not attachID:
        logger.error(f"Subscription failed: {sdk.GetLastError()}")
        sdk.Logout(loginID)
        return

    logger.info(
        "Subscription to traffic junction events successful. Monitoring started."
    )

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Stopping the monitoring...")

    sdk.StopLoadPic(attachID)
    sdk.Logout(loginID)
    sdk.Cleanup()
    logger.info("Cleaned up and exited successfully.")
