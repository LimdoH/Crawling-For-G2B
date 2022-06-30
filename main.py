# 크롬 브라우저를 띄우기 위해, 웹드라이버를 가져오기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import Detail1

# 크롬 드라이버로 크롬을 실행한다.
service = Service('./chromedriver')
driver = webdriver.Chrome(service=service)
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches",["enable-logging"])
browser = webdriver.Chrome(options=options)

try:
    # 입찰정보 검색 페이지로 이동
    driver.get('https://www.g2b.go.kr:8101/ep/tbid/tbidFwd.do')
    
  
    # 업무 종류 체크
    # task_dict = {'물품':'taskClCds1','용역': 'taskClCds5',
    #              '민간': 'taskClCds20',
    #              '기타': 'taskClCds4'}
    # for task in task_dict.values():
    #     checkbox = driver.find_element(By.ID, task)
    #     checkbox.click()
    # 검색어
    print('검색어 입력')
    query = input()
    # id값이 bidNm인 태그 가져오기
    bidNm = driver.find_element(By.ID,'bidNm')
    # 내용을 삭제 (버릇처럼 사용할 것!)
    bidNm.clear()
    # 검색어 입력후 엔터
    bidNm.send_keys(query)
    bidNm.send_keys(Keys.RETURN)

    # 검색 조건 체크
    option_dict = {'검색기간 1달': 'setMonth1_1', '입찰마감건 제외': 'exceptEnd', '검색건수 표시': 'useTotalCount'}
    for option in option_dict.values():
        checkbox = driver.find_element(By.ID,option)
        checkbox.click()

    # 목록수 50건 선택 (드롭다운)
    recordcountperpage = driver.find_element(By.NAME,'recordCountPerPage')
    selector = Select(recordcountperpage)
    selector.select_by_value('50')

    # 검색 버튼 클릭
    search_button = driver.find_element(By.CLASS_NAME,'btn_mdl')
    search_button.click()

    # 검색 결과 확인
    elem = driver.find_element(By.CLASS_NAME,'results')
    div_list = elem.find_elements(By.TAG_NAME,'div')
    titlename = elem.find_elements(By.TAG_NAME, 'th')
    # 검색 결과 모두 긁어서 리스트로 저장
    results = []
    
    # # 링크 포함 재분류
    # results.append('업무')
    # results.append('공고번호-차수')
    # results.append('링크1')
    # results.append('분류')
    # results.append('공고명')
    # results.append('링크2')
    # results.append('공고기관')
    # results.append('수요기관')
    # results.append('계약방법')
    # results.append('입력일시(입찰마감일시)')
    # results.append('공동수급')
    # results.append('투찰')
    
    # # 기존 분류 형태
    # for titles in titlename:
    #     results.append(titles.text)
    # results.append(' ')
    # results.append(' ')

    for div in div_list:
        results.append(div.text)
        a_tags = div.find_elements(By.TAG_NAME,'a')
        if a_tags:
            for a_tag in a_tags:
                link = a_tag.get_attribute('href')
                results.append(link)

    
    
except Exception as e:
    # 위 코드에서 에러가 발생한 경우 출력
    print(e)
finally:
    # 에러와 관계없이 실행되고, 크롬 드라이버를 종료
    driver.quit()
    

    # 검색결과 모음 리스트를 12개씩 분할하여 새로운 리스트로 저장 
    result = [results[i * 12:(i + 1) * 12] for i in range((len(results) + 12 - 1) // 12 )]
    with open('test.csv','w',newline='') as f:
        write = csv.writer(f)
        write.writerows(result)

    # 결과 출력    
    
    csvfile = open('test.csv','r')
    rdr = csv.reader(csvfile)
    
    for line in rdr:
        print(line[2])
        Detail1.getting(line[2])
