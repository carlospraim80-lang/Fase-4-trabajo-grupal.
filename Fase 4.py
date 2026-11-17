# Proyecto: Sistema integral de gestión de clientes, servicios y reservas.
# A continuación voy a importar las herramientas necesarias que estan en python para el programa.
from abc import ABC, abstractmethod
import logging
import os
import re
# Ahora configuro lo que es registros y excepciones, primeramente ya que lo pide el anexo.
# Creo la carpeta para guardar los registros.
os.makedirs("logs", exist_ok=True)
# Configuro el archivo donde se guarden los eventos y errores.
logging.basicConfig(
    filename="logs/software_fj.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
    force=True)

logger = logging.getLogger("SoftwareFJ")
# Creo excepciones propias para controlar errores.
class ErrorSistema(Exception):
    pass


class DatosInvalidosError(ErrorSistema):
    pass


class ServicioNoDisponibleError(ErrorSistema):
    pass


class ReservaError(ErrorSistema):
    pass
  
