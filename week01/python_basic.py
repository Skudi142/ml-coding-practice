a = 3
a = 4

# 지수승
print(a ** b)
print(a ** 3)

# 나머지 연산
print(a % b)
print(7 % 3)

# 나눗셈 몫 구하기
print(a // b)
print(7 // 3)

s1 = "Hello Python"
print(s1)

s3 = '''Hello
Python'''
print(s3)

head = 'Python'
tail = " is fun"
printf(head + tail)

# 문자열 곱하기
print(head * 2)
print("=" * 5)

# 문자열 인덱싱
a = "Now is better than never"
print(a[0])
print(a[4])
print(a[-1])
print(a[-2])

# 문자열 슬라이싱
b = a[0] + a[1] + a[2]
print(b)

print(a[4:6])
print(a[19:])
print(a[:3])
print(a[7:-11])

# 문자 개수 계산
a = "Python"
print(a.count('p'))

#문자 위치 확인
print(a.find('y'))
print(a.find('p'))
print(a.index('y'))
# print(a.index('p')) # 오류 발생

# 문자 삽입
b = ","
c = b.join("Abcd")
print(c)

# 대소문자 변환
print(a.upper())
print(a.lower())

# 공백 제거
d = "          py     "