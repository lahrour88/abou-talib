
from flask import Flask 
app = Flask(__name__ )

class Post:
    def __init__(self, body,date ,page,title,name,topic ,img1 ,img2,img3,img4):
        self.body = body
        self.date=date
        self.page=page
        self.title = title 
        self.name=name
        self.topic=topic
        self.img1=img1
        self.img2=img2
        self.img3=img3
        self.img4=img4
        
class users:
    def __init__(self ,password , email , name , matier ,is_admin ,profile_filename):
        self.password=password
        self.email=email
        self.name=name
        self.matier=matier
        self.is_admin=is_admin
        self.profile_filename =profile_filename
