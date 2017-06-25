import random
import re
# import pandas as pd
import csv
from operator import itemgetter

# 3조
# csv 파일 형태 : 팀명/선수명/안타수/홈런수/타수/타율/체력/부상여부

###################################################################################################
## 기록 및 스테이터스 관련 클래스
###################################################################################################
class Record:
    def __init__(self):
        # 기록
        self.__hit = 0  # 안타 수
        self.__homerun = 0  # 홈런 수
        self.__atbat = 0  # 타수
        self.__avg = 0.0  # 타율
        # 상태
        self.__hp = 100  # 체력(health point)
        self.__hp_dec = random.randint(0,2)  # 체력감소율
        self.__condition = {0:'good',1:'normal',2:'bad'}  # 컨디션
        self.__injure_n = random.randint(0, 20)   # 부상 랜덤수 생성
        # self.__injure = ''

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
    def hp(self):
        return self.__hp

    @hp.setter
    def hp(self, hp):
        self.__hp = hp

    @property
    def hp_dec(self):
        return self.__hp_dec

    @hp_dec.setter
    def hp_dec(self, hp_dec):
        self.__hp_dec = hp_dec

    @property
    def injure_n(self):
        return self.__injure_n

    @injure_n.setter
    def injure_n(self, injure_n):
        self.__injure_n = injure_n

    @property
    def condition(self):
        return self.__condition

    @condition.setter
    def condition(self, condition):
        self.__condition = condition

    # @property
    # def injure(self):
    #     return self.__injure
    #
    # @injure.setter
    # def injure(self):
    #     if self.__injure_n < 20:
    #         self.__injure = 'False'
    #     else:
    #         self.__injure = 'True'


    # 타자 기록 관련 메서드
    def batter_record(self, hit, homerun):
        self.hit += hit
        self.homerun += homerun
        self.atbat += 1
        self.avg = self.hit / self.atbat

    # 타자 상태 관련 메소드
    def batter_status(self, hp_dec):
        if hp_dec == 0:
            self.hp -= 1
        elif hp_dec == 1:
            self.hp -= 3
        else: self.hp -= 5

    # 타자 부상 관련 메소드
    def batter_injure(self, injure_n):
        if injure_n < 20:
            return False
        else:
            return True

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

    # 선수 상태 관련 메소드
    def player_status(self, hp_dec):
        self.__record.batter_status(hp_dec)

    # 선수 부상 관련 메소드
    def player_injure(self, injure_n):
        self.__record.batter_injure(injure_n)

