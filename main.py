import os
import sys
import runpy

SRC_FOLDER = 'src'

def run_script(script_name):
    script_path = os.path.join(SRC_FOLDER, script_name)

    if not os.path.exists(script_path):
        print(f"\n[ERROR]: {script_path}")
        print(f"Make sure that '{script_name}' is inside the '{SRC_FOLDER}' folder.")
        return

    print(f"\n--- Executing file {script_name} ---")
    try:
        runpy.run_path(script_path, run_name="__main__")
    except KeyboardInterrupt:
        print("\nExecution interrupted by the user.")
    except Exception as e:
        print(f"\n[ERROR] An error occurred while executing '{script_name}': {e}")
    
    print(f"--- End of execution of {script_name} ---\n")

def main():
    while True:
        print("\n=======================================================")
        print("   INFORMATION RETRIEVAL SYSTEM (Main Menu)  ")
        print("=======================================================")
        print(f"Scripts: ./{SRC_FOLDER}/")
        print("-------------------------------------------------------")
        print("1. Normalization of text (normalization.py)")
        print("2. Indexing (indexing.py)")
        print("3. Boolean model (boolean-model.py)")
        print("4. Vector model (vector-model.py)")
        print("5. Probabilistic model (probabilistic.py)")
        print("0. Exir")
        print("=======================================================")

        choice = input("Option > ").strip()

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
            print("Exiting...")
            break
        else:
            print("\nInvalid option. Please select a number from the menu.")

if __name__ == "__main__":
    if not os.path.isdir(SRC_FOLDER):
        print(f"[WARNING] The folder '{SRC_FOLDER}' cannot be found in this directory.")
    
    main()