# AdventureWorks-Sales
# 📊 AdventureWorks Sales Analysis (FastAPI + SQLite)

개인 과제로 AdventureWorks 판매 데이터를 분석하고  
RFM 세분화 및 CLV 예측 모델을 구축하여 FastAPI로 API 서비스를 제공하였습니다.

---

## 📂 Project Overview

- 📁 SQLite DB 생성 (sales 테이블)
- 📈 EDA 분석 및 시각화 (plots/)
- 🧮 RFM 고객 세분화 (VIP, Loyal, Regular 등)
- 🤖 CLV 예측 모델(RandomForest) 학습 및 저장
- 🚀 FastAPI 백엔드로 분석 + 예측 API 제공

---

## 📁 Project Structure

adventureworks-sales/
│
├── data/
│ ├── AdventureWorks_Sales.csv
│ └── adventureworks.db
│
├── models/
│ └── clv_model.pkl
│
├── plots/
│
├── load_data.py
├── rfm_analysis.py
├── eda_plots.py
├── train_clv_model.py
├── api.py
└── README.md

yaml
코드 복사

---

## ⚙️ Setup

pip install -r requirements.txt

yaml
코드 복사

---

## 🧪 Workflow

### 1) Load Data to SQLite
python load_data.py

shell
코드 복사

### 2) RFM Analysis
python rfm_analysis.py

shell
코드 복사

### 3) EDA Visualization
python eda_plots.py

shell
코드 복사

### 4) Train CLV Model
python train_clv_model.py

yaml
코드 복사

---

## 🚀 Run FastAPI Backend

uvicorn api:app --reload --port 8000

yaml
코드 복사

📄 API Docs:  
http://127.0.0.1:8000/docs

---

## 🔌 Endpoints

- GET `/health` – 서버 상태 체크  
- GET `/stats/summary` – KPI 통계  
- GET `/rfm/segments` – 고객 RFM 테이블  
- POST `/predict/clv` – CLV 예측  

---

## 🔐 External API

이 프로젝트는 **외부 API를 전혀 사용하지 않습니다.**

- 로컬 SQLite  
- 로컬 .pkl 모델  
- 로컬 FastAPI  

따라서 API Key는 **필요 없습니다.**

---

## 👤 Author

**Asset Bayan**  
Kyungbok University • Big Data Department


