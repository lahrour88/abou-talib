
from flask import Flask 
app = Flask(__name__)

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

data={'id': 334,
       'body': 'e\r\ne\r\ne\r\ne\r\ne\r\ne\r\ne\r\ne\r\ne\r\ne\r\ne',
         'page': 'sport',
           'title': 'eeeeeeeeeeeeeee',
             'date': '2025-09-25',
               'img1': 'https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/images/posts/1b8e3d7b38cd423d912473a981cbc9c0_1758827483.png',
                'name': 'abdelaadime lahrour',
                'topic': '',
                'img2': 'https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/images/posts/4c1973dcbbdd4182bb6e9119b627f730_1758827484.png',
                'img3': 'https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/images/posts/0ff3ab0a0c004bbe98e6bcc336a18f05_1758827484.png',
                'img4': 'https://biytrshphtxlywabygcc.supabase.co/storage/v1/object/public/images/posts/8e583934470a4399b3a677fab32f9998_1758827484.png',
                'img1_name': '1b8e3d7b38cd423d912473a981cbc9c0_1758827483.png',
                'img2_name': '4c1973dcbbdd4182bb6e9119b627f730_1758827484.png',
                'img3_name': '0ff3ab0a0c004bbe98e6bcc336a18f05_1758827484.png',
                'img4_name': '8e583934470a4399b3a677fab32f9998_1758827484.png'}