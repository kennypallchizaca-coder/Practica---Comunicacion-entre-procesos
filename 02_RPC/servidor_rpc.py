"""
Servidor XML-RPC con control de errores
Implementa cálculo de IMC con historial de cálculos
"""

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Historial global para almacenar los últimos 5 cálculos
historial_calculos = []


def validar_entrada(peso_kg, altura_m):
    """
    Valida que los parámetros sean válidos.
    
    Args:
        peso_kg: Peso en kilogramos
        altura_m: Altura en metros
        
    Returns:
        dict: {'valido': bool, 'mensaje': str}
    """
    if peso_kg <= 0 or altura_m <= 0:
        return {
            'valido': False,
            'mensaje': 'Error: Peso y altura deben ser mayores a cero.'
        }
    
    if peso_kg > 500:
        return {
            'valido': False,
            'mensaje': 'Error: Peso inválido (valor muy alto).'
        }
    
    if altura_m > 3 or altura_m < 0.5:
        return {
            'valido': False,
            'mensaje': 'Error: Altura inválida (fuera de rango razonable).'
        }
    
    return {'valido': True, 'mensaje': ''}


def calcular_categoria_imc(imc):
    """
    Determina la categoría de IMC según valores estándar.
    
    Args:
        imc: Índice de masa corporal
        
    Returns:
        str: Categoría (Bajo peso / Normal / Sobrepeso / Obesidad)
    """
    if imc < 18.5:
        return "Bajo peso"
    elif imc < 25:
        return "Normal"
    elif imc < 30:
        return "Sobrepeso"
    else:
        return "Obesidad"


def calcular_imc(peso_kg, altura_m):
    """
    Calcula el IMC y su categoría.
    
    Args:
        peso_kg: Peso en kilogramos (debe ser > 0)
        altura_m: Altura en metros (debe ser > 0)
        
    Returns:
        dict: {'imc': float, 'categoria': str} o {'error': str}
    """
    # Validar entrada
    validacion = validar_entrada(peso_kg, altura_m)
    if not validacion['valido']:
        return {'error': validacion['mensaje']}
    
    # Calcular IMC
    imc = peso_kg / (altura_m ** 2)
    imc = round(imc, 2)
    
    # Obtener categoría
    categoria = calcular_categoria_imc(imc)
    
    # Guardar en historial
    resultado = {
        'peso_kg': peso_kg,
        'altura_m': altura_m,
        'imc': imc,
        'categoria': categoria
    }
    historial_calculos.insert(0, resultado)
    
    # Mantener solo los últimos 5 cálculos
    if len(historial_calculos) > 5:
        historial_calculos.pop()
    
    return {
        'imc': imc,
        'categoria': categoria
    }


def historial():
    """
    Retorna los últimos 5 cálculos realizados.
    
    Returns:
        list: Lista de diccionarios con los cálculos (del más reciente al más antiguo)
    """
    return historial_calculos


def obtener_info(nombre):
    """
    Función de prueba que retorna información del servidor.
    
    Args:
        nombre: Nombre a saludar
        
    Returns:
        str: Mensaje de saludo desde RPC
    """
    return f"Hola {nombre} desde RPC!"


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)


if __name__ == '__main__':
    # Crear servidor en localhost:8080
    server = SimpleXMLRPCServer(("localhost", 8080), logRequests=True)
    
    # Registrar funciones
    server.register_function(calcular_imc)
    server.register_function(historial)
    server.register_function(obtener_info)
    
    print("Servidor RPC escuchando en localhost:8080")
    print("Funciones disponibles:")
    print("  - calcular_imc(peso_kg, altura_m)")
    print("  - historial()")
    print("  - obtener_info(nombre)")
    
    # Mantener servidor ejecutándose
    server.serve_forever()