###################################################################################################
## 팀 관련 클래스b
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
        'HANHWA': ({1:'하주석'}, {2:'장민석'}, {3:'정근우'}, {4:'송광민'}, {5:'로사리오'}, {6:'김태균'}, {7:'양성우'}, {8:'강경학'}, {9:'차일목'}, {10:'이성열'}, {11:'최재훈'}, {12:'김회성'}, {13:'김경언'}, {14:'최진행'}, {15:'김원석'}, {16:'이동훈'}, {17:'이양기'}, {18:'조인성'}, {19:'허도환'}, {20:'이용규'}),
        'LOTTE': ({1:'손아섭'}, {2:'이대호'}, {3:'최준석'}, {4:'강민호'}, {5:'이우민'}, {6:'김문호'}, {7:'신본기'}, {8:'번즈'}, {9:'정훈'}, {10:'김상호'}, {11:'김동한'}, {12:'나경민'}, {13:'김대륙'}, {14:'문규현'}, {15:'김사훈'}, {16:'전준우'}, {17:'박헌도'}, {18:'황진수'}, {19:'김대우'}, {20:'김민수'}),
        'SAMSUNG': ({1:'구자욱'}, {2:'박해민'}, {3:'김헌곤'}, {4:'강한울'}, {5:'이지영'}, {6:'이승엽'}, {7:'조동찬'}, {8:'러프'}, {9:'이원석'}, {10:'배영섭'}, {11:'정병곤'}, {12:'김상수'}, {13:'권정웅'}, {14:'박한이'}, {15:'백상원'}, {16:'김정혁'}, {17:'성의준'}, {18:'김성윤'}, {19:'우동균'}, {20:'나성용'}),
        'KIA': ({1:'김선빈'}, {2:'최형우'}, {3:'나지완'}, {4:'버나디나'}, {5:'김민식'}, {6:'서동욱'}, {7:'안치홍'}, {8:'이명기'}, {9:'김주찬'}, {10:'한승택'}, {11:'이범호'}, {12:'김호령'}, {13:'신종길'}, {14:'김주형'}, {15:'김지성'}, {16:'고장혁'}, {17:'최원준'}, {18:'이진영'}, {19:'이호신'}, {19:'노관현'}),
        'SK': ({1:'이대수'}, {2:'최정용'}, {3:'한동민'}, {4:'최정'}, {5:'조용호'}, {6:'나주환'}, {7:'김동엽'}, {8:'정의윤'}, {9:'정진기'}, {10:'김성현'}, {11:'노수광'}, {12:'박정권'}, {13:'이재원'}, {14:'김강민'}, {15:'박승욱'}, {16:'로맥'}, {17:'이홍구'}, {18:'최승준'}, {19:'이성우'}, {20:'김주한'}),
        'LG': ({1:'박용택'}, {2:'강승호'}, {3:'백창수'}, {4:'정성훈'}, {5:'이형종'}, {6:'안익훈'}, {7:'이천웅'}, {8:'손주인'}, {9:'임훈'}, {10:'정상호'}, {11:'채은성'}, {12:'김재율'}, {13:'양석환'}, {14:'오지환'}, {15:'히메네스'}, {16:'김용의'}, {17:'조윤준'}, {18:'최재원'}, {19:'유강남'}, {20:'이병규'}),
        'DOOSAN': ({1:'김재환'}, {2:'민병헌'}, {3:'에반스'}, {4:'최주환'}, {5:'오재원'}, {5:'오재일'}, {7:'김재호'}, {8:'양의지'}, {9:'허경민'}, {10:'박건우'}, {11:'류지혁'}, {12:'박세혁'}, {13:'정진호'}, {14:'국해성'}, {15:'조수행'}, {16:'신성현'}, {17:'김인태'}, {18:'김민혁'}, {19:'이성곤'}, {20:'김강률'}),
        'NEXEN': ({1:'이정후'}, {2:'윤석민'}, {3:'김하성'}, {4:'서건창'}, {5:'김민성'}, {6:'채태인'}, {7:'고종욱'}, {8:'허정협'}, {9:'박동원'}, {10:'이택근'}, {11:'김재현'}, {12:'김웅빈'}, {13:'김태완'}, {14:'김지수'}, {15:'박정음'}, {16:'주효상'}, {17:'대니돈'}, {18:'송성문'}, {19:'유재신'}, {20:'김규민'}),
        'KT': ({1:'오정복'}, {2:'유한준'}, {3:'이진영'}, {4:'김동욱'}, {5:'이대형'}, {6:'박경수'}, {7:'심우준'}, {8:'이해창'}, {9:'정현'}, {10:'오태곤'}, {11:'장성우'}, {12:'박기혁'}, {13:'윤요섭'}, {14:'유민상'}, {15:'하준호'}, {16:'김사연'}, {17:'김연훈'}, {18:'로하스'}, {19:'전민수'}, {20:'김진곤'}),
        'NC': ({1:'김태우'}, {2:'강진성'}, {3:'나성범'}, {4:'박민우'}, {5:'이상호'}, {6:'이종욱'}, {7:'손시헌'}, {8:'모창민'}, {9:'스크럭스'}, {10:'권희동'}, {11:'김준완'}, {12:'김태군'}, {13:'박석민'}, {14:'박광열'}, {15:'김성욱'}, {16:'지석훈'}, {17:'황윤호'}, {18:'윤병호'}, {19:'도태훈'}, {20:'조평호'})
    }
    INNING = 1  # 1 이닝부터 시작
    CHANGE = 0  # 0 : hometeam, 1 : awayteam
    STRIKE_CNT = 0  # 스트라이크 개수
    OUT_CNT = 0  # 아웃 개수
    ADVANCE = [0, 0, 0]  # 진루 상황
    SCORE = [0, 0]  # [home, away]
    BATTER_NUMBER = [1, 1]  # [home, away] 타자 순번

    def __init__(self, game_team_list):
        # csv 파일 위치
        self.home_location = "D:\\Baseball_data\\"+game_team_list[0]+".csv"
        self.away_location = "D:\\Baseball_data\\"+game_team_list[1]+".csv"

        # csv파일을 불러와서 임시로 담아두는 리스트
        self.home_temp = []
        self.away_temp = []

        # csv파일을 불러와서 정렬한다음 임시로 담아두는 리스트
        self.home_temp_sort = []
        self.away_temp_sort = []

        # csv파일을 불러올 때 int타입, float타입으로 불러오는 변수 구분
        self.int_labels = ['안타수', '체력', '홈런수', '타수']
        self.float_labels = ['타율']

        # 홈팀의 라인업을 담는 딕셔너리
        self.hometeam_dict = {}

        # 어웨이 팀의 라인업을 담는 딕셔너리
        self.awayteam_dict = {}

        # 홈팀 csv 로드
        with open(self.home_location, 'r') as f:
            for idx, item in enumerate(csv.DictReader(f), 0):
                for value in self.int_labels:
                    item[value] = int(item[value])
                for value in self.float_labels:
                    item[value] = round(float(item[value]), 3)
                self.home_temp.append(item)
        self.home_temp_sort = sorted(self.home_temp, key=itemgetter('체력'), reverse=True)
        print(self.home_temp_sort)

        # 어웨이팀 csv 로드
        with open(self.away_location, 'r') as f:
            for idx, item in enumerate(csv.DictReader(f), 0):
                for value in self.int_labels:
                    item[value] = int(item[value])
                for value in self.float_labels:
                    item[value] = round(float(item[value]), 3)
                    self.away_temp.append(item)

        self.away_temp_sort = sorted(self.away_temp, key=itemgetter('체력'), reverse=True)
        print(self.away_temp_sort)
        # 홈팀 라인업 구성
        self.value_h = tuple({int(i['등번호']): i['선수명']} for i in self.home_temp_sort)
        self.__hometeam = Team(game_team_list[0], self.value_h)
        #print(value_h)
        # 어웨이팀 라인업 구성
        self.value_a = tuple({int(i['등번호']): i['선수명']} for i in self.away_temp_sort)
        self.__awayteam = Team(game_team_list[1], self.value_a)
        #print(value_h)

        print('====================================================================================================')
        print('== 선수단 구성')
        print('====================================================================================================')
        print(game_team_list[0]+' : ', self.value_h)
        print(game_team_list[1]+' : ', self.value_a)
        print('====================================================================================================')
        print('== 선수단 구성이 완료 되었습니다.\n')


    @property
    def hometeam(self):
        return self.__hometeam

    @property
    def awayteam(self):
        return self.__awayteam

    # 게임 수행 메서드
    def start_game(self):
        while Game.INNING <= 1:
            print('====================================================================================================')
            print('== {} 이닝 {} 팀 공격 시작합니다.'.format(Game.INNING, self.hometeam.team_name if Game.CHANGE == 0 else self.awayteam.team_name))
            print('====================================================================================================\n')
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
        print('====================================================================================================')
        print('==  {} | {}   =='.format(self.hometeam.team_name.center(44, ' ') if re.search('[a-zA-Z]+', self.hometeam.team_name) is not None else self.hometeam.team_name.center(42, ' '),
                                        self.awayteam.team_name.center(44, ' ') if re.search('[a-zA-Z]+', self.awayteam.team_name) is not None else self.awayteam.team_name.center(42, ' ')))
        print('==  {} | {}   =='.format(('('+str(Game.SCORE[0])+')').center(44, ' '), ('('+str(Game.SCORE[1])+')').center(44, ' ')))
        print('====================================================================================================')
        print('== {} | {} | {} | {} | {} | {} | {} | {} '.format('이름'.center(8, ' '), '타율'.center(5, ' '), '타석'.center(4, ' '), '안타'.center(3, ' '), '홈런'.center(3, ' '), '체력'.center(3, ' '), '부상'.center(3, ' '), '컨디션'.center(2, ' ')), end='')
        print('| {} | {} | {} | {} | {} | {} | {} | {}  =='.format('이름'.center(8, ' '), '타율'.center(5, ' '), '타석'.center(4, ' '), '안타'.center(3, ' '), '홈런'.center(3, ' '), '체력'.center(3, ' '), '부상'.center(3, ' '), '컨디션'.center(3, ' ')))
        print('====================================================================================================')

        hometeam_players = self.hometeam.player_list
        awayteam_players = self.awayteam.player_list


        for i in range(9):
            hp = hometeam_players[i]
            hp_rec = hp.record
            ap = awayteam_players[i]
            ap_rec = ap.record

            # 홈팀 스탯
            print('== {} | {} | {} | {} | {} | {} | {} | {} '.format(hp.name.center(6+(4-len(hp.name)), ' '), str(round(float(hp_rec.avg), 2)).center(7, ' '),
                                                      str(hp_rec.atbat).center(6, ' '), str(hp_rec.hit).center(5, ' '), str(hp_rec.homerun).center(5, ' '),
                                                      str(hp_rec.hp).center(5, ' '), str(hp_rec.batter_injure(hp_rec.injure_n)).center(5, ' '), str(hp_rec.condition[hp_rec.hp_dec]).center(5, ' ')), end='')

            # 어웨이팀 스탯
            print(' {} | {} | {} | {} | {} | {} | {} | {} =='.format(ap.name.center(6+(4-len(ap.name)), ' '), str(round(float(ap_rec.avg), 2)).center(7, ' '),
                                                        str(ap_rec.atbat).center(6, ' '), str(ap_rec.hit).center(5, ' '), str(ap_rec.homerun).center(5, ' '),
                                                        str(ap_rec.hp).center(5, ' '),str(ap_rec.batter_injure(ap_rec.injure_n)).center(5, ' '), str(ap_rec.condition[ap_rec.hp_dec]).center(5, ' ')))

        # 홈팀 csv 파일 저장 + 체력 높은 순으로 정렬 + 정렬 후 높은 순으로 순위 부여
        home_csv1 = open('D://Baseball_data//'+game_team_list[0]+'.csv', 'r', encoding='euc_kr', newline='')
        home_csv1_read = csv.reader(home_csv1)
        temp_h = []
        for i in home_csv1_read:
            # ff.append(i)
            temp_h.append(i)
        home_csv1.close()

        temp_h2 = sorted(temp_h, key=lambda temp_h: temp_h[6], reverse=False)

        for i in range(0, len(temp_h2), 1):
            temp_h2[i].append(i + 1)
        # print(temp_h2)
        home_open_csv_header1 = open("d:/Baseball_data/"+game_team_list[0]+".csv", 'w', encoding='euc_kr', newline='')
        home_csv_writer1 = csv.writer(home_open_csv_header1)
        home_csv_writer1.writerow(['팀명', '선수명', '타수', '안타수', '홈런수', '타율', '체력', '부상여부', '등번호'])
        home_open_csv_header1.close()

        home_open_csv_header2 = open("d:/Baseball_data/"+game_team_list[0]+".csv", 'a', encoding='euc_kr', newline='')
        home_csv_writer2 = csv.writer(home_open_csv_header2)
        for i in range(0, 20, 1):
            home_csv_writer2.writerow(temp_h2[i])
        home_open_csv_header2.close()

        home_csv_read3 = open('D://Baseball_data//'+game_team_list[0]+'.csv', 'r', encoding='euc_kr', newline='')
        home_csv_reader3 = csv.reader(home_csv_read3)
        temp_h3 = []
        for ia in home_csv_reader3:
            # ff.append(i)
            temp_h3.append(ia)
        home_csv_read3.close()
        #print(temp_h3)

        # 어웨이팀 csv 파일 저장 + 체력 높은 순으로 정렬 + 정렬 후 높은 순으로 순위 부여
        away_csv1 = open('D://Baseball_data//'+game_team_list[1]+'.csv', 'r', encoding='euc_kr', newline='')
        away_csv1_read = csv.reader(away_csv1)
        temp_a = []
        for i in away_csv1_read:
            # ff.append(i)
            temp_a.append(i)
        away_csv1.close()

        temp_a2 = sorted(temp_a, key=lambda temp_a: temp_a[6], reverse=False)

        for i in range(0, len(temp_a2), 1):
            temp_a2[i].append(i + 1)
        # print(temp_h2)
        away_open_csv_header1 = open("d:/Baseball_data/"+game_team_list[1]+".csv", 'w', encoding='euc_kr', newline='')
        away_csv_writer1 = csv.writer(away_open_csv_header1)
        away_csv_writer1.writerow(['팀명', '선수명', '타수', '안타수', '홈런수', '타율', '체력', '부상여부', '등번호'])
        away_open_csv_header1.close()

        away_open_csv_header2 = open("d:/Baseball_data/"+game_team_list[1]+".csv", 'a', encoding='euc_kr', newline='')
        away_csv_writer2 = csv.writer(away_open_csv_header2)
        for i in range(0, 20, 1):
            away_csv_writer2.writerow(temp_a2[i])
        away_open_csv_header2.close()

        away_csv_read3 = open('D://Baseball_data//'+game_team_list[1]+'.csv', 'r', encoding='euc_kr', newline='')
        away_csv_reader3 = csv.reader(away_csv_read3)
        temp_a3 = []
        for ia in away_csv_reader3:
            # ff.append(i)
            temp_a3.append(ia)
        away_csv_read3.close()
        #print(temp_h3)

        # # 홈팀 선수 기록 세이브
        # for i in range(20):
        #     hp = hometeam_players[i]
        #     hp_rec = hp.record
        #     open_csv_header_h = open("d:/Baseball_data/"+game_team_list[0]+".csv", 'a', encoding='euc_kr', newline='')
        #     csv_writer_h = csv.writer(open_csv_header_h)
        #     csv_writer_h.writerow(
        #         [game_team_list[0], int(hp.number), hp.name, int(hp_rec.atbat), int(hp_rec.hit), int(hp_rec.homerun), round(float(hp_rec.avg),3),
        #          int(hp_rec.hp), hp_rec.batter_injure(hp_rec.injure_n)])
        #     open_csv_header_h.close()

        # # 어웨이팀 선수 기록 세이브
        # for i in range(20):
        #     ap = awayteam_players[i]
        #     ap_rec = ap.record
        #     open_csv_header_a = open("d:/Baseball_data/"+game_team_list[1]+".csv", 'a', encoding='euc_kr', newline='')
        #     csv_writer_a = csv.writer(open_csv_header_a)
        #     csv_writer_a.writerow(
        #         [game_team_list[1], int(ap.number), ap.name, int(ap_rec.atbat), int(ap_rec.hit), int(ap_rec.homerun), round(float(ap_rec.avg),3),
        #          int(ap_rec.hp), ap_rec.batter_injure(ap_rec.injure_n)])
        #     open_csv_header_a.close()

        # 홈팀 csv 정렬 및 순위 부여
        with open(self.home_location, 'r') as f:
            for idx, item in enumerate(csv.DictReader(f), 0):
                for value in self.int_labels:
                    item[value] = int(item[value])
                for value in self.float_labels:
                    item[value] = round(float(item[value]), 3)
                self.home_temp.append(item)
        self.home_temp_sort = sorted(self.home_temp, key=itemgetter('체력'), reverse=True)
        print(self.home_temp_sort)

        # 어웨이팀 csv 정렬 및 순위 부여
        with open(self.away_location, 'r') as f:
            for idx, item in enumerate(csv.DictReader(f), 0):
                for value in self.int_labels:
                    item[value] = int(item[value])
                for value in self.float_labels:
                    item[value] = round(float(item[value]), 3)
                    self.away_temp.append(item)





        print('====================================================================================================')





    # 공격 수행 메서드
    def attack(self):
        curr_team = self.hometeam if Game.CHANGE == 0 else self.awayteam
        player_list = curr_team.player_list

        if Game.OUT_CNT < 3:
            player = self.select_player(Game.BATTER_NUMBER[Game.CHANGE], player_list)
            print('====================================================================================================')
            print('== [{}] {}번 타자[{}] 타석에 들어섭니다.'.format(curr_team.team_name, player.number, player.name))
            print('====================================================================================================\n')

            while True:
                random_numbers = self.throws_numbers()  # 컴퓨터가 랜덤으로 숫자 4개 생성
                print('== [전광판] =========================================================================================')
                print('==   {}      | {} : {}'.format(Game.ADVANCE[1], self.hometeam.team_name, Game.SCORE[0]))
                print('==  {}  {}    | {} : {}'.format(Game.ADVANCE[2], Game.ADVANCE[0], self.awayteam.team_name, Game.SCORE[1]))
                print('== [OUT : {}, STRIKE : {}]'.format(Game.OUT_CNT, Game.STRIKE_CNT))
                print('====================================================================================================')
                print('== 현재 타석 : {}번 타자[{}], 타율 : {}'.format(player.number, player.name, player.record.avg))
                print('== 컨디션 : {}, 체력 : {}'.format(player.record.condition[player.record.hp_dec], player.record.hp))
                try:
                    hit_numbers = set(int(hit_number) for hit_number in input('== 숫자를 입력하세요(1~40) : ').split(' '))  # 유저가 직접 숫자 4개 입력
                    if self.hit_number_check(hit_numbers) is False:
                        raise Exception()
                except Exception:
                    print('== ▣ 잘못된 숫자가 입력되었습니다.')
                    print('====================================================================================================')
                    print('▶ 컴퓨터가 발생 시킨 숫자 : {}\n'.format(random_numbers))
                    continue
                print('====================================================================================================')
                print('▶ 컴퓨터가 발생 시킨 숫자 : {}\n'.format(random_numbers))

                hit_cnt = self.hit_judgment(random_numbers, hit_numbers)  # 안타 판별
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
                        print('== ▣ 홈런!!!\n')
                    self.advance_setting(hit_cnt)
                    break

            player.hit_and_run(1 if hit_cnt > 0 else 0, 1 if hit_cnt == 4 else 0)
            player.player_status(player.record.hp_dec)

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
            print('====================================================================================================')
            print('== 공수교대 하겠습니다.')
            print('====================================================================================================\n')

    # 진루 및 득점 설정하는 메서드
    def advance_setting(self, hit_cnt):
        if hit_cnt == 4:  # 홈런인 경우
            Game.SCORE[Game.CHANGE] += Game.ADVANCE.count(1)
            Game.ADVANCE = [0, 0, 0]
        else:
            for i in range(len(Game.ADVANCE), 0, -1):
                if Game.ADVANCE[i-1] == 1:
                    if (i + hit_cnt) > 3:  # 기존에 출루한 선수들 중 득점 가능한 선수들에 대한 진루 설정
                        Game.SCORE[Game.CHANGE] += 1
                        Game.ADVANCE[i-1] = 0
                    else:  # 기존 출루한 선수들 중 득점권에 있지 않은 선수들에 대한 진루 설정
                        Game.ADVANCE[i-1 + hit_cnt] = 1
                        Game.ADVANCE[i-1] = 0
            Game.ADVANCE[hit_cnt-1] = 1  # 타석에 있던 선수에 대한 진루 설정

    # 컴퓨터가 생성한 랜덤 수와 플레이어가 입력한 숫자가 얼마나 맞는지 판단
    def hit_judgment(self, random_ball, hit_numbers):
        cnt = 0
        for hit_number in hit_numbers:
            if hit_number in random_ball:
                cnt += 1
        return cnt

    # 선수가 입력한 숫자 확인
    def hit_number_check(self, hit_numbers):
        if len(hit_numbers) == 4:
            for hit_number in hit_numbers:
                if hit_number <= 0 or hit_number > 55:
                    return False
            return True
        return False

    # 선수 선택
    def select_player(self, number, player_list):
        for player in player_list:
            if number == player.number:
                return player

    # 랜덤으로 숫자 생성(1~55)
    def throws_numbers(self):
        random_balls = set()
        while True:
            random_balls.add(random.randint(1, 55))  # 1 ~ 55 중에 랜덤 수를 출력
            if len(random_balls) == 4:  # 생성된 ball 이 4개 이면(set 객체라 중복 불가)
                return random_balls


if __name__ == '__main__':
    while True:
        game_team_list = []
        print('====================================================================================================')
        game_team_list = input('=> 게임을 진행할 두 팀을 입력하세요 : ').split(' ')
        print('====================================================================================================\n')
        if (game_team_list[0] in Game.TEAM_LIST) and (game_team_list[1] in Game.TEAM_LIST):
            game = Game(game_team_list)
            game.start_game()
            break

        else:
            print('입력한 팀 정보가 존재하지 않습니다. 다시 입력해주세요.')

