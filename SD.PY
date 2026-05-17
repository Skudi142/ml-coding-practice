import requests
from bs4 import BeautifulSoup

# 접속 정보 설정
url = "https://reviews.webmd.com/drugs/drugreview-wegovy-semaglutide"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')

# 리뷰 텍스트가 담겨있던 블록 가져오기
review_blocks = soup.find_all('div', class_='review-details') 
if not review_blocks:
    review_blocks = soup.find_all('div', class_='userPost')

if review_blocks:
    # 첫 번째 리뷰의 HTML 구조만 텍스트 파일로 저장
    with open('review_html_sample.txt', 'w', encoding='utf-8') as f:
        f.write(review_blocks[0].prettify())
    print("✅ 'review_html_sample.txt' 파일이 생성되었습니다! 이 파일의 내용을 복사해서 알려주세요.")
else:
    print("리뷰 블록을 찾지 못했습니다.")