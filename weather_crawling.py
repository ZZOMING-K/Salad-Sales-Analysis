from selenium import webdriver #크롬창을 조정하는 모듈 
from selenium.webdriver.common.by import By #웹사이트 구성요소 선택 
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager #웹드라이버 설치 모듈 
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
url = 'https://weather.kweather.co.kr/weather/legacy_weather'
driver.get(url)

#지역선택 
driver.find_element(By.XPATH , '//*[@id="category"]/option[7]').click()
#시군구선택
driver.find_element(By.XPATH , '//*[@id="city"]/option[5]').click()
#날짜선택
for i in range(34):
    driver.find_element(By.XPATH , '/html/body/div[2]/div[2]/div[2]/span[3]/div/div[1]').click()
driver.find_element(By.XPATH , '/html/body/div[2]/div[2]/div[2]/span[3]/button').click()


df_list = []

for _ in range(18) :

    time.sleep(3)
    
    #날짜와 날씨 정보를 담고 있는 객체 찾기 
    date_weather = driver.find_elements(By.CLASS_NAME , 'weather_text_date')
    year = driver.find_elements(By.CLASS_NAME , 'date_selector')

    #연도만 가져오기
    year_text = year[0].text
    year_text = int(re.search(r'\b(\d{4})\b', year_text).group(1))
    year_text

    #날짜,날씨를 담을 리스트 생성 
    dw_list = []

    #날짜, 날씨 가져오기 
    for item in date_weather : 
        date,weather = item.text.split('\n')
        dw_list.append({'년도' : year_text , '날짜' : date , '날씨' : weather})

    df = pd.DataFrame(dw_list)
    df_list.append(df)

    #다음페이지 넘어가기 
    driver.find_element(By.XPATH , '/html/body/div[2]/div[2]/div[2]/span[3]/div/div[3]').click()
    #검색 클릭 
    driver.find_element(By.XPATH , '/html/body/div[2]/div[2]/div[2]/span[3]/button').click()

df_weather = pd.concat(df_list).reset_index(drop=True)

df_weather['날짜'][0].split('.')
df_weather['월'] = df_weather['날짜'].apply(lambda x: int(x.split('.')[0]))
df_weather['일'] = df_weather['날짜'].apply(lambda x: int(x.split('.')[1]))
df_weather['date']= pd.to_datetime(df_weather[['년도','월','일']].astype(str).agg('-'.join , axis = 1))
df_weather = df_weather[['date','날씨']]

#저장
df_weather.to_csv('df_weather.csv' , encoding = 'cp949')
