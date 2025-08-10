# One‑Pager — E‑Commerce Analytics

**Objective:** แปลงข้อมูลคำสั่งซื้อให้เป็น insight ที่ตัดสินใจได้  
**Stack:** SQL → Python → Excel → Power BI

## KPIs
- Revenue, Orders, Units, AOV
- Breakdown: Channel, Payment, Category
- Trend: Monthly

## Process
1) SQL รวมตาราง fact/dim + งบโฆษณา (ถ้ามี)  
2) Python ทำความสะอาดและฟีเจอร์เวลา  
3) Excel pivot ตรวจ sanity check  
4) Power BI ทำแดชบอร์ดดูภาพรวมและ drill‑down

## Deliverables
- README + โค้ด reproducible
- Dashboard (ภาพใน `docs/figs/`)
- ข้อเสนอแนะเชิงปฏิบัติ (เช่น โฟกัสช่องทางที่ ROAS สูง, แก้ bottleneck อัตราแปลง)

