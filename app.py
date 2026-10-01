import streamlit as st
import pandas as pd
from datetime import datetime

# =====================================================
# CẤU HÌNH
# =====================================================

st.set_page_config(
    page_title="LYLY - Tính Bill",
    page_icon="🧋",
    layout="wide"
)

# =====================================================
# GIAO DIỆN
# =====================================================

st.markdown("""
<style>
    .title {
        text-align: center;
        font-size: 45px;
        font-weight: bold;
        color: #d85c8a;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #777;
        margin-bottom: 25px;
    }

    .total-box {
        background-color: #fff0f5;
        border: 2px solid #f5a9c4;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        margin-top: 20px;
    }

    .total-text {
        font-size: 20px;
        font-weight: bold;
    }

    .total-money {
        font-size: 35px;
        font-weight: bold;
        color: #d85c8a;
    }

    .bill {
        background-color: #fffafa;
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 25px;
    }
</style>
""", unsafe_allow_html=True)


# =====================================================
# TIÊU ĐỀ
# =====================================================

st.markdown(
    '<div class="title">🧋 LYLY</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Trà sữa ngon - Vị ngọt yêu thương ❤️</div>',
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# MENU
# =====================================================

MENU = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa thái xanh": 30000,
    "Trà sữa thái đỏ": 30000,
    "Trà sữa bạc hà": 35000,
    "Trà sữa caramel": 40000,

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
# SESSION STATE
# =====================================================

if "so_mon" not in st.session_state:
    st.session_state.so_mon = 1


# =====================================================
# THÔNG TIN KHÁCH HÀNG
# =====================================================

st.subheader("👤 Thông tin khách hàng")

ten_khach = st.text_input(
    "Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)


# =====================================================
# THÊM / XÓA MÓN
# =====================================================

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


# =====================================================
# CHỌN MÓN
# =====================================================

st.subheader("🛒 Chọn món")

don_hang = []

for i in range(st.session_state.so_mon):

    st.markdown(f"### 🧋 Món {i + 1}")

    # ---------------------------------------------
    # LOẠI TRÀ + SỐ LƯỢNG
    # ---------------------------------------------

    col1, col2, col3 = st.columns([4, 1, 2])

    with col1:
        loai_tra = st.selectbox(
            "Loại trà / trà sữa",
            list(MENU.keys()),
            key=f"loai_tra_{i}"
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
        gia = MENU[loai_tra]

        st.write("**Giá / ly**")
        st.write(f"### {gia:,} đ")

    # ---------------------------------------------
    # TOPPING - ĐƯỜNG - ĐÁ
    # ---------------------------------------------

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

    # ---------------------------------------------
    # TÍNH TIỀN
    # ---------------------------------------------

    tien_topping = sum(
        TOPPING[x]
        for x in topping
    )

    don_gia = gia + tien_topping

    thanh_tien = don_gia * so_luong

    # ---------------------------------------------
    # LƯU ĐƠN HÀNG
    # ---------------------------------------------

    don_hang.append({
        "STT": i + 1,
        "Loại trà / trà sữa": loai_tra,
        "Số lượng": so_luong,
        "Topping": (
            ", ".join(topping)
            if topping
            else "Không topping"
        ),
        "Mức đường": muc_duong,
        "Mức đá": muc_da,
        "Đơn giá": don_gia,
        "Thành tiền": thanh_tien
    })

    st.divider()


# =====================================================
# TÍNH TỔNG
# =====================================================

tong_tien = sum(
    item["Thành tiền"]
    for item in don_hang
)


# =====================================================
# HIỂN THỊ KẾT QUẢ ĐÃ NHẬP
# =====================================================

st.subheader("📋 ĐƠN HÀNG CỦA BẠN")

df = pd.DataFrame(don_hang)

df_hien_thi = df.copy()

df_hien_thi["Đơn giá"] = df_hien_thi[
    "Đơn giá"
].apply(
    lambda x: f"{x:,} VNĐ"
)

df_hien_thi["Thành tiền"] = df_hien_thi[
    "Thành tiền"
].apply(
    lambda x: f"{x:,} VNĐ"
)

st.dataframe(
    df_hien_thi,
    use_container_width=True,
    hide_index=True
)


# =====================================================
# TỔNG TIỀN
# =====================================================

st.markdown(
    f"""
    <div class="total-box">

        <div class="total-text">
            💰 TỔNG SỐ TIỀN CẦN THANH TOÁN
        </div>

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

    # Kiểm tra tên khách hàng

    if ten_khach.strip() == "":
        st.error(
            "⚠️ Vui lòng nhập tên khách hàng!"
        )

    else:

        # =============================================
        # TẠO MÃ HÓA ĐƠN
        # =============================================

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


        # =============================================
        # BILL
        # =============================================

        st.markdown(
            '<div class="bill">',
            unsafe_allow_html=True
        )

        st.markdown(
            "## 🧾 LYLY MILK TEA"
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


        # =============================================
        # CHI TIẾT BILL
        # =============================================

        for item in don_hang:

            st.markdown(
                f"""
                ### 🧋 {item["STT"]}. {item["Loại trà / trà sữa"]}

                **Số lượng:** {item["Số lượng"]}

                **Topping:** {item["Topping"]}

                **Mức đường:** {item["Mức đường"]}

                **Mức đá:** {item["Mức đá"]}

                **Đơn giá:** {item["Đơn giá"]:,} VNĐ

                **Thành tiền:** {item["Thành tiền"]:,} VNĐ
                """
            )

            st.divider()


        # =============================================
        # TỔNG THANH TOÁN
        # =============================================

        st.markdown(
            f"""
            ## 💰 TỔNG THANH TOÁN

            # {tong_tien:,} VNĐ
            """
        )

        st.markdown(
            """
            ### 💗 Cảm ơn quý khách đã ủng hộ LYLY!
            """
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


        # =============================================
        # TẠO FILE EXCEL
        # =============================================

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


        # =============================================
        # NÚT TẢI EXCEL
        # =============================================

        st.subheader("📥 Xuất hóa đơn")

        st.download_button(
            label="📥 TẢI BILL EXCEL",
            data=df_excel.to_csv(
                index=False
            ).encode("utf-8-sig"),
            file_name=f"Bill_Lyly_{ma_bill}.csv",
            mime="text/csv",
            use_container_width=True
        )
