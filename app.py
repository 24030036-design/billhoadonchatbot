import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
st.image("hinhanhcuaquan.png")
# =========================
# CẤU HÌNH APP
# =========================
st.set_page_config(
    page_title="Trà Sữa - Tính Bill",
    page_icon="🧋",
    layout="centered"
)

st.title("🧋 QUÁN TRÀ SỮA")
st.subheader("📋 Tính tiền và xuất hóa đơn")

# =========================
# MENU
# =========================
menu = {
    "Trà sữa truyền thống": 30000,
    "Trà sữa matcha": 35000,
    "Trà sữa socola": 35000,
    "Trà sữa khoai môn": 35000,
    "Trà sữa dâu": 35000,
    "Trà sữa thái xanh": 30000,
    "Trà sữa thái đỏ": 30000
}

topping_menu = {
    "Không topping": 0,
    "Trân châu đen": 5000,
    "Trân châu trắng": 5000,
    "Thạch phô mai": 7000,
    "Pudding trứng": 7000,
    "Thạch trái cây": 5000,
    "Kem cheese": 10000
}

# =========================
# NHẬP THÔNG TIN
# =========================
ten_khach = st.text_input(
    "👤 Tên khách hàng",
    placeholder="Nhập tên khách hàng..."
)

st.divider()

loai_tra = st.selectbox(
    "🧋 Chọn loại trà sữa",
    list(menu.keys())
)

so_luong = st.number_input(
    "🔢 Số lượng",
    min_value=1,
    max_value=50,
    value=1,
    step=1
)

topping = st.multiselect(
    "🍡 Chọn topping",
    list(topping_menu.keys())
)

duong = st.radio(
    "🍬 Mức độ đường",
    ["100%", "70%", "50%", "0%"],
    horizontal=True
)

da = st.radio(
    "🧊 Mức độ đá",
    ["Ít đá", "Nhiều đá", "Không đá"],
    horizontal=True
)

# =========================
# TÍNH TIỀN
# =========================
gia_tra = menu[loai_tra]

gia_topping = 0

for tp in topping:
    gia_topping += topping_menu[tp]

don_gia = gia_tra + gia_topping
thanh_tien = don_gia * so_luong

# =========================
# HIỂN THỊ ĐƠN HÀNG
# =========================
st.divider()
st.subheader("🛒 THÔNG TIN ĐƠN HÀNG")

col1, col2 = st.columns(2)

with col1:
    st.write("👤 **Khách hàng:**", ten_khach if ten_khach else "Chưa nhập")
    st.write("🧋 **Trà sữa:**", loai_tra)
    st.write("🔢 **Số lượng:**", so_luong)

with col2:
    st.write("🍬 **Đường:**", duong)
    st.write("🧊 **Đá:**", da)

if topping:
    st.write("🍡 **Topping:**", ", ".join(topping))
else:
    st.write("🍡 **Topping:** Không topping")

st.info(
    f"💰 Đơn giá: **{don_gia:,} VNĐ**\n\n"
    f"💵 Tổng tiền: **{thanh_tien:,} VNĐ**"
)

# =========================
# NÚT THANH TOÁN
# =========================
if st.button("💳 THANH TOÁN", use_container_width=True):

    if ten_khach.strip() == "":
        st.warning("⚠️ Vui lòng nhập tên khách hàng!")
        st.stop()

    # Mã hóa đơn
    ma_bill = datetime.now().strftime("%Y%m%d%H%M%S")

    # Thời gian thanh toán
    thoi_gian = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # =========================
    # HIỂN THỊ BILL
    # =========================
    st.success("✅ Thanh toán thành công!")

    st.divider()

    st.subheader("🧾 HÓA ĐƠN")

    st.write(f"**Mã hóa đơn:** {ma_bill}")
    st.write(f"**Thời gian:** {thoi_gian}")
    st.write(f"**Khách hàng:** {ten_khach}")

    st.write("---")

    st.write(f"🧋 **Loại trà sữa:** {loai_tra}")
    st.write(f"🔢 **Số lượng:** {so_luong}")

    if topping:
        st.write(f"🍡 **Topping:** {', '.join(topping)}")
    else:
        st.write("🍡 **Topping:** Không topping")

    st.write(f"🍬 **Đường:** {duong}")
    st.write(f"🧊 **Đá:** {da}")

    st.write("---")

    st.markdown(
        f"""
        ### 💰 TỔNG THANH TOÁN: {thanh_tien:,} VNĐ
        """
    )

    # =========================
    # TẠO DỮ LIỆU EXCEL
    # =========================

    topping_excel = ", ".join(topping) if topping else "Không topping"

    data = {
        "Mã hóa đơn": [ma_bill],
        "Thời gian": [thoi_gian],
        "Tên khách hàng": [ten_khach],
        "Loại trà sữa": [loai_tra],
        "Số lượng": [so_luong],
        "Topping": [topping_excel],
        "Mức đường": [duong],
        "Mức đá": [da],
        "Đơn giá": [don_gia],
        "Tổng tiền": [thanh_tien]
    }

    df = pd.DataFrame(data)

    # =========================
    # XUẤT EXCEL
    # =========================

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(
            writer,
            index=False,
            sheet_name="Hóa đơn"
        )

        worksheet = writer.sheets["Hóa đơn"]

        # Chỉnh độ rộng cột
        for column in worksheet.columns:
            max_length = 0
            column_letter = column[0].column_letter

            for cell in column:
                try:
                    if len(str(cell.value)) > max_length:
                        max_length = len(str(cell.value))
                except:
                    pass

            worksheet.column_dimensions[column_letter].width = max_length + 3

    excel_data = output.getvalue()

    # =========================
    # NÚT DOWNLOAD EXCEL
    # =========================

    st.download_button(
        label="📥 TẢI BILL EXCEL",
        data=excel_data,
        file_name=f"Bill_{ma_bill}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )
