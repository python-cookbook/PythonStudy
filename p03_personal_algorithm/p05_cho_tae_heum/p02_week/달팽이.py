snail_size = int(input('달팽이 껍질의 크기를 입력하시오 '))
snail = [[number for number in range(1, snail_size+1)] for number in range(snail_size)]

#######################

for i in range(snail_size//2):
    for j in range(snail_size-2*(i+1)):
        snail[i+1][j+1+i] = snail_size+1 + (3+4*(i))*snail_size - int(4+(8*1/2*i*(i+1))+(4*i)) + j

########################

for i in range(snail_size // 2):
    for j in range(1, snail_size - 2 * i):
        snail[j + i][snail_size - 1 - i] = snail_size + j + (0 + 4 * i) * snail_size - int(0 + (8 * 1 / 2 * i * (i + 1)) + (-2 * i))

#########################

for i in range(snail_size//2):
    for j in range(1+i, snail_size-1):
        snail[j][i] = snail_size+i + (3+4*i)*snail_size - int(4+(8*1/2*i*(i+1))+(4*i)) - (j-1)

############################

for i in range(snail_size//2):
    for j in range(snail_size, 1+2*i, -1):
        snail[snail_size-1-i][snail_size-j+i] = snail_size + (2+4*i)*snail_size - int(2+(8*1/2*i*(i+1))+(2*i)) - (snail_size-j)*1

#########################

for ptn in snail:
    print(ptn)
