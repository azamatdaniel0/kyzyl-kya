from logger import setup_logging, get_logger
from services.dolibarr import Dolibarr
from frigate.mqtt_client import start_mqtt_client

setup_logging()

logger = get_logger("MAIN FRIGATE")
dolibarr = Dolibarr(
    host="http://192.168.6.29/htdocs/api/index.php/equipmentsapi",
    entrypoint_get_camera_list="cameras?sortfield=t.rowid&sortorder=ASC&limit=100",
    entrypoint_push_event="autovisionhistorys",
    api_key="MpauKZ043hqeA3r6GQlne57AX5j8BN2S",
)

if __name__ == "__main__":
    start_mqtt_client()
