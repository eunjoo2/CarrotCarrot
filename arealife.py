from datetime import datetime
from User import User

# # 사용자 클래스 : 사용자 정보
# class User:
#     def __init__(self, user_id, name, location):
#         self.user_id = user_id # 회원 고유 아이디
#         self.name = name # 사용자 이름
#         self.location = location # 지역 정보
#         self.posts = [] # 사용자가 작성한 게시글을 저장하는 리스트
#
#     # 사용자가 게시글을 작성할 때 posts 리스트에 게시글을 추가
#     def write_post(self, post):
#         self.posts.append(post)
#
#     def __str__(self):
#         return f'{self.name}({self.location})'

# 동네생활 클래스 : 게시글 하나의 정보
class AreaLife:
    def __init__(self, life_id, user, title, content, status):
        self.life_id = life_id # 게시글 고유 ID
        self.user = user # 작성자
        self.title = title # 게시글 제목
        self.content = content # 게시글 내용
        self.status = status # 게시글 상태

        self.timestamp = datetime.now() # 게시글 작성 시각(현재 시각)
        self.comments = [] # 댓글 저장 리스트
        self.views = 0 # 조회수 초기값
        self.likes = set() # '공감하기'를 누른 사용자 집합(중복 방지용)

        # 작성자가 작성한 글 목록에 추가
        self.user.write_post(self)

    # 게시글 조회시 조회수를 1씩 증가
    def view(self):
        self.views = self.views + 1

    # 게시글에 댓글 추가
    def add_comment(self, comment):
        self.comments.append(comment)

    # 사용자가 게시글에 '공감하기'를 누르는 함수
    def like(self, user):
        if user not in self.likes: # '공감하기'를 누른적이 없으면
            self.likes.add(user) # '공감하기' 집합에 추가
            print(f'{user.nick_name} 님이 공감하기를 눌렀습니다.')
        else:
            print(f'{user.nick_name} 님은 이미 공감하기를 눌렀습니다.')

    # 사용자가 '공감하기'를 취소하는 함수
    def unlike(self, user):
        if user in self.likes: # '공감하기'를 누른 상태면
            self.likes.remove(user) # '공감하기' 집합에서 제거
            print(f'{user.nick_name} 님이 공감하기를 취소했습니다.')
        else:
            print(f'{user.nick_name} 님은 공감하기를 누르지 않았습니다.')

    def __str__(self):
        return (f'[제목 :{self.title}] / 작성자 : {self.user}' f'조회수 : {self.views}, 좋아요{len(self.likes)}')

# 댓글 클래스
class Comment:
    def __init__(self, content, user):
        self.content = content # 댓글 내용
        self.user = user # 댓글 작성자(user)
        self.timestamp = datetime.now() # 댓글 작성 시각

    def __str__(self):
        return f'{self.user.nick_name} : {self.content}'

# 게시글 전체 관리 클래스(게시판)
class AreaLifeBoard:
    def __init__(self):
        self.posts = [] # 등록된 모든 게시글을 저장하는 리스트
        self.next_id = 1 # 게시물 인덱스 번호

    # 게시글 생성 함수
    def create_post(self, user, title, content, status):
        if not user.cookie:
            print(f'[글쓰기 실패] {user.nick_name} 님은 로그인 상태가 아닙니다.')
            return None

        post = AreaLife(self.next_id, user, title, content, status) # 새 게시글 객체 생성
        self.posts.append(post) # 게시판에 게시글 추가
        self.next_id = self.next_id + 1 # 다음 게시글 번호 증가
        return post

    # 게시글 목록 전체 출력
    def list_posts(self):
        for post in self.posts:
            print(post)

    # 특정 제목을 가진 게시글을 검색하고 조회수 1 증가
    def find_post_by_title(self, title):
        for post in self.posts:
            if post.title == title:
                post.view() # 조회수 1 증가
                return post
        print(f'[검색 실패] {title} 제목의 글이 없습니다.')
        return None # 없으면 None 반환