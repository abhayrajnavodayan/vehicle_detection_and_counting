import cv2
import numpy as np
from flask import Flask, render_template, Response

app = Flask(__name__)

# Web Camera
cap = cv2.VideoCapture('video.mp4')
min_width_rect = 80  # min width rectangle
min_height_rect = 80  # min height rectangle
count_line_position = 550

# Initialize Subtractor
algo = cv2.createBackgroundSubtractorMOG2()

def center_handle(x, y, w, h):  # this is for counting the vehicle
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

detect = []
offset = 6  # Allowable error between pixel
counter = 0  # Initialize counter as a global variable

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    global counter  # Declare counter as a global variable
    while True:
        ret, frame1 = cap.read()  # for reading the video
        if not ret:
            break
        grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)  # Changing into gray color
        blur = cv2.GaussianBlur(grey, (3, 3), 5)

        # Applying on each frame
        img_sub = algo.apply(blur)
        dilat = cv2.dilate(img_sub, np.ones((5, 5)))
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
        dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)
        countershape, h = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)  # this is line which will be drawn on frame

        for (x, y) in detect:
            if y < (count_line_position + offset) and y > (count_line_position - offset):
                counter += 1  # this will count the number of vehicles
                cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (127, 255, 0), 3)  # This will change the color of the line when a vehicle will cross it.
                detect.remove((x, y))  # it will remove and detect
                print('Vehicle Counter:' + str(counter))

        cv2.putText(frame1, 'VEHICLE COUNTER:' + str(counter), (450, 70), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 0, 255), 5)

        for (i, c) in enumerate(countershape):
            (x, y, w, h) = cv2.boundingRect(c)
            validate_counter = (w >= min_width_rect) and (h >= min_height_rect)
            if not validate_counter:
                continue
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)  # this is for making a rectangle around the vehicle
            cv2.putText(frame1, 'Vehicle' + str(counter), (x, y - 20), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (255, 244, 0), 2)
            center = center_handle(x, y, w, h)
            detect.append(center)
            cv2.circle(frame1, center, 4, (0, 0, 255), -1)

        ret, buffer = cv2.imencode('.jpg', frame1)
        frame1 = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame1 + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
