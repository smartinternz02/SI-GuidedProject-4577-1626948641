import numpy as np
import os
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import tensorflow as tf
from twilio.rest import Client
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
app = Flask(__name__)
model = load_model(
    "/Users/aishaandatt/Downloads/Externship IBM/PROJECT_IBM/animal_custom.h5")


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['image']
        print("current path")
        basepath = os.path.dirname(__file__)
        print("current path", basepath)
        filepath = os.path.join(basepath, 'uploads', f.filename)
        print("upload folder is ", filepath)
        f.save(filepath)

        img = image.load_img(filepath, target_size=(64, 64))
        x = image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        preds = model.predict(x)

        print("prediction", preds)

        index = ['Domestic Animal', 'Human', 'Wild Animal']

        print(np.argmax(preds))

        text = "the predicted animal is : " + str(index[np.argmax(preds)])
        if np.argmax(preds) == 2:
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
        else:
            print("No Danger")
       # break
    return text


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
