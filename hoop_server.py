import socket
import struct
import zlib
import pickle
import cv2

# Hop server configuration
NEXT_HOP_IP = '127.0.0.1'  # IP of the next hop or final server
NEXT_HOP_PORT = 8082  # Port of the next hop or final server

# Create a socket object for the current hop
current_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
current_socket.bind(('0.0.0.0', 8081))  # Listen on port 8081
current_socket.listen(5)
print("Hop server is listening...")

# Accept connection from the previous hop or client
client_socket, addr = current_socket.accept()
print(f"Connection established with {addr}")

# Create a socket object for the next hop
next_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
next_socket.connect((NEXT_HOP_IP, NEXT_HOP_PORT))
print(f"Connected to next hop: {NEXT_HOP_IP}:{NEXT_HOP_PORT}")

# Data handling loop
payload_size = struct.calcsize("L")
data = b""

while True:
    try:
        # Receive message size
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet:
                print("Connection closed by client.")
                break
            data += packet

        if len(data) < payload_size:
            break

        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("L", packed_msg_size)[0]

        # Receive the actual frame data
        while len(data) < msg_size:
            data += client_socket.recv(4096)

        compressed_frame_data = data[:msg_size]
        data = data[msg_size:]

        
        # Decompress and deserialize the frame
        frame_data = zlib.decompress(compressed_frame_data)
        frame = pickle.loads(frame_data)

        # Display the frame
        cv2.imshow('HOOP_CCTV Feed', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


        # Forward the data to the next hop
        next_socket.sendall(packed_msg_size + compressed_frame_data)

    except Exception as e:
        print(f"Error in hop server: {e}")
        break

# Close connections
client_socket.close()
next_socket.close()
current_socket.close()
