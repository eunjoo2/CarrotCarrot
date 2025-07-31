from datetime import datetime

class User:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.posts = []

    def write_post(self, post):
        self.posts.append(post)

    def __str__(self):
        return f'{self.name}({self.location})'

class Post:
    def __init__(self, title, content, category, user):
        self.title = title
        self.content = content
        self.category = category
        self.user = user
        self.timestamp = datetime.now()
        self.comments = []

        self.views = 0
        self.likes = set()

        user.write_post(self)

    def view(self):
        self.views = self.views + 1

    def add_comment(self, comment):
        self.comments.append(comment)

    def like(self, user):
        if user not in self.likes:
            self.likes.add(user)
            print(f'{user.name} 님이 좋아요를 눌렀습니다.')
        else:
            print(f'{user.name} 님은 이미 좋아요를 눌렀습니다.')

    def unlike(self, user):
        if user in self.likes:
            self.likes.remove(user)
            print(f'{user.name} 님이 좋아요를 취소했습니다.')
        else:
            print(f'{user.name} 님은 좋아요를 누르지 않았습니다.')

    def __str__(self):
        return (f'{self.category}{self.title} / 작성자 : {self.user}' f'조회수 : {self.views}, 좋아요{len(self.likes)}')

class Comment:
    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id
        self.timestamp = datetime.now()

    def __str__(self):
        return f'{self.user_id.name} : {self.content}'

class AreaLife:
    def __init__(self):
        self.posts = []

    def create_post(self, title, content, category, user_id):
        post = Post(title, content, category, user_id)
        self.posts.append(post)
        return post

    def list_posts(self, category_filter = None):
        for post in self.posts:
            if category_filter is None or post.category == category_filter:
                print(post)

    def find_post_by_title(self, title):
        for post in self.posts:
            if post.title == title:
                post.view()
                return post
        return None