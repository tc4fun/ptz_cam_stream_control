from flask import Flask, render_template, request, jsonify
import subprocess
import socket

app = Flask(__name__)

def get_server_ip():
    """Get the server's external IP address."""
    import socket
    try:
        # Create a temporary socket to determine the external IP address
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Use a non-routable IP and port to determine the local interface
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        print(f"Error determining external IP: {e}")
        return "127.0.0.1"  # Fallback to localhost if detection fails

def send_ptz_command(control, value):
    """
    Send a PTZ command using v4l2-ctl.
    control: The V4L2 control name (e.g., pan_speed, tilt_speed, zoom_absolute).
    value: The target value for the control.
    """
    try:
        command = ["v4l2-ctl", "-d", "/dev/video0", f"--set-ctrl={control}={value}"]
        print("Executing command:", " ".join(command))
        subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return f"PTZ command sent: {control}={value}"
    except subprocess.CalledProcessError as e:
        error_message = e.stderr.decode().strip()
        return f"Failed to send PTZ command: {error_message}"

@app.route("/")
def index():
    """Render the PTZ control page."""
    server_ip = get_server_ip()
    return render_template("index.html", server_ip=server_ip)

@app.route("/control", methods=["POST"])
def control():
    """
    Handle PTZ control commands from the web interface.
    """
    direction = request.form.get("direction")
    action = request.form.get("action")  # "start", "stop", or zoom level

    if not direction:
        return jsonify({"error": "Missing direction"}), 400

    # Determine control and value based on direction and action
    if direction == "down":
        control = "tilt_speed"
        value = -1 if action == "start" else 0
    elif direction == "up":
        control = "tilt_speed"
        value = 1 if action == "start" else 0
    elif direction == "left":
        control = "pan_speed"
        value = -1 if action == "start" else 0
    elif direction == "right":
        control = "pan_speed"
        value = 1 if action == "start" else 0
    elif direction == "zoom":
        control = "zoom_absolute"
        value = int(action)  # Zoom level passed directly from slider
    else:
        return jsonify({"error": "Invalid direction"}), 400

    # Send the PTZ command
    result = send_ptz_command(control, value)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
