import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

def scrape_glp1_master(drug_urls, pages_per_drug=5):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.9'
    }

    all_reviews_data = []

    # 1. 약물 리스트를 하나씩 돌면서 수집 시작
    for drug_name, base_url in drug_urls.items():
        print(f"\n🚀 [{drug_name}] 데이터 수집을 시작합니다...")
        
        # 2. 각 약물마다 지정된 페이지 수만큼 반복
        for page in range(1, pages_per_drug + 1):
            separator = '&' if '?' in base_url else '?'
            url = f"{base_url}{separator}page={page}" if page > 1 else base_url
                
            print(f"  -> {page}페이지 수집 중... ", end="")
            
            try:
                response = requests.get(url, headers=headers)
                if response.status_code != 200:
                    print(f"실패 (상태 코드 {response.status_code})")
                    continue

                soup = BeautifulSoup(response.text, 'html.parser')
                review_blocks = soup.find_all('div', class_='review-details')
                
                # 해당 페이지에 더 이상 리뷰가 없으면 다음 약물로 넘어감 (안전장치)
                if not review_blocks:
                    print("리뷰 없음. 다음 약물로 넘어갑니다.")
                    break 

                # 3. 데이터 추출
                for block in review_blocks:
                    details_div = block.find('div', class_='details')
                    reviewer_info = " ".join([span.text.strip().replace('|', '').strip() for span in details_div.find_all('span')]) if details_div else 'N/A'

                    desc_p = block.find('p', class_='description-text')
                    review_text = desc_p.text.strip() if desc_p else 'N/A'

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

                    # 💡 여기에 '약물 이름(Drug_Name)' 컬럼을 추가해서 저장!
                    all_reviews_data.append({
                        'Drug_Name': drug_name, 
                        'Reviewer_Info': reviewer_info,
                        'Review_Text': review_text,
                        'Effectiveness': ratings.get('Effectiveness', 'N/A'),
                        'Ease_of_Use': ratings.get('Ease of Use', 'N/A'),
                        'Satisfaction': ratings.get('Satisfaction', 'N/A')
                    })
                
                print(f"완료 ({len(review_blocks)}개)")
                
                # IP 차단 방지를 위한 휴식
                time.sleep(random.uniform(1.5, 3.0))

            except Exception as e:
                print(f"에러 발생: {e}")
                continue

    # 전체 수집된 데이터를 판다스 표로 변환
    df = pd.DataFrame(all_reviews_data)
    return df

# --- 실행 부분 ---
# WebMD의 주요 GLP-1 약물 URL 딕셔너리
glp1_urls = {
    "Wegovy": "https://reviews.webmd.com/drugs/drugreview-wegovy-semaglutide",
    "Ozempic": "https://reviews.webmd.com/drugs/drugreview-ozempic-semaglutide",
    "Saxenda": "https://reviews.webmd.com/drugs/drugreview-saxenda-liraglutide",
    "Mounjaro": "https://reviews.webmd.com/drugs/drugreview-mounjaro-tirzepatide",
    "Zepbound": "https://reviews.webmd.com/drugs/drugreview-zepbound-tirzepatide",
    "Rybelsus": "https://reviews.webmd.com/drugs/drugreview-rybelsus-semaglutide"
}

# 각 약물당 몇 페이지씩 수집할지 설정 (예: 10페이지 = 약물당 200개, 총 1200개)
# 우선 테스트를 위해 약물당 3페이지만 돌려보겠습니다.
final_df = scrape_glp1_master(glp1_urls, pages_per_drug=3)

if not final_df.empty:
    print(f"\n✅ 전체 수집 성공! 총 {len(final_df)}개의 다종 GLP-1 리뷰를 확보했습니다.")
    
    file_name = 'glp1_master_reviews.csv'
    final_df.to_csv(file_name, index=False, encoding='utf-8-sig')
    print(f"파일이 '{file_name}'로 저장되었습니다.")