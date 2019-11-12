import pyrebase
import time
config = {
    "apiKey": "AIzaSyBwfvkoffX7MNGrWrf7nYYQ9wmOwS5_yaI",
    "authDomain": "stpwin-home.firebaseapp.com",
    "databaseURL": "https://stpwin-home.firebaseio.com",
    "storageBucket": "stpwin-home.appspot.com",
    "messagingSenderId": "796798924451",
    "appId": "1:796798924451:web:f0c42c137da2bdb69cf116"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()
data = {"value": 900, "timestamp": time.time()}
db.child("device").child("bmp280").child(
    "pressure").child(int(time.time())).set(900)
