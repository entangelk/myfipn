# * 웹 크롤링 동작
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

from pymongo import MongoClient
# MongoDB 연결
client = MongoClient('mongodb://localhost:27017/')
db = client['myfipn_db']



webdriver_manager_directory = ChromeDriverManager().install()
browser = webdriver.Chrome(service=ChromeService(webdriver_manager_directory))
# ChromeDriver 실행

# Chrome WebDriver의 capabilities 속성 사용
capabilities = browser.capabilities

# - 주소  입력
browser.get("https://www.myfipn.com/product/list.html?cate_no=86")

# - 가능 여부에 대한 OK 받음
pass

# - 정보 획득
from selenium.webdriver.common.by import By


time.sleep(2)


product_element = '#contents > div.container > div.xans-element-.xans-product.xans-product-normalpackage > div.product_area > div > ul > li'
product_comments = browser.find_elements(by=By.CSS_SELECTOR, value=product_element)
counter = 0

for product in product_comments:

    
    time.sleep(2)

    counter += 1
    if True:
        if counter in range(1, 19):
            continue
    browser.switch_to.default_content()
    try:
        product_click = product.find_element(By.CSS_SELECTOR, "div.thumbnail").click()
    except:
        # 방법 3: 요소가 보이는 위치로 스크롤 후 클릭
        thumbnail = browser.find_element(By.CSS_SELECTOR, f"#contents > div.container > div.xans-element-.xans-product.xans-product-normalpackage > div.product_area > div > ul > li:nth-child({counter})")
        browser.execute_script("arguments[0].scrollIntoView(true);", thumbnail)
        time.sleep(1)  # 스크롤 동작 완료 대기
        thumbnail.click()

    time.sleep(2)


    product_name = browser.find_element(By.CSS_SELECTOR, "#contents > div.xans-element-.xans-product.xans-product-detail > div.infoArea > div.display-m > div.headingArea > h1").text

    product_price = browser.find_element(By.CSS_SELECTOR, "#span_product_price_text").text
    product_price = int(product_price.replace(',', '').replace('원', ''))

    review_count = browser.find_element(By.CSS_SELECTOR, "#contents > div.xans-element-.xans-product.xans-product-detail > div.infoArea > div.mobile-fix-footer > span.btnNormal.sizeL.relative.jsGoReview > span.xans-element-.xans-product.xans-product-additional.review-count.alpha_review_count").text

    review_click = browser.find_element(By.CSS_SELECTOR, "#contents > div.xans-element-.xans-product.xans-product-detail > div.infoArea > div.mobile-fix-footer > span.btnNormal.sizeL.relative.jsGoReview").click()
        
    time.sleep(5)
    
    browser.switch_to.frame("alpha_widget_8")
    time.sleep(1)

    review_count = int(review_count.replace(',', ''))

    roof_count = review_count // 5
    if review_count % 5 != 0:
        roof_count += 1

    for i in range(roof_count):

        review_comments = browser.find_elements(by=By.CSS_SELECTOR, value='#widget_review_74175 > div.widget_w > div')

        for reviews in review_comments:
            try:
                # class가 'alph_star_full'인 모든 svg 요소 찾기
                full_stars = reviews.find_elements(By.CSS_SELECTOR, "svg.alph_star_full")
                star_count = len(full_stars)
            except:
                star_count = None


            try:
                writer =  reviews.find_element(By.CSS_SELECTOR, "span.widget_item_none_username_2").text
            except:
                writer = None

            try:
                date = reviews.find_element(By.CSS_SELECTOR, "div.widget_item_date_product_none").text
            except:
                date = None

            try:
                content = reviews.find_element(By.CSS_SELECTOR, "div.widget_item_tab_2_text > div > div > span").text

            except:
                content = None

            # MongoDB에 바로 저장
            review_data = {
                'product' : product_name,
                'price' : product_price,
                'writer': writer,
                'content': content,
                'date': date,
                'rating': star_count
            }
            
            db.reviews.insert_one(review_data)

        
        try:    
            # next_button = browser.find_element(By.CSS_SELECTOR, "#widget_74175 > div > div:nth-child(7) > div > div.indicator > div > nav > ul > li:nth-child(7)").click()
            # 또는 방법 3: 스크롤 후 클릭
            next_button = browser.find_element(By.CSS_SELECTOR, "#widget_74175 > div > div:nth-child(7) > div > div.indicator > div > nav > ul > li:nth-child(7)")
            browser.execute_script("arguments[0].scrollIntoView(true);", next_button)
            time.sleep(1)  # 스크롤 후 잠시 대기
            next_button.click()
        except:
            pass
        time.sleep(1)

    browser.switch_to.default_content()
    browser.back()




pass

browser.quit()