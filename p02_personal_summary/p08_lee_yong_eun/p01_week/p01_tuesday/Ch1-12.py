#######################################################################################
# 1.12) 시퀀스에 가장 많은 아이템 찾기
#
# collections.Counter : 각 요소가 몇 개씩 나왔는지 카운트
# most_common() : 가장 많이 나온 요소 반환
# +, -
#######################################################################################

words = [
    'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
    'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
    'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
    'my', 'eyes', "you're", 'under'
]

from collections import Counter

# 각 단어가 얼마나 나왔는지
word_counts = Counter(words)
print(word_counts) # Counter({'eyes': 8, 'the': 5, 'look': 4, 'into': 3, 'my': 3, 'around': 2, 'not': 1, "don't": 1, "you're": 1, 'under': 1})

# 가장 많이 나온 단어 3개
top_three = word_counts.most_common(3)
print(top_three) # [('eyes', 8), ('the', 5), ('look', 4)]

# 단어 갯수 업데이트
morewords = ['why', 'are', 'you', 'not', 'looking', 'in', 'my', 'eyes']
word_counts.update(morewords)
print(word_counts) # Counter({'eyes': 9, 'the': 5, 'look': 4, 'my': 4, 'into': 3, 'not': 2, 'around': 2, "don't": 1, "you're": 1, 'under': 1, 'why': 1, 'are': 1, 'you': 1, 'looking': 1, 'in': 1})

# 카운트 합치기
a = Counter(words)
b = Counter(morewords)
c = a + b
print(c) # 위 업데이트한 결과와 동일

# 카운트 빼기
d = a - b
print(d) # Counter({'eyes': 7, 'the': 5, 'look': 4, 'into': 3, 'my': 2, 'around': 2, "don't": 1, "you're": 1, 'under': 1})