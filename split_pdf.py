"""
PDF Splitter - Herramienta para separar páginas de archivos PDF

Este programa permite extraer páginas individuales o rangos de páginas de un archivo PDF
y guardarlas como archivos PDF separados.

Ejemplo de uso:
    python split_pdf.py documento.pdf 1-10,15,20-25 salida.pdf
"""

import sys
import os
from pypdf import PdfReader, PdfWriter


def parse_page_ranges(ranges_str):
    """
    Convierte una cadena de rangos de páginas en una lista de números de página.
    
    Args:
        ranges_str (str): Cadena con rangos separados por comas. 
                         Ejemplo: "1-10,15,20-25"
    
    Returns:
        list: Lista ordenada de números de página (empezando desde 0 para índices)
    
    Ejemplos:
        >>> parse_page_ranges("1-3,5")
        [0, 1, 2, 4]
        >>> parse_page_ranges("10")
        [9]
    """
    pages = set()  # Usamos set para evitar duplicados
    
    # Separar por comas para obtener cada rango o página individual
    ranges = ranges_str.split(',')
    
    for range_part in ranges:
        range_part = range_part.strip()  # Eliminar espacios en blanco
        
        if '-' in range_part:
            # Es un rango: "1-10"
            start, end = range_part.split('-')
            start = int(start.strip())
            end = int(end.strip())
            
            # Agregar todas las páginas del rango
            # Restamos 1 porque los índices en pypdf empiezan en 0
            for page_num in range(start, end + 1):
                pages.add(page_num - 1)
        else:
            # Es una página individual: "5"
            page_num = int(range_part)
            pages.add(page_num - 1)
    
    # Convertir a lista ordenada
    return sorted(list(pages))


def split_pdf(input_path, pages, output_path):
    """
    Extrae páginas específicas de un PDF y las guarda en un nuevo archivo.
    
    Args:
        input_path (str): Ruta del archivo PDF de origen
        pages (list): Lista de números de página a extraer (índices base 0)
        output_path (str): Ruta donde se guardará el PDF resultante
    
    Raises:
        FileNotFoundError: Si el archivo de entrada no existe
        ValueError: Si alguna página está fuera de rango
    """
    # Verificar que el archivo de entrada existe
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"El archivo '{input_path}' no existe.")
    
    # Leer el PDF de origen
    print(f"Leyendo archivo: {input_path}")
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    print(f"Total de páginas en el PDF: {total_pages}")
    
    # Validar que todas las páginas solicitadas existen
    for page_num in pages:
        if page_num < 0 or page_num >= total_pages:
            raise ValueError(
                f"Página {page_num + 1} fuera de rango. "
                f"El PDF tiene {total_pages} páginas."
            )
    
    # Crear el escritor de PDF
    writer = PdfWriter()
    
    # Agregar las páginas seleccionadas
    print(f"Extrayendo {len(pages)} página(s)...")
    for page_num in pages:
        writer.add_page(reader.pages[page_num])
        print(f"  - Página {page_num + 1} agregada")
    
    # Guardar el nuevo PDF
    print(f"Guardando archivo: {output_path}")
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)
    
    print(f"¡Listo! PDF creado exitosamente.")


def parse_multiple_ranges(ranges_str):
    """
    Convierte una cadena de rangos en una lista de rangos individuales.
    
    Args:
        ranges_str (str): Cadena con rangos separados por comas.
                         Ejemplo: "1-2,3-12,13-15"
    
    Returns:
        list: Lista de tuplas (nombre_rango, lista_paginas)
    
    Ejemplos:
        >>> parse_multiple_ranges("1-2,3-12")
        [("1-2", [0, 1]), ("3-12", [2, 3, 4, 5, 6, 7, 8, 9, 10, 11])]
    """
    ranges_list = []
    
    # Separar por comas para obtener cada rango
    ranges = ranges_str.split(',')
    
    for range_part in ranges:
        range_part = range_part.strip()
        pages = []
        
        if '-' in range_part:
            # Es un rango: "1-10"
            start, end = range_part.split('-')
            start = int(start.strip())
            end = int(end.strip())
            
            # Agregar todas las páginas del rango
            for page_num in range(start, end + 1):
                pages.append(page_num - 1)
        else:
            # Es una página individual: "5"
            page_num = int(range_part)
            pages.append(page_num - 1)
        
        ranges_list.append((range_part, pages))
    
    return ranges_list


