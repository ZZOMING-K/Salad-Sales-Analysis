# 🥗 Salad-Sales-Analysis
* 본 프로젝트는 실제 기업 데이터를 기반으로 진행되어, 보안상의 이유로 모델 구조 및 구현 코드만 제공합니다.
* 주관 : (기업체 주관 빅데이터 분석 프로그램 | 경상국립대학교)
* 기간 : 2022.07.05~2022.07.28
<br>

# 👀 프로젝트 개요 

### 목표
* 샐러드 매장의 POS 데이터를 활용하여 매출에 영향을 미치는 **유의미한 요인 분석**
* **매출 추이 및 상품 소비 패턴 분석** 
* 분석결과 기반 **마케팅 전략 제안** → 매출 증대 및 고객 만족도 향상
<br>

# 📊 데이터

### 1. 데이터 수집 
* 수집기간 : 2021.01 ~ 2022.06
* **샐러드 매장 상품별 월 매출 데이터** 확보
* 날씨 데이터 → Selenium을 활용한 Crawling

### 2. 데이터 재구조화
* 불필요한 column 및 결측치 제거 
* `pivot_table` 과 `melt`를 활용해 날짜별 상품 수량 및 매출 집계를 용이하게 변환하여 분석을 위한 형태로 재구성

### 3. 데이터 전처리
* 상품명 통일: **동일 상품의 명칭 표준화**
* 상품 명확성 확보: **메인 메뉴와 토핑** 
* 메뉴 카테고리 생성: 상품을 **카테고리(샐러드, 랩, 음료 등)** 으로 분류하여 카테고리화

### 4. 파생변수 생성 
* 월/요일 : 날짜별 소비패턴 분석을 위해 관련 변수 추가 
* 대학 방학 기간 : 방학 기간의 영향 분석을 위해 관련 변수 추가 
* 날씨 : 기온, 강수량 등 날씨 데이터 반영하여 매출 패턴과의 관계 분석을 위해 변수 추가

<br>

# 👍🏻 주요 작업 

### 1. 요인 분석 

다양한 요인(월, 요일, 방학 여부 등)이 매출에 유의미한 영향을 미치는지 분석

* 통계적 검정 
  * ANOVA: 세 그룹 이상의 평균 차이 검정
  * T-Test: 두 그룹 간 평균 차이 검정
* 시각화: `KdePlot`, `BoxPlot`을 활용해 데이터 분포 및 결과 해석

<br>

# ⭐ 결과
인사이트 도출 및 전략 제시 
