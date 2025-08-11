# -*- coding: utf-8 -*-
#Cleaning data with Python in google collab





 === CLEAN ECOM DATA 
import pandas as pd
import numpy as np

# 0) โหลดไฟล์
df = pd.read_csv("ECOM AFTER CLEANED.csv")

# 1) สร้างสำเนาทำงาน
out = df.copy()

# 2) มาตรฐานชื่อคอลัมน์
out.columns = (out.columns
               .str.strip()
               .str.replace(r"\s+", "_", regex=True)
               .str.lower())

# 3) ตัดช่องว่างในคอลัมน์ข้อความ
obj_cols = out.select_dtypes(include="object").columns
for c in obj_cols:
    out[c] = out[c].astype(str).str.strip().replace({"nan": pd.NA})

# 4) แปลงวันเวลา + Feature วันที่
if "order_date" in out.columns:
    out["order_datetime"] = pd.to_datetime(out["order_date"], errors="coerce")
    out = out[(out["order_datetime"].between("2015-01-01","2030-12-31")) | out["order_datetime"].isna()]
    out["order_date"]  = out["order_datetime"].dt.date
    out["order_year"]  = out["order_datetime"].dt.year
    out["order_month"] = out["order_datetime"].dt.month
    out["order_week"]  = out["order_datetime"].dt.isocalendar().week.astype("Int64")

# 5) บังคับชนิดข้อมูลตัวเลข
for c in ["quantity","unit_price","discount_rate","line_total","ad_spend"]:
    if c in out.columns:
        out[c] = pd.to_numeric(out[c], errors="coerce")

# 6) ลบแถวซ้ำ
out = out.drop_duplicates()



# 10) เซฟไฟล์
out.to_csv("ecom_cleaned_ready.csv", index=False)

print({
    "rows_before": len(df),
    "rows_after": len(out),
    "duplicates_removed": df.duplicated().sum()
})
out.head(3)

 ==== ขั้นตอนEDA 
 #import library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams["figure.figsize"] = (10,4)

def load_df():
    try:
        return out.copy()  # จากขั้นตอน clean ที่ทำไว้เมื่อกี๊
    except NameError:
        pass
    for f in ["ecom_step6.csv", "ECOM AFTER CLEANED.csv"]:
        if Path(f).exists():
            return pd.read_csv(f, low_memory=False)
    raise FileNotFoundError("ไม่พบ out / ecom_step6.csv / ECOM AFTER CLEANED.csv")

df = load_df()

# วันเวลา
if "order_datetime" in df.columns:
    df["order_datetime"] = pd.to_datetime(df["order_datetime"], errors="coerce")
elif "order_date" in df.columns:
    df["order_datetime"] = pd.to_datetime(df["order_date"], errors="coerce")
else:
    df["order_datetime"] = pd.NaT

# ยอดเงิน (เผื่อมีค่า line_total บางอันข้อมูลไม่สมบูณ์)
if "line_total" not in df.columns or df["line_total"].isna().all():
    if set(["quantity","unit_price"]).issubset(df.columns):
        disc = df["discount_rate"].fillna(0) if "discount_rate" in df.columns else 0
        df["line_total"] = pd.to_numeric(df["quantity"], errors="coerce") * \
                           pd.to_numeric(df["unit_price"], errors="coerce") * (1 - disc)
    else:
        df["line_total"] = np.nan
df["line_total"] = pd.to_numeric(df["line_total"], errors="coerce")

# สถานะ
status = df["status"].astype(str).str.lower() if "status" in df.columns else ""
is_completed = status.eq("completed") if isinstance(status, pd.Series) else pd.Series(False, index=df.index)
is_cancelled = status.eq("cancelled") if isinstance(status, pd.Series) else pd.Series(False, index=df.index)
is_returned  = status.eq("returned")  if isinstance(status, pd.Series) else pd.Series(False, index=df.index)

# KPI OVERVIEW 
date_min = df["order_datetime"].min()
date_max = df["order_datetime"].max()
orders_all = df["order_id"].nunique() if "order_id" in df.columns else len(df)
orders_cmp = df.loc[is_completed, "order_id"].nunique() if "order_id" in df.columns else is_completed.sum()
revenue    = df.loc[is_completed, "line_total"].sum(skipna=True)
units      = df.loc[is_completed, "quantity"].sum(skipna=True) if "quantity" in df.columns else np.nan
aov        = revenue / orders_cmp if orders_cmp else np.nan
cancel_rt  = is_cancelled.mean() if isinstance(is_cancelled, pd.Series) else np.nan
return_rt  = is_returned.mean()  if isinstance(is_returned , pd.Series) else np.nan
roas = np.nan
if "ad_spend" in df.columns:
    ad_total = pd.to_numeric(df["ad_spend"], errors="coerce").sum(skipna=True)
    roas = revenue / ad_total if ad_total else np.nan

kpi = pd.DataFrame([{
    "date_range": f"{date_min.date() if pd.notna(date_min) else '-'} → {date_max.date() if pd.notna(date_max) else '-'}",
    "orders_all": orders_all,
    "orders_completed": orders_cmp,
    "revenue_completed": round(revenue, 2),
    "units_completed": units,
    "AOV_completed": round(aov, 2) if pd.notna(aov) else np.nan,
    "cancel_rate": round(float(cancel_rt), 4) if pd.notna(cancel_rt) else np.nan,
    "return_rate": round(float(return_rt), 4) if pd.notna(return_rt) else np.nan,
    "ROAS_overall": round(float(roas), 3) if pd.notna(roas) else np.nan
}])
print("=== KPI OVERVIEW ===")
print(kpi.T)

