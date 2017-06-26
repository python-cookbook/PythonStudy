import random
import re
import os
import ctypes


###################################################################################################
## 기록 관련 클래스
###################################################################################################
class Record:
    def __init__(self):
        self.__hit = 0  # 안타 수
        self.__homerun = 0  # 홈런 수
        self.__atbat = 0  # 타수
        self.__avg = 0.6  # 타율
        self.__rbi = 0  # 타점

    @property
    def hit(self):
        return self.__hit

    @hit.setter
    def hit(self, hit):
        self.__hit = hit

    @property
    def homerun(self):
        return self.__homerun

    @homerun.setter
    def homerun(self, homerun):
        self.__homerun = homerun

    @property
    def atbat(self):
        return self.__atbat

    @atbat.setter
    def atbat(self, atbat):
        self.__atbat = atbat

    @property
    def avg(self):
        return self.__avg

    @avg.setter
    def avg(self, avg):
        self.__avg = avg

    @property
    def rbi(self):
        return self.__rbi

    @rbi.setter
    def rbi(self, rbi):
        self.__rbi = rbi

    # 타자 기록 관련 메서드
    def batter_record(self, hit, homerun):
        self.hit += hit
        self.homerun += homerun
        self.atbat += 1
        self.avg = self.hit / self.atbat

    # 타자 타점 관련 메서드
    def batter_rbi(self, rbi):
        self.rbi += rbi

###################################################################################################
## 선수 관련 클래스
###################################################################################################
class Player:
    def __init__(self, team_name, number, name):
        self.__team_name = team_name  # 팀 이름
        self.__number = number  # 타순
        self.__name = name  # 이름
        self.__record = Record()  # 기록

    @property
    def team_name(self):
        return self.__team_name

    @property
    def number(self):
        return self.__number

    @property
    def name(self):
        return self.__name

    @property
    def record(self):
        return self.__record

    @property
    def player_info(self):
        return self.__team_name + ', ' + str(self.__number) + ', ' + self.__name

    # 선수 타율 관련 메서드
    def hit_and_run(self, hit, homerun):
        self.__record.batter_record(hit, homerun)

    # 선수 타점 관련 메서드
    def rbi(self, rbi):
        self.__record.batter_rbi(rbi)

###################################################################################################
## 팀 관련 클래스
###################################################################################################
class Team:
    def __init__(self, team_name, players):
        self.__team_name = team_name  # 팀 이름
        self.__player_list = self.init_player(players)  # 해당 팀 소속 선수들 정보

    @property
    def team_name(self):
        return self.__team_name

    @property
    def player_list(self):
        return self.__player_list

    # 선수단 초기화
    def init_player(self, players):
        temp = []
        for player in players:
            number, name = list(player.items())[0]
            temp.append(Player(self.__team_name, number, name))
        return temp

    def show_players(self):
        for player in self.__player_list:
            print(player.player_info)


