import cv2
import numpy as np
import time
from win10toast import ToastNotifier
from urllib.parse import quote

# RTSP stream credentials
username = "your_username"
password = "your_password"

# URL-encode the username and password
encoded_username = quote(username)
encoded_password = quote(password)

# RTSP stream URL with encoded authentication (assuming the default port 554)
rtsp_url = f"rtsp://{encoded_username}:{encoded_password}@IP_ADDRESS/stream2"

# Initialize variables
movement_detected = False
movement_start_time = time.time()
no_movement_time_threshold = 10  # 10 seconds - feel free to change this

# Create a ToastNotifier object
toaster = ToastNotifier()

# Open the RTSP stream
cap = cv2.VideoCapture(rtsp_url)

# Check if the stream opened successfully
if not cap.isOpened():
    print("Error: Could not open the stream.")
    exit()

# Read the first frame to initialize background
ret, frame1 = cap.read()
if not ret:
    print("Error: Could not read the frame.")
    exit()

# Convert the first frame to grayscale
gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
gray1 = cv2.GaussianBlur(gray1, (21, 21), 0)

while True:
    # Read the next frame
    ret, frame2 = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.GaussianBlur(gray2, (21, 21), 0)

    # Compute the absolute difference between the current frame and the previous frame
    frame_diff = cv2.absdiff(gray1, gray2)

    # Apply a threshold to get the binary image
    _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the frame
    for contour in contours:
        if cv2.contourArea(contour) < 500:
            continue
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame2, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Check if movement is detected
    if len(contours) > 0:
        movement_detected = True
        movement_start_time = time.time()
        print("Movement detected.")
    else:
        movement_detected = False

    # If no movement is detected for the threshold time, notify the user
    if not movement_detected and time.time() - movement_start_time > no_movement_time_threshold:
        print("No movement detected for 10 seconds.")
        toaster.show_toast("Motion Detection", "No movement detected for 10 seconds.", duration=30)
        break

    # Display the resulting frame
    cv2.imshow('RTSP Stream', frame2)

    # Update the previous frame
    gray1 = gray2

    # Exit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
