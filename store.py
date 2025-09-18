
from flask import Flask 
app = Flask(__name__)

class Post:
    def __init__(self,public_url, photo_url, body,date ,page,title,name,topic):
        self.photo_url = photo_url
        self.body = body
        self.date=date
        self.page=page
        self.title = title 
        self.public_url= public_url
        self.name=name
        self.topic=topic
        


class users:
    def __init__(self ,password , email , name , matier ,is_admin ,profile_filename):
        self.password=password
        self.email=email
        self.name=name
        self.matier=matier
        self.is_admin=is_admin
        self.profile_filename =profile_filename
