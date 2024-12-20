import socket
import cv2
import pickle
import struct
import zlib

# Final server configuration
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('0.0.0.0', 8082))  # Listen on port 8082
server_socket.listen(5)
print("Final server is listening...")

# Accept a connection from the last hop
client_socket, addr = server_socket.accept()
print(f"Connection established with {addr}")

# Variables for receiving data
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
        cv2.imshow('CCTV Feed', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    except Exception as e:
        print(f"Error receiving data: {e}")
        break

# Release resources
client_socket.close()
server_socket.close()
cv2.destroyAllWindows()
