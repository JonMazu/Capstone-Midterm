from flask import Response
from flask import Flask
from flask import render_template, request
from phue import Bridge
import cv2

main = Flask(__name__)
vid = cv2.VideoCapture(0)

def generateFrames():#Generates the frames and returns them to the page.
    while True:
        success, frame = vid.read()
        if (success):
            cv2.imwrite('place.jpg',frame)
            yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + open('place.jpg', 'rb').read() + b'\r\n')
        else:
            break


@main.route('/', methods = ['POST'])
def input(): #This is where you handle your inputs from the webpage
    hue =  Bridge('192.168.1.248')
    if request.method == "POST":
        if(request.form.get("submit") == "connect"):
            try:
                hue.connect()
            except:
                print("Press the button Doof")
        if(request.form.get("submit") == "toggle"):
            if(hue.get_light("Jon's light", 'bri') <= 1):
                hue.set_light("Jon's light", 'bri', 254)
            else:
                hue.set_light("Jon's light", 'bri', 0)

    return render_template("indexHue.html")

@main.route('/')
def index():
    return render_template('indexHue.html') 

@main.route('/video_feed')
def video_feed():
    return Response(generateFrames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    main.run(debug=True, use_reloader=False)