# DECLARACIÓN DE USO DE IA - Actividad 2.2 RPC con Control de Errores

## Resumen
Esta actividad fue desarrollada utilizando GitHub Copilot (Claude Haiku 4.5) como asistente de programación para acelerar la implementación de un servidor y cliente XML-RPC con control de errores.

## Consultas realizadas a la IA
1. **Estructura básica de servidor XML-RPC en Python**: Consulté cómo crear un servidor con `SimpleXMLRPCServer` y cómo registrar funciones remotas.
2. **Manejo de errores en RPC**: Cómo retornar mensajes de error descriptivos en lugar de excepciones sin manejar.
3. **Persistencia de datos en memoria**: Cómo mantener un historial entre llamadas usando una estructura de datos global.
4. **Validación de parámetros**: Rangos razonables para peso y altura.
5. **Cliente XML-RPC**: Cómo crear un cliente para hacer pruebas con casos de éxito y error.

## Qué generó la IA
- **Estructura completa del servidor**: Clase `SimpleXMLRPCServer`, registro de funciones, configuración del puerto.
- **Función `calcular_imc()`**: Lógica de cálculo, categorización según IMC estándar.
- **Función `validar_entrada()`**: Validación de parámetros con retorno de errores descriptivos.
- **Función `historial()`**: Gestión de lista con los últimos 5 cálculos.
- **Cliente con pruebas**: Estructura de 7 pruebas incluyendo casos de error.
- **Documentación y comentarios**: Docstrings y comentarios explicativos en el código.

## Qué modifiqué
- **Validaciones adicionales**: Añadí límites máximos razonables (peso < 500 kg, altura 0.5-3 m).
- **Formato de respuestas**: Estructuré las respuestas de error de manera consistente con `{'error': mensaje}`.
- **Pruebas adicionales**: Agregué casos de prueba para altura inválida (prueba 6) además de los 4 mínimos requeridos.
- **Historial mejorado**: Uso de `insert(0, ...)` para mantener el orden cronológico inverso (más reciente primero).
- **Salida del cliente**: Añadí formato mejorado con separadores visuales para facilitar la lectura.

## Tecnologías utilizadas
- **xmlrpc.server**: Módulo estándar de Python para crear servidores XML-RPC
- **xmlrpc.client**: Cliente para hacer llamadas RPC
- **Tipos de datos**: Diccionarios para retornar resultados complejos
- **Listas**: Para mantener el historial de cálculos

## Pruebas incluidas (7 total, > 4 requeridas)
1. ✓ Caso exitoso - Peso Normal
2. ✗ Caso de error - Peso negativo
3. ✗ Caso de error - Altura cero
4. ✓ Caso exitoso - Sobrepeso
5. ✓ Caso exitoso - Obesidad
6. ✗ Caso de error - Altura inválida
7. ✓ Historial con 5 últimos cálculos

## Instrucciones para ejecutar
1. Abrir dos terminales/shells
2. En la primera terminal: `python servidor_rpc.py`
3. En la segunda terminal: `python cliente_rpc.py`
4. Esperar a que el cliente complete todas las pruebas

## Aprendizajes
- XML-RPC es una forma simple de llamar funciones remotas sin necesidad de APIs REST complejas
- El manejo de errores en RPC requiere convenciones claras (retornar dicts con campo 'error')
- Las variables globales en Python pueden ser útiles para mantener estado entre llamadas RPC
- La validación de entrada es crítica para evitar errores y comportamientos inesperados

## Explicación técnica del manejo de múltiples clientes

Aquí explico, en un tono de estudiante universitario (no tan formal), los puntos más relevantes sobre cómo mi implementación trata a varios clientes y qué debería cambiarse si queremos que el servidor soporte concurrencia real:

- **Modelo actual (secuencial):** El servidor se crea con `SimpleXMLRPCServer` sin mixins de concurrencia, así que atiende una petición a la vez en el hilo principal. Si varios clientes llaman a la vez, quedan en cola y se procesan uno por uno.
- **Para atender varios clientes a la vez:** Lo más simple es usar hilos. Se puede crear un servidor mezclando `socketserver.ThreadingMixIn` con `SimpleXMLRPCServer` (ej: `class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer): pass`). Con eso cada conexión se atiende en su propio hilo.
- **Protección del estado compartido:** En mi implementación uso una lista global `historial_calculos`. Si cambias a hilos, hay que protegerla con un `threading.Lock()` para no tener condiciones de carrera al insertar o truncar la lista.

	Ejemplo práctico (mini-snippet):

	```python
	from socketserver import ThreadingMixIn
	from xmlrpc.server import SimpleXMLRPCServer
	import threading

	class ThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
			pass

	historial_lock = threading.Lock()

	# al modificar el historial:
	with historial_lock:
			historial_calculos.insert(0, resultado)
			if len(historial_calculos) > 5:
					historial_calculos.pop()
	```

- **Consideraciones prácticas:** Los hilos son fáciles de probar pero no son la solución óptima para cargas muy altas; para muchos clientes conviene usar un pool de procesos, un servidor asíncrono o mover el historial a una base de datos/cola.
- **Serialización y seguridad:** XML-RPC serializa tipos simples; siempre valida y normaliza los datos en el servidor y devuelve errores controlados (`{'error': ...}`) en lugar de lanzar excepciones sin manejar.
- **Resumen corto:** ahora mismo el servidor funciona bien para pruebas pero maneja clientes de forma secuencial; para concurrencia segura necesitamos hilos/procesos y sincronización del `historial_calculos`.
