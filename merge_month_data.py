import warnings
warnings.filterwarnings(action='ignore')
import os 
import re 
import glob

#파일 읽어오기 
def read_file(path) :
    df = pd.read_excel(path)
    return df 

#데이터 재구조화
def dataframe_restruct(df) :
    
    #0~1행 삭제 
    df = df.drop([0,1] , axis = 0).reset_index(drop = True)
    

    #불필요한 컬럼 삭제 
    df = df.drop('상품별월조회' , axis = 1)
    
    #1행은 수량,금액을 나타냄 
    df['Unnamed: 1'].iloc[1] = 'kind'
    
    #마지막 행은 합계이므로 삭제
    df.drop(df.index[-1], axis = 0 , inplace = True)
    
    #Transpose 
    df = df.T

    # 첫번째 행을 헤더로 가져오고 삭제 
    df.columns = df.iloc[0]
    df = df[1:]
    
    df = df.melt(id_vars = ['상품명','kind'] , var_name = '메뉴' , value_name = '값')
    
    #NaN을 0으로 채우기
    df = df.fillna(0)
    
    #상품명을 날짜로 변경 
    df = df.rename(columns = {'상품명' : '날짜'})

    #날짜 데이터 추가 
    for i in range(1,len(df),2) :
        df.at[i,'날짜'] = df.at[i-1 , '날짜']
    
    #메뉴 공백 제거 
    df['메뉴'] = df['메뉴'].str.replace(' ','')
    
    #날짜,메뉴별 매출,수량 나타내기
    df= pd.pivot_table(df , values = '값' , index = ['날짜' , '메뉴'] , 
                   columns = ['kind'] , aggfunc = 'sum').reset_index()
    
    #인덱스 이름 제거 
    df = df.rename_axis(None , axis = 1)
    
    return df


#연도,월 삽입    
def insert_ym(df , path) :
    year = os.path.splitext(os.path.basename(path))[0][-6:-4]
    df.insert(0 , 'year' , 2000 + int(year))
    month = os.path.splitext(os.path.basename(path))[0][-3:-1]
    df.insert(1,'month', month)

    return df


file_path = glob.glob('data/*.xlsx')

file_list = []

for i in range(len(file_path)) :
    read_df = read_file(file_path[i])
    restruct_df = dataframe_restruct(read_df)
    result_df = insert_ym(restruct_df , file_path[i])
    file_list.append(result_df)
    
df = pd.concat(file_list)
#인덱스 재설정 
df = df.reset_index(drop=True)
#파일저장
df.to_csv('salad_month_sales.csv' , encoding = 'cp949')
