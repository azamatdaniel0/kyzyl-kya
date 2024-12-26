import requests
import json
from logger import get_logger
from typing import Any, List, Optional

logger = get_logger("DOLIBARR")


class Dolibarr:
    def __init__(
        self,
        host: str,
        entrypoint_get_camera_list: str,
        api_key: str,
        entrypoint_push_event: str,
    ) -> None:
        self.host: str = host
        self.entrypoint_get_camera_list: str = entrypoint_get_camera_list
        self.entrypoint_push_event: str = entrypoint_push_event
        self.api_key: str = api_key
        self.camera_data: Optional[List[dict]] = None

    def push_event(self, event_data: dict) -> None:
        headers = {"DOLAPIKEY": self.api_key}
        response: requests.Response = requests.post(
            f"{self.host}/{self.entrypoint_push_event}",
            headers=headers,
            json=event_data,
        )

        if response.status_code == 200:
            logger.debug("Event successfully pushed.")
        else:
            logger.error(
                f"Failed to push event. Status code: {response.status_code}, Response: {response.text}"
            )

    def get_camera_list(self) -> Optional[List[dict]]:
        """Fetches camera data from the API with DOLAPIKEY."""
        headers = {"DOLAPIKEY": self.api_key}
        response: requests.Response = requests.get(
            f"{self.host}/{self.entrypoint_get_camera_list}", headers=headers
        )
        if response.status_code == 200:
            self.camera_data = response.json()
            logger.debug("Camera data fetched successfully.")
            return self.camera_data
        else:
            logger.error(f"Error fetching data: {response.status_code}")
            return None

    def extract_camera_fields(self) -> Optional[List[dict]]:
        """Extract specific fields from the camera data."""
        if not self.camera_data:
            logger.warning("No camera data available. Fetching camera data.")
            self.get_camera_list()

        if self.camera_data:
            extracted_data = []
            for item in self.camera_data:
                logger.debug(f"Processing camera data: {item}")
                if (
                    item.get("username") is not None
                    and item.get("password") is not None
                    and item.get("porthttp") is not None
                    and item.get("portrtsp") is not None
                    and item.get("entrypointrtsp") is not None
                    and item.get("ipaddress") is not None
                    and item.get("status") == 1
                    and item.get("code") == "Camera_Checkpoint_Entrance"
                ):

                    extracted_data.append(
                        {
                            "status": item["status"],
                            "id": item["id"],
                            "code": item["code"],
                            "username": item["username"],
                            "password": item["password"],
                            "porthttp": item["porthttp"],
                            "portrtsp": item["portrtsp"],
                            "entrypointrtsp": item["entrypointrtsp"],
                            "ipaddress": item["ipaddress"],
                        }
                    )

                else:
                    logger.debug(f"Camera data skipped: {item}")

            if extracted_data:
                logger.debug("Camera fields extracted successfully.")
                return extracted_data
            else:
                logger.warning("No camera fields matched the criteria.")
                return None
        else:
            logger.error("Failed to extract camera fields due to missing camera data.")
            return None
