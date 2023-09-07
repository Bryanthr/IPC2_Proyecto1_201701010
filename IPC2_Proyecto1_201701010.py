# Importa la clase LecturaXML y otras clases necesarias
from LecturaXML import LecturaXML
from ListaSimple import ListaSimple
from Senal import Senal
from Pila import Pila
from Cola import Cola
from Graph import Graph
from Tiempo import Tiempo
import copy
import xml.etree.ElementTree as ET
import subprocess  # Para ejecutar comandos externos

# Definición de la función generar_dot_grafica_senal
def generar_dot_grafica_senal(nombre_senal, tiempo_maximo, amplitud_maxima, frecuencias):
    dot_code = f'digraph G {{\n'
    dot_code += f'    label="Nombre de la Señal: {nombre_senal}";\n'
    dot_code += f'    tiempo_maximo="t: {tiempo_maximo}";\n'
    dot_code += f'    amplitud_maxima="A: {amplitud_maxima}";\n'
    
    # Agregar nodos para representar las frecuencias
    for i, frecuencia in enumerate(frecuencias):
        dot_code += f'    F{i} [label="F{i}: {frecuencia}"];\n'
    
    # Conectar los nodos
    for i in range(len(frecuencias) - 1):
        dot_code += f'    F{i} -> F{i + 1};\n'
    
    dot_code += '}\n'
    return dot_code


# Declarar objLectura como una variable global
objLectura = None

# Función para cargar un archivo XML
def cargarArchivoXML():
    global objLectura 
    # Solicita al usuario la ruta del archivo XML
    ruta_archivo = input("Ingrese la ruta del archivo XML: ")

    try:
        # Crea una instancia de la clase LecturaXML
        objLectura = LecturaXML(ruta_archivo)
        print("Archivo cargado exitosamente.")
    except FileNotFoundError:
        print("Error: El archivo no se encuentra.")
    except Exception as e:
        print(f"Error al cargar el archivo: {str(e)}")

# Función para procesar el archivo XML cargado previamente
def procesarArchivoXML():
    global objLectura  # Declara objLectura como global para acceder a la instancia creada en la opción 1

    try:
        # Utiliza los métodos de objLectura para procesar los datos del archivo
        objLectura.getSenal()  # Llama al método que obtiene la información de las señales
        objLectura.getDatos()  # Llama al método que procesa los datos de las señales
        print("Archivo procesado exitosamente.")
    except Exception as e:
        print(f"Error al procesar el archivo: {str(e)}")

# Función para escribir el archivo de salida
def escribirArchivoSalida():
    global objLectura  # Declara objLectura como global para acceder a la instancia creada en la opción 1

    try:
        # Solicita al usuario la ruta donde desea guardar el archivo de salida
        ruta_salida = input("Ingrese la ruta para guardar el archivo de salida: ")

        with open(ruta_salida, 'w') as archivo_salida:
            archivo_salida.write("Datos del archivo procesado:\n\n")
            archivo_salida.write("Listado de Señales:\n")
            
            # Recorre y escribe los datos de las señales en el archivo
            senalGuardada = objLectura.getSenal().getInicio()
            while senalGuardada is not None:
                archivo_salida.write(f"Nombre de la Señal: {senalGuardada.getDato().getNombre()}\n")
                archivo_salida.write(f"Tiempo Máximo: {senalGuardada.getDato().getTiempoMaximo()}\n")
                archivo_salida.write(f"Amplitud Máxima: {senalGuardada.getDato().getAmplitudMaxima()}\n\n")
                senalGuardada = senalGuardada.getSiguiente()
            
            archivo_salida.write("Datos de las Señales:\n")
            # Recorre y escribe los datos de las señales en el archivo
            senalGuardada = objLectura.getSenal().getInicio()
            while senalGuardada is not None:
                archivo_salida.write(f"Datos de la Señal: {senalGuardada.getDato().getNombre()}\n")
                
                # Obtiene los datos de la señal y los escribe
                datosSenal = objLectura.getDatosSenal(senalGuardada.getDato().getNombre())
                for dato in datosSenal:
                    archivo_salida.write(f"{dato}\n")
                
                archivo_salida.write("\n")
                senalGuardada = senalGuardada.getSiguiente()

        print(f"Archivo de salida guardado en: {ruta_salida}")
    except Exception as e:
        print(f"Error al escribir el archivo de salida: {str(e)}")

