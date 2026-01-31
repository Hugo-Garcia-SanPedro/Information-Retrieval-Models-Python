import os
import sys
import runpy

# Configuración: Nombre de la carpeta donde están los scripts
SRC_FOLDER = 'src'

def run_script(script_name):
    # Construimos la ruta completa (ej: src/vector-model.py)
    script_path = os.path.join(SRC_FOLDER, script_name)

    # Verificamos que el archivo exista en esa ruta
    if not os.path.exists(script_path):
        print(f"\n[ERROR] No se encuentra el archivo: {script_path}")
        print(f"Asegúrate de que '{script_name}' esté dentro de la carpeta '{SRC_FOLDER}'.")
        return

    print(f"\n--- Iniciando ejecución de {script_name} ---")
    try:
        # runpy ejecuta el archivo estableciendo correctamente el contexto (__file__)
        # Esto es vital para que tus scripts encuentren la carpeta 'data'
        runpy.run_path(script_path, run_name="__main__")
    except KeyboardInterrupt:
        print("\nEjecución interrumpida por el usuario.")
    except Exception as e:
        print(f"\n[ERROR] Ocurrió un fallo al ejecutar '{script_name}': {e}")
    
    print(f"--- Fin de ejecución de {script_name} ---\n")

def main():
    while True:
        print("\n=======================================================")
        print("   SISTEMA DE RECUPERACIÓN DE INFORMACIÓN (Main Menu)  ")
        print("=======================================================")
        print(f"Scripts ubicados en: ./{SRC_FOLDER}/")
        print("-------------------------------------------------------")
        print("1. Normalización de Textos  (normalization.py)")
        print("2. Indexación               (indexing.py)")
        print("3. Modelo Booleano          (boolean-model.py)")
        print("4. Modelo Vectorial         (vector-model.py)")
        print("5. Modelo Probabilístico    (probabilistic.py)")
        print("0. Salir")
        print("=======================================================")

        choice = input("Opción > ").strip()

        if choice == '1':
            run_script('normalization.py')
        elif choice == '2':
            run_script('indexing.py')
        elif choice == '3':
            run_script('boolean-model.py')
        elif choice == '4':
            run_script('vector-model.py')
        elif choice == '5':
            run_script('probabilistic.py')
        elif choice == '0':
            print("Saliendo del sistema...")
            break
        else:
            print("\nOpción no válida. Por favor, selecciona un número del menú.")

if __name__ == "__main__":
    # Opcional: Verificar que la carpeta src existe antes de arrancar
    if not os.path.isdir(SRC_FOLDER):
        print(f"[ADVERTENCIA] No se encuentra la carpeta '{SRC_FOLDER}' en este directorio.")
    
    main()