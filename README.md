# E‑Commerce Analytics — SQL → Python → Excel → Power BI

**Single‑project portfolio**  โดยผมเริ่มจาก *SQL join* → *Python data cleaning* → *Excel Pivot* → *Power BI dashboard* 
<div align="left">
  
![Stack](https://img.shields.io/badge/SQL-analytics-blue) 
![Python](https://img.shields.io/badge/Python-pandas%2Fmatplotlib-yellow) 
![Excel](https://img.shields.io/badge/Excel-Pivot-success) 
![Power%20BI](https://img.shields.io/badge/Power%20BI-Dashboard-orange)
![Reproducible](https://img.shields.io/badge/Reproducible-Yes-brightgreen)

</div>

## 🎯 What I built
- **SQL data model**: รวมข้อมูลคำสั่งซื้อ ลูกค้า สินค้า รายการสั่งซื้อ และงบโฆษณา เข้าด้วยกัน (ดู `sql/01_ecom_join.sql`)
- **Python cleaning pipeline**: ตั้งชื่อคอลัมน์ให้มาตรฐาน, แปลงวันที่, บังคับชนิดข้อมูล, ลบค่าซ้ำและเพิ่มฟีเจอร์เวลา (ดู `src/ecom_clean.py`)
- **Excel Pivot workbook**: ใช้ทำ quick slice & dice ก่อนส่งเข้า Power BI
- **Power BI dashboard**: KPI cards + เทรนด์รายเดือน + Breakdown ช่องทาง/วิธีชำระ + Top 10 จากสินค้าทั้งหมด

## 🗺️ Pipeline (Mermaid)
```mermaid
flowchart LR
  A[SQL: Join ] --> B[CSV export]
  B --> C[Python: Clean & Feature]
  C --> D[Excel Pivot]
  D --> E[Power BI Dashboard]
```

## 📁 Repository structure
```
ecom-analytics-portfolio/
├─ sql/
│  └─ 01_ecom_join.sql
├─ src/
│  └─ ecom_clean.py
├─ data/
│  └─ sample/
│     ├─ top10_sales.csv
│     ├─ sales_by_payment_channel.csv
│     └─ monthly_sales_by_category.csv
├─ docs/
│  ├─ ONE-PAGER.md
│  └─ figs/
│     ├─ top10.png
│     ├─ by_category.png
│     └─ trend.png
└─ README.md
```


## 📊 Quick look
<p align="left">
  <img src="docs/figs/top10.png" alt="Top 10" width="45%">
  <img src="docs/figs/trend.png" alt="Monthly Trend" width="45%">
</p>




## 🧠 Problem framing
- เป้าหมาย: รู้ว่า **ยอดขายมาจากไหน ลดลง/เพิ่มขึ้นเพราะอะไร** เพื่อนำไปปรับกลยุทธ์การตลาดให้องค์กรมีประสิทธิภาพมากยิ่งขึ้น
- แกนวิเคราะห์: ช่องทางการขาย, วิธีชำระ, หมวดสินค้า, เทรนด์เดือน, Top 10 รายการ
- KPI หลัก: Revenue, Orders, Units, AOV, (ROAS หากมี `ad_spend`)




— _Made with ❤️ by a Data Analyst intern (Economics major)_
