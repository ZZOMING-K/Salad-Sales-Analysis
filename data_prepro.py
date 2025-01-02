# -*- coding: utf-8 -*-

import datetime as dt
import koreanize_matplotlib
import holidays
from datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings(action='ignore')

def topping_source_menu(df) :

    topping = ['계절과일(토핑)','모짜렐라','방울토마토','병아리콩','양파슬라이스','양파후레이크',
           '에그','옥수수콘','할라피뇨','당근', '닭가슴살','닭다리살','베이컨','소불고기',
           '언리미트','훈제오리','매콤제육','훈제연어','버섯','데리야끼닭목살','버터새우',
          '애호박','아보카도','포테이토','미역국수']

    source = ['간장참깨','어니언','오리엔탈','올리브발사믹','칠리크리미','곡물','크림시저']

    df['메뉴명'] = df['메뉴명'].apply(lambda x : x+'추가' if x in topping else x)

    #(홀)이 있다면 제거 하고 '드레싱'붙이기
    df['메뉴명'] = df['메뉴명'].apply(lambda x : x.replace('(홀)','') if '(홀)' in x else x)
    df['메뉴명'] = df['메뉴명'].apply(lambda x : x+'드레싱' if x in source else x)

    return df

menu_mapping = {
    '리이브사과주스': '사과주스',
    '오늘자람사과즙': '사과주스',
    '오늘자람사과즙10개': '사과주스',
    '아메리카노ICE': '아메리카노',
    '아메리카노HOT': '아메리카노',
    '영양만점샤브랑': '샤브랑',
    '샤브랑(1EA)': '샤브랑',
    '힛더티슈퍼말차클린': '슈퍼말차클린',
    '드링킷유기농팥물100ml': '드링킷유기농팥물',
    '플라이밀라이블링': '밀라이블링',
    '토민샤인클링': '샤인클링',
    '와로샐러드정기구독권': '정기권',
    '허브티(얼그레이)' : '얼그레이허브티',
    '허브티(쟈스민)' : '쟈스민허브티',
    '허브티(캐모마일)' : '캐모마일허브티',
    '허브티(페퍼민트)' : '페퍼민트허브티'
}


def same_menu(df , menu_mapping) :

    #[신메뉴]제거
    df['메뉴명'] = df['메뉴명'].apply(lambda x : x.replace('[신메뉴]','') if '[신메뉴]' in x else x)

    #[내맘샐],(내맘샐)제거
    df['메뉴명'] = df['메뉴명'].apply(lambda x : x.replace('(내맘샐)','') if '(내맘샐)' in x else x)
    df['메뉴명'] = df['메뉴명'].apply(lambda x : x.replace('[내맘샐]','') if '[내맘샐]' in x else x)

    #오타정정
    df['메뉴명'] = df['메뉴명'].apply(lambda x : x.replace('풀드','폴드') if '풀드' in x else x)
    df['메뉴명'] = df['메뉴명'].apply(lambda x : x.replace('에기베이컨','에그베이컨') if '에기베이컨' in x else x)
    df['메뉴명'] = df['메뉴명'].apply(lambda x : x.replace('어니언불고기','어니언불고기샐버거') if x == '어니언불고기' else x)

    #모든 배달팁을 '배달팁'으로 통일
    delivery_list = df[df['메뉴명'].str.startswith('배달')]['메뉴명'].unique()
    df['메뉴명'] = df['메뉴명'].apply(lambda x : '배달팁' if x in delivery_list else x )

    df['메뉴명'] = df['메뉴명'].replace(menu_mapping)

    df = df[~((df['메뉴명'] == '우주부품9월장부') |( df['메뉴명'] == '아침정기배송(4주)') | (df['메뉴명'] == '에그베이컨'))]
    return df

sub_menu = ['샤브랑','로제율피떡볶이','크림율피떡볶이','율피떡볶이(기본)',
            '[합천]율피떡Set','레이즌오트밀쿠키','화이트마카다미아쿠키']

def categorize_menu(menu):
    if menu.endswith('추가'):
        return '토핑'
    elif menu.endswith('샐러드'):
        return '샐러드'
    elif menu.endswith('랩'):
        return '랩'
    elif menu.endswith('웜플레이트'):
        return '웜플레이트'
    elif menu.endswith('샐버거'):
        return '샐버거'
    elif menu.endswith('드레싱'):
        return '드레싱'
    elif menu.endswith('도시락'):
        return '건강도시락'
    elif menu.endswith('정기권'):
        return '정기권'
    elif menu in sub_menu:
        return '서브메뉴'
    else:
        return '음료'

