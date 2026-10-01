import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# =====================================================
# CẤU HÌNH TRANG
# =====================================================
st.image("hinhanhcuaquan.png")
st.set_page_config(
    page_title="Lyly Milk Tea",
    page_icon="🧋",
    layout="wide"
)

# =====================================================
# GIAO DIỆN
# =====================================================

st.markdown("""
<style>
.main-title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    margin-bottom: 25px;
}

.total-box {
    padding: 20px;
    border-radius: 15px;
    text-align: center;
    background-color: #fff0f5;
    border: 2px solid #ffb6c1;
}

.total-money {
    font-size: 32px;
    font-weight: bold;
}

.bill-title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# TIÊU ĐỀ QUÁN
# =====================================================

st.markdown(
    '<div class="main-title">🧋 LYLY</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Trà sữa ngon - Vị ngọt yêu thương ❤️</div>',
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# MENU
# =====================================================

MENU = {

    # TRÀ SỮA
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa thái xanh": 30000,
    "Trà sữa thái đỏ": 30000,
    "Trà sữa bạc hà": 35000,
    "Trà sữa caramel": 40000,

    # TRÀ TRÁI CÂY
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà mãng cầu": 35000
}


# =====================================================
# TOPPING
# =====================================================

TOPPING = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch phô mai": 7000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000
}


# =====================================================
# THÔNG TIN KHÁCH HÀNG
# =====================================================

st.subheader("👤 Thông tin khách hàng")

ten_khach = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)


# =====================================================
# SESSION STATE
# =====================================================

if "so_mon" not in st.session_state:
    st.session_state.so_mon = 1


# =====================================================
# THÊM / XÓA MÓN
# =====================================================

col1, col2 = st.columns(2)

with col1:
    if st.button(
        "➕ Thêm loại trà sữa",
        use_container_width=True
    ):
        st.session_state.so_mon += 1
        st.rerun()

with col2:
    if st.button(
        "➖ Xóa món cuối",
        disabled=st.session_state.so_mon <= 1,
        use_container_width=True
    ):
        st.session_state.so_mon -= 1
        st.rerun()


st.divider()


# =====================================================
# CHỌN MÓN
# =====================================================

don_hang = []

st.subheader("🛒 Chọn món")

for i in range(st.session_state.so_mon):

    st.markdown(f"### 🧋 Món {i + 1}")

    col1, col2, col3 = st.columns([3, 1, 2])

    # -----------------------------
    # LOẠI TRÀ
    # -----------------------------

    with col1:

        loai_tra = st.selectbox(
            "Loại trà / trà sữa",
            list(MENU.keys()),
            key=f"tra_{i}"
        )

    # -----------------------------
    # SỐ LƯỢNG
    # -----------------------------

    with col2:

        so_luong = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=50,
            value=1,
            step=1,
            key=f"sl_{i}"
        )

    # -----------------------------
    # GIÁ
    # -----------------------------

    with col3:

        gia_tra = MENU[loai_tra]

        st.write("Giá / ly")
        st.write(
            f"**{gia_tra:,} VNĐ**"
        )

    # -----------------------------
    # TOPPING - ĐƯỜNG - ĐÁ
    # -----------------------------

    col4, col5, col6 = st.columns(3)

    with col4:

        topping = st.multiselect(
            "🍡 Topping",
            list(TOPPING.keys()),
            key=f"topping_{i}"
        )

    with col5:

        duong = st.selectbox(
            "🍬 Mức độ đường",
            [
                "100%",
                "70%",
                "50%",
                "0%"
            ],
            key=f"duong_{i}"
        )

    with col6:

        da = st.selectbox(
            "🧊 Mức độ đá",
            [
                "Ít đá",
                "Nhiều đá",
                "Không đá"
            ],
            key=f"da_{i}"
        )

    # =================================================
    # TÍNH TIỀN
    # =================================================

    tien_topping = 0

    for tp in topping:
        tien_topping += TOPPING[tp]

    don_gia = gia_tra + tien_topping

    thanh_tien = don_gia * so_luong

    # Lưu đơn hàng

    don_hang.append({

        "STT": i + 1,

        "Loại trà / trà sữa": loai_tra,

        "Số lượng": so_luong,

        "Topping":
            ", ".join(topping)
            if topping
            else "Không topping",

        "Mức đường": duong,

        "Mức đá": da,

        "Đơn giá": don_gia,

        "Thành tiền": thanh_tien
    })

    st.divider()


# =====================================================
# TỔNG TIỀN
# =====================================================

tong_tien = sum(
    item["Thành tiền"]
    for item in don_hang
)


# =====================================================
# HIỂN THỊ ĐƠN HÀNG
# =====================================================

st.subheader("📋 KIỂM TRA ĐƠN HÀNG")

df = pd.DataFrame(don_hang)

df_hien_thi = df.copy()

df_hien_thi["Đơn giá"] = (
    df_hien_thi["Đơn giá"]
    .apply(lambda x: f"{x:,} VNĐ")
)

df_hien_thi["Thành tiền"] = (
    df_hien_thi["Thành tiền"]
    .apply(lambda x: f"{x:,} VNĐ")
)

st.dataframe(
    df_hien_thi,
    use_container_width=True,
    hide_index=True
)


# =====================================================
# HIỂN THỊ TỔNG TIỀN
# =====================================================

st.markdown(
    f"""
    <div class="total-box">
        <div>TỔNG SỐ TIỀN CẦN THANH TOÁN</div>

        <div class="total-money">
            {tong_tien:,} VNĐ
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.write("")


# =====================================================
# THANH TOÁN
# =====================================================

if st.button(
    "💳 THANH TOÁN",
    type="primary",
    use_container_width=True
):

    # Kiểm tra tên khách

    if not ten_khach.strip():

        st.error(
            "⚠️ Vui lòng nhập tên khách hàng!"
        )

        st.stop()


    # =================================================
    # TẠO MÃ BILL
    # =================================================

    ma_bill = datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )

    thoi_gian = datetime.now().strftime(
        "%d/%m/%Y %H:%M:%S"
    )


    st.success(
        "✅ Thanh toán thành công!"
    )

    st.divider()


    # =================================================
    # BILL
    # =================================================

    st.markdown(
        '<div class="bill-title">🧾 BILL HÓA ĐƠN</div>',
        unsafe_allow_html=True
    )

    st.write(
        "**🧋 LYLY MILK TEA**"
    )

    st.write(
        f"**Mã hóa đơn:** {ma_bill}"
    )

    st.write(
        f"**Thời gian:** {thoi_gian}"
    )

    st.write(
        f"**Khách hàng:** {ten_khach}"
    )

    st.divider()


    # =================================================
    # CHI TIẾT TỪNG MÓN
    # =================================================

    for item in don_hang:

        st.markdown(
            f"""
            ### {item["STT"]}. {item["Loại trà / trà sữa"]}

            **Số lượng:** {item["Số lượng"]}

            **Topping:** {item["Topping"]}

            **Đường:** {item["Mức đường"]}

            **Đá:** {item["Mức đá"]}

            **Đơn giá:** {item["Đơn giá"]:,} VNĐ

            **Thành tiền:** {item["Thành tiền"]:,} VNĐ
            """
        )

        st.divider()


    # =================================================
    # TỔNG THANH TOÁN
    # =================================================

    st.markdown(
        f"""
        ### 💰 TỔNG THANH TOÁN

        # {tong_tien:,} VNĐ
        """
    )

    st.success(
        "💗 Cảm ơn quý khách đã ủng hộ LYLY!"
    )


    # =================================================
    # XUẤT EXCEL
    # =================================================

    st.subheader("📥 Xuất hóa đơn")

    df_excel = pd.DataFrame(don_hang)

    df_excel.insert(
        0,
        "Mã hóa đơn",
        ma_bill
    )

    df_excel.insert(
        1,
        "Thời gian",
        thoi_gian
    )

    df_excel.insert(
        2,
        "Khách hàng",
        ten_khach
    )


    # =================================================
    # TẠO FILE EXCEL
    # =================================================

    output = BytesIO()

    with pd.ExcelWriter(
        output,
        engine="openpyxl"
    ) as writer:

        df_excel.to_excel(
            writer,
            index=False,
            sheet_name="Hóa đơn"
        )

        worksheet = writer.sheets["Hóa đơn"]


        # Điều chỉnh độ rộng cột

        for column in worksheet.columns:

            max_length = 0

            column_letter = (
                column[0].column_letter
            )

            for cell in column:

                try:

                    if len(str(cell.value)) > max_length:

                        max_length = len(
                            str(cell.value)
                        )

                except:
                    pass

            worksheet.column_dimensions[
                column_letter
            ].width = max_length + 3


    excel_data = output.getvalue()


    # =================================================
    # DOWNLOAD EXCEL
    # =================================================

    st.download_button(

        label="📥 TẢI BILL EXCEL",

        data=excel_data,

        file_name=
            f"Bill_Lyly_{ma_bill}.xlsx",

        mime=
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet",

        use_container_width=True
    )
```

### Menu hiện tại của Lyly

**Trà sữa:**

* Trà sữa truyền thống — 30.000đ
* Trà sữa matcha — 35.000đ
* Trà sữa socola — 35.000đ
* Trà sữa khoai môn — 35.000đ
* Trà sữa dâu — 35.000đ
* Trà sữa thái xanh — 30.000đ
* Trà sữa thái đỏ — 30.000đ
* Trà sữa bạc hà — 35.000đ
* Trà sữa caramel — 40.000đ

**Trà trái cây mới thêm:**

* 🍑 **Trà đào — 30.000đ**
* 🍇 **Trà vải — 30.000đ**
* 🥭 **Trà mãng cầu — 35.000đ**

Bạn chỉ cần chạy lại `app.py` là 3 món mới sẽ xuất hiện trong danh sách chọn món.
