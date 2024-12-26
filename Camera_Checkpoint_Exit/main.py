from services.traffic_monitor import start_traffic_monitor
from logger import setup_logging, get_logger
from services.dolibarr import Dolibarr
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

setup_logging()

logger = get_logger("MAIN")
dolibarr = Dolibarr(
    host="http://192.168.6.29/htdocs/api/index.php/equipmentsapi",
    entrypoint_get_camera_list="cameras?sortfield=t.rowid&sortorder=ASC&limit=100",
    entrypoint_push_event="autovisionhistorys",
    api_key="MpauKZ043hqeA3r6GQlne57AX5j8BN2S",
)


def start_monitor_for_camera(camera):
    try:
        camera_ip = camera.get("ipaddress", "10.118.210.122")
        camera_port = camera.get("port", 37777)
        camera_username = camera.get("username", "admin")
        camera_password = camera.get("password", "petabyte2024")
        camera_code = camera.get("code", 0)
        camera_id = camera.get("id", 0)

        logger.info(
            f"Starting traffic monitor for camera {camera['code']} at {camera_ip}:{camera_port}"
        )
        start_traffic_monitor(
            camera_ip,
            camera_port,
            camera_username,
            camera_password,
            camera_code,
            camera_id,
        )

    except Exception as e:
        logger.error(f"Failed to start monitor for camera {camera['code']}: {e}")
        return camera["code"], False
    return camera["code"], True


def start_monitor_for_cameras_parallel(camera_fields):
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_camera = {
            executor.submit(start_monitor_for_camera, camera): camera
            for camera in camera_fields
        }

        for future in as_completed(future_to_camera):
            camera = future_to_camera[future]
            try:
                camera_id, result = future.result()
                if result:
                    logger.info(
                        f"Successfully started traffic monitor for camera {camera_id}"
                    )
                else:
                    logger.error(
                        f"Failed to start traffic monitor for camera {camera_id}"
                    )
            except Exception as exc:
                logger.error(f"Camera {camera['code']} generated an exception: {exc}")


if __name__ == "__main__":
    # Fetch and extract the camera data
    camera_fields = dolibarr.extract_camera_fields()
    if camera_fields:
        logger.info(json.dumps(camera_fields, indent=4))
        start_monitor_for_cameras_parallel(camera_fields)
    else:
        logger.error("No camera data available to start traffic monitor.")
