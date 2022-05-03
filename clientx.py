# ==
# python clientx.py --shape-predictor shape_predictor_68_face_landmarks.dat
import socket
import select
import errno
# import time
# ==
from scipy.spatial import distance as dist
from imutils.video import FileVideoStream
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2
# ==
HEADER_LENGTH = 10

#IP = "192.168.1.10"
PORT = 1234
my_username = input("Username: ")
IP = input("IP: ")

# Create a socket
# socket.AF_INET - address family, IPv4, some otehr possible are AF_INET6, AF_BLUETOOTH, AF_UNIX
# socket.SOCK_STREAM - TCP, conection-based, socket.SOCK_DGRAM - UDP, connectionless, datagrams, socket.SOCK_RAW - raw IP packets
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to a given ip and port
client_socket.connect((IP, PORT))

# Set connection to non-blocking state, so .recv() call won;t block, just return some exception we'll handle
client_socket.setblocking(True)

# Prepare username and header and send them
# We need to encode username to bytes, then count number of bytes and prepare header of fixed size, that we encode to bytes as well
username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
client_socket.send(username_header + username)

# ==


def aspek_rasio_mata(mata):
    # Menghitung jarak euclidean antara dua set
    # landmark mata vertikal (x, y) -dikordinasikan
    A = dist.euclidean(mata[1], mata[5])
    B = dist.euclidean(mata[2], mata[4])

    # hitung jarak euclidean antara horizontal
    # mata landmark (x, y) -coordinate
    C = dist.euclidean(mata[0], mata[3])

    # menghitung rasio aspek mata
    arm = (A + B) / (2.0 * C)

    # mengembalikan rasio aspek mata
    return arm


# bangun argumen parse dan parsing argumen
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--shape-predictor", required=True,
                help="path to facial landmark prediksi")
ap.add_argument("-v", "--video", type=str, default="",
                help="path to input video file")
args = vars(ap.parse_args())

# tentukan dua konstanta, satu untuk rasio aspek mata untuk ditunjukkan
# berkedip dan kemudian konstanta kedua untuk jumlah berturut-turut
# membingkai mata harus di bawah ambang batas
thres_kedip = 0.2
batas_ambang = 3

# menginisialisasi penghitung bingkai dan jumlah total kedipan
hitung = 0
total = 0

# inisialisasi pendeteksi wajah dlib (berbasis HOG) lalu buat
# Prediktor tengara wajah
print("[INFO] loading facial landmark prediksi...")
detektor = dlib.get_frontal_face_detector()
prediksi = dlib.shape_predictor(args["shape_predictor"])

# ambil indeks landmark wajah untuk kiri dan
# mata kanan, masing-masing
(krMulai, krAkhir) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(knMulai, knAkhir) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

# mulai utas streaming video
print("[INFO] starting video stream thread...")
# vs = FileVideoStream(args["video"]).start()
# fileStream = True
vs = VideoStream(src=0).start()
# vs = VideoStream(usePiCamera=True).start()
fileStream = False
time.sleep(1.0)
p = 0
g = 0
r = 100
total1 = 0
total2 = 0

# while True:


# for i in range(1, 9):
#     time.sleep(1)
#     message = str(i)
#     # If message is not empty - send it
#     if message:
#         # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
#         message = message.encode('utf-8')
#         message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
#         client_socket.send(message_header + message)

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


while True:
    # jika ini adalah aliran video file, maka kita perlu memeriksa apakah
    # masih ada frame yang tersisa di buffer untuk diproses
    if fileStream and not vs.more():
        break

    # ambil bingkai dari aliran file video berulir, ubah ukuran
    # itu, dan ubah menjadi grayscale
    # saluran)
    frame = vs.read()
    # ksize = (30, 30)
    # frame = cv2.blur(frame, ksize)
    frame = imutils.resize(frame, width=600)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # mendeteksi wajah dalam bingkai abu-abu
    rects = detektor(gray, 0)

    # loop over the face detections
    for rect in rects:
        # tentukan landmark wajah untuk wilayah wajah, lalu
        # Konversikan landmark wajah (x, y) -dikordinasikan ke NumPy
        # Himpunan
        bentuk = prediksi(gray, rect)
        bentuk = face_utils.shape_to_np(bentuk)

        # ekstrak koordinat mata kiri dan kanan, lalu gunakan
    # Koordinat untuk menghitung rasio aspek mata untuk kedua mata
        matakanan = bentuk[krMulai:krAkhir]
        matakiri = bentuk[knMulai:knAkhir]
        armkiri = aspek_rasio_mata(matakanan)
        armkanan = aspek_rasio_mata(matakiri)

        # rata-rata rasio aspek mata bersama untuk kedua mata
        arm = (armkiri + armkanan) / 2.0

        # hitung cembung lambung untuk mata kiri dan kanan, lalu
    # Visualisasikan setiap mata
        frame_matakanan = cv2.convexHull(matakanan)
        frame_matakiri = cv2.convexHull(matakiri)
        cv2.drawContours(frame, [frame_matakanan], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [frame_matakiri], -1, (0, 255, 0), 1)

        # periksa untuk melihat apakah rasio aspek mata di bawah blink
    # threshold, dan jika ya, tambahkan penghitung bingkai blink
        if arm < thres_kedip:
            hitung += 1

        # jika tidak, rasio aspek mata tidak di bawah blink
    # threshold
        else:
            # jika mata ditutup untuk jumlah yang cukup
            # lalu menambah jumlah total kedipan
            if hitung >= batas_ambang:
                total += 1

            # mengatur ulang penghitung bingkai mata
            hitung = 0

        # gambarkan jumlah total kedipan pada bingkai bersama dengan
    # rasio aspek mata yang dihitung untuk bingkai
        cv2.putText(frame, "Berkedip: {}".format(total), (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "Rasio Mata: {:.2f}".format(arm), (250, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # tunjukkan bingkai
    p += 1
    # total1 = total
    if (p % 200 == 0):
        # total2 = total1
        total1 = total

    if (p % 300 == 0):
        if (total1 == total):
            r = 255
            g = 0
            # send("1")
            message = "INACTIVATE"
            # If message is not empty - send it
            # if message:
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)
        else:
            r = 0
            g = 255
            # send("0")
            message = "ACTIVATE"
            # If message is not empty - send it
            # if message:
            # Encode message to bytes, prepare header and convert to bytes, like for username above, then send
            message = message.encode('utf-8')
            message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
            client_socket.send(message_header + message)

    if (p == 1000):
        p = 0

    cv2.putText(frame, "iterasi: {:.2f}".format(p), (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "sementara: {:.2f}".format(total1), (250, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.putText(frame, "cek: {:.2f}".format(total), (100, 90),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    cv2.circle(frame, (10, 320), 10, (0, g, r), -2)
    cv2.imshow("Hasil Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # jika tombol `q` ditekan, patahkan dari loop
    if key == ord("q"):
        break

# lakukan sedikit pembersihan
cv2.destroyAllWindows()
vs.stop()
