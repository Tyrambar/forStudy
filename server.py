import socket


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 2222))
s.listen(5)
rsp = s.recv(1024)

while True:
  conn, adrr = s.accept()
  while True:
    data = conn.recv(1024)
    if not data or data == "close": break
    conn.send(data)
  conn.close()
