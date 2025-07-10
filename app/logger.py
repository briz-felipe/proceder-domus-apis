# app/logger.py

import logging

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,  # use logging.DEBUG se quiser mais verbosidade
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Cria um logger com nome personalizado (opcional)
logger = logging.getLogger("mgm-api")