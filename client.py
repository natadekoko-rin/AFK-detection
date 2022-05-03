# import socket
# import time

# HEADER = 64
# PORT = 5050
# FORMAT = 'utf-8'
# DISCONNECT_MESSAGE = "!DISCONNECT"
# SERVER = "192.168.1.6"
# ADDR = (SERVER, PORT)

# client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client.connect(ADDR)


# def send(msg):
#     message = msg.encode(FORMAT)
#     msg_length = len(message)
#     send_length = str(msg_length).encode(FORMAT)
#     send_length += b' ' * (HEADER - len(send_length))
#     client.send(send_length)
#     client.send(message)
#     print(client.recv(2048).decode(FORMAT))


# send("1")
# time.sleep(9)
# send("2")
# # input()
# # send("Hello Everyone!")
# # input()
# # send("Hello Tim!")

# # send(DISCONNECT_MESSAGE)
# ===============================
# import socket

# HEADERSIZE = 10

# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((socket.gethostname(), 1234))

# while True:
#     full_msg = ''
#     new_msg = True
#     while True:
#         msg = s.recv(16)
#         if new_msg:
#             print("new msg len:", msg[:HEADERSIZE])
#             msglen = int(msg[:HEADERSIZE])
#             new_msg = False

#         print(f"full message length: {msglen}")

#         full_msg += msg.decode("utf-8")

#         print(len(full_msg))

#         if len(full_msg)-HEADERSIZE == msglen:
#             print("full msg recvd")
#             print(full_msg[HEADERSIZE:])
#             new_msg = True

# ====================================
# import socket
# import time
# HOST = '127.0.0.1'  # The server's hostname or IP address
# PORT = 65432        # The port used by the server

# # clientsocket.send(bytes(msg, "utf-8"))

# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b'Hello, world')
#     s.sendall(b'Hello, world')

#     data = s.recv(1024)
#     # for i in range(1, 9):
#     #     msg= i.encode(FORMAT)
#     #     s.sendall(b'Hello, world')


# print('Received', repr(data))
# ==
# import socket


# def client_program():
#     host = socket.gethostname()  # as both code is running on same pc
#     port = 5000  # socket server port number

#     client_socket = socket.socket()  # instantiate
#     client_socket.connect((host, port))  # connect to the server

#     message = input(" -> ")  # take input

#     while message.lower().strip() != 'bye':
#         client_socket.send(message.encode())  # send message
#         data = client_socket.recv(1024).decode()  # receive response

#         print('Received from server: ' + data)  # show in terminal

#         message = input(" -> ")  # again take input

#     client_socket.close()  # close the connection


# if __name__ == '__main__':
#     client_program()
# ===
# lets make the client code
# import socket
# import cv2
# import pickle
# import struct

# # create socket
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_ip = '192.168.137.1'  # paste your server ip address here
# port = 9999
# client_socket.connect((host_ip, port))  # a tuple
# data = b""
# payload_size = struct.calcsize("Q")
# while True:
#     while len(data) < payload_size:
#         packet = client_socket.recv(4*1024)  # 4K
#         if not packet:
#             break
#         data += packet
#     packed_msg_size = data[:payload_size]
#     data = data[payload_size:]
#     msg_size = struct.unpack("Q", packed_msg_size)[0]

#     while len(data) < msg_size:
#         data += client_socket.recv(4*1024)
#     frame_data = data[:msg_size]
#     data = data[msg_size:]
#     frame = pickle.loads(frame_data)
#     cv2.imshow("RECEIVING VIDEO", frame)
#     key = cv2.waitKey(1) & 0xFF
#     if key == ord('q'):
#         break
# client_socket.close()
# ====
import socket
import select
import errno
import time

HEADER_LENGTH = 10

IP = "127.0.0.1"
PORT = 1234
my_username = input("Username: ")

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(False)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

while True:

    # Wait for user to input a message
    for i in range(1, 9):
        time.sleep(1)
    #  message = input(f'{my_username} > ')
        message = str(i)

    # If message is not empty - send it
        if message:

            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

    # try:
    #     # Now we want to loop over received messages (there might be more than one) and print them
    #     while True:

    #         # Receive our "header" containing username length, it's size is defined and constant
    #         username_header = client_socket.recv(HEADER_LENGTH)

    #         # If we received no data, server gracefully closed a connection, for example using socket.close() or socket.shutdown(socket.SHUT_RDWR)
    #         if not len(username_header):
    #             print('Connection closed by the server')
    #             sys.exit()

    #         # Convert header to int value
    #         username_length = int(username_header.decode('utf-8').strip())

    #         # Receive and decode username
    #         username = client_socket.recv(username_length).decode('utf-8')

    #         # Now do the same for message (as we received username, we received whole message, there's no need to check if it has any length)
    #         message_header = client_socket.recv(HEADER_LENGTH)
    #         message_length = int(message_header.decode('utf-8').strip())
    #         message = client_socket.recv(message_length).decode('utf-8')

    #         # Print message
    #         print(f'{username} > {message}')

    # except IOError as e:
    #     # This is normal on non blocking connections - when there are no incoming data error is going to be raised
    #     # Some operating systems will indicate that using AGAIN, and some using WOULDBLOCK error code
    #     # We are going to check for both - if one of them - that's expected, means no incoming data, continue as normal
    #     # If we got different error code - something happened
    #     if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
    #         print('Reading error: {}'.format(str(e)))
    #         sys.exit()

    #     # We just did not receive anything
    #     continue

    # except Exception as e:
    #     # Any other exception - something happened, exit
    #     print('Reading error: '.format(str(e)))
    #     sys.exit()
