# PDF Splitter

Herramienta de línea de comandos para separar y extraer páginas específicas de archivos PDF.

## Descripción

PDF Splitter permite extraer páginas individuales o rangos de páginas de un archivo PDF y guardarlas como un nuevo documento PDF. Útil para dividir documentos grandes o extraer secciones específicas.

## Requisitos

- Python 3.7 o superior
- pypdf 4.0.0 o superior

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/tu-usuario/split-pdf.git
cd split-pdf
```

2. Crear y activar el entorno virtual:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Modo Comando
```bash
python split_pdf.py <archivo_entrada.pdf> <rangos> <archivo_salida.pdf>
```

### Modo Interactivo
```bash
python split_pdf.py
```

## Ejemplos

Extraer páginas individuales:
```bash
python split_pdf.py documento.pdf "1,5,10" resultado.pdf
```

Extraer rangos de páginas:
```bash
python split_pdf.py documento.pdf "1-10,20-30" resultado.pdf
```

Extraer combinación de páginas y rangos:
```bash
python split_pdf.py documento.pdf "1-34,56-58,60-90" resultado.pdf
```

## Estructura del Proyecto

```
split-pdf/
├── split_pdf.py        # Programa principal
├── requirements.txt    # Dependencias del proyecto
├── README.md          # Documentación
└── venv/              # Entorno virtual (no incluido en Git)
```