def split_pdf_multiple(input_path, ranges_str, output_prefix="documento"):
    """
    Separa un PDF en múltiples archivos, uno por cada rango.
    
    Args:
        input_path (str): Ruta del archivo PDF de origen
        ranges_str (str): Cadena con rangos separados por comas
        output_prefix (str): Prefijo para los nombres de archivos de salida
    
    Returns:
        list: Lista de nombres de archivos creados
    """
    # Verificar que el archivo de entrada existe
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"El archivo '{input_path}' no existe.")
    
    # Leer el PDF de origen
    print(f"Leyendo archivo: {input_path}")
    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    
    print(f"Total de páginas en el PDF: {total_pages}")
    print()
    
    # Parsear los rangos
    ranges_list = parse_multiple_ranges(ranges_str)
    
    print(f"Se crearán {len(ranges_list)} archivo(s) PDF:")
    print()
    
    created_files = []
    
    # Crear un PDF por cada rango
    for rango_nombre, pages in ranges_list:
        # Validar páginas
        for page_num in pages:
            if page_num < 0 or page_num >= total_pages:
                raise ValueError(
                    f"Página {page_num + 1} fuera de rango. "
                    f"El PDF tiene {total_pages} páginas."
                )
        
        # Crear nombre de archivo
        output_filename = f"{output_prefix}_paginas_{rango_nombre}.pdf"
        
        # Crear escritor de PDF
        writer = PdfWriter()
        
        # Agregar páginas
        for page_num in pages:
            writer.add_page(reader.pages[page_num])
        
        # Guardar archivo
        with open(output_filename, 'wb') as output_file:
            writer.write(output_file)
        
        created_files.append(output_filename)
        print(f"✓ Creado: {output_filename} ({len(pages)} página(s))")
    
    print()
    print(f"¡Listo! Se crearon {len(created_files)} archivo(s) PDF.")
    
    return created_files



def main():
    """
    Función principal que maneja la interfaz de línea de comandos.
    """
    # Mostrar banner
    print("=" * 60)
    print("PDF SPLITTER - Separador de Páginas PDF")
    print("=" * 60)
    print()
    
    # Verificar argumentos de línea de comandos
    if len(sys.argv) == 4:
        # Modo: python split_pdf.py input.pdf "1-10,15" output.pdf
        input_path = sys.argv[1]
        ranges_str = sys.argv[2]
        output_path = sys.argv[3]
    else:
        # Modo interactivo
        print("Uso: python split_pdf.py <archivo_entrada.pdf> <rangos> <archivo_salida.pdf>")
        print()
        print("Ejemplos de rangos:")
        print("  - Páginas individuales: 1,5,10")
        print("  - Rangos: 1-10,15-20")
        print("  - Combinado: 1-10,15,20-25")
        print()
        
        # Solicitar información al usuario
        input_path = input("Archivo PDF de entrada: ").strip()
        ranges_str = input("Páginas a extraer (ej: 1-34,56-58,60-90): ").strip()
        output_path = input("Nombre del archivo de salida: ").strip()
    
    print()
    
    try:
        # Preguntar modo de separación (solo en modo interactivo)
        if len(sys.argv) != 4:
            print("¿Deseas generar archivos separados por rango?")
            print("  (s) = Sí, crear múltiples archivos (uno por cada rango)")
            print("  (n) = No, crear un solo archivo con todos los rangos")
            modo = input("Selecciona (s/n): ").strip().lower()
            print()
        else:
            # En modo comando, siempre usar modo simple (un solo archivo)
            modo = 'n'
        
        if modo == 's':
            # MODO MÚLTIPLE: Crear varios archivos
            # Obtener prefijo para nombres de archivo
            base_name = os.path.splitext(os.path.basename(input_path))[0]
            prefijo = input(f"Prefijo para archivos (Enter para '{base_name}'): ").strip()
            if not prefijo:
                prefijo = base_name
            
            print()
            
            # Separar en múltiples archivos
            split_pdf_multiple(input_path, ranges_str, prefijo)
            
        else:
            # MODO SIMPLE: Crear un solo archivo (comportamiento original)
            # Asegurar que el archivo de salida tenga extensión .pdf
            if not output_path.lower().endswith('.pdf'):
                output_path = output_path + '.pdf'
                print(f"Nota: Se agregó extensión .pdf al archivo de salida")
                print()
            
            # Parsear los rangos de páginas
            pages = parse_page_ranges(ranges_str)
            print(f"Páginas a extraer: {len(pages)} página(s)")
            print()
            
            # Realizar la separación
            split_pdf(input_path, pages, output_path)

        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
