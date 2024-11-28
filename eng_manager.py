import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder



st.set_page_config(layout="wide", page_title="login")

# اعمال تنظیمات راست به چپ برای بدنه و فونت فارسی
st.markdown("""
    <style>
    @import url('https://v1.fontapi.ir/css/Vazir');
    body {
        direction: rtl;
        font-family: 'Vazir', sans-serif;
    }
    </style>
    """, unsafe_allow_html=True)


# داده‌های نمونه به صورت DataFrame
data = pd.DataFrame([
    {
        "نام درخواست دهنده": "بابک کریم پور",
        "شماره درخواست": "TO120",
        "واحد": "ابزار",
        "کد پروژه": "C101002S05",
        "ارجاع مهندسی": "",
        "ارجاع ساخت": "",
        "تاریخ درخواست": "",
        "وضعیت": ""
    }
])

# گزینه‌های SelectBox
engineering_options = ["تایید", "رد", "در انتظار"]
manufacturing_options = ["تایید", "رد", "در انتظار"]

# تنظیم Grid
gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_column("نام درخواست دهنده", editable=True)
gb.configure_column("شماره درخواست", editable=True)
gb.configure_column("واحد", editable=True)
gb.configure_column("کد پروژه", editable=True)
gb.configure_column("ارجاع مهندسی", editable=True, cellEditor="agSelectCellEditor", cellEditorParams={"values": engineering_options})
gb.configure_column("ارجاع ساخت", editable=True, cellEditor="agSelectCellEditor", cellEditorParams={"values": manufacturing_options})
gb.configure_column("تاریخ درخواست", editable=True)
gb.configure_column("وضعیت", editable=True)

grid_options = gb.build()

# نمایش DataEditor
st.subheader("جدول مدیریت درخواست‌ها")
response = AgGrid(data, gridOptions=grid_options, editable=True, fit_columns_on_grid_load=True)

# نمایش داده‌ها پس از ویرایش
st.write("داده‌های ویرایش شده:")
st.write(response['data'])
