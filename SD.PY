import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_webmd_reviews(url):
    # 1. 봇 차단을 피하기 위한 User-Agent 설정 (사람의 브라우저 접속처럼 위장)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    print("웹페이지에 접속 중입니다...")
    response = requests.get(url, headers=headers)
    
    # 접속이 정상적으로 되었는지 확인 (200이면 정상)
    if response.status_code != 200:
        print(f"접속 실패: 상태 코드 {response.status_code}")
        return None

    # 2. HTML 구조 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    reviews_data = []
    
    # 3. 리뷰 카드를 담고 있는 컨테이너 찾기
    # (주의: WebMD 사이트 업데이트에 따라 class 이름은 바뀔 수 있으므로, 안 긁히면 F12를 눌러 확인해야 합니다)
    # 일반적으로 review-details 또는 userPost 같은 클래스명을 사용합니다.
    review_blocks = soup.find_all('div', class_='review-details') 
    
    # 만약 위 클래스로 못 찾는다면 더 넓은 범위의 박스를 찾습니다.
    if not review_blocks:
        review_blocks = soup.find_all('div', class_='userPost')

    print(f"총 {len(review_blocks)}개의 리뷰 블록을 찾았습니다. 데이터 추출을 시작합니다.")

    # 4. 각 리뷰 블록에서 필요한 정보만 쏙쏙 뽑아내기
    for block in review_blocks:
        try:
            # 환자 정보 (나이, 성별 등)
            reviewer_info = block.find('p', class_='reviewerInfo').text.strip() if block.find('p', class_='reviewerInfo') else 'N/A'
            
            # 복용 기간 (Time on Medication)
            condition_info = block.find('div', class_='conditionInfo').text.strip() if block.find('div', class_='conditionInfo') else 'N/A'
            
            # 리뷰 본문 (Review Text)
            review_text = block.find('p', class_='description-text').text.strip() if block.find('p', class_='description-text') else 'N/A'
            
            # 별점 (Effectiveness, Ease of Use, Satisfaction)
            # 별점은 보통 span 태그 안의 숫자로 되어 있습니다.
            ratings = block.find_all('div', class_='star-rating')
            rating_scores = [rating.text.strip() for rating in ratings] if ratings else ['N/A', 'N/A', 'N/A']

            # 딕셔너리 형태로 저장
            reviews_data.append({
                'Reviewer_Info': reviewer_info,
                'Condition_&_Time': condition_info,
                'Review_Text': review_text,
                'Effectiveness': rating_scores[0] if len(rating_scores) > 0 else 'N/A',
                'Ease_of_Use': rating_scores[1] if len(rating_scores) > 1 else 'N/A',
                'Satisfaction': rating_scores[2] if len(rating_scores) > 2 else 'N/A'
            })
            
        except Exception as e:
            print(f"데이터 추출 중 에러 발생: {e}")
            continue

    # 5. 보기 좋은 데이터프레임(표) 형식으로 변환
    df = pd.DataFrame(reviews_data)
    return df

# --- 실행 부분 ---
# 타겟 URL 입력 (여러 페이지를 돌려면 URL의 page=1, page=2 부분을 바꿔가며 반복문을 돌리면 됩니다)
target_url = "https://reviews.webmd.com/drugs/drugreview-wegovy-semaglutide"

# 함수 실행
df_reviews = scrape_webmd_reviews(target_url)

if df_reviews is not None and not df_reviews.empty:
    print("\n✅ 데이터 추출 성공!")
    display(df_reviews.head()) # 상위 5개 데이터 확인
    
    # CSV 파일로 저장해두기
    df_reviews.to_csv('webmd_wegovy_reviews.csv', index=False, encoding='utf-8-sig')
    print("파일이 'webmd_wegovy_reviews.csv'로 저장되었습니다.")
else:
    print("데이터를 가져오지 못했습니다. 사이트 구조가 변경되었거나 동적 렌더링(JS)이 필요할 수 있습니다.")