def mostrarDatosEstudiante():
    print("\nDatos del Estudiante:")
    print("Nombre: Bryant Herrera Rubio")
    print("Carné: 201701010")
    print("Correo Electrónico: 2988707890101@ingenieria.usac.edu.gt")
    print("Introducción a la Programación y Computación 2 sección N")
    print("Ingeniería en Ciencias y Sistemas")
    print("4to semestre")
    # Puedes agregar más información si es necesario

# Función para generar una gráfica de una señal de audio
def generarGrafica():
    global objLectura  # Declara objLectura como global para acceder a la instancia creada en la opción 1

    try:
        # Solicita al usuario el nombre de la señal que desea graficar
        nombre_senal = input("Ingrese el nombre de la señal que desea graficar: ")

        # Obtiene la señal con el nombre especificado
        senal = objLectura.getSenalPorNombre(nombre_senal)

        if senal is not None:
            # Genera un archivo DOT para la gráfica
            dot_file = f"{nombre_senal}.dot"
            with open(dot_file, 'w') as f:
                f.write(senal.generarDotGraph())

            # Convierte el archivo DOT a formato de imagen (por ejemplo, PNG)
            image_file = f"{nombre_senal}.png"
            subprocess.run(["dot", "-Tpng", dot_file, "-o", image_file], check=True)

            print(f"Gráfica generada: {image_file}")
        else:
            print(f"No se encontró una señal con el nombre '{nombre_senal}'.")

    except Exception as e:
        print(f"Error al generar la gráfica: {str(e)}")

# Función para generar una gráfica de una señal de audio
def generarGrafica():
    global objLectura  # Declara objLectura como global para acceder a la instancia creada en la opción 1

    try:
        # Solicita al usuario el nombre de la señal que desea graficar
        nombre_senal = input("Ingrese el nombre de la señal que desea graficar: ")

        # Obtiene la señal con el nombre especificado
        senal = objLectura.getSenalPorNombre(nombre_senal)

        if senal is not None:
            # Genera un archivo DOT para la gráfica de la señal original
            dot_original = generar_dot_grafica_senal(
                senal.getNombre(),
                senal.getTiempoMaximo(),
                senal.getAmplitudMaxima(),
                [f.getAmplitud() for f in senal.getTiempos()]
            )

            # Guarda el archivo DOT
            dot_file_original = f"{nombre_senal}_original.dot"
            with open(dot_file_original, 'w') as f:
                f.write(dot_original)

            # Convierte el archivo DOT a formato de imagen (por ejemplo, PNG)
            image_file_original = f"{nombre_senal}_original.png"
            subprocess.run(["dot", "-Tpng", dot_file_original, "-o", image_file_original], check=True)

            print(f"Gráfica original generada: {image_file_original}")

            # Debes hacer lo mismo para la matriz reducida
            # ...

        else:
            print(f"No se encontró una señal con el nombre '{nombre_senal}'.")

    except Exception as e:
        print(f"Error al generar la gráfica: {str(e)}")

# Menú principal
while True:
    print("\nMenú Principal:")
    print("1. Cargar Archivo")
    print("2. Procesar Archivo")
    print("3. Escribir Archivo de Salida")
    print("4. Mostrar Datos del Estudiante")
    print("5. Generar Gráfica")
    print("6. Salida")

    opcion = input("Seleccione una opción: ")

    if opcion == "1":
        cargarArchivoXML()
    elif opcion == "2":
        procesarArchivoXML()
    elif opcion == "3":
        escribirArchivoSalida()
    elif opcion == "4":
        mostrarDatosEstudiante()
    elif opcion == "5":
        generarGrafica()
    elif opcion == "6":
        print("Saliendo del programa...")
        break
    else:
        print("Por favor, seleccione una opción válida.")
