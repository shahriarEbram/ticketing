import streamlit as st
import code_validator
from func import today_shamsi, show_box
from Database import add_ticket

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

col1row1, col2row1, col3row1 = st.columns([3, 3, 3])
with col1row1:
    show_box("علی سهرابی", "نام درخواست کننده")
with col2row1:
    show_box("CU1245", "شماره درخواست")
with col3row1:
    show_box(str(today_shamsi), "تاریخ درخواست")

with st.container(border=True):
    col1row2, col2row2, col3row2, col4row2, col5row2, col6row2 = st.columns([1, 1, 1, 1, 0.6, 0.5])
    with col1row2:
        type = st.selectbox("نوع کار",
                            key='type',
                            options=(code_validator.map_type.values()),
                            index=None,
                            placeholder="نوع کار را انتخاب کنید")
        if type:
            typ_key = next((k for k, v in code_validator.map_type.items() if v == type), None)
    with col2row2:
        product = st.selectbox(
            "محصول",
            key="product",
            options=(code_validator.product_name.values()),
            index=None,
            placeholder="محصول را انتخاب کنید")
        if product:
            pro_key = next((k for k, v in code_validator.product_name.items() if v == product), None)
    with col3row2:
        equ = st.selectbox("دسته بندی درخواست",
                           options=(code_validator.equipment_name.values()),
                           index=None,
                           placeholder="نوع تجهیز را انتخاب کنید",
                           )
        if equ:
            equ_key = [k for k, v in code_validator.equipment_name.items() if v == equ]
            equ_key = equ_key[0]
    with col4row2:
        if equ:
            equ_key = [k for k, v in code_validator.equipment_name.items() if v == equ]
            equ_key = equ_key[0]
        else:
            subset = st.selectbox("جزئیات",
                                  placeholder="ابتدا نوع تجهیز را انتخاب کنید!",
                                  options=[""])
        if equ:
            subset = st.selectbox(
                "Subset",
                key="subset",
                options=(code_validator.equipment_name_subset.get(equ_key[0]).values()),
                index=None,
                placeholder="زیرمجموعه را انتخاب کنید",
            )
        if subset:
            subset_key = next(
                (k for k, v in code_validator.equipment_name_subset[equ_key[0]].items() if v == subset),
                None)
            print(subset_key)
    with col5row2:
        number = st.number_input(
            "شمارنده(دست چندمه؟)",
            min_value=1,
            max_value=99,
            step=1,
            key="counter",
            value=1,
            placeholder="Type a number..."
        )
        formatted_number = str(number).zfill(2)
    with col6row2:
        options = ["فوری", "عادی"]
        priority = st.pills("اولویت بندی",
                            options, default="عادی", selection_mode="single")

    col1row3, col2row3, col3row3 = st.columns([3, 3, 3])
    with col1row3:
        with st.container(border=True):
            st.write("تاریخ نیاز")
            col7, col8, col9 = st.columns(3)
            with col7:
                day = st.number_input('روز', min_value=today_shamsi.day, max_value=31, value=today_shamsi.day)
                day = f'{int(day):02}'
            with col8:
                month = st.number_input('ماه', min_value=today_shamsi.month, max_value=12, value=today_shamsi.month,
                                        disabled=False)
                month = f'{int(month):02}'
            with col9:
                year = st.number_input('سال', min_value=1300, max_value=1500, value=today_shamsi.year, disabled=True)
            # task_date = jdatetime.date(year, month, day)
            # تبدیل تاریخ شمسی به رشته با فرمت 1403-6-31
            req_date = f"{year}-{month}-{day}"
    with col2row3:
        with st.container(border=True):
            req_description = st.text_area('توضیحات/شرح درخواست',
                                           height=79,
                                           max_chars=100, )
    with col3row3:
        with st.container(border=True):
            uploaded_files = st.file_uploader(
                "پیوست فایل (اختیاری)",
                accept_multiple_files=True,
            )
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                st.write("filename:", uploaded_file.name)
                st.write(bytes_data)

    col1row4, col2row4, col3row4 = st.columns([3, 1, 3])
    with col1row4:
        pass
    with col2row4:
        submitted_task = st.button("ارجاع به واحد مهندسی", key="task_submit_button")
    with col3row4:
        pass

    if submitted_task:
        # بررسی پر شدن تمام فیلدهای ضروری
        if not type:
            st.warning("لطفاً نوع کار را انتخاب کنید.")
        elif not product:
            st.warning("لطفاً محصول را انتخاب کنید.")
        elif not equ:
            st.warning("لطفاً دسته‌بندی درخواست را انتخاب کنید.")
        elif not subset:
            st.warning("لطفاً زیرمجموعه را انتخاب کنید.")
        elif not req_description.strip():
            st.warning("لطفاً شرح درخواست را وارد کنید.")
        elif not priority:
            st.warning("لطفاً اولویت را انتخاب کنید.")
        else:

            # اگر همه فیلدها پر باشند، اطلاعات را چاپ می‌کنیم
            new_task = {
                "نوع کار": type,
                "محصول": product,
                "دسته‌بندی درخواست": equ,
                "زیرمجموعه": subset,
                "شمارنده": formatted_number,
                "اولویت": priority[0] if priority else None,
                "تاریخ نیاز": req_date,
                "شرح درخواست": req_description,
            }
            st.success("همه فیلدها با موفقیت پر شدند!")
            coding = str(equ_key + subset_key + pro_key + "02" + typ_key + formatted_number)
            add_ticket(requester_name="بابک کریم پور",
                       requester_unit="CA",
                       request_number="112",
                       need_date=str(req_date),
                       request_date=str(today_shamsi),
                       project_code=coding,
                       request_description=req_description,
                       request_priority=priority,
                       )
