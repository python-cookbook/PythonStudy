# 코드는 아래와 같습니다

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
    def game(self):
        return self.__game

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
    TEAM_LIST = ['HANHWA', 'LOTTE', 'SAMSUNG', 'KIA', 'SK', 'LG', 'DOOSAN' , 'NEXEN' , 'KT' ,'NC']
    INNING = 1  # 1 이닝부터 시작
    CHANGE = 0  # 0 : hometeam, 1 : awayteam
    STRIKE_CNT = 0  # 스트라이크 개수
    OUT_CNT = 0  # 아웃 개수
    ADVANCE = [0, 0, 0]  # 진루 상황
    SCORE = [0, 0]  # [home, away]
    BATTER_NUMBER = [1, 1]  # [home, away] 타자 순번

    def __init__(self, game_team_list):
        self.record = Record()
        # csv 파일 위치
        self.home_location = "C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[0]+".csv"
        self.away_location = "C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[1]+".csv"

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
        with open(self.home_location, 'r') as hf:
            for idx, item in enumerate(csv.DictReader(hf), 0):
                for value in self.int_labels:
                    item[value] = int(item[value])
                for value in self.float_labels:
                    item[value] = round(float(item[value]), 3)
                self.home_temp.append(item)
        self.home_temp_sort = sorted(self.home_temp, key=itemgetter('체력'), reverse=True)
        # print(self.home_temp_sort)
        hf.close()

        # 어웨이팀 csv 로드
        with open(self.away_location, 'r') as af:
            for idx, item in enumerate(csv.DictReader(af), 0):
                for value in self.int_labels:
                    item[value] = int(item[value])
                for value in self.float_labels:
                    item[value] = round(float(item[value]), 3)
                    self.away_temp.append(item)
        af.close()

        self.away_temp_sort = sorted(self.away_temp, key=itemgetter('체력'), reverse=True)
        # print(self.away_temp_sort)
        # 홈팀 라인업 구성
        self.value_h = tuple({int(i['등번호']): i['선수명']} for i in self.home_temp_sort)
        self.__hometeam = Team(game_team_list[0], self.value_h)
        # print(self.value_h)
        # 어웨이팀 라인업 구성
        self.value_a = tuple({int(i['등번호']): i['선수명']} for i in self.away_temp_sort)
        self.__awayteam = Team(game_team_list[1], self.value_a)
        # print(self.value_a)

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

        # 홈팀 선수 기록 1차 저장
        h_csv1_header1 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[0]+".csv", 'w', encoding='euc_kr', newline='')
        h_csv1_writer1 = csv.writer(h_csv1_header1)
        h_csv1_writer1.writerow(['팀명', '선수명', '타수', '안타수', '홈런수', '타율', '체력', '부상여부', '등번호'])
        h_csv1_header1.close()

        for i in range(20):
            hp = hometeam_players[i]
            hp_rec = hp.record
            open_csv_header_h = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[0]+".csv", 'a', encoding='euc_kr', newline='')
            csv_writer_h = csv.writer(open_csv_header_h)
            csv_writer_h.writerow(
                [game_team_list[0], hp.name, int(hp_rec.atbat), int(hp_rec.hit), int(hp_rec.homerun), round(float(hp_rec.avg),3),
                 int(hp_rec.hp), hp_rec.batter_injure(hp_rec.injure_n)])
            open_csv_header_h.close()

        # 어웨이팀 선수 기록 1차 저장
        a_csv1_header1 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[1]+".csv", 'w', encoding='euc_kr', newline='')
        a_csv1_writer1 = csv.writer(a_csv1_header1)
        a_csv1_writer1.writerow(['팀명', '선수명', '타수', '안타수', '홈런수', '타율', '체력', '부상여부', '등번호'])
        a_csv1_header1.close()

        for i in range(20):
            ap = awayteam_players[i]
            ap_rec = ap.record
            open_csv_header_a = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[1]+".csv", 'a', encoding='euc_kr', newline='')
            csv_writer_a = csv.writer(open_csv_header_a)
            csv_writer_a.writerow(
                [game_team_list[1], ap.name, int(ap_rec.atbat), int(ap_rec.hit), int(ap_rec.homerun), round(float(ap_rec.avg),3),
                 int(ap_rec.hp), ap_rec.batter_injure(ap_rec.injure_n)])
            open_csv_header_a.close()
        #팀명   선수명   타수   안타수   홈런수   타율   체력   부상여부   등번호

        # 홈팀 csv 파일 저장 + 체력 높은 순으로 정렬 + 정렬 후 높은 순으로 순위 부여
        home_csv1 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[0]+".csv", 'r', encoding='euc_kr', newline='')
        home_csv1_read = csv.reader(home_csv1)
        next(home_csv1_read, None)  # csv 파일의 첫 row가 header 인 경우 next로 넘김
        temp_h = []
        for i in home_csv1_read:
            # ff.append(i)
            temp_h.append(i[0:8])   # 정렬전 순위를 빼고 append한다
        home_csv1.close()

        temp_h2 = sorted(temp_h, key=lambda temp_h: int(temp_h[6]), reverse=True)   # 체력 순으로 desc 정렬

        for i in range(0, len(temp_h2), 1):
            temp_h2[i].append(i + 1)
        # print(temp_h2)
        home_open_csv_header1 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[0]+".csv", 'w', encoding='euc_kr', newline='')
        home_csv_writer1 = csv.writer(home_open_csv_header1)
        home_csv_writer1.writerow(['팀명', '선수명', '타수', '안타수', '홈런수', '타율', '체력', '부상여부', '등번호'])
        home_open_csv_header1.close()

        home_open_csv_header2 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[0]+".csv", 'a', encoding='euc_kr', newline='')
        home_csv_writer2 = csv.writer(home_open_csv_header2)
        for i in range(0, 20, 1):
            home_csv_writer2.writerow(temp_h2[i])
        home_open_csv_header2.close()

        home_csv_read3 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[0]+".csv", 'r', encoding='euc_kr', newline='')
        home_csv_reader3 = csv.reader(home_csv_read3)
        temp_h3 = []
        for ia in home_csv_reader3:
            # ff.append(i)
            temp_h3.append(ia)
        home_csv_read3.close()
        #print(temp_h3)

        # 어웨이팀 csv 파일 저장 + 체력 높은 순으로 정렬 + 정렬 후 높은 순으로 순위 부여
        away_csv1 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[1]+".csv", 'r', encoding='euc_kr', newline='')
        away_csv1_read = csv.reader(away_csv1)
        next(away_csv1_read, None)
        temp_a = []
        for i in away_csv1_read:
            # ff.append(i)
            temp_a.append(i[0:8])
        away_csv1.close()

        temp_a2 = sorted(temp_a, key=lambda temp_a: int(temp_a[6]), reverse=True)

        for i in range(0, len(temp_a2), 1):
            temp_a2[i].append(i + 1)
        # print(temp_h2)
        away_open_csv_header1 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[1]+".csv", 'w', encoding='euc_kr', newline='')
        away_csv_writer1 = csv.writer(away_open_csv_header1)
        away_csv_writer1.writerow(['팀명', '선수명', '타수', '안타수', '홈런수', '타율', '체력', '부상여부', '등번호'])
        away_open_csv_header1.close()

        away_open_csv_header2 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[1]+".csv", 'a', encoding='euc_kr', newline='')
        away_csv_writer2 = csv.writer(away_open_csv_header2)
        for i in range(0, 20, 1):
            away_csv_writer2.writerow(temp_a2[i])
        away_open_csv_header2.close()

        away_csv_read3 = open("C:\\Users\\Won Tae CHO\\Desktop\\basball_data"+game_team_list[1]+".csv", 'r', encoding='euc_kr', newline='')
        away_csv_reader3 = csv.reader(away_csv_read3)
        temp_a3 = []
        for ia in away_csv_reader3:
            # ff.append(i)
            temp_a3.append(ia)
        away_csv_read3.close()
        #print(temp_h3)

        print('====================================================================================================')

    # 공격 수행 메서드
    def attack(self):
        curr_team = self.hometeam if Game.CHANGE == 0 else self.awayteam
        player_list = curr_team.player_list
        if Game.OUT_CNT < 3:
            player = self.select_player(Game.BATTER_NUMBER[Game.CHANGE], player_list)
            hometeam_players = self.hometeam.player_list
            awayteam_players = self.awayteam.player_list
            for idx,i in enumerate(self.home_temp_sort):
                hp = hometeam_players[idx]
                hp_rec = hp.record
                hp_rec.hp = i['체력']
                hp_rec.homerun = i['홈런수']
                hp_rec.avg = i['타율']
                hp_rec.hit = i['안타수']
                hp_rec.atbat = i['타수']
            for idx,i in enumerate(self.away_temp_sort):
                ap = awayteam_players[idx]
                ap_rec = ap.record
                ap_rec.hp = i['체력']
                ap_rec.homerun = i['홈런수']
                ap_rec.avg = i['타율']
                ap_rec.hit = i['안타수']
                ap_rec.atbat = i['타수']
            print('====================================================================================================')
            print('== [{}] {}번 타자[{}] 타석에 들어섭니다.'.format(curr_team.team_name, player.number, player.name))
            print('====================================================================================================\n')
            while True:
                random_numbers = self.throws_numbers(player)  # 컴퓨터가 랜덤으로 숫자 4개 생성
                print('== [전광판] =========================================================================================')
                print('==   {}      | {} : {}'.format(Game.ADVANCE[1], self.hometeam.team_name, Game.SCORE[0]))
                print('==  {}  {}    | {} : {}'.format(Game.ADVANCE[2], Game.ADVANCE[0], self.awayteam.team_name, Game.SCORE[1]))
                print('== [OUT : {}, STRIKE : {}]'.format(Game.OUT_CNT, Game.STRIKE_CNT))
                print('====================================================================================================')
                print('== 현재 타석 : {}번 타자[{}], 타율 : {}'.format(player.number, player.name, player.record.avg))
                print('== 컨디션 : {}, 체력 : {}'.format(player.record.condition[player.record.hp_dec], player.record.hp))
                try:
                    if player.record.condition[player.record.hp_dec] == 'good':
                        print('==선수의 컨디션이 "good" 입니다. 1~55 사이의 숫자를 선택하세요.')
                    if player.record.condition[player.record.hp_dec] == 'normal':
                        print('==선수의 컨디션이 "normal" 입니다. 1~65 사이의 숫자를 선택하세요.')
                    if player.record.condition[player.record.hp_dec] == 'bad':
                        print('==선수의 컨디션이 "bad" 입니다. 1~75 사이의 숫자를 선택하세요.')
                    hit_numbers = set(int(hit_number) for hit_number in input('== 컨디션에 따른 숫자를 공백구분으로 4개 입력하세요(중복불가능) : ').split(' '))  # 유저가 직접 숫자 4개 입력
                    if self.hit_number_check(hit_numbers, player) is False:
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
    def hit_number_check(self, hit_numbers, player):
            if player.record.condition[player.record.hp_dec] == 'good':
                if len(hit_numbers) == 4:
                    for hit_number in hit_numbers:
                        if hit_number <= 0 or hit_number > 50:
                            return False
                    return True
                return False
            if player.record.condition[player.record.hp_dec] == 'normal':
                if len(hit_numbers) == 4:
                    for hit_number in hit_numbers:
                        if hit_number <= 0 or hit_number > 55:
                            return False
                    return True
                return False
            if player.record.condition[player.record.hp_dec] == 'bad':
                if len(hit_numbers) == 4:
                    for hit_number in hit_numbers:
                        if hit_number <= 0 or hit_number > 60:
                            return False
                    return True
                return False
        # if len(hit_numbers) == 4:
        #     for hit_number in hit_numbers:
        #         if hit_number <= 0 or hit_number > 75:
        #             return False
        #     return True
        # return False

    # 선수 선택
    def select_player(self, number, player_list):
        for player in player_list:
            if number == player.number:
                return player

    # 랜덤으로 숫자 생성(1~55)
    def throws_numbers(self, player):
        random_balls = set()
        while True:
            if player.record.condition[player.record.hp_dec] == 'good':
                random_balls.add(random.randint(1, 55))  # 컨디션이 좋은 선수는 1 ~ 55 중에 랜덤 수를 출력
                if len(random_balls) == 4:  # 생성된 ball 이 4개 이면(set 객체라 중복 불가)
                    return random_balls
            if player.record.condition[player.record.hp_dec] == 'normal':
                random_balls.add(random.randint(1, 65))  # 컨디션이 보통인 선수는 1 ~ 65 중에 랜덤 수를 출력
                if len(random_balls) == 4:  # 생성된 ball 이 4개 이면(set 객체라 중복 불가)
                    return random_balls
            if player.record.condition[player.record.hp_dec] == 'bad':
                random_balls.add(random.randint(1, 75))  # 1 ~ 75 중에 랜덤 수를 출력
                if len(random_balls) == 4:  # 생성된 ball 이 4개 이면(set 객체라 중복 불가)
                    return random_balls
            # random_balls.add(random.randint(1, 65))  # 컨디션이 보통인 선수는 1 ~ 65 중에 랜덤 수를 출력
            # if len(random_balls) == 4:  # 생성된 ball 이 4개 이면(set 객체라 중복 불가)
            #     return random_balls
#
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
