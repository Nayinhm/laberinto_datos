from typing import Dict, List, Optional, Set


class Asignatura:
    """Representa una asignatura universitaria con código y nombre."""

    def __init__(self, codigo: str, nombre: str) -> None:
        self.codigo = self.normalizar_codigo(codigo)
        self.nombre = nombre.strip()

    @staticmethod
    def normalizar_codigo(codigo: str) -> str:
        """Limpia espacios y estandariza el código en mayúsculas."""
        return codigo.strip().upper()

    def __str__(self) -> str:
        return f"{self.codigo} - {self.nombre}"


class NodoABB:
    """Nodo de un Árbol Binario de Búsqueda indexado por código de asignatura."""

    def __init__(self, codigo: str) -> None:
        self.codigo = codigo
        self.izquierdo: Optional["NodoABB"] = None
        self.derecho: Optional["NodoABB"] = None


class ArbolBinarioBusqueda:
    """Estructura ABB basada en nodos para almacenar y buscar códigos."""

    def __init__(self) -> None:
        self.raiz: Optional[NodoABB] = None

    def insertar(self, codigo: str) -> None:
        """Inserta un código en el árbol manteniendo el orden ABB."""
        codigo_limpio = Asignatura.normalizar_codigo(codigo)
        self.raiz = self._insertar_recursivo(self.raiz, codigo_limpio)

    def _insertar_recursivo(self, actual: Optional[NodoABB], codigo: str) -> NodoABB:
        if actual is None:
            return NodoABB(codigo)
        if codigo < actual.codigo:
            actual.izquierdo = self._insertar_recursivo(actual.izquierdo, codigo)
        elif codigo > actual.codigo:
            actual.derecho = self._insertar_recursivo(actual.derecho, codigo)
        return actual

    def buscar(self, codigo: str) -> bool:
        """Busca si un código existe en el árbol."""
        codigo_limpio = Asignatura.normalizar_codigo(codigo)
        return self._buscar_recursivo(self.raiz, codigo_limpio)

    def _buscar_recursivo(self, actual: Optional[NodoABB], codigo: str) -> bool:
        if actual is None:
            return False
        if codigo == actual.codigo:
            return True
        if codigo < actual.codigo:
            return self._buscar_recursivo(actual.izquierdo, codigo)
        return self._buscar_recursivo(actual.derecho, codigo)

    def recorrido_inorden(self) -> List[str]:
        """Devuelve los códigos almacenados en orden ascendente."""
        recorrido: List[str] = []
        self._inorden_recursivo(self.raiz, recorrido)
        return recorrido

    def _inorden_recursivo(self, actual: Optional[NodoABB], recorrido: List[str]) -> None:
        if actual is not None:
            self._inorden_recursivo(actual.izquierdo, recorrido)
            recorrido.append(actual.codigo)
            self._inorden_recursivo(actual.derecho, recorrido)


class GrafoAsignaturas:
    """Grafo dirigido para representar relaciones entre asignaturas."""

    def __init__(self) -> None:
        self.adyacencia: Dict[str, List[str]] = {}

    def agregar_nodo(self, codigo: str) -> None:
        """Registra un nodo en el grafo si aún no existe."""
        codigo_limpio = Asignatura.normalizar_codigo(codigo)
        if codigo_limpio not in self.adyacencia:
            self.adyacencia[codigo_limpio] = []

    def agregar_relacion(self, origen: str, destino: str) -> None:
        """Crea una arista dirigida desde 'origen' hacia 'destino'."""
        origen_limpio = Asignatura.normalizar_codigo(origen)
        destino_limpio = Asignatura.normalizar_codigo(destino)
        self.agregar_nodo(origen_limpio)
        self.agregar_nodo(destino_limpio)
        if destino_limpio not in self.adyacencia[origen_limpio]:
            self.adyacencia[origen_limpio].append(destino_limpio)

    def obtener_relaciones(self, codigo: str) -> Optional[List[str]]:
        """Retorna las asignaturas conectadas desde 'codigo', o None si no existe."""
        codigo_limpio = Asignatura.normalizar_codigo(codigo)
        return self.adyacencia.get(codigo_limpio)

    def mostrar_grafo(self, catalogo: Dict[str, Asignatura]) -> None:
        """Muestra todas las conexiones dirigidas registradas."""
        print("\n--- Conexiones dirigidas en el Grafo ---")
        for origen, destinos in self.adyacencia.items():
            nombre_origen = catalogo[origen].nombre if origen in catalogo else "Sin registro"
            if destinos:
                destinos_fmt = ", ".join(
                    f"{d} ({catalogo[d].nombre})" if d in catalogo else d for d in destinos
                )
                print(f"  {origen} ({nombre_origen}) -> {destinos_fmt}")
            else:
                print(f"  {origen} ({nombre_origen}) -> Sin relaciones salientes")


