class Dirtynumber:
    def __init__(self):
        self.n = 0
        self.answer = []

    def inputn(self):
        self.n = int(input('숫자입력 ㄱㄱ : '))

    def dnum(self):
        for i in range(0, self.n, 1):
            for j in range(0, self.n, 1):
                for k in range(0, self.n, 1):
                    self.answer.append((2**i)*(3**j)*(5**k))
        print(list(set(sorted(self.answer)))[self.n-1])

    def run(self):
        self.inputn()
        if self.n != 0:
            self.dnum()

        if self.n == 0:
            quit()
        return self.run()



if __name__ == '__main__':
    dn = Dirtynumber()
    dn.run()
