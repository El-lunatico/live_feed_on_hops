import cv2
import socket
import pickle
import struct
import zlib

# Client configuration
NEXT_HOP_IP = '127.0.0.1'  # IP of the next hop or final server
NEXT_HOP_PORT = 8081  # Port of the next hop or final server

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((NEXT_HOP_IP, NEXT_HOP_PORT))
print(f"Connected to {NEXT_HOP_IP}:{NEXT_HOP_PORT}")

# Open a connection to the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame")
        break

    # Resize frame for faster transmission
    frame = cv2.resize(frame, (640, 480))

    # Serialize and compress the frame
    data = pickle.dumps(frame)
    compressed_data = zlib.compress(data)

    # Pack the frame size and send it along with the data
    message_size = struct.pack("L", len(compressed_data))

    try:
        client_socket.sendall(message_size + compressed_data)
        print(f"Frame sent, size: {len(compressed_data)} bytes")
    except Exception as e:
        print(f"Error sending data: {e}")
        break

    # Preview the frame locally (optional)
    cv2.imshow('Webcam Streaming Preview', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
client_socket.close()
cv2.destroyAllWindows()
