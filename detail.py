# 크롬 브라우저를 띄우기 위해, 웹드라이버를 가져오기
from ast import Not
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

# 크롬 드라이버로 크롬을 실행한다.
def getting(link):
    service = Service('./chromedriver')
    driver = webdriver.Chrome(service=service)
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches",["enable-logging"])
    browser = webdriver.Chrome(options=options)

    try:
        driver.implicitly_wait(10)
        driver.get(link)
        
    
        elem = driver.find_element(By.ID,'container')
        p_list = elem.find_elements(By.TAG_NAME,'p')
        result_list = elem.find_elements(By.CLASS_NAME,'tb_inner')
        list1 = []
        list2 = []
        list1.append('링크')
        list2.append(link)
        for p in p_list:
            if not (p.text == '' or p.text.startswith('PQ심사신청서')  or p.text.startswith('SW사업 가격점수')):
                list1.append(p.text)

            if(p.text.startswith('PQ심사신청서') ):
                setup = p.find_element(By.XPATH,"../following-sibling::*[1]")
                if(setup.text != ''):
                    list1.append(p.text)

        for result in result_list:
            list2.append(result.text)

        try:
            purchasing = elem.find_element(By.CLASS_NAME,'table_list_useablePriceTbl')
            purchasing.find_element(By.CLASS_NAME,'tb_data_none')
            list2.append('공개된 정보가 없습니다.')
            list2.append('공개된 정보가 없습니다.')
        except:
            print('가용금액 없음')
            

        try:
            base_purchasing = elem.find_element(By.CLASS_NAME,'table_list_baseEstiPriceTbl')

            try:
                base_purchasing.find_element(By.TAG_NAME,'p')
            except:
                ths = base_purchasing.find_elements(By.TAG_NAME,'th')
                for th in ths:
                        list1.append(th.text)

            try:
                base_purchasing.find_element(By.CLASS_NAME,'tb_data_none')
                for i in range(4):
                    list2.append('자료없음')
            except:
                tds = base_purchasing.find_elements(By.TAG_NAME,'td')
                for td in tds:
                    list2.append(td.text)
        except:
            print('기초금액 없음')
            
            
        try:
            files = elem.find_element(By.CLASS_NAME,"table_list_attchFileTbl")
            div_list = files.find_elements(By.TAG_NAME,'div')
            for div in div_list:
                print(div.text)
                list1.append(div.text)
                a_tag = div.find_element(By.TAG_NAME,'a')
                tag = a_tag.get_attribute('href')
                dump = []
                dump = tag.split('\'')
                target = "https://g2b.go.kr:8081/ep/co/fileDownload.do?fileTask=NOTIFY&fileSeq=" +dump[1]
                list2.append(target)
        except:
            print("첨부파일 없음")            

        f = open('list.csv','a',newline='')
        wr = csv.writer(f)
        wr.writerow(list1)
        wr.writerow(list2)
        f.close()
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        
