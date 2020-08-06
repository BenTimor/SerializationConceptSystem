from utils import database

class Config:
    config = None

    def __init__(self, users, posts, comments):
        self.users = users
        self.posts = posts
        self.comments = comments
        Config.config = self

    @staticmethod
    def update():
        database["concept", True]["config", "WHERE id=1"] = Config.config

    @staticmethod
    def setup():
        try:
            Config.config = database["concept", True]["config", "WHERE id=1"][0][0]
        except:
            Config.config = Config([User("Admin", "admin123", True)], [Post("Admin", 0, "Hello World!", "Lorem Ipsum")], {0: [Comment("Admin", "Lorem Ipsum")]})
            database["concept", True]["config"] = Config.config

class User:
    def __init__(self, name, password, is_admin=False):
        self.name = name
        self.is_admin = is_admin
        self.password = password

    @staticmethod
    def new_user(name, password, is_admin=False):
        Config.config.users.append(User(name, password, is_admin))
        Config.update()

    @staticmethod
    def get_user(name):
        for user in Config.config.users:
            if user.name == name:
                return user

class Post:
    def __init__(self, user, id, title, content):
        self.user = user
        self.id = id
        self.title = title
        self.content = content

    @staticmethod
    def new_post(user, title, content):
        Config.config.posts.append(Post(user, len(Config.config.posts), title, content))
        Config.update()

class Comment:
    def __init__(self, user, content):
        self.user = user
        self.content = content

    @staticmethod
    def new_comment(post, user, content):
        if not Config.config.comments[post]:
            Config.config.comments[post] = []
        Config.config.comments[post].append(Comment(user, content))
        Config.update()