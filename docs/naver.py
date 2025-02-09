import requests
import pandas as pd
import json
import time

from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
db = client['myfipn_db']


url = 'https://openapi.naver.com/v1/search/blog'
headers = {
   'X-Naver-Client-Id': 'NtLeqJGtcTpNKXOlmtzV',
   'X-Naver-Client-Secret': '3ndCmeLwzE'
}

# 전체 검색 결과 수 확인
initial_params = {
   'query': '마이피픈',
   'sort': 'date',
   'display': 1,
   'start': 1
}

initial_response = requests.get(url, headers=headers, params=initial_params)
total_results = json.loads(initial_response.content)['total']
print(f"검색된 총 결과 수: {total_results}")

# 최대 1000개까지만 가져올 수 있음
max_results = min(1000, total_results)
display = 100
counter = 0

try:
   for start in range(1, max_results + 1, display):
       params = {
           'query': '마이피픈',
           'sort': 'date',
           'display': min(display, max_results - start + 1),
           'start': start
       }
       
       response = requests.get(url, headers=headers, params=params)
       contents = json.loads(response.content)
       
       if 'items' not in contents or not contents['items']:
           print("더 이상 데이터가 없습니다.")
           break
           
       for element in contents['items']:
           title = element['title']
           link = element['link']
           description = element['description']
           blogger = element['bloggername']
           bloggerlink = element['bloggerlink']
           date = element['postdate']
           
           review_data = {
               'title': title,
               'link': link,
               'description': description,
               'blogger': blogger,
               'bloggerlink': bloggerlink,
               'date': date
           }
           
           result = db.blog.insert_one(review_data)
           if result.inserted_id:
               counter += 1
               if counter % 10 == 0:
                   print(f"현재 {counter}개 데이터 저장 완료 (날짜: {date})")
       
       time.sleep(0.1)

except Exception as e:
   print(f"에러 발생: {e}")

finally:
   final_count = db.blog.count_documents({})
   print(f"\n수집 완료:")
   print(f"시도된 데이터 수: {counter}")
   print(f"최종 DB 데이터 수: {final_count}")