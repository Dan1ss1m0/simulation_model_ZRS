import logging

logging.basicConfig(level=logging.INFO, filename="./src/last_start_logs.log",filemode="w",
                     format="%(asctime)s %(levelname)s: %(message)s")

logger = logging.getLogger('model')