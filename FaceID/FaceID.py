from model import *
from module import *
import cv2
import os

siamese_model = tf.keras.models.load_model('siamesemodelv2.h5', 
                                   custom_objects={'L1Dist':L1Dist, 'BinaryCrossentropy':tf.losses.BinaryCrossentropy})

cap = cv2.VideoCapture(0)
c = 5

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    x, y, w, h = 180, 50, 270, 270
    frame1 = frame[y:y + h, x:x + w, :]

    start_point = (x, y)
    end_point = (x + w, y + h)
    thickness = 2

    if c == 5:
        color = (255, 0, 0)
        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)

    if cv2.waitKey(10) & 0xFF == ord('v'):
        cv2.imwrite(os.path.join('application_data', 'input_image', 'input_image.jpg'), frame1)
        results, verified = verify(siamese_model, 0.5, 0.5)
        if verified:
            c = 1
            print("verified")
        else:
            c = 0
            print("unverified")

    if c == 1:
        color = (0, 255, 0)
        text = "Verified"
        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
    elif c == 0:
        color = (0, 0, 255)
        text = "Unverified"
        frame = cv2.rectangle(frame, start_point, end_point, color, thickness)
    else:
        text = ""

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.6
    font_thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_x = x + (w - text_size[0]) // 2
    text_y = y + h + 25
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, color, font_thickness)

    cv2.imshow('Verification', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
