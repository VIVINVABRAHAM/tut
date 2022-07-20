from django.shortcuts import render
import pyrebase
from regex import E
from django.contrib import auth
config={

    "apiKey": "AIzaSyBHarVpnSGSt5UrG_k8KXd9KuBlIYK3vwU",
    "authDomain": "tita-1a2a0.firebaseapp.com",
    "databaseURL": "https://tita-1a2a0-default-rtdb.firebaseio.com",
    "projectId": "tita-1a2a0",
    "storageBucket": "tita-1a2a0.appspot.com",
    "messagingSenderId": "875507388348",
    "appId": "1:875507388348:web:762f3437dceabda94025b9",
    "measurementId": "G-6GTETXK7QR"

}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()
database=firebase.database()
