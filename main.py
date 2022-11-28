# Integration: Jerome
import os
import socket
import hashlib
from tcp import start_client, start_server, broadcast_existence, listen_for_broadcasts

send_to = {}

def merge_sender_entropy(sender, entropy):
  return (hashlib.sha256((f"{sender}+{entropy}").encode('utf-8')).hexdigest())[0:6]

entropy = os.urandom(4)
who_am_i = socket.gethostbyname(socket.getfqdn())
my_fingerprint = merge_sender_entropy(who_am_i, entropy)
sender_fingerprints = {}

#sender_fingerprints[who_am_i] = my_fingerprint
known_fingerprints = []

print(sender_fingerprints)

def on_broadcast(content, sender):
  current_fingerprint = merge_sender_entropy(sender[0], content)
  if not current_fingerprint in known_fingerprints:
    known_fingerprints.append(current_fingerprint)
    sender_fingerprints[sender[0]] = current_fingerprint
    print(
      sender_fingerprints,
      current_fingerprint,
      my_fingerprint,
      int(current_fingerprint, 16),
      int(my_fingerprint, 16),
      int(current_fingerprint, 16) < int(my_fingerprint, 16)
    )

    def create_socket(addr, data):
      print(addr)
      def send_data(conn, addr):
        conn.sendall(data.encode('utf8'))
      start_client(addr, send_data)
    send_to[sender_fingerprints[sender[0]]] = lambda x:create_socket(sender[0], x)
    

listen_for_broadcasts(on_broadcast)

def onserverconn(conn, addr):
  print('New server conn!', addr)
def onservermsg(conn, msg):
  print('New server msg!', msg)

start_server(onserverconn, onservermsg)
broadcast_existence(entropy)

while True:
  command = input()
  dest, *contents = command.split('<=')
  send_to[dest]('<='.join(contents))
