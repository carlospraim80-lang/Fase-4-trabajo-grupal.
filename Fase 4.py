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
# Creo una clase abstracta Servicio y al menos tres servicios especializados que hereden de ella.
# Defino las caracteristicas comunes de los servicios.
class Servicio(Entidad, ABC):

    contador = 1

    def __init__(self, nombre, precio):

        if not nombre.strip() or precio <= 0:
            raise DatosInvalidosError("Nombre o precio incorrecto.")

        super().__init__(Servicio.contador)
        Servicio.contador += 1

        self.nombre = nombre
        self.precio = precio
        self.disponible = True

    # Metodo con parametros opcionales para variar el calculo.
    @abstractmethod
    def calcular_costo(self, horas, impuesto=0, descuento=0):
        pass

    @abstractmethod
    def describir(self):
        pass

    def validar(self, horas):

        if not self.disponible:
            raise ServicioNoDisponibleError("El servicio no esta disponible.")

        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
            raise DatosInvalidosError("La duracion debe ser mayor que cero.")

        if not 0 <= impuesto_valido(0) <= 100:
            raise DatosInvalidosError("Parametro incorrecto.")


# Funcion para validar parametros porcentuales.
def impuesto_valido(valor):
    return valor
#-----
# Servicios especializados (Subclases)
# Cada servicio hereda de Servicio y redefine sus metodos.
class Sala(Servicio):

    def __init__(self, nombre, precio, capacidad):
        super().__init__(nombre, precio)

        if capacidad <= 0:
            raise DatosInvalidosError("Capacidad incorrecta.")

        self.capacidad = capacidad

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        self.validar(horas)

        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise DatosInvalidosError("Impuesto o descuento incorrecto.")

        subtotal = self.precio * horas
        return round(subtotal * (1 + impuesto / 100) * (1 - descuento / 100), 2)

    def describir(self):
        return f"Sala {self.nombre} - Capacidad: {self.capacidad} personas"


class Equipo(Servicio):

    def __init__(self, nombre, precio, cantidad):
        super().__init__(nombre, precio)

        if cantidad <= 0:
            raise DatosInvalidosError("Cantidad incorrecta.")

        self.cantidad = cantidad

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        self.validar(horas)

        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise DatosInvalidosError("Impuesto o descuento incorrecto.")

        subtotal = self.precio * horas
        return round(subtotal * (1 + impuesto / 100) * (1 - descuento / 100), 2)

    def describir(self):
        return f"Alquiler de {self.nombre} - Cantidad: {self.cantidad}"


class Asesoria(Servicio):

    def __init__(self, nombre, precio, especialidad):
        super().__init__(nombre, precio)

        if not especialidad.strip():
            raise DatosInvalidosError("La especialidad es obligatoria.")

        self.especialidad = especialidad

    def calcular_costo(self, horas, impuesto=0, descuento=0):
        self.validar(horas)

        if not 0 <= impuesto <= 100 or not 0 <= descuento <= 100:
            raise DatosInvalidosError("Impuesto o descuento incorrecto.")

        subtotal = self.precio * horas
        return round(subtotal * (1 + impuesto / 100) * (1 - descuento / 100), 2)

    def describir(self):
        return f"Asesoria {self.nombre} - Especialidad: {self.especialidad}"
#  Creo una clase Reserva
# Relaciona un cliente con el servicio que desea utilizar.
class Reserva(Entidad):

    contador = 1

    def __init__(self, cliente, servicio, horas):

        if not isinstance(cliente, Cliente) or not isinstance(servicio, Servicio):
            raise ReservaError("Cliente o servicio incorrecto.")

        if isinstance(horas, bool) or not isinstance(horas, (int, float)) or horas <= 0:
            raise ReservaError("La duracion de la reserva no es valida.")

        super().__init__(Reserva.contador)
        Reserva.contador += 1

        self.cliente = cliente
        self.servicio = servicio
        self.horas = horas
        self.estado = "Pendiente"
        self.costo = 0

    # Proceso y confirmo la reserva.
    def confirmar(self, impuesto=0, descuento=0):

        try:
            self.costo = self.servicio.calcular_costo(
                self.horas, impuesto, descuento
            )

        except Exception as error:
            logger.exception("Error al procesar la reserva.")

            # Encadeno el error original con uno personalizado.
            raise ReservaError("No se pudo procesar la reserva.") from error

        else:
            self.estado = "Confirmada"
            print("Reserva confirmada correctamente.")

        finally:
            logger.info(f"Finalizo el procesamiento de reserva {self.id}.")

    def cancelar(self):

        if self.estado != "Pendiente" and self.estado != "Confirmada":
            raise ReservaError("La reserva no se puede cancelar.")

        self.estado = "Cancelada"
        logger.info(f"Reserva {self.id} cancelada.")

    def mostrar(self):
        return (f"Reserva {self.id} | Cliente: {self.cliente.nombre} | "
                f"Servicio: {self.servicio.nombre} | Estado: {self.estado} | "
                f"Costo: ${self.costo}")
# Creo listas internas del sistema.
# Guardo los objetos en listas, sin utilizar bases de datos.
clientes = []
servicios = []
reservas = []
#---
# Funciones de gestios 
def registrar_cliente(nombre, correo, telefono):

    try:
        cliente = Cliente(nombre, correo, telefono)

        if any(c._Cliente__correo == correo.lower().strip() for c in clientes):
            raise DatosInvalidosError("El correo ya esta registrado.")

        clientes.append(cliente)
        logger.info(f"Cliente registrado: {nombre}")
        print(cliente.mostrar())
        return cliente

    except ErrorSistema as error:
        logger.exception("Error al registrar cliente.")
        print("Error:", error)
        return None

    finally:
        print("Finalizo el registro del cliente.")


