import requests
from bs4 import BeautifulSoup
import pandas as pd
import time  # 사람처럼 쉬어주기 위한 모듈
import random # 쉬는 시간을 랜덤하게 주기 위한 모듈

def scrape_webmd_multiple_pages(base_url, total_pages=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    all_reviews_data = []

    # 1페이지부터 설정한 total_pages까지 반복
    for page in range(1, total_pages + 1):
        # WebMD의 페이지 넘김 URL 규칙 적용 (예: ?conditionid=&page=2)
        # 첫 페이지는 그대로, 2페이지부터는 page 파라미터 추가
        if page == 1:
            url = base_url
        else:
            # 기존 URL에 이미 '?'가 있다면 '&'로, 없다면 '?'로 파라미터 연결
            separator = '&' if '?' in base_url else '?'
            url = f"{base_url}{separator}page={page}"
            
        print(f"[{page}/{total_pages}] 페이지 수집 중... (URL: {url})")
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"  -> 접속 실패 (상태 코드 {response.status_code}), 다음 페이지로 넘어갑니다.")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')
            review_blocks = soup.find_all('div', class_='review-details')
            
            if not review_blocks:
                print("  -> 이 페이지에는 더 이상 리뷰가 없거나 차단되었습니다. 수집을 종료합니다.")
                break # 리뷰가 없으면 전체 반복문 종료

            # 현재 페이지의 리뷰 추출
            for block in review_blocks:
                # 1. 환자 정보
                details_div = block.find('div', class_='details')
                reviewer_info = " ".join([span.text.strip().replace('|', '').strip() for span in details_div.find_all('span')]) if details_div else 'N/A'

                # 2. 리뷰 텍스트
                desc_p = block.find('p', class_='description-text')
                review_text = desc_p.text.strip() if desc_p else 'N/A'

                # 3. 세부 별점
                ratings = {'Effectiveness': 'N/A', 'Ease of Use': 'N/A', 'Satisfaction': 'N/A'}
                categories_div = block.find('div', class_='categories')
                if categories_div:
                    for sec in categories_div.find_all('section'):
                        category_name_tag = sec.find('strong')
                        if category_name_tag:
                            category_name = category_name_tag.text.strip()
                            slider = sec.find('div', role='slider')
                            if slider and slider.has_attr('aria-valuenow'):
                                ratings[category_name] = slider['aria-valuenow']

                all_reviews_data.append({
                    'Reviewer_Info': reviewer_info,
                    'Review_Text': review_text,
                    'Effectiveness': ratings.get('Effectiveness', 'N/A'),
                    'Ease_of_Use': ratings.get('Ease of Use', 'N/A'),
                    'Satisfaction': ratings.get('Satisfaction', 'N/A')
                })
            
            print(f"  -> {len(review_blocks)}개 리뷰 수집 완료. (총 누적: {len(all_reviews_data)}개)")
            
            # IP 차단 방지를 위한 랜덤 휴식 (2초 ~ 4초 사이)
            sleep_time = random.uniform(2.0, 4.0)
            time.sleep(sleep_time)

        except Exception as e:
            print(f"  -> 페이지 에러 발생: {e}")
            continue

    # 전체 수집된 데이터를 데이터프레임으로 변환
    df = pd.DataFrame(all_reviews_data)
    return df

# --- 실행 부분 ---
target_url = "https://reviews.webmd.com/drugs/drugreview-wegovy-semaglutide"

# total_pages를 늘리면 원하는 만큼 페이지를 넘기며 수집합니다. (예: 10페이지면 약 200개 데이터)
# 테스트를 위해 우선 5페이지(약 100개)만 돌려보겠습니다.
final_df = scrape_webmd_multiple_pages(target_url, total_pages=100)

if not final_df.empty:
    print(f"\n✅ 대규모 데이터 수집 성공! 총 {len(final_df)}개의 리뷰를 확보했습니다.")
    print(final_df.head(3))
    
    file_name = 'webmd_wegovy_reviews_massive.csv'
    final_df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"\n파일이 '{file_name}'로 저장되었습니다.")