kpi = pd.DataFrame([{
    "date_range": f"{date_min.date() if pd.notna(date_min) else '-'} → {date_max.date() if pd.notna(date_max) else '-'}",
    "orders_all": orders_all,
    "orders_completed": orders_cmp,
    "revenue_completed": round(revenue, 2),
    "units_completed": units,
    "AOV_completed": round(aov, 2) if pd.notna(aov) else np.nan,
    "cancel_rate": round(float(cancel_rt), 4) if pd.notna(cancel_rt) else np.nan,
    "return_rate": round(float(return_rt), 4) if pd.notna(return_rt) else np.nan,
    "ROAS_overall": round(float(roas), 3) if pd.notna(roas) else np.nan
}])
print("=== KPI OVERVIEW ===")
print(kpi.T)

# ----- FIXED: Monthly Orders & Revenue -----
x = df.copy()  

# เช็คให้แน่ใจว่าเป็น datetime
if "order_datetime" in x.columns:
    x["order_datetime"] = pd.to_datetime(x["order_datetime"], errors="coerce")
elif "order_date" in x.columns:
    x["order_datetime"] = pd.to_datetime(x["order_date"], errors="coerce")
x = x.dropna(subset=["order_datetime"]).sort_values("order_datetime")

# mask ของ Completed ต้องคำนวณจาก x (เฟรมเดียวกัน)
if "status" in x.columns:
    mask_cmp = x["status"].astype(str).str.lower().eq("completed")
else:
    mask_cmp = pd.Series(True, index=x.index)  # ถ้าไม่มี status ก็ใช้ทุกออเดอร์

# ทำดัชนีเวลา
xm = x.set_index("order_datetime")

# จำนวนออเดอร์ต่อเดือน
m_orders_all = (
    xm["order_id"].resample("ME").nunique()
    if "order_id" in x.columns else
    xm.resample("ME").size()
)


# รายได้ต่อเดือน (เอาเฉพาะ Completed)
m_rev = (
    x.loc[mask_cmp]
      .set_index("order_datetime")["line_total"]
      .resample("ME").sum()
)

# วาดกราฟ
ax = m_orders_all.plot()
m_rev.plot(secondary_y=True, ax=ax)
ax.set_title("Monthly Orders (left) & Revenue (right)")
ax.set_ylabel("orders")
ax.right_ax.set_ylabel("revenue")
plt.tight_layout(); plt.show()

def kpi_by(col):
    d = df[is_completed].copy() if is_completed.any() else df.copy()
    if col not in d.columns:
        return pd.DataFrame()
    g = d.groupby(col, dropna=False)
    tab = pd.DataFrame({
        "revenue": g["line_total"].sum(),
        "orders":  g["order_id"].nunique() if "order_id" in d.columns else g.size()
    })
    tab["AOV"] = tab["revenue"] / tab["orders"].replace(0, np.nan)
    if "ad_spend" in d.columns:
        tab["ad_spend"] = g["ad_spend"].sum()
        tab["ROAS"] = tab["revenue"] / tab["ad_spend"].replace(0, np.nan)
    return tab.sort_values("revenue", ascending=False).reset_index()

by_channel = kpi_by("channel")
if not by_channel.empty:
    print("\n=== Channel KPI (Completed) ===")
    print(by_channel.head(10))
    # บาร์เรียบ ๆ
    by_channel.set_index("channel")["revenue"].head(10).plot(kind="bar")
    plt.title("Top Channels by Revenue (Completed)")
    plt.tight_layout(); plt.show()


# CATEGORY TOP10 
def top_table(cols, n=10):
    d = df[is_completed].copy() if is_completed.any() else df.copy()
    g = d.groupby(cols, dropna=False)
    tab = pd.DataFrame({
        "revenue": g["line_total"].sum(),
        "orders":  g["order_id"].nunique() if "order_id" in d.columns else g.size(),
        "units":   g["quantity"].sum() if "quantity" in d.columns else np.nan,
    }).sort_values("revenue", ascending=False).head(n)
    return tab.reset_index()

top_cat = top_table(["category"], n=10) if "category" in df.columns else pd.DataFrame()
if not top_cat.empty:
    print("\n=== Top 10 Categories (by Revenue, Completed) ===")
    print(top_cat)
    top_cat.set_index("category")["revenue"].plot(kind="bar")
    plt.title("Top Categories by Revenue (Completed)")
    plt.tight_layout(); plt.show()


# PRODUCT TOP10 

top_prod = top_table([prod_key], n=10) if prod_key else pd.DataFrame()
if not top_prod.empty:
    print("\n=== Top 10 Products (by Revenue, Completed) ===")
    print(top_prod)

    # ตั้งแนวกราฟ
    (top_prod
        .set_index(prod_key)["revenue"]
        .plot(kind="bar"))

    plt.title("Top 10 Products by Revenue (Completed)")
    plt.xlabel("Product"); plt.ylabel("Revenue")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
  
    plt.show()