###################################################################################################
## 게임 관련 클래스
###################################################################################################
class Game:
    TEAM_LIST = {
        '한화': (
        {1: '정근우'}, {2: '이용규'}, {3: '송광민'}, {4: '최진행'}, {5: '하주석'}, {6: '장민석'}, {7: '로사리오'}, {8: '이양기'}, {9: '최재훈'}),
        '롯데': (
        {1: '나경민'}, {2: '손아섭'}, {3: '최준석'}, {4: '이대호'}, {5: '강민호'}, {6: '김문호'}, {7: '정훈'}, {8: '번즈'}, {9: '신본기'}),
        '삼성': (
        {1: '박해민'}, {2: '강한울'}, {3: '구자욱'}, {4: '이승엽'}, {5: '이원석'}, {6: '조동찬'}, {7: '김헌곤'}, {8: '이지영'}, {9: '김정혁'}),
        'KIA': (
        {1: '버나디나'}, {2: '이명기'}, {3: '나지완'}, {4: '최형우'}, {5: '이범호'}, {6: '안치홍'}, {7: '서동욱'}, {8: '김민식'}, {9: '김선빈'}),
        'SK': (
        {1: '노수광'}, {2: '정진기'}, {3: '최정'}, {4: '김동엽'}, {5: '한동민'}, {6: '이재원'}, {7: '박정권'}, {8: '김성현'}, {9: '박승욱'}),
        'LG': (
        {1: '이형종'}, {2: '김용의'}, {3: '박용택'}, {4: '히메네스'}, {5: '오지환'}, {6: '양석환'}, {7: '임훈'}, {8: '정상호'}, {9: '손주인'}),
        '두산': (
        {1: '허경민'}, {2: '최주환'}, {3: '민병헌'}, {4: '김재환'}, {5: '에반스'}, {6: '양의지'}, {7: '김재호'}, {8: '신성현'}, {9: '정진호'}),
        '넥센': (
        {1: '이정후'}, {2: '김하성'}, {3: '서건창'}, {4: '윤석민'}, {5: '허정협'}, {6: '채태인'}, {7: '김민성'}, {8: '박정음'}, {9: '주효상'}),
        'KT': (
        {1: '심우준'}, {2: '정현'}, {3: '박경수'}, {4: '유한준'}, {5: '장성우'}, {6: '윤요섭'}, {7: '김사연'}, {8: '오태곤'}, {9: '김진곤'}),
        'NC': (
        {1: '김성욱'}, {2: '모창민'}, {3: '나성범'}, {4: '스크럭스'}, {5: '권희동'}, {6: '박석민'}, {7: '지석훈'}, {8: '김태군'}, {9: '이상호'})
    }

    INNING = 0  # 1 이닝부터 시작
    CHANGE = 0  # 0 : hometeam, 1 : awayteam
    STRIKE_CNT = 0  # 스트라이크 개수
    OUT_CNT = 0  # 아웃 개수
    ADVANCE = [0, 0, 0]  # 진루 상황
    SCORE = [0, 0]  # [home, away]
    BATTER_NUMBER = [1, 1]  # [home, away] 타자 순번

    def __init__(self, game_team_list):
        print('====================================================================================================')
        print('== 선수단 구성')
        print('====================================================================================================')
        print(game_team_list[0] + ' : ', Game.TEAM_LIST[game_team_list[0]])
        print(game_team_list[1] + ' : ', Game.TEAM_LIST[game_team_list[1]])
        print('====================================================================================================')
        self.__hometeam = Team(game_team_list[0], Game.TEAM_LIST[game_team_list[0]])
        self.__awayteam = Team(game_team_list[1], Game.TEAM_LIST[game_team_list[1]])
        print('== 선수단 구성이 완료 되었습니다.\n')

    @property
    def hometeam(self):
        return self.__hometeam

    @property
    def awayteam(self):
        return self.__awayteam


    def get_save_path(self):
        self.save_path = input("Enter the file name and file location : ")
        self.save_path = self.save_path.replace("\\", "/")
        if not os.path.isdir(os.path.split(self.save_path)[0]):
            os.mkdir(os.path.split(self.save_path)[0])  # 폴더가 없으면 만드는 작업
        return self.save_path


    # 게임 수행 메서드
    def start_game(self,weather):

        while Game.INNING <= weather:
            print(
                '====================================================================================================')
            print('== {} 이닝 {} 팀 공격 시작합니다.'.format(Game.INNING,
                                                   self.hometeam.team_name if Game.CHANGE == 0 else self.awayteam.team_name))
            print(
                '====================================================================================================\n')

            self.attack()
            if Game.CHANGE == 2:  # 이닝 교체
                Game.INNING += 1
                Game.CHANGE = 0

        print('====================================================================================================')
        print('== 게임 종료!!!')
        print('====================================================================================================\n')
        self.show_record()

    # 팀별 선수 기록 출력
    def show_record(self):
        f = open(self.get_save_path(), 'a')
        labels = ['선수이름', '타율', '타석', '안타', '홈런', '타점']
        print('====================================================================================================')
        print('==  {} | {}   =='.format(self.hometeam.team_name.center(44, ' ') if re.search('[a-zA-Z]+',
                                                                                             self.hometeam.team_name) is not None else self.hometeam.team_name.center(
            42, ' '),
                                        self.awayteam.team_name.center(44, ' ') if re.search('[a-zA-Z]+',
                                                                                             self.awayteam.team_name) is not None else self.awayteam.team_name.center(
                                            42, ' ')))
        print('==  {} | {}   =='.format(('(' + str(Game.SCORE[0]) + ')').center(44, ' '),
                                        ('(' + str(Game.SCORE[1]) + ')').center(44, ' ')))
        print('====================================================================================================')
        print('== {} | {} | {} | {} | {} | {}'.format('이름'.center(8, ' '), '타율'.center(5, ' '), '타석'.center(4, ' '),
                                                  '안타'.center(3, ' '), '홈런'.center(3, ' '), '타점'.center(3, ' ')), end='')
        print('| {} | {} | {} | {} | {} | {} =='.format('이름'.center(8, ' '), '타율'.center(5, ' '), '타석'.center(4, ' '),
                                                    '안타'.center(3, ' '), '홈런'.center(3, ' '), '타점'.center(3, ' ')))
        print('====================================================================================================')

        hometeam_players = self.hometeam.player_list
        awayteam_players = self.awayteam.player_list

        f.write(str(game_team_list[0]) + ', ')
        f.write(str(Game.SCORE[0]) + '\n')

        for label in labels:
            f.write(label + ', ')
        f.write('\n')

        for i in range(9):
            hp = hometeam_players[i]
            hp_rec = hp.record
            ap = awayteam_players[i]
            ap_rec = ap.record
            hp_labels = [hp.name, hp_rec.avg, hp_rec.atbat, hp_rec.hit, hp_rec.homerun, hp_rec.rbi]

            print('== {} | {} | {} | {} | {} | {} '.format(hp.name.center(6 + (4 - len(hp.name)), ' '),
                                                       str(hp_rec.avg).center(7, ' '),
                                                       str(hp_rec.atbat).center(6, ' '), str(hp_rec.hit).center(5, ' '),
                                                       str(hp_rec.homerun).center(5, ' '), str(hp_rec.rbi).center(5, ' ')), end='')
            print(' {} | {} | {} | {} | {} | {} =='.format(ap.name.center(6 + (4 - len(ap.name)), ' '),
                                                       str(ap_rec.avg).center(7, ' '),
                                                       str(ap_rec.atbat).center(6, ' '), str(ap_rec.hit).center(5, ' '),                                                    str(ap_rec.homerun).center(5, ' '), str(ap_rec.rbi).center(5, ' ')))
            for hp_label in hp_labels:
                f.write(str(hp_label) + ', ')
            f.write('\n')


        f.write(str(game_team_list[1]) + ', ')
        f.write(str(Game.SCORE[1]) + '\n')

        for j in range(9):
            ap = awayteam_players[j]
            ap_rec = ap.record
            ap_labels = [ap.name, ap_rec.avg, ap_rec.atbat, ap_rec.hit, ap_rec.homerun, ap_rec.rbi]

            for ap_label in ap_labels:
                f.write(str(ap_label) + ', ')
            f.write('\n')

        f.write('\n')
        print('====================================================================================================')
        f.close()



    # 공격 수행 메서드
    def attack(self):
        curr_team = self.hometeam if Game.CHANGE == 0 else self.awayteam
        player_list = curr_team.player_list
        if abs(Game.SCORE[0] - Game.SCORE[1]) < 20:
            if Game.OUT_CNT < 3:
                player = self.select_player(Game.BATTER_NUMBER[Game.CHANGE], player_list)
                print(
                    '====================================================================================================')
                print('== [{}] {}번 타자[{}] 타석에 들어섭니다.'.format(curr_team.team_name, player.number, player.name))
                print(
                    '====================================================================================================\n')
                while True:
                    random_numbers = self.throws_numbers()  # 컴퓨터가 랜덤으로 숫자 4개 생성
                    print(self.number_randomly(),'타율적용한 랜덤 숫자 범위')                     # ran_num_1은 number_randomly
                    print(
                        '== [전광판] =========================================================================================')
                    print('==   {}      | {} : {}'.format(Game.ADVANCE[1], self.hometeam.team_name, Game.SCORE[0]))
                    print('==  {}  {}    | {} : {}'.format(Game.ADVANCE[2], Game.ADVANCE[0], self.awayteam.team_name,
                                                           Game.SCORE[1]))
                    print('== [OUT : {}, STRIKE : {}]'.format(Game.OUT_CNT, Game.STRIKE_CNT))
                    print(
                        '====================================================================================================')
                    print('== 현재 타석 : {}번 타자[{}], 타율 : {}, 타점 : {}'.format(player.number, player.name, player.record.avg, player.record.rbi))

                    try:
                        check_num = self.number_randomly()
                        if check_num == 20:
                            hit_numbers = set(int(hit_number) for hit_number in
                                              input('== 숫자를 입력하세요(1~20) : ').split(' '))  # 유저가 직접 숫자 4개 입력
                            if self.hit_number_check(hit_numbers) is False:
                                raise Exception()
                        else:
                            hit_numbers = set(int(hit_number) for hit_number in
                                              input('== 숫자를 입력하세요(1~40) : ').split(' '))  # 유저가 직접 숫자 4개 입력
                            if self.hit_number_check(hit_numbers) is False:
                                raise Exception()
                    except Exception:
                        ctypes.windll.user32.MessageBoxW(None, '숫자를 잘못 입력하셨습니다.', "Error", 0)
                        print(
                            '====================================================================================================')
                        print('▶ 컴퓨터가 발생 시킨 숫자 : {}\n'.format(random_numbers))
                        continue
                    print(
                        '====================================================================================================')
                    print('▶ 컴퓨터가 발생 시킨 숫자 : {}\n'.format(random_numbers))
                    hit_cnt = self.hit_judgment(random_numbers, hit_numbers)  # 안타 판별
                    num_random_choice = random.randrange(1,101)          # ran_num은 num_random_choice
                    print(num_random_choice,'파울을 결정하는 random숫자 1~19까지는 파울이 아님')
                    if num_random_choice < 98 or hit_cnt == 0:
                        if hit_cnt == 0:  # strike !!!
                            Game.STRIKE_CNT += 1
                            print('== ▣ 스트라이크!!!\n')
                            if Game.STRIKE_CNT == 3:
                                print('== ▣ 삼진 아웃!!!\n')
                                Game.STRIKE_CNT = 0
                                Game.OUT_CNT += 1
                                break
                        else:
                            Game.STRIKE_CNT = 0
                            if hit_cnt != 4:
                                print('== ▣ {}루타!!!\n'.format(hit_cnt))
                            else:
                                print('== ▣ {} {} 점 홈런!!!\n'.format(player.name, Game.ADVANCE.count(1)+1))
                            self.advance_setting(hit_cnt)
                            break
                    elif num_random_choice == 99 and hit_cnt >= 1:
                        if Game.STRIKE_CNT == 0 or Game.STRIKE_CNT == 1:
                            Game.STRIKE_CNT += 1
                            print('== ▣ 파울!!!\n')
                        elif Game.STRIKE_CNT == 2:
                            Game.STRIKE_CNT = 2
                            print('== ▣ 파울!!!\n')
                    elif num_random_choice== 100:
                        print('데드볼')
                        if Game.ADVANCE == [0,0,0] or Game.ADVANCE==[0,1,0] or Game.ADVANCE==[0,1,1] or Game.ADVANCE==[0,0,1]:
                            Game.ADVANCE[0] = 1   # 1루에 주자 없을때

                        elif Game.ADVANCE.count(1) == 2:
                            Game.ADVANCE = [1,1,1]

                        elif Game.ADVANCE == [1,1,1]:
                            Game.SCORE[Game.CHANGE] += 1
                            player.rbi(1)
                        elif Game.ADVANCE == [1,0,0]:
                            Game.ADVANCE = [1,1,0]
                        #
                        # else:
                        #     for i in range(len(Game.ADVANCE), 0, -1):
                        #         if Game.ADVANCE[i - 1] == 1:
                        #             if (i + 1) > 3:  # 기존에 출루한 선수들 중 득점 가능한 선수들에 대한 진루 설정
                        #                 Game.SCORE[Game.CHANGE] += 1
                        #                 player.rbi(1)
                        #                 Game.ADVANCE[i - 1] = 0
                        #             else:  # 기존 출루한 선수들 중 득점권에 있지 않은 선수들에 대한 진루 설정
                        #                 Game.ADVANCE[i - 1 + 1] = 1
                        #                 Game.ADVANCE[i - 1] = 0
                            # Game.ADVANCE[hit_cnt - 1] = 1  # 타석에 있던 선수에 대한 진루 설정



                            # 만루일때 1점 증가
                            #     else:  # 기존 출루한 선수들 중 득점권에 있지 않은 선수들에 대한 진루 설정
                            #         Game.ADVANCE[i - 1 + 1] = 1
                            #         Game.ADVANCE[i - 1] = 0
                            # Game.ADVANCE[1] = 1  # 타석에 있던 선수에 대한 진루 설정




                player.hit_and_run(1 if hit_cnt > 0 else 0, 1 if hit_cnt == 4 else 0)
                if Game.BATTER_NUMBER[Game.CHANGE] == 9:
                    Game.BATTER_NUMBER[Game.CHANGE] = 1
                else:
                    Game.BATTER_NUMBER[Game.CHANGE] += 1
                self.attack()
            else:
                Game.CHANGE += 1
                Game.STRIKE_CNT = 0
                Game.OUT_CNT = 0
                Game.ADVANCE = [0, 0, 0]
                print(
                    '====================================================================================================')
                print('== 공수교대 하겠습니다.')
                print(
                '====================================================================================================\n')
        elif abs(Game.SCORE[0] - Game.SCORE[1]) > 19:
            print('CalledGame으로 {}'.format(self.hometeam.team_name if Game.SCORE[0] - Game.SCORE[1] > 0  else self.awayteam.team_name),abs(Game.SCORE[0] - Game.SCORE[1]),'점차로 승리하셨습니다')
            Game.INNING = 10
            self.show_record()
            quit()

    # 진루 및 득점 설정하는 메서드
    def advance_setting(self, hit_cnt):
        curr_team = self.hometeam if Game.CHANGE == 0 else self.awayteam
        player_list = curr_team.player_list
        player = self.select_player(Game.BATTER_NUMBER[Game.CHANGE], player_list)

        if hit_cnt == 4:  # 홈런인 경우
            Game.SCORE[Game.CHANGE] += Game.ADVANCE.count(1)+1
            player.rbi(Game.ADVANCE.count(1)+1)
            Game.ADVANCE = [0, 0, 0]
        else:
            for i in range(len(Game.ADVANCE), 0, -1):
                if Game.ADVANCE[i - 1] == 1:
                    if (i + hit_cnt) > 3:  # 기존에 출루한 선수들 중 득점 가능한 선수들에 대한 진루 설정
                        Game.SCORE[Game.CHANGE] += 1
                        player.rbi(1)
                        Game.ADVANCE[i - 1] = 0
                    else:  # 기존 출루한 선수들 중 득점권에 있지 않은 선수들에 대한 진루 설정
                        Game.ADVANCE[i - 1 + hit_cnt] = 1
                        Game.ADVANCE[i - 1] = 0
            Game.ADVANCE[hit_cnt - 1] = 1  # 타석에 있던 선수에 대한 진루 설정


    # 컴퓨터가 생성한 랜덤 수와 플레이어가 입력한 숫자가 얼마나 맞는지 판단
    def hit_judgment(self, random_ball, hit_numbers):
        cnt = 0
        for hit_number in hit_numbers:
            if hit_number in random_ball:
                cnt += 1
        return cnt

    # 선수가 입력한 숫자 확인
    def hit_number_check(self, hit_numbers):
        check_num = self.number_randomly()                                            # ddd는 check_num
        if check_num == 20:
            if len(hit_numbers) == 4:
                for hit_number in hit_numbers:
                    if hit_number <= 0 or hit_number > 20:
                        return False
                return True
            return False
        else:
            if len(hit_numbers) == 4:
                for hit_number in hit_numbers:
                    if hit_number <= 0 or hit_number > 40:
                        return False
                return True
            return False

    # 선수 선택
    def select_player(self, number, player_list):
        for player in player_list:
            if number == player.number:
                return player

    def number_randomly(self):                                # ran_num_1은 number_randomly
        curr_team = self.hometeam if Game.CHANGE == 0 else self.awayteam
        player_list = curr_team.player_list
        player = self.select_player(Game.BATTER_NUMBER[Game.CHANGE], player_list)
        avg = player.record.avg
        if avg >= 0.5:
            return int(20)
        elif avg < 0.5:
            return int(40)

    # 랜덤으로 숫자 생성(1~20)
    def throws_numbers(self):
        random_balls = set()
        random_no = self.number_randomly()                               # ab는 random_no
        while True:
            random_balls.add(random.randint(1, 4))  # 1 ~ 20 중에 랜덤 수를 출력
            if len(random_balls) == 4:  # 생성된 ball 이 4개 이면(set 객체라 중복 불가)
                return random_balls