def crear_reserva(cliente, servicio, horas):

    try:
        reserva = Reserva(cliente, servicio, horas)
        reservas.append(reserva)
        logger.info(f"Reserva {reserva.id} creada.")
        print("Reserva creada correctamente.")
        return reserva

    except ErrorSistema as error:
        logger.exception("Error al crear reserva.")
        print("Error:", error)
        return None
#----        
# Pruebas automaticas: 10 operaciones
def ejecutar_pruebas():

    print("\n===== PRUEBAS DE SOFTWARE FJ =====")

    # 1. Registro de cliente valido.
    c1 = registrar_cliente("Carlos Perez", "carlos@gmail.com", "3101234567")

    # 2. Registro de cliente invalido.
    registrar_cliente("Andres", "correo_malo", "3001234567")

    # 3. Registro de otro cliente valido.
    c2 = registrar_cliente("Laura Gomez", "laura@gmail.com", "3201234567")

    # 4. Creacion de sala.
    sala = Sala("Sala principal", 50000, 10)
    servicios.append(sala)
    print("4. Servicio creado:", sala.describir())

    # 5. Creacion de alquiler de equipos.
    equipo = Equipo("Computador", 15000, 5)
    servicios.append(equipo)
    print("5. Servicio creado:", equipo.describir())

    # 6. Creacion de asesoria.
    asesoria = Asesoria("Asesoria tecnica", 80000, "Programacion")
    servicios.append(asesoria)
    print("6. Servicio creado:", asesoria.describir())

    # 7. Intento de crear un servicio con precio invalido.
    try:
        Sala("Sala incorrecta", -5000, 10)
    except ErrorSistema as error:
        logger.exception("Error al crear servicio.")
        print("7. Servicio rechazado:", error)

    # 8. Creacion de una reserva correcta.
    r1 = crear_reserva(c1, sala, 2)

    # 9. Confirmacion de reserva con impuesto y descuento.
    if r1:
        r1.confirmar(impuesto=19, descuento=10)
        print(r1.mostrar())

    # 10. Reserva con servicio no disponible.
    equipo.disponible = False
    r2 = crear_reserva(c2, equipo, 2)

    if r2:
        try:
            r2.confirmar()
        except ReservaError as error:
            logger.exception("Fallo al confirmar reserva.")
            print("10. Reserva fallida:", error)

    # Operaciones adicionales de cancelacion y calculo.
    if r1:
        r1.cancelar()
        print("Reserva cancelada:", r1.mostrar())

    print("\nTotal clientes:", len(clientes))
    print("Total servicios:", len(servicios))
    print("Total reservas:", len(reservas))

    logger.info("Pruebas automaticas finalizadas.")
    
# Menu principal por consola.
# -----
def menu():

    while True:
        print("\n====== SISTEMA SOFTWARE FJ ======")
        print("1. Registrar cliente")
        print("2. Consultar clientes")
        print("3. Consultar servicios")
        print("4. Crear reserva")
        print("5. Confirmar reserva")
        print("6. Cancelar reserva")
        print("7. Consultar reservas")
        print("8. Ejecutar pruebas automaticas")
        print("0. Salir")

        try:
            opcion = input("Seleccione una opcion: ").strip()

            if opcion == "1":
                registrar_cliente(
                    input("Nombre: "),
                    input("Correo: "),
                    input("Telefono: "))

            elif opcion == "2":
                for c in clientes:
                    print(c.mostrar())

            elif opcion == "3":
                for s in servicios:
                    print(s.id, s.describir())

            elif opcion == "4":
                id_c = int(input("ID del cliente: "))
                id_s = int(input("ID del servicio: "))

                c = next((x for x in clientes if x.id == id_c), None)
                s = next((x for x in servicios if x.id == id_s), None)

                if c is None or s is None:
                    raise ReservaError("Cliente o servicio no encontrado.")

                horas = float(input("Duracion en horas: "))
                crear_reserva(c, s, horas)

            elif opcion == "5":
                id_r = int(input("ID de reserva: "))
                r = next((x for x in reservas if x.id == id_r), None)

                if r is None:
                    raise ReservaError("Reserva no encontrada.")

                r.confirmar(impuesto=19)

            elif opcion == "6":
                id_r = int(input("ID de reserva: "))
                r = next((x for x in reservas if x.id == id_r), None)

                if r is None:
                    raise ReservaError("Reserva no encontrada.")

                r.cancelar()
                print("Reserva cancelada.")

            elif opcion == "7":
                for r in reservas:
                    print(r.mostrar())

            elif opcion == "8":
                ejecutar_pruebas()

            elif opcion == "0":
                print("Gracias por utilizar Software FJ.")
                logger.info("Sistema cerrado por el usuario.")
                break

            else:
                raise DatosInvalidosError("Opcion incorrecta.")

        except (ValueError, ErrorSistema) as error:
            logger.exception("Error controlado en el menu.")
            print("No se pudo realizar la operacion:", error)

        except Exception as error:
            logger.exception("Error inesperado en el sistema.")
            print("Se presento un error inesperado:", error)

        else:
            logger.info(f"Operacion de menu {opcion} finalizada.")

        finally:
            print("Fin de la operacion.")
#-------------------
# Inicio del programa.

if __name__ == "__main__":

    try:
        logger.info("Inicio del sistema Software FJ.")
        menu()

    except KeyboardInterrupt:
        print("\nPrograma interrumpido.")

    finally:
        logger.info("Finalizacion del sistema Software FJ.")
        print("Sistema finalizado.")



        
