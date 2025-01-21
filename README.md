# CCTV Video Streaming Application

This repository contains the implementation of a **CCTV Video Streaming Application** using Python, OpenCV, and sockets. The system includes sender, final server, and a final hop server for handling and displaying live video streams over a network.

## Features
- Real-time video streaming.
- Compression of video frames to optimize data transfer.
- Efficient handling of network communication using sockets.
- Displays received video feed on the final server.

## Code Overview
### Files
1. `final_server.py`: The final server that receives and displays the video feed.
2. `sender.py`: The sender script responsible for capturing video and sending it to the final server.
3. `hoop_server.py`: An intermediary hop server that forwards the video stream to the final server.

### `final_server.py`
- Listens for incoming connections on port `8082`.
- Receives video frame data from the last hop (hoop server).
- Decompresses, deserializes, and displays the video feed using OpenCV.

## Prerequisites
- Python 3.7 or higher
- Libraries: Install the following using pip:
  ```bash
  pip install opencv-python
  pip install opencv-contrib-python
  pip install zlib
  ```
- Ensure the devices running the scripts are on the same network for seamless communication.

## Usage
### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/cctv-streaming.git
cd cctv-streaming
```

### 2. Run the Scripts
#### Step 1: Start the Final Server
```bash
python final_server.py
```
This will start the final server and listen on port `8082`.

#### Step 2: Run the Sender and Hoop Server
Ensure the `sender.py` sends video data to the `hoop_server.py`, which forwards it to `final_server.py`. Detailed instructions for running the sender and hoop server will be included in their respective files.

### 3. Display Video Feed
The final server will display the video feed in a window titled **CCTV Feed**. Press `q` to close the feed and terminate the final server.

## How It Works
1. The **sender** captures video frames using OpenCV.
2. Frames are serialized, compressed using zlib, and sent over the network.
3. The **hoop server** forwards the compressed frames to the final server.
4. The **final server** decompresses and deserializes the frames, displaying the video feed using OpenCV.

## Error Handling
- Handles connection drops gracefully.
- Logs errors related to data transmission or frame decoding.

## Future Enhancements
- Add encryption for secure video transmission.
- Implement multi-client support to allow multiple senders to send video streams to a single final server.
- Include a configuration file for customizable ports and IPs.

## Contributing
Feel free to fork the repository, make changes, and submit pull requests. Contributions are welcome!

## License
This project is licensed under the MIT License. See the `LICENSE` file for more details.

---
For questions or support, please contact El-lunatico(mailto:pushkarkr030@gmail.com).

