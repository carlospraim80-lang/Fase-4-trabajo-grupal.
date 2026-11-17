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

# Ahora como el trabajo debe basarse en una arquitectura orientada a objetos.
# Empiezo a incluir lo siguiente:
# Una clase Astracta que representa entidades generales del sistema
# Representa los elementos generales del sistema.
class Entidad(ABC):

    def __init__(self, identificador):
        self._id = identificador

    @property
    def id(self):
        return self._id

    @abstractmethod
    def mostrar(self):
        pass
 
