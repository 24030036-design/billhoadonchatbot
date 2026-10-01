import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

# =========================================================
# CẤU HÌNH TRANG
# =========================================================

st.set_page_config(
    page_title="LYLY Milk Tea",
    page_icon="🧋",
    layout="wide"
)

# =========================================================
# GIAO DIỆN
# =========================================================

st.markdown("""
<style>

.main-title {
    text-align: center;
    font-size: 48px;
    font-weight: bold;
    color: #d85c8a;
    margin-bottom: 0px;
}

.sub-title {
    text-align: center;
    font-size: 18px;
    color: #777;
    margin-bottom: 25px;
}

.total-box {
    background-color: #fff0f5;
    border: 2px solid #f3a8c0;
    border-radius: 15px;
    padding: 25px;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 20px;
}

.total-title {
    font-size: 20px;
    font-weight: bold;
}

.total-money {
    font-size: 36px;
    font-weight: bold;
    color: #d85c8a;
}

.bill-box {
    background-color: #fffafc;
    border: 2px solid #f0b6c8;
    border-radius: 15px;
    padding: 25px;
}

.bill-header {
    text-align: center;
    font-size: 32px;
    font-weight: bold;
    color: #d85c8a;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# TIÊU ĐỀ
# =========================================================

st.markdown(
    '<div class="main-title">🧋 LYLY</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Trà sữa ngon - Vị ngọt yêu thương ❤️</div>',
    unsafe_allow_html=True
)

st.divider()


# =========================================================
# MENU
# =========================================================

MENU = {

    # -------- TRÀ SỮA --------
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa thái xanh": 30000,
    "Trà sữa thái đỏ": 30000,
    "Trà sữa bạc hà": 35000,
    "Trà sữa caramel": 40000,

    # -------- TRÀ --------
    "Trà đào": 30000,
    "Trà vải": 30000,
    "Trà mãng cầu": 35000
}


# =========================================================
# TOPPING
# =========================================================

TOPPING = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch trái cây": 5000,
    "Thạch phô mai": 7000,
    "Pudding trứng": 7000,
    "Kem cheese": 10000
}


# =========================================================
# SIZE
# =========================================================

SIZE = {
    "M": 0,
    "L": 5000
}


# =========================================================
# SESSION STATE
# =========================================================

if "so_mon" not in st.session_state:
    st.session_state.so_mon = 1


# =========================================================
# THÔNG TIN KHÁCH HÀNG
# =========================================================

st.subheader("👤 THÔNG TIN KHÁCH HÀNG")

ten_khach = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)


# =========================================================
# THÊM / XÓA MÓN
# =========================================================

st.subheader("🛒 THÊM MÓN")

col1, col2 = st.columns(2)

with col1:

    if st.button(
        "➕ THÊM MÓN",
        use_container_width=True
    ):

        st.session_state.so_mon += 1
        st.rerun()


with col2:

    if st.button(
        "➖ XÓA MÓN CUỐI",
        disabled=st.session_state.so_mon <= 1,
        use_container_width=True
    ):

        st.session_state.so_mon -= 1
        st.rerun()


st.divider()


# =========================================================
# DANH SÁCH ĐƠN HÀNG
# =========================================================

don_hang = []


# =========================================================
# NHẬP TỪNG MÓN
# =========================================================

for i in range(st.session_state.so_mon):

    st.markdown(f"## 🧋 MÓN {i + 1}")

    # -----------------------------------------------------
    # TÊN MÓN + SỐ LƯỢNG + SIZE
    # -----------------------------------------------------

    col1, col2, col3 = st.columns([4, 1, 2])

    with col1:

        loai_nuoc = st.selectbox(
            "Loại trà / trà sữa",
            list(MENU.keys()),
            key=f"loai_nuoc_{i}"
        )


    with col2:

        so_luong = st.number_input(
            "Số lượng",
            min_value=1,
            max_value=50,
            value=1,
            step=1,
            key=f"so_luong_{i}"
        )


    with col3:

        size = st.radio(
            "Size",
            ["M", "L"],
            horizontal=True,
            key=f"size_{i}"
        )


    # -----------------------------------------------------
    # TOPPING - ĐƯỜNG - ĐÁ
    # -----------------------------------------------------

    col4, col5, col6 = st.columns(3)


    with col4:

        topping = st.multiselect(
            "🍡 Topping",
            list(TOPPING.keys()),
            key=f"topping_{i}"
        )


    with col5:

        muc_duong = st.selectbox(
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

        muc_da = st.selectbox(
            "🧊 Mức độ đá",
            [
                "Ít đá",
                "Nhiều đá",
                "Không đá"
            ],
            key=f"da_{i}"
        )


    # =====================================================
    # TÍNH GIÁ
    # =====================================================

    gia_co_ban = MENU[loai_nuoc]

    gia_size = SIZE[size]

    tien_topping = sum(
        TOPPING[x]
        for x in topping
    )

    don_gia = (
        gia_co_ban
        + gia_size
        + tien_topping
    )

    thanh_tien = don_gia * so_luong


    # =====================================================
    # HIỂN THỊ GIÁ MÓN
    # =====================================================

    st.info(
        f"💰 Đơn giá: **{don_gia:,} VNĐ/ly**  |  "
        f"Thành tiền: **{thanh_tien:,} VNĐ**"
    )


    # =====================================================
    # LƯU ĐƠN
    # =====================================================

    don_hang.append({

        "STT": i + 1,

        "Loại trà / trà sữa": loai_nuoc,

        "Size": size,

        "Số lượng": so_luong,

        "Topping":
            ", ".join(topping)
            if topping
            else "Không topping",

        "Mức đường": muc_duong,

        "Mức đá": muc_da,

        "Đơn giá": don_gia,

        "Thành tiền": thanh_tien
    })


    st.divider()


# =========================================================
# TÍNH TỔNG TIỀN
# =========================================================

tong_tien = sum(
    item["Thành tiền"]
    for item in don_hang
)


# =========================================================
# HIỂN THỊ KẾT QUẢ ĐÃ NHẬP
# =========================================================

st.subheader("📋 CHI TIẾT ĐƠN HÀNG")

df = pd.DataFrame(don_hang)


# Tạo bảng hiển thị đẹp hơn
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


# =========================================================
# TỔNG TIỀN
# =========================================================

st.markdown(
    f"""
    <div class="total-box">

        <div class="total-title">
            💰 TỔNG SỐ TIỀN CẦN THANH TOÁN
        </div>

        <div class="total-money">
            {tong_tien:,} VNĐ
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# NÚT THANH TOÁN
# =========================================================

if st.button(
    "💳 THANH TOÁN",
    type="primary",
    use_container_width=True
):

    # -----------------------------------------------------
    # KIỂM TRA TÊN KHÁCH
    # -----------------------------------------------------

    if ten_khach.strip() == "":

        st.error(
            "⚠️ Vui lòng nhập tên khách hàng!"
        )

        st.stop()


    # -----------------------------------------------------
    # TẠO BILL
    # -----------------------------------------------------

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


    # =====================================================
    # BILL
    # =====================================================

    st.markdown(
        '<div class="bill-box">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="bill-header">🧾 LYLY MILK TEA</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;'>"
        "Trà sữa ngon - Vị ngọt yêu thương ❤️"
        "</p>",
        unsafe_allow_html=True
    )


    st.divider()


    # -----------------------------------------------------
    # THÔNG TIN BILL
    # -----------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Mã hóa đơn:** {ma_bill}"
        )

        st.write(
            f"**Khách hàng:** {ten_khach}"
        )


    with col2:

        st.write(
            f"**Thời gian:** {thoi_gian}"
        )

        st.write(
            f"**Số món:** {len(don_hang)}"
        )


    st.divider()


    # =====================================================
    # CHI TIẾT TỪNG MÓN TRÊN BILL
    # =====================================================

    for item in don_hang:

        st.markdown(
            f"""
### 🧋 {item["STT"]}. {item["Loại trà / trà sữa"]}

| Thông tin | Chi tiết |
|---|---|
| Size | **{item["Size"]}** |
| Số lượng | **{item["Số lượng"]} ly** |
| Topping | **{item["Topping"]}** |
| Mức đường | **{item["Mức đường"]}** |
| Mức đá | **{item["Mức đá"]}** |
| Đơn giá | **{item["Đơn giá"]:,} VNĐ** |
| Thành tiền | **{item["Thành tiền"]:,} VNĐ** |
"""
        )

        st.divider()


    # =====================================================
    # TỔNG THANH TOÁN
    # =====================================================

    st.markdown(
        f"""
## 💰 TỔNG THANH TOÁN

# {tong_tien:,} VNĐ
"""
    )


    st.markdown(
        """
        <p style="text-align:center;
                  font-size:18px;
                  color:#d85c8a;">
            💗 Cảm ơn quý khách đã ủng hộ LYLY! 💗
        </p>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # =====================================================
    # XUẤT EXCEL
    # =====================================================

    st.divider()

    st.subheader("📥 XUẤT BILL")


    df_excel = pd.DataFrame(don_hang)


    # Thêm thông tin hóa đơn

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


    # =====================================================
    # TẠO FILE EXCEL
    # =====================================================

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


    # =====================================================
    # NÚT DOWNLOAD
    # =====================================================

    st.download_button(

        label="📥 TẢI BILL EXCEL",

        data=excel_data,

        file_name=f"Bill_Lyly_{ma_bill}.xlsx",

        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),

        use_container_width=True
    )