class Weather:
    def weather_search(team_for_loc):              # team1은 team_for_loc, loc은 location의 약자
        import urllib.request
        from  bs4 import BeautifulSoup
        import re

        team_stadium = team_for_loc                 # abc는 team_stadium
        if team_stadium == '넥센':
            print('돔구장이라 상관없이 9회 진행합니다.')
            return 1

        else:
            team = {
                '두산': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%9E%A0%EC%8B%A4+%EB%82%A0%EC%94%A8',
                'LG': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%9E%A0%EC%8B%A4+%EB%82%A0%EC%94%A8',
                'SK': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%AC%B8%ED%95%99%EB%8F%99+%EB%82%A0%EC%94%A8',
                '삼성': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%97%B0%ED%98%B8%EB%8F%99+%EB%82%A0%EC%94%A8',
                '한화': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EB%B6%80%EC%82%AC%EB%8F%99+%EB%82%A0%EC%94%A8',
                'KIA': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%9E%84%EB%8F%99+%EB%82%A0%EC%94%A8',
                '롯데': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%82%AC%EC%A7%81%EB%8F%99+%EB%82%A0%EC%94%A8',
                'KT': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%A1%B0%EC%9B%90%EB%8F%99+%EB%82%A0%EC%94%A8',
                'NC': 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=1&ie=utf8&query=%EC%96%91%EB%8D%95%EB%8F%99+%EB%82%A0%EC%94%A8'}
            team_for_weather = team[team_stadium]                                     # a는 team_for_weather
            # binary = 'D:\chromedriver/chromedriver.exe'
            # browser = webdriver.Chrome(binary)
            list_url = team_for_weather
            url = urllib.request.Request(list_url)
            res = urllib.request.urlopen(url).read().decode('utf-8')
            soup = BeautifulSoup(res, 'html.parser')
            weather_contents = soup.find('div', class_='contents03')               # b는 weather_contents
            now_weather = weather_contents.find_all('div', class_='w_now2')[0]      # c는 now_weather
            img_weather = now_weather.find('img')                                    # d는 img_weather
            print('===============================================================================================')
            weather_get_text = img_weather.get_text().split()[2]                      # e는 weather_get_text
            celcius = re.sub('[1-9,℃]', '', weather_get_text)                             # f는 celcius
            print(celcius)

            if celcius == '비':
                print('날씨관계로 6회까지만 진행합니다.')
                return int(6)
            else:
                print('정상적으로 9회 진행합니다.')
                return int(9)


if __name__ == '__main__':
    game_start = ctypes.windll.user32.MessageBoxW(None, '게임을 시작하시겠습니까?', "게임 시작", 4)
    if game_start == 6:
        while True:
            game_team_list = []
            print('=============================================================================================================')
            print('한화(대전) | 롯데(부산) | 삼성(대구) | KIA(광주) | SK(인천) | LG(잠실) | 두산(잠실) | 넥센(고척) | KT(수원) | NC(마산) |')
            print('=============================================================================================================')
            game_team_list = input('=> 게임을 진행할 두 팀을 입력하세요 : ').split(' ')
            print('===========================================================================================================\n')
            if (game_team_list[0] in Game.TEAM_LIST) and (game_team_list[1] in Game.TEAM_LIST):
                weather = Weather.weather_search(game_team_list[0])
                game = Game(game_team_list)
                game.start_game(weather)
                break
            else:
                ctypes.windll.user32.MessageBoxW(None, '팀명을 잘못 입력하셨습니다.', "Error", 0)
    else:
        print('게임을 종료합니다.')
