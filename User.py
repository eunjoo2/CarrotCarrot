class User:
    user_list = []

    def __init__(self, user_id, nick_name, area_name, phone_num, temper, block_list, bad_count):
        self.user_id = user_id
        self.nick_name = nick_name
        self.area_name = area_name
        self.phone_num = phone_num
        self.temper = temper
        self.block_list = block_list
        self.bad_count = bad_count

        # 로그인 성공여부 체크를 위한 모드
        self.cookie = False
        self.user = {}

    def register(self):
        User.user_list.append(self)
        print(f"등록 완료 : {self.nick_name} ")


    @classmethod
    def login(cls,phone_num):
        for user in cls.user_list:
            if user.phone_num == phone_num:
                print("로그인에 성공하였습니다.")
                user.cookie = True
            return user
        print("로그인에 실패하였습니다.")
        return None

    def logout(self):
        if self.cookie:
            self.cookie = False
            print(f"[로그아웃 성공] {self.nick_name} 님 로그아웃되었습니다.")
        else:
            print(f"[로그아웃 실패] {self.nick_name} 님은 현재 로그인 상태가 아닙니다.")



    # i = 유저 아이디 , p = 폰 번호
    @classmethod
    def show_all_users(cls):
        print("현재 등록된 유저 목록:")
        for user in cls.user_list:
            print(f"- {user.user_id}: {user.nick_name} ({user.area_name})")

    @classmethod
    def delete(cls,user_id):
        for user in cls.user_list:
            if user.user_id == user_id:
                cls.user_list.remove(user)
                print(f"해당 유저는 삭제되었습니다: {user.nick_name} ")



# 테스트용 실행
if __name__ == "__main__":
    # 첫 번째 유저 생성 및 등록

    u1 = User("u001", "민기", "서울", "010-1111-2222", 36.5, 0, 0)
    u1.register()

    logged_user = User.login("010-1111-2222")

    if logged_user:
        logged_user.logout()

    User.show_all_users()
    User.delete("u001")


