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
 # Una clase Cliente con validaciones robustas y encapsulación de datos personales.
# Permite registrar clientes y proteger sus datos.
class Cliente(Entidad):

    contador = 1

    def __init__(self, nombre, correo, telefono):

        # Valido los datos antes de crear el cliente.
        if not nombre.strip():
            raise DatosInvalidosError("El nombre es obligatorio.")

        if not re.match(r"^[\w.+-]+@[\w.-]+\.[a-zA-Z]{2,}$", correo):
            raise DatosInvalidosError("El correo no es valido.")

        if not telefono.isdigit() or not 7 <= len(telefono) <= 15:
            raise DatosInvalidosError("El telefono no es valido.")

        super().__init__(Cliente.contador)
        Cliente.contador += 1

        # Los datos personales quedan encapsulados.
        self.__nombre = nombre.strip()
        self.__correo = correo.lower().strip()
        self.__telefono = telefono

    @property
    def nombre(self):
        return self.__nombre

    def mostrar(self):
        return f"ID: {self.id} | {self.nombre} | {self.__correo} | {self.__telefono}"
