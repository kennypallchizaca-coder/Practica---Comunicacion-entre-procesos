import socket, threading, sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 65432))

def recibir():
    while True:
        try:
            # [CORREGIDO POR IA]: Se separó el recv() del print y se añadió "if not data" 
            # para cerrar correctamente el hilo sin causar un 'Fatal Python error' al usar SALIR.
            data = s.recv(1024)
            if not data:
                break
            print("\n[Otro]: " + data.decode('utf-8'))
        except:
            break

threading.Thread(target=recibir, daemon=True).start()

print("Conectado. Escribe un mensaje o 'SALIR'.")
while True:
    msg = input("")
    s.sendall(msg.encode('utf-8'))
    
    if msg == 'SALIR':
        s.close()
        sys.exit() #
