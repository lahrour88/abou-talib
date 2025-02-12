
class Post:
    def __init__(self, id, photo_url, body, date,page,vedio):
        self.id = id
        self.photo_url = photo_url
        self.body = body
        self.date = date
        self.page=page
        self.vedio=vedio
        

class PostStore:
    def __init__(self):
        self.posts = []

    def add(self, post):
        self.posts.append(post)

    def get_all(self):
        return self.posts[::-1]