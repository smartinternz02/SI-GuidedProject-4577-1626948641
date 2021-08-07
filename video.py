#import opencv
import cv2
#import numpy
import numpy as np
from keras.preprocessing import image
from keras.models import load_model
# import Client from twilio API
from twilio.rest import Client

model = load_model(
    '/Users/aishaandatt/Downloads/Externship IBM/PROJECT_IBM/animal_custom.h5')
# To read webcam
video = cv2.VideoCapture(0)
# Type of classes or names of the labels that we considered
name = ['Domestic Animal', 'Human', 'Wild Animal']
# To execute the program repeatedly using while loop
while(1):
    success, frame = video.read()
    cv2.imwrite("image.jpg", frame)
    img = image.load_img("image.jpg", target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    pred = model.predict_classes(x)
    p = pred[0]
    # print(pred)
    cv2.putText(frame, "predicted  class = "+str(name[p]), (100, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)

    pred = model.predict_classes(x)
    if pred[0] == 2:
        # twilio account ssid
        account_sid = 'AC4c30a8e1c7127a077cbf05414eb7ef38'
        # twilo account authentication toke
        auth_token = 'd22f9b76fffb3403cda21cec95461000'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
                body='Danger!. Wild animal is detected, stay alert',
                from_=' +12293515154',  # the free number of twilio
                to='+919149492527')
        print(message.sid)
        print('Danger!!')
        print('Animal Detected')
        print('SMS sent!')
        # break
    else:
        print("No Danger")
       # break
    cv2.imshow("image", frame)
    if cv2.waitKey(1) & 0xFF == ord('a'):
        break

video.release()
cv2.destroyAllWindows()