def category_menu(df) :
    df['메뉴종류'] = df['메뉴명'].apply(categorize_menu)
    return df

def prepro_data(df) :
    #합계 데이터 제외
    df = df[df['일'] !='합계'].reset_index(drop = True)

    #메뉴만 살펴보기위해 배달팁 제외
    df = df[~(df['메뉴명'] == '배달팁')]
    df['datetime'] = pd.to_datetime(df['연도'].astype(str) + '-' + df['월'].astype(str).str.zfill(2) + '-' + df['일'].astype(str).str.zfill(2), errors='coerce')

    # '날짜' 열을 가장 첫 번째 열로 이동
    df.insert(0, 'datetime', df.pop('datetime'))

    #연도,월,일 삭제
    df = df.drop(['연도','월','일'] , axis = 1)
    return df

def vacation(date_x) :
    if datetime(2021, 1, 1) <= date_x < datetime(2021, 3, 1):
        return '방학'
    elif datetime(2021, 3, 1) <= date_x < datetime(2021, 6, 14):
        return '개강'
    elif datetime(2021, 6, 14) <= date_x < datetime(2021, 9, 1):
        return '방학'
    elif datetime(2021, 9, 1) <= date_x < datetime(2021, 12, 16):
        return '개강'
    elif datetime(2021, 12, 16) <= date_x < datetime(2022, 3, 1):
        return '방학'
    elif datetime(2022, 3, 1) <= date_x < datetime(2022, 6, 16):
        return '개강'
    else:
        return '방학'

def read_data(path = './data') : #날씨,기온 데이터 가져오기
    weather = pd.read_csv(path + '/' + 'df_weather.csv' , encoding = 'cp949' , index_col = [0])

    temp = pd.read_csv(path + '/' +'temperature.csv' , encoding = 'cp949')
    temp = temp.drop(['지점' , '지점명'] , axis = 1) #필요없는 열 삭제
    temp = temp.rename(columns = {'일시' : 'datetime' , '평균기온(°C)' : '평균기온'})
    temp['datetime'] = pd.to_datetime(temp['datetime'])
    temp['datetime'] = pd.to_datetime(temp['datetime'])

    return weather , temp


def make_feature(df_sales , weather , temp) :
    #월 추가
    df_sales['월'] = df_sales['datetime'].dt.month
    #요일 추가
    df_sales['요일'] = df_sales['datetime'].dt.day_name()

    #연휴여부 추가(만일 공휴일일 경우1 , 아닐경우 0)
    kr_holidays = holidays.KR()
    df_sales['공휴일여부'] = df_sales['datetime'].apply(lambda x : 1 if x in kr_holidays else 0 )
    df_sales

    #날씨 불러오기
    weather = weather.rename(columns = {'date' : 'datetime'})
    weather['datetime'] = pd.to_datetime(weather['datetime'])
    weather

    #날씨 데이터와 합치기
    df_merge = pd.merge(df_sales, weather, on='datetime', how='left')
    df_merge = df_merge.rename(columns ={'금액' : '매출'})

    # 비 여부에 따라 나누기
    df_merge['날씨'] = df_merge['날씨'].apply(lambda x : '맑음' if ((x == '구름조금') | (x == '구름많음')) | (x == '흐림') else x )

    #기온 데이터와 합치기
    df_merge = pd.merge(df_merge, temp, on='datetime', how='left')
    df_merge['평균기온'] = df_merge['평균기온'].fillna(method='ffill') #결측치 처리
    df_merge

    #방학여부 추가
    df_merge['방학여부'] = df_merge['datetime'].apply(vacation)

    df_merge = df_merge[~(df_merge['매출'] == 0)] #평균매출액을 살펴보기 위해 운영을 하지 않은 날은 삭제 진행 => 매출이 0
    df_merge.head()

    return df_merge


df = pd.read_csv('./data/salad_month_sales.csv' , encoding = 'cp949' , index_col = [0])
df.columns = ['연도', '월', '일', '메뉴명', '금액', '수량']

df = topping_source_menu(df)
df = same_menu(df , menu_mapping)
df = category_menu(df)
df

df.to_csv('./data/prepro_final.csv')