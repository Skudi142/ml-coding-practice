import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_webmd_reviews(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    print("웹페이지에 접속 중입니다...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"접속 실패: 상태 코드 {response.status_code}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    reviews_data = []
    
    # 리뷰 블록 컨테이너 찾기
    review_blocks = soup.find_all('div', class_='review-details')
    print(f"총 {len(review_blocks)}개의 리뷰를 찾았습니다. 데이터 추출을 시작합니다.")

    for block in review_blocks:
        try:
            # 1. 환자 정보 추출 (여러 span 태그의 텍스트를 하나로 합침)
            details_div = block.find('div', class_='details')
            if details_div:
                # 불필요한 공백과 '|' 기호를 정리하여 깔끔하게 연결
                spans = details_div.find_all('span')
                reviewer_info = " ".join([span.text.strip().replace('|', '').strip() for span in spans])
            else:
                reviewer_info = 'N/A'

            # 2. 리뷰 텍스트 추출
            desc_p = block.find('p', class_='description-text')
            review_text = desc_p.text.strip() if desc_p else 'N/A'

            # 3. 세부 별점 추출 (aria-valuenow 속성 활용)
            ratings = {'Effectiveness': 'N/A', 'Ease of Use': 'N/A', 'Satisfaction': 'N/A'}
            categories_div = block.find('div', class_='categories')
            
            if categories_div:
                sections = categories_div.find_all('section')
                for sec in sections:
                    # 항목 이름 찾기 (예: Effectiveness)
                    category_name_tag = sec.find('strong')
                    if category_name_tag:
                        category_name = category_name_tag.text.strip()
                        # 숨겨진 별점 숫자 찾기
                        slider = sec.find('div', role='slider')
                        if slider and slider.has_attr('aria-valuenow'):
                            ratings[category_name] = slider['aria-valuenow']

            # 딕셔너리에 담기
            reviews_data.append({
                'Reviewer_Info': reviewer_info,
                'Review_Text': review_text,
                'Effectiveness': ratings.get('Effectiveness', 'N/A'),
                'Ease_of_Use': ratings.get('Ease of Use', 'N/A'),
                'Satisfaction': ratings.get('Satisfaction', 'N/A')
            })
            
        except Exception as e:
            print(f"데이터 추출 중 에러 발생: {e}")
            continue

    # 데이터프레임으로 변환
    df = pd.DataFrame(reviews_data)
    return df

# --- 실행 부분 ---
target_url = "https://reviews.webmd.com/drugs/drugreview-wegovy-semaglutide"