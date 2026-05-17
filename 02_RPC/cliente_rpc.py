"""
Cliente XML-RPC para probar el servidor de cálculo de IMC
Incluye casos de éxito y casos de error
"""

import xmlrpc.client

# El proxy hace la llamada remota parecia local
proxy = xmlrpc.client.ServerProxy("http://localhost:8080/")

print("=" * 70)
print("CLIENTE RPC - PRUEBAS DE CÁLCULO DE IMC CON CONTROL DE ERRORES")
print("=" * 70)
print()

# PRUEBA 1: Caso exitoso - Persona con peso normal
print("PRUEBA 1: Caso exitoso - Peso Normal")
print("-" * 70)
peso = 65
altura = 1.75
print(f"Entrada: peso={peso} kg, altura={altura} m")
resultado = proxy.calcular_imc(peso, altura)
print(f"Resultado: {resultado}")
print()

# PRUEBA 2: Caso de error - Peso negativo
print("PRUEBA 2: Caso de error - Peso negativo")
print("-" * 70)
peso = -70
altura = 1.75
print(f"Entrada: peso={peso} kg, altura={altura} m")
resultado = proxy.calcular_imc(peso, altura)
print(f"Resultado: {resultado}")
print()

# PRUEBA 3: Caso de error - Altura cero
print("PRUEBA 3: Caso de error - Altura cero")
print("-" * 70)
peso = 70
altura = 0
print(f"Entrada: peso={peso} kg, altura={altura} m")
resultado = proxy.calcular_imc(peso, altura)
print(f"Resultado: {resultado}")
print()

# PRUEBA 4: Caso exitoso - Persona con sobrepeso
print("PRUEBA 4: Caso exitoso - Sobrepeso")
print("-" * 70)
peso = 90
altura = 1.70
print(f"Entrada: peso={peso} kg, altura={altura} m")
resultado = proxy.calcular_imc(peso, altura)
print(f"Resultado: {resultado}")
print()

# PRUEBA 5: Caso exitoso - Persona con obesidad
print("PRUEBA 5: Caso exitoso - Obesidad")
print("-" * 70)
peso = 110
altura = 1.65
print(f"Entrada: peso={peso} kg, altura={altura} m")
resultado = proxy.calcular_imc(peso, altura)
print(f"Resultado: {resultado}")
print()

# PRUEBA 6: Caso de error - Altura inválida (muy alta)
print("PRUEBA 6: Caso de error - Altura inválida (fuera de rango)")
print("-" * 70)
peso = 70
altura = 5.0
print(f"Entrada: peso={peso} kg, altura={altura} m")
resultado = proxy.calcular_imc(peso, altura)
print(f"Resultado: {resultado}")
print()

# PRUEBA 7: Mostrar historial después de todas las pruebas
print("PRUEBA 7: Historial de cálculos (últimos 5)")
print("-" * 70)
historial = proxy.historial()
historial_lista = historial if isinstance(historial, list) else []
print(f"Total de cálculos en historial: {len(historial_lista)}")
for i, calculo in enumerate(historial_lista, 1):
    print(f"\n  {i}. Peso: {calculo['peso_kg']} kg, Altura: {calculo['altura_m']} m")
    print(f"     IMC: {calculo['imc']}, Categoría: {calculo['categoria']}")
print()

print("=" * 70)
print("PRUEBAS COMPLETADAS")
print("=" * 70)
