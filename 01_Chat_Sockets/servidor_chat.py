import socket, threading, datetime

clientes = [] 

def manejar_cliente(conn, addr):
    clientes.append(conn)
    while True:
        data = conn.recv(1024)
        mensaje = data.decode('utf-8')
        
        if mensaje == 'SALIR':
            break
            
        tiempo = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # [CORREGIDO POR IA]: Se cambió addr[3] por addr[0] (IP) y addr[1] (PUERTO) para evitar IndexError
        print(f"[{tiempo}] {addr[0]}:{addr[1]} -> '{mensaje}'")
        
        for c in clientes:
            if c != conn:
                c.sendall(data)
                
    clientes.remove(conn)
    conn.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 65432))
s.listen()
print("Servidor iniciado...")

while True:
    conn, addr = s.accept()
    threading.Thread(target=manejar_cliente, args=(conn, addr)).start()