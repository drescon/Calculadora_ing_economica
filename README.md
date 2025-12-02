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

## Generar Ejecutable (Windows)

Para crear un archivo `.exe` independiente, ejecute el siguiente comando en su terminal (asegúrese de tener `pyinstaller` instalado):

```bash
pyinstaller --noconsole --onefile --name="CalculadoraCreditos" main.py
```

El ejecutable se generará en la carpeta `dist/`.
