from logger import get_logger
import os
import requests
import base64
import re

logger = get_logger("AUTOVISION")


class StateNumberDetector:
    def __init__(self, api_url: str, timeout: int = 100):
        self.api_url = api_url
        self.timeout = timeout

    def detect_state_number(self, jpeg_path: str, camera_code, camera_id, a) -> dict:
        if not os.path.exists(jpeg_path):
            logger.warning(f"Image not found: {jpeg_path}")
            return {}

        try:
            # with open(jpeg_path, "rb") as file:
            #     response = requests.post(
            #         self.api_url,
            #         files={"file": file},
            #         timeout=self.timeout,
            #     )
            #
            # response.raise_for_status()
            # auto = response.json()
            #
            # logger.debug(
            #     f"Detected state number for event {jpeg_path}: {auto['data']['license_plate_number']}"
            # )

            return self._prepare_data(jpeg_path, camera_code, camera_id, a)

        except (requests.RequestException, KeyError) as e:
            logger.error(f"Error detecting state number in {jpeg_path}: {e}")
            return {}

    def transform_license_plate(self, plate: str) -> str:
        """
        Проверяет номер машины и добавляет 'KG' после второго символа, 
        если номер начинается с '0', за ним идут цифры, а последние символы - буквы.
        
        :param plate: Строка с номером машины.
        :return: Преобразованный номер или оригинальный, если условия не выполнены.
        """
        # Шаблон для проверки номера
        pattern = r"^0\d*[A-Za-z]+$"
        
        if re.match(pattern, plate):
            # Добавляем 'KG' после второго символа
            return plate[:2] + "KG" + plate[2:]
        return plate

    def _prepare_data(
        self, jpeg_path: str, camera_code: str, camera_id: int, a
    ) -> dict:
        logger.info("+++++++++++++++++++++++++++++++")
        logger.info(a["plate_number_str"])
        logger.info(type(a["plate_number_str"]))
        logger.info(type(str(a["plate_number_str"])))
        logger.info("+++++++++++++++++++++++++++++++")
        test = self.transform_license_plate(a['plate_number_str'])
        logger.info(f"new plate {test}")
        with open(jpeg_path, "rb") as file:
            encoded_image = base64.b64encode(file.read()).decode("utf-8")

        data = {
            "module": "equipments",
            "ref": "(PROV)",
            "status": 0,
            "label": a["plate_number_str"],
            "photocontent": encoded_image,
            "licenseplatenumber": a["plate_number_str"],
            "licenseplatenumberscore": 0.00,
            "licenseplatecountrycode": "Dahua",
            "licenseplatecountryscore": 0.00,
            "carbrandcode": a["object_subType_str"],
            "carbrandscore": "0.00",
            "carcolorcode": a["vehicle_color_str"],
            "carcolorscore": 0.00,
            "cartypebodycode": a["object_subType_str"],
            "cartypebodyscore": 0.00,
            "camera": camera_id,
            "cameracode": camera_code,
        }

        return data