class LaberintoDeDatos:
    """Clase coordinadora que integra ABB, Tabla Hash y Grafo."""

    def __init__(self) -> None:
        self.arbol_codigos = ArbolBinarioBusqueda()
        self.tabla_hash: Dict[str, Asignatura] = {}
        self.grafo = GrafoAsignaturas()

    def registrar_asignatura(self, codigo: str, nombre: str) -> None:
        """Agrega una asignatura al ABB, a la tabla hash y como nodo al grafo."""
        asignatura = Asignatura(codigo, nombre)
        self.arbol_codigos.insertar(asignatura.codigo)
        self.tabla_hash[asignatura.codigo] = asignatura
        self.grafo.agregar_nodo(asignatura.codigo)

    def registrar_relacion(self, origen: str, destino: str) -> bool:
        """Registra una conexión dirigida si ambas asignaturas existen."""
        origen_limpio = Asignatura.normalizar_codigo(origen)
        destino_limpio = Asignatura.normalizar_codigo(destino)
        if origen_limpio not in self.tabla_hash or destino_limpio not in self.tabla_hash:
            return False
        self.grafo.agregar_relacion(origen_limpio, destino_limpio)
        return True

    def consultar_asignatura(self, codigo: str) -> None:
        """Verifica en el ABB y recupera la información desde la tabla hash."""
        codigo_limpio = Asignatura.normalizar_codigo(codigo)
        existe_en_arbol = self.arbol_codigos.buscar(codigo_limpio)
        asignatura = self.tabla_hash.get(codigo_limpio)

        print(f"\nConsulta para código '{codigo_limpio}':")
        print(f"  - Búsqueda en ABB (nodos): {'Encontrado' if existe_en_arbol else 'No encontrado'}")
        if existe_en_arbol and asignatura is not None:
            print(f"  - Consulta en Tabla Hash (dict): {asignatura.codigo} -> {asignatura.nombre}")
            relaciones = self.grafo.obtener_relaciones(codigo_limpio) or []
            if relaciones:
                print(f"  - Relaciones dirigidas (Grafo): {', '.join(relaciones)}")
            else:
                print("  - Relaciones dirigidas (Grafo): Ninguna")
        else:
            print("  - Aviso: El código de asignatura no existe en el sistema.")

    def cargar_datos_iniciales(self) -> None:
        """Carga las asignaturas y relaciones definidas en el problema."""
        asignaturas_iniciales = [
            ("PR101", "Fundamentos de Programación"),
            ("PR102", "Programación Orientada a Objetos"),
            ("ES201", "Estructuras de Datos"),
            ("BD201", "Bases de Datos"),
            ("AL201", "Algoritmos"),
        ]
        for codigo, nombre in asignaturas_iniciales:
            self.registrar_asignatura(codigo, nombre)

        relaciones_iniciales = [
            ("PR101", "PR102"),
            ("PR101", "BD201"),
            ("PR102", "ES201"),
            ("PR102", "AL201"),
        ]
        for origen, destino in relaciones_iniciales:
            self.registrar_relacion(origen, destino)

    def ejecutar_pruebas_minimas(self) -> None:
        """Ejecuta los casos de prueba solicitados en el Paso 5."""
        print("\n=== EJECUCIÓN DE PRUEBAS MÍNIMAS (PASO 5) ===")
        # 1. Asignatura existente en ABB y Tabla Hash
        self.consultar_asignatura("ES201")
        # 2. Visualizar relaciones en el grafo
        self.grafo.mostrar_grafo(self.tabla_hash)
        # 3. Código inexistente controlado
        self.consultar_asignatura("XX999")
        print("=== FIN DE PRUEBAS ===")


def mostrar_menu() -> None:
    print("\n================ LABERINTO DE DATOS ================")
    print("1. Consultar asignatura por código (ABB + Tabla Hash)")
    print("2. Ver todas las relaciones del grafo")
    print("3. Ver códigos ordenados en el ABB (Inorden)")
    print("4. Agregar nueva asignatura")
    print("5. Agregar relación dirigida entre asignaturas")
    print("6. Ejecutar pruebas mínimas del Paso 5")
    print("0. Salir")
    print("====================================================")


def main() -> None:
    sistema = LaberintoDeDatos()
    sistema.cargar_datos_iniciales()

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            codigo = input("Ingrese el código de la asignatura (ej. PR101): ")
            sistema.consultar_asignatura(codigo)
        elif opcion == "2":
            sistema.grafo.mostrar_grafo(sistema.tabla_hash)
        elif opcion == "3":
            print("\nCódigos en ABB (recorrido inorden):", sistema.arbol_codigos.recorrido_inorden())
        elif opcion == "4":
            codigo = input("Nuevo código: ")
            nombre = input("Nombre de la asignatura: ")
            if not codigo.strip() or not nombre.strip():
                print("Error: el código y el nombre no pueden estar vacíos.")
            else:
                sistema.registrar_asignatura(codigo, nombre)
                print(f"Asignatura {Asignatura.normalizar_codigo(codigo)} registrada correctamente.")
        elif opcion == "5":
            origen = input("Código asignatura origen: ")
            destino = input("Código asignatura destino: ")
            if sistema.registrar_relacion(origen, destino):
                print(
                    f"Relación registrada: {Asignatura.normalizar_codigo(origen)} -> "
                    f"{Asignatura.normalizar_codigo(destino)}"
                )
            else:
                print("Error: verifique que ambos códigos existan en el sistema.")
        elif opcion == "6":
            sistema.ejecutar_pruebas_minimas()
        elif opcion == "0":
            print("Saliendo de Laberinto de Datos...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")


if __name__ == "__main__":
    main()