import streamlit as st
st.image("logo.jpg")
from decimal import Decimal, ROUND_HALF_UP

# =========================
# CẤU HÌNH TRANG
# =========================
st.set_page_config(
    page_title="Tính lãi tiền gửi tiết kiệm",
    page_icon="💰",
    layout="centered"
)

st.title("💰 Công cụ tính tiền gửi tiết kiệm ngân hàng_NGUYEN TRAN QUYNH TRANG")
st.write("Nhập thông tin khoản tiền gửi để tính tiền lãi và tổng số tiền nhận được.")

# =========================
# HÀM ĐỊNH DẠNG TIỀN
# =========================
def format_money(value):
    value = Decimal(str(value)).quantize(
        Decimal("1"),
        rounding=ROUND_HALF_UP
    )
    return f"{int(value):,}".replace(",", ".") + " VNĐ"


# =========================
# NHẬP THÔNG TIN
# =========================
st.subheader("📋 Thông tin tiền gửi")

so_tien = st.number_input(
    "Số tiền gửi (VNĐ)",
    min_value=0.0,
    value=100_000_000.0,
    step=1_000_000.0,
    format="%.0f",
    help="Nhập số tiền bạn muốn gửi tiết kiệm."
)

ky_han = st.selectbox(
    "Kỳ hạn",
    options=[1, 3, 6, 9, 12, 18, 24, 36],
    format_func=lambda x: f"{x} tháng"
)

lai_suat = st.number_input(
    "Lãi suất (%/năm)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    format="%.2f",
    help="Nhập lãi suất ngân hàng công bố theo năm."
)

hinh_thuc = st.selectbox(
    "Hình thức nhận lãi",
    [
        "Cuối kỳ",
        "Hàng tháng",
        "Hàng quý"
    ]
)

# =========================
# TÍNH TOÁN
# =========================
if st.button("🧮 Tính lãi", type="primary", use_container_width=True):

    if so_tien <= 0:
        st.error("Vui lòng nhập số tiền gửi lớn hơn 0.")
        st.stop()

    if lai_suat < 0:
        st.error("Lãi suất không được nhỏ hơn 0%.")
        st.stop()

    # Lãi suất dạng thập phân
    lai_suat_nam = lai_suat / 100

    # Số tháng trong kỳ hạn
    so_thang = ky_han

    # Tổng tiền lãi:
    # Tiền lãi = Tiền gốc × Lãi suất năm × Số tháng / 12
    tong_tien_lai = so_tien * lai_suat_nam * so_thang / 12

    # =========================
    # TÍNH LÃI ĐỊNH KỲ
    # =========================

    if hinh_thuc == "Cuối kỳ":
        so_ky_nhan_lai = 1
        lai_dinh_ky = tong_tien_lai
        don_vi_ky = "cuối kỳ"

    elif hinh_thuc == "Hàng tháng":
        so_ky_nhan_lai = so_thang
        lai_dinh_ky = tong_tien_lai / so_thang
        don_vi_ky = "tháng"

    else:  # Hàng quý
        so_ky_nhan_lai = so_thang // 3
        lai_dinh_ky = tong_tien_lai / so_ky_nhan_lai
        don_vi_ky = "quý"

    # Tổng tiền gốc + lãi
    tong_tien_nhan = so_tien + tong_tien_lai

    # =========================
    # HIỂN THỊ KẾT QUẢ
    # =========================
    st.divider()
    st.subheader("📊 Kết quả tính toán")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Tiền lãi định kỳ",
            format_money(lai_dinh_ky)
        )

    with col2:
        st.metric(
            "Tổng tiền lãi",
            format_money(tong_tien_lai)
        )

    col3, col4 = st.columns(2)

    with col3:
        st.metric(
            "Tiền gốc",
            format_money(so_tien)
        )

    with col4:
        st.metric(
            "Tổng gốc + lãi",
            format_money(tong_tien_nhan)
        )

    # =========================
    # CHI TIẾT KHOẢN GỬI
    # =========================
    st.divider()
    st.subheader("📝 Chi tiết")

    st.write(f"**Số tiền gửi:** {format_money(so_tien)}")
    st.write(f"**Kỳ hạn:** {ky_han} tháng")
    st.write(f"**Lãi suất:** {lai_suat:.2f}%/năm")
    st.write(f"**Hình thức nhận lãi:** {hinh_thuc}")

    if hinh_thuc == "Cuối kỳ":
        st.info(
            f"Bạn nhận toàn bộ tiền lãi vào cuối kỳ: "
            f"**{format_money(tong_tien_lai)}**."
        )

    elif hinh_thuc == "Hàng tháng":
        st.info(
            f"Mỗi tháng bạn nhận khoảng "
            f"**{format_money(lai_dinh_ky)}** tiền lãi."
        )

    elif hinh_thuc == "Hàng quý":
        st.info(
            f"Mỗi quý bạn nhận khoảng "
            f"**{format_money(lai_dinh_ky)}** tiền lãi."
        )

    # =========================
    # BẢNG LÃI ĐỊNH KỲ
    # =========================
    if hinh_thuc != "Cuối kỳ":

        st.subheader("📅 Lịch nhận lãi")

        if hinh_thuc == "Hàng tháng":
            so_ky = so_thang
            ten_ky = "Tháng"
        else:
            so_ky = so_thang // 3
            ten_ky = "Quý"

        for i in range(1, so_ky + 1):
            st.write(
                f"**{ten_ky} {i}:** {format_money(lai_dinh_ky)}"
            )

# =========================
# GHI CHÚ
# =========================
st.divider()

with st.expander("ℹ️ Lưu ý về cách tính"):
    st.write(
        """
        - Công cụ sử dụng công thức lãi đơn: **Tiền lãi = Tiền gốc × Lãi suất năm × Kỳ hạn / 12**.
        - Lãi suất được hiểu là lãi suất **%/năm**.
        - Hình thức "Cuối kỳ": toàn bộ tiền lãi được nhận khi đáo hạn.
        - Hình thức "Hàng tháng": tổng tiền lãi được chia đều cho số tháng gửi.
        - Hình thức "Hàng quý": tổng tiền lãi được chia đều cho số quý trong kỳ hạn.
        - Kết quả mang tính tham khảo. Số tiền thực tế có thể khác tùy theo quy định
          của từng ngân hàng, phương pháp tính ngày thực tế, ngày gửi/rút tiền,
          thuế hoặc các điều kiện của sản phẩm tiền gửi.
        """
    )
