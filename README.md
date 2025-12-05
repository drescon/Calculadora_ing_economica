# Calculadora de Créditos Bancarios

Esta es una aplicación de escritorio desarrollada en Python con Tkinter que permite calcular cuotas de créditos bancarios con diferentes periodicidades.

## Estructura del Proyecto

El proyecto sigue el patrón de diseño MVC (Modelo-Vista-Controlador):

- `app/models/`: Contiene la lógica financiera (`CreditCalculator`).
- `app/views/`: Contiene la interfaz gráfica (`MainWindow`).
- `app/controllers/`: Conecta la vista y el modelo (`MainController`).
- `main.py`: Punto de entrada de la aplicación.

## Requisitos

- Python 3.x
- `pyinstaller` (para generar el ejecutable)

## Instalación de Dependencias

### Python Packages
```bash
pip install -r requirements.txt
```

### Dependencias del Sistema (Linux)
Si estás en Linux, es posible que necesites instalar `tkinter` manualmente:

- **Arch Linux / Manjaro**:
  ```bash
  sudo pacman -S tk
  ```
- **Ubuntu / Debian**:
  ```bash
  sudo apt-get install python3-tk
  ```

## Ejecución

Para correr la aplicación desde el código fuente:

```bash
python main.py
```

## Generar Ejecutable (Windows) - Paso a Paso

Siga estos pasos para crear un archivo `.exe` independiente de la aplicación:

1.  **Instalar dependencias**:
    Asegúrese de haber instalado todas las librerías necesarias, incluyendo `pyinstaller`.
    ```bash
    pip install -r requirements.txt
    ```

2.  **Ejecutar PyInstaller**:
    Corra el siguiente comando en la terminal (estando en la carpeta raíz del proyecto):
    ```bash
    pyinstaller --noconsole --onefile --name="CalculadoraCreditos" main.py
    ```
    *   `--noconsole`: Oculta la ventana de consola negra al ejecutar la app.
    *   `--onefile`: Empaqueta todo en un único archivo `.exe`.
    *   `--name`: Define el nombre del archivo de salida.

3.  **Localizar el ejecutable**:
    Una vez finalizado el proceso, encontrará el archivo `CalculadoraCreditos.exe` en la carpeta `dist/` que se ha creado en su proyecto.

4.  **Ejecutar**:
    Puede mover este archivo a cualquier ubicación y ejecutarlo con doble clic.

