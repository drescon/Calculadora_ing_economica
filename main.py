import sys

try:
    import tkinter
except ImportError as e:
    print(f"Error crítico: Tkinter no está instalado o configurado correctamente.")
    print(f"Detalle del error: {e}")
    print("\nSolución para Linux (Arch/Manjaro):")
    print("   sudo pacman -S tk")
    print("\nSolución para Linux (Ubuntu/Debian):")
    print("   sudo apt-get install python3-tk")
    print("\nPor favor instale la librería y vuelva a intentar.")
    sys.exit(1)

from app.controllers.main_controller import MainController

if __name__ == "__main__":
    app = MainController()
    app.run()
