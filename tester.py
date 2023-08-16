import socketio

# Initialize the SocketIO client
sio = socketio.Client()

# Define the message to send
message = {
    "user_input": "I want a saree for onam"
}

# Define event handlers
@sio.on("connect")
def on_connect():
    print("Connected to server")

@sio.on("message")
def on_message(data):
    print("Received response from server:")
    print(data)

@sio.on("disconnect")
def on_disconnect():
    print("Disconnected from server")

if __name__ == "__main__":
    # Connect to the Flask socket server
    sio.connect("http://127.0.0.1:3000")
    
    # Emit the 'message' event with the user input
    sio.emit("message", message)
    
    # Wait for the response and keep the connection alive for a few seconds
    sio.wait(seconds=5)
    
    # Disconnect from the server
    sio.disconnect()
