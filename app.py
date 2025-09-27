# === CÁC THƯ VIỆN CẦN THIẾT ===
import streamlit as st
import pandas as pd
import numpy as np
import requests
from io import BytesIO
from zipfile import ZipFile
import re
from datetime import datetime, timedelta
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import os
import glob
import zipfile

# === CẤU HÌNH TRANG & GIAO DIỆN ===
st.set_page_config(
    page_title="VnStock Pro - Nền tảng Phân tích Chứng khoán Chuyên nghiệp",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Khởi tạo session state cho giao diện.
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'df' not in st.session_state:
    st.session_state.df = None

def get_theme_colors():
    """Lấy mã màu dựa trên giao diện hiện tại - tối ưu cho nền đen và trắng."""
    if st.session_state.theme == 'light':
        return {
            'background': '#f8fafc',
            'card_bg': '#ffffff',
            'border': '#e2e8f0',
            'text': '#1e293b',
            'text_secondary': '#475569',
            'primary': '#3b82f6',
            'primary_dark': '#1d4ed8',
            'primary_light': '#60a5fa',
            'positive': '#10b981',
            'negative': '#ef4444',
            'neutral': '#374151',
            'gradient': 'linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%)',
            'chart_bg': '#ffffff',
            'grid_color': 'rgba(30, 41, 59, 0.15)',
            'header_bg': 'linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #334d73 100%)',  # Xanh đậm hơn
            'accent1': '#f59e0b',
            'accent2': '#8b5cf6',
            'accent3': '#06b6d4',
            'hologram': 'linear-gradient(45deg, #0f172a, #1e3a5f, #334d73, #10b981)',  # Xanh đậm
            'hologram_text': 'linear-gradient(45deg, #1e3a5f, #334d73)',
            'card_shadow': '0 10px 25px rgba(0, 0, 0, 0.1)',
            'hover_shadow': '0 20px 40px rgba(0, 0, 0, 0.15)',
            'glassmorphism': 'rgba(255, 255, 255, 0.25)',
            'glassmorphism_border': 'rgba(30, 41, 59, 0.2)'
        }
    else:  # Dark theme - nền xanh đậm hơn
        return {
            'background': '#0c1220',  # Xanh đậm hơn
            'card_bg': '#1e293b',
            'border': '#475569',
            'text': '#f8fafc',
            'text_secondary': '#cbd5e1',
            'primary': '#60a5fa',
            'primary_dark': '#3b82f6',
            'primary_light': '#93c5fd',
            'positive': '#22c55e',
            'negative': '#ef4444',
            'neutral': '#94a3b8',
            'gradient': 'linear-gradient(135deg, #0c1220 0%, #1e293b 100%)',  # Xanh đậm hơn
            'chart_bg': '#1e293b',
            'grid_color': 'rgba(203, 213, 225, 0.15)',
            'header_bg': 'linear-gradient(135deg, #0c1220 0%, #1e3a5f 50%, #2d4a73 100%)',  # Xanh đậm hơn
            'accent1': '#fbbf24',
            'accent2': '#a78bfa',
            'accent3': '#22d3ee',
            'hologram': 'linear-gradient(45deg, #0c1220, #1e3a5f, #2d4a73, #22c55e)',  # Xanh đậm hơn
            'hologram_text': 'linear-gradient(45deg, #1e3a5f, #2d4a73)',
            'card_shadow': '0 10px 25px rgba(0, 0, 0, 0.5)',
            'hover_shadow': '0 20px 40px rgba(0, 0, 0, 0.7)',
            'glassmorphism': 'rgba(30, 41, 59, 0.4)',
            'glassmorphism_border': 'rgba(203, 213, 225, 0.2)'
        }

def get_theme_css():
    """Tạo CSS cho giao diện chuyên nghiệp với hiệu ứng hologram và glassmorphism."""
    colors = get_theme_colors()
    return f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', sans-serif;
        background: {colors['background']};
        color: {colors['text']};
        overflow-x: hidden;
    }}
    
    .stApp {{ 
        background: {colors['background']}; 
        background-image: 
            radial-gradient(circle at 10% 20%, rgba(96, 165, 250, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 90% 80%, rgba(167, 139, 250, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 50% 50%, rgba(34, 211, 238, 0.05) 0%, transparent 70%);
        background-attachment: fixed;
    }}
    
    /* Header siêu chuyên nghiệp với hologram effect */
    .header-container {{
        background: {colors['header_bg']};
        height: 90px;
        border-bottom: 3px solid transparent;
        border-image: {colors['hologram']} 1;
        display: flex;
        align-items: center;
        padding: 0 2rem;
        margin-bottom: 1rem;
        box-shadow: {colors['hover_shadow']};
        position: relative;
        overflow: hidden;
        z-index: 10;
    }}
    
    .header-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: {colors['hologram']};
        opacity: 0.1;
        animation: hologramShift 8s ease-in-out infinite;
        z-index: -1;
    }}
    
    .header-container::after {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 600px;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(96, 165, 250, 0.2));
        transform: skewX(-15deg);
        z-index: -1;
    }}
    
    .header-title {{
        color: #ffffff !important;
        font-weight: 900;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 0 0 20px rgba(96, 165, 250, 0.5), 0 0 40px rgba(167, 139, 250, 0.3);
        z-index: 1;
        position: relative;
        display: flex;
        align-items: center;
        background: {colors['hologram_text']};
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .header-title i {{
        margin-right: 1rem;
        font-size: 2.8rem;
        color: #60a5fa;
        animation: iconPulse 3s infinite, iconRotate 8s linear infinite;
        text-shadow: 0 0 20px rgba(96, 165, 250, 0.8);
        -webkit-text-fill-color: #60a5fa;
    }}
    
    @keyframes hologramShift {{
        0%, 100% {{ transform: translateX(-5px) rotate(0deg); }}
        25% {{ transform: translateX(5px) rotate(1deg); }}
        50% {{ transform: translateX(-3px) rotate(-1deg); }}
        75% {{ transform: translateX(3px) rotate(0.5deg); }}
    }}
    
    @keyframes iconPulse {{
        0% {{ transform: scale(1); opacity: 1; }}
        50% {{ transform: scale(1.1); opacity: 0.8; }}
        100% {{ transform: scale(1); opacity: 1; }}
    }}
    
    @keyframes iconRotate {{
        0% {{ filter: hue-rotate(0deg); }}
        100% {{ filter: hue-rotate(360deg); }}
    }}
    
    .header-title::after {{
        content: '';
        position: absolute;
        bottom: -12px;
        left: 0;
        width: 80px;
        height: 4px;
        background: {colors['hologram']};
        border-radius: 2px;
        animation: hologramShift 4s ease-in-out infinite;
    }}
    
    /* Glassmorphism sidebar */
    .css-1d391kg {{
        background: {colors['glassmorphism']} !important;
        backdrop-filter: blur(20px) saturate(180%);
        border-right: 1px solid {colors['glassmorphism_border']};
        border-radius: 0 20px 20px 0;
        padding-top: 1rem;
        box-shadow: {colors['card_shadow']};
    }}
    
    /* Enhanced chart container */
    .chart-container {{
        background: {colors['glassmorphism']};
        backdrop-filter: blur(20px) saturate(180%);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: {colors['hover_shadow']};
        border: 1px solid {colors['glassmorphism_border']};
        margin-bottom: 1rem;
        position: relative;
        overflow: hidden;
    }}
    
    .chart-container::before {{
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: {colors['hologram']};
        animation: hologramShift 6s ease-in-out infinite;
    }}
    
    /* Enhanced buttons */
    .stButton > button {{
        background: {colors['hologram']} !important;
        color: white !important;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 700;
        font-size: 0.95rem;
        transition: all 0.4s ease;
        box-shadow: 0 8px 20px rgba(96, 165, 250, 0.3);
        position: relative;
        overflow: hidden;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }}
    
    .stButton > button::before {{
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
        transition: left 0.5s;
    }}
    
    .stButton > button:hover::before {{
        left: 100%;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 30px rgba(96, 165, 250, 0.4);
    }}
    
    /* Enhanced inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stDateInput > div > div > input {{
        border-radius: 12px;
        border: 2px solid {colors['glassmorphism_border']};
        padding: 1rem;
        background: {colors['glassmorphism']};
        backdrop-filter: blur(10px);
        color: {colors['text']};
        font-weight: 500;
        transition: all 0.3s ease;
    }}
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stDateInput > div > div > input:focus {{
        border-color: {colors['primary']};
        box-shadow: 0 0 20px rgba(96, 165, 250, 0.3);
        transform: scale(1.02);
    }}
    
    /* Enhanced checkboxes */
    .stCheckbox > div {{
        background: {colors['glassmorphism']};
        backdrop-filter: blur(10px);
        border-radius: 10px;
        padding: 0.5rem 1rem;
        border: 1px solid {colors['glassmorphism_border']};
        transition: all 0.3s ease;
    }}
    
    .stCheckbox > div:hover {{
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(96, 165, 250, 0.2);
    }}
    
    .stCheckbox > div > label > div {{
        color: {colors['text']} !important;
        font-weight: 600;
    }}
    
    /* Section headers với độ tương phản cao */
    .section-header {{
        color: {colors['text']} !important;
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        margin: 1.5rem 0 1rem 0;
        padding: 0.5rem 0;
        border-bottom: 3px solid {colors['primary']};
        position: relative;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }}
    
    .section-header::after {{
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 30%;
        height: 2px;
        background: {colors['hologram']};
        animation: hologramShift 4s ease-in-out infinite;
    }}
    
    /* Info cards */
    .info-card {{
        background: {colors['glassmorphism']};
        backdrop-filter: blur(20px);
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid {colors['glassmorphism_border']};
        box-shadow: {colors['card_shadow']};
        transition: all 0.3s ease;
    }}
    
    .info-card:hover {{
        transform: translateY(-5px);
        box-shadow: {colors['hover_shadow']};
    }}
    
    /* Info card headers với độ tương phản cao */
    .info-card h3, .info-card h4 {{
        color: {colors['text']} !important;
        font-weight: 700 !important;
        text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        margin-top: 0 !important;
    }}
    
    .info-card p, .info-card p strong {{
        color: {colors['text']} !important;
        font-weight: 500 !important;
    }}
    
    /* Price indicators */
    .price-positive {{
        color: {colors['positive']} !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(34, 197, 94, 0.3);
    }}
    
    .price-negative {{
        color: {colors['negative']} !important;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(239, 68, 68, 0.3);
    }}
    
    /* Error styling */
    .stError {{
        background: rgba(239, 68, 68, 0.1);
        border: 1px solid {colors['negative']};
        border-radius: 10px;
        padding: 1rem;
        color: {colors['negative']};
        font-weight: 600;
    }}
    
    /* Loading animation */
    .loading {{
        display: inline-block;
        width: 25px;
        height: 25px;
        border: 3px solid rgba(96, 165, 250, 0.3);
        border-radius: 50%;
        border-top-color: {colors['primary']};
        animation: spin 1s linear infinite;
    }}
    
    @keyframes spin {{
        to {{ transform: rotate(360deg); }}
    }}
    
    /* Scrollbar styling */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['card_bg']};
        border-radius: 10px;
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['hologram']};
        border-radius: 10px;
        animation: hologramShift 8s ease-in-out infinite;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['primary']};
    }}
    
    /* Expander styling - Cách tiếp cận mạnh mẽ hơn */
    .streamlit-expander {{
        border: none !important;
        border-radius: 10px !important;
        margin-bottom: 1rem !important;
    }}
    
    .streamlit-expanderHeader {{
        background-color: {colors['card_bg']} !important;
        color: {colors['text']} !important;
        border-radius: 10px !important;
        border: 1px solid {colors['border']} !important;
        padding: 0.75rem 1rem !important;
        font-weight: 600 !important;
    }}
    
    .streamlit-expanderContent {{
        background-color: {colors['card_bg']} !important;
        color: {colors['text']} !important;
        border-radius: 0 0 10px 10px !important;
        border: 1px solid {colors['border']} !important;
        border-top: none !important;
        padding: 1rem !important;
    }}
    
    /* Đảm bảo tất cả văn bản trong expander có màu phù hợp */
    .streamlit-expanderContent *,
    .streamlit-expanderContent h1,
    .streamlit-expanderContent h2,
    .streamlit-expanderContent h3,
    .streamlit-expanderContent h4,
    .streamlit-expanderContent h5,
    .streamlit-expanderContent h6,
    .streamlit-expanderContent p,
    .streamlit-expanderContent li,
    .streamlit-expanderContent span,
    .streamlit-expanderContent strong,
    .streamlit-expanderContent div,
    .streamlit-expanderContent ul,
    .streamlit-expanderContent ol {{
        color: {colors['text']} !important;
    }}
    
    /* Màu cho các bullet points */
    .streamlit-expanderContent ul li::before,
    .streamlit-expanderContent ol li::before {{
        color: {colors['primary']} !important;
    }}
    
    /* Định dạng cho các mục trong danh sách */
    .streamlit-expanderContent li {{
        margin-bottom: 0.5rem !important;
    }}
    
    /* Định dạng cho tiêu đề trong expander */
    .streamlit-expanderContent h3 {{
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        margin-bottom: 1rem !important;
        padding-bottom: 0.5rem !important;
        border-bottom: 2px solid {colors['primary']} !important;
    }}
    
    /* Định dạng cho các đoạn văn bản */
    .streamlit-expanderContent p {{
        margin-bottom: 0.75rem !important;
        line-height: 1.6 !important;
    }}
    
    /* Định dạng cho văn bản in đậm */
    .streamlit-expanderContent strong {{
        font-weight: 700 !important;
    }}
</style>
"""

# Áp dụng CSS tùy chỉnh
st.markdown(get_theme_css(), unsafe_allow_html=True)

# === HÀM XỬ LÍ DỮ LIỆU ===
def get_trading_days(start_date, end_date):
    """Lấy tất cả các ngày giao dịch trong khoảng thời gian đã cho"""
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    trading_days = [d for d in date_range if d.dayofweek < 5]
    
    vietnamese_holidays = [
        '01-01', '02-10', '04-30', '05-01', '09-02',
    ]
    
    trading_days = [d for d in trading_days if d.strftime('%m-%d') not in vietnamese_holidays]
    return pd.DatetimeIndex(trading_days)

def filter_trading_days(df, date_column='date'):
    """Lọc dữ liệu chỉ giữ lại các ngày giao dịch"""
    df[date_column] = pd.to_datetime(df[date_column])
    start_date = df[date_column].min().strftime('%Y-%m-%d')
    end_date = df[date_column].max().strftime('%Y-%m-%d')
    trading_days = get_trading_days(start_date, end_date)
    df = df[df[date_column].isin(trading_days)]
    return df.sort_values(date_column)

def validate_date_range(start_date, end_date):
    """Kiểm tra logic ngày giao dịch"""
    if start_date >= end_date:
        return False, "Ngày bắt đầu phải nhỏ hơn ngày kết thúc!"
    
    if start_date > datetime.now().date():
        return False, "Ngày bắt đầu không thể ở tương lai!"
    
    if (end_date - start_date).days < 1:
        return False, "Khoảng thời gian phải ít nhất 1 ngày!"
    
    # Kiểm tra năm đi ngược
    if start_date.year > end_date.year:
        return False, "Năm bắt đầu không thể lớn hơn năm kết thúc!"
    
    # Bỏ giới hạn 3 năm - cho phép hiển thị tất cả dữ liệu
    
    return True, ""

# === HÀM TẢI DỮ LIỆU TỪ CAFEF ===
def download_data_for_date(target_date, extract_path):
    """Tải dữ liệu cho một ngày cụ thể"""
    date_str_path = target_date.strftime('%Y%m%d')
    date_str_file = target_date.strftime('%d%m%Y')
    
    url = f"https://cafef1.mediacdn.vn/data/ami_data/{date_str_path}/CafeF.SolieuGD.Upto{date_str_file}.zip"
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        # Lưu file zip
        zip_file_path = os.path.join(extract_path, f"{date_str_path}.zip")
        with open(zip_file_path, 'wb') as f:
            f.write(response.content)
        
        # Giải nén
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        
        # Xóa file zip
        os.remove(zip_file_path)
        
        return True
    except requests.exceptions.RequestException:
        # Bỏ qua lỗi và trả về False
        return False
    except Exception as e:
        # Bỏ qua lỗi và trả về False
        return False

@st.cache_data(ttl=3600, show_spinner=False)
def download_latest_data():
    """Tải dữ liệu mới nhất từ CafeF với retry logic."""
    MAX_DAYS_TO_CHECK = 10
    extract_path = "stock_data"

    # Tạo thư mục nếu chưa có
    if not os.path.exists(extract_path):
        os.makedirs(extract_path)
    
    # Xóa các file cũ nếu có
    for file in os.listdir(extract_path):
        file_path = os.path.join(extract_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Vòng lặp tìm ngày có dữ liệu
    for i in range(1, MAX_DAYS_TO_CHECK + 1):
        check_date = datetime.now() - timedelta(days=i)
        
        if download_data_for_date(check_date, extract_path):
            return check_date
    
    return None

def combine_data_files():
    """Đọc các file dữ liệu vừa giải nén, gộp lại và lưu thành file alldata.csv"""
    data_directory = "stock_data"
    file_pattern = os.path.join(data_directory, "*.*")
    file_list = glob.glob(file_pattern)

    if not file_list:
        return False

    all_dataframes = []
    for file_path in file_list:
        # Bỏ qua file zip nếu còn sót lại
        if file_path.endswith('.zip'):
            continue
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            all_dataframes.append(df)
        except Exception:
            # Bỏ qua lỗi và tiếp tục
            continue
    
    if all_dataframes:
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        output_filename = "alldata.csv"
        combined_df.to_csv(output_filename, index=False, encoding='utf-8-sig')
        return True
    
    return False

def get_stock_data(df_total, symbol, start_date, end_date):
    """Lấy dữ liệu cổ phiếu theo symbol và khoảng thời gian"""
    if df_total is None:
        return None
    
    # Lọc theo symbol
    df_filtered = df_total[df_total['<Ticker>'] == symbol.upper()].copy()
    
    if df_filtered.empty:
        return None
    
    # Lọc theo khoảng thời gian
    start_datetime = pd.to_datetime(start_date)
    end_datetime = pd.to_datetime(end_date)
    
    df_filtered = df_filtered[
        (df_filtered['<DTYYYYMMDD>'] >= start_datetime) & 
        (df_filtered['<DTYYYYMMDD>'] <= end_datetime)
    ].copy()
    
    if df_filtered.empty:
        return None
    
    # Chuyển đổi định dạng để tương thích với chart
    df_filtered = df_filtered.rename(columns={
        '<DTYYYYMMDD>': 'date',
        '<Open>': 'open',
        '<High>': 'high',
        '<Low>': 'low',
        '<Close>': 'close',
        '<Volume>': 'volume'
    })
    
    return df_filtered.sort_values('date')

def create_fireant_candlestick(df, title):
    """Tạo biểu đồ nến theo style FireAnt với tính năng zoom/pan nâng cao"""
    colors = get_theme_colors()
    
    # Lọc chỉ các ngày giao dịch
    df = filter_trading_days(df)
    
    # Tạo một bản sao của DataFrame để xử lý
    df_plot = df.copy()
    
    # Chuyển đổi ngày thành chuỗi để sử dụng với category type
    df_plot['date_str'] = df_plot['date'].dt.strftime('%Y-%m-%d')
    
    # Tính toán các đường MA nếu được chọn
    ma_traces = []
    if st.session_state.get('show_ma', False):
        ma_periods = st.session_state.get('ma_periods', [20])
        ma_colors = [colors['accent1'], colors['accent2'], colors['accent3'], colors['primary'], colors['positive'], colors['negative']]
        
        for i, period in enumerate(ma_periods):
            if len(df_plot) >= period:
                df_plot[f'MA{period}'] = df_plot['close'].rolling(window=period).mean()
                ma_traces.append({
                    'period': period,
                    'data': df_plot[f'MA{period}'],
                    'color': ma_colors[i % len(ma_colors)]
                })
    
    # Xác định số hàng cho subplot
    rows = 1
    row_heights = [1.0]
    subplot_titles = [title]
    
    if st.session_state.get('show_volume', True):
        rows += 1
        row_heights = [0.75, 0.25]  # Nến và volume sát nhau hơn
        subplot_titles.append('Khối lượng giao dịch')
    
    if st.session_state.get('show_rsi', False):
        rows += 1
        if len(row_heights) == 1:
            row_heights = [0.6, 0.4]
            subplot_titles.append('RSI (14)')
        else:
            row_heights = [0.5, 0.25, 0.25]  # Giảm khoảng cách hơn nữa
            subplot_titles.append('RSI (14)')
    
    if st.session_state.get('show_macd', False):
        rows += 1
        if len(row_heights) == 1:
            row_heights = [0.6, 0.4]
        elif len(row_heights) == 2:
            row_heights = [0.45, 0.25, 0.3]  # Giảm khoảng cách hơn nữa
        else:
            row_heights = [0.4, 0.2, 0.2, 0.2]  # Giảm khoảng cách hơn nữa
        subplot_titles.append('MACD')
    
    # Tạo subplot với khoảng cách rất nhỏ
    fig = make_subplots(
        rows=rows,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.005,  # Khoảng cách rất nhỏ
        subplot_titles=subplot_titles,
        row_heights=row_heights
    )
    
    # Thêm biểu đồ nến với style FireAnt
    fig.add_trace(
        go.Candlestick(
            x=df_plot['date_str'],
            open=df_plot['open'],
            high=df_plot['high'],
            low=df_plot['low'],
            close=df_plot['close'],
            name="Giá",
            increasing_line_color=colors['positive'],
            decreasing_line_color=colors['negative'],
            increasing_fillcolor=colors['positive'],
            decreasing_fillcolor=colors['negative'],
            line=dict(width=1),
            whiskerwidth=0.8,
            opacity=0.9
        ),
        row=1, col=1
    )
    
    # Thêm các đường MA
    for ma_trace in ma_traces:
        fig.add_trace(
            go.Scatter(
                x=df_plot['date_str'],
                y=ma_trace['data'],
                mode='lines',
                name=f"MA{ma_trace['period']}",
                line=dict(
                    color=ma_trace['color'],
                    width=2,
                    dash='solid'
                ),
                opacity=0.8
            ),
            row=1, col=1
        )
    
    current_row = 2
    
    # Thêm biểu đồ volume nếu được chọn
    if st.session_state.get('show_volume', True):
        volume_colors = [colors['positive'] if close >= open else colors['negative'] 
                        for close, open in zip(df_plot['close'], df_plot['open'])]
        
        fig.add_trace(
            go.Bar(
                x=df_plot['date_str'],
                y=df_plot['volume'],
                name="Khối lượng",
                marker_color=volume_colors,
                opacity=0.7
            ),
            row=current_row, col=1
        )
        current_row += 1
    
    # Thêm RSI nếu được chọn
    if st.session_state.get('show_rsi', False):
        rsi_period = st.session_state.get('rsi_period', 14)
        delta = df_plot['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
        rs = gain / loss
        df_plot['RSI'] = 100 - (100 / (1 + rs))
        
        fig.add_trace(
            go.Scatter(
                x=df_plot['date_str'],
                y=df_plot['RSI'],
                mode='lines',
                name=f"RSI ({rsi_period})",
                line=dict(color=colors['accent3'], width=2)
            ),
            row=current_row, col=1
        )
        
        # Thêm các đường reference cho RSI
        fig.add_hline(y=70, line=dict(color=colors['negative'], width=1, dash="dash"), row=current_row, col=1)
        fig.add_hline(y=30, line=dict(color=colors['positive'], width=1, dash="dash"), row=current_row, col=1)
        fig.add_hline(y=50, line=dict(color=colors['neutral'], width=1, dash="dot"), row=current_row, col=1)
        
        current_row += 1
    
    # Thêm MACD nếu được chọn
    if st.session_state.get('show_macd', False):
        ema_12 = df_plot['close'].ewm(span=12).mean()
        ema_26 = df_plot['close'].ewm(span=26).mean()
        df_plot['MACD'] = ema_12 - ema_26
        df_plot['Signal'] = df_plot['MACD'].ewm(span=9).mean()
        df_plot['Histogram'] = df_plot['MACD'] - df_plot['Signal']
        
        fig.add_trace(
            go.Scatter(
                x=df_plot['date_str'],
                y=df_plot['MACD'],
                mode='lines',
                name="MACD",
                line=dict(color=colors['primary'], width=2)
            ),
            row=current_row, col=1
        )
        
        fig.add_trace(
            go.Scatter(
                x=df_plot['date_str'],
                y=df_plot['Signal'],
                mode='lines',
                name="Signal",
                line=dict(color=colors['accent1'], width=2)
            ),
            row=current_row, col=1
        )
        
        histogram_colors = [colors['positive'] if h >= 0 else colors['negative'] for h in df_plot['Histogram']]
        fig.add_trace(
            go.Bar(
                x=df_plot['date_str'],
                y=df_plot['Histogram'],
                name="Histogram",
                marker_color=histogram_colors,
                opacity=0.6
            ),
            row=current_row, col=1
        )
    
    # Cấu hình layout nâng cao
    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=20, color=colors['text'], family="Inter"),
            x=0.02
        ),
        template="plotly_dark" if st.session_state.theme == 'dark' else "plotly_white",
        height=800 if rows > 2 else 600,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color=colors['text'])
        ),
        margin=dict(l=10, r=10, t=60, b=20),
        paper_bgcolor=colors['chart_bg'],
        plot_bgcolor=colors['chart_bg'],
        font=dict(color=colors['text'], family="Inter"),
        hovermode='x unified',
        dragmode='pan',  # Mặc định là pan (kéo thả)
        showlegend=True
    )
    
    # Tạo danh sách ngày tháng hiển thị thông minh như FireAnt
    def create_smart_ticks(dates):
        """Tạo danh sách ngày tháng hiển thị thông minh như FireAnt"""
        if len(dates) <= 10:
            # Nếu ít hơn 10 ngày, hiển thị tất cả
            return dates, [d.strftime('%d/%m') for d in dates]
        
        # Xác định số ngày cần hiển thị (tối đa 8-10 ngày)
        num_ticks = min(10, max(5, len(dates) // 20))
        
        # Tạo các vị trí tick đều đặn
        tick_indices = np.linspace(0, len(dates) - 1, num_ticks, dtype=int)
        
        # Lấy ngày tại các vị trí tick
        tick_dates = [dates[i] for i in tick_indices]
        
        # Định dạng ngày tháng
        tick_labels = [d.strftime('%d/%m') for d in tick_dates]
        
        # Đảm bảo ngày đầu và ngày cuối luôn được hiển thị
        if 0 not in tick_indices:
            tick_indices = np.append(tick_indices, 0)
            tick_dates = [dates[i] for i in tick_indices]
            tick_labels = [d.strftime('%d/%m') for d in tick_dates]
        
        if len(dates) - 1 not in tick_indices:
            tick_indices = np.append(tick_indices, len(dates) - 1)
            tick_dates = [dates[i] for i in tick_indices]
            tick_labels = [d.strftime('%d/%m') for d in tick_dates]
        
        # Sắp xếp lại các chỉ số
        sorted_indices = np.argsort(tick_indices)
        tick_indices = tick_indices[sorted_indices]
        tick_dates = [tick_dates[i] for i in sorted_indices]
        tick_labels = [tick_labels[i] for i in sorted_indices]
        
        return tick_dates, tick_labels
    
    # Lấy danh sách ngày tháng từ DataFrame
    dates = pd.to_datetime(df_plot['date_str']).tolist()
    
    # Tạo danh sách ngày tháng hiển thị thông minh
    tick_dates, tick_labels = create_smart_ticks(dates)
    
    # Cấu hình trục X và Y cho tất cả các subplot
    for i in range(1, rows + 1):
        # Ẩn ngày tháng ở các subplot trên cùng (nến, RSI, MACD)
        if i < rows:
            fig.update_xaxes(
                gridcolor=colors['grid_color'],
                gridwidth=0.5,
                showspikes=True,
                spikethickness=1,
                spikedash="dot",
                spikecolor=colors['text_secondary'],
                spikemode="across",
                showline=True,
                linewidth=1,
                linecolor=colors['border'],
                # Sử dụng type='category' để loại bỏ khoảng trống
                type='category',
                # Ẩn ngày tháng
                showticklabels=False,
                row=i, col=1
            )
        else:
            # Chỉ hiển thị ngày tháng ở subplot cuối cùng (volume)
            fig.update_xaxes(
                gridcolor=colors['grid_color'],
                gridwidth=0.5,
                showspikes=True,
                spikethickness=1,
                spikedash="dot",
                spikecolor=colors['text_secondary'],
                spikemode="across",
                showline=True,
                linewidth=1,
                linecolor=colors['border'],
                # Sử dụng type='category' để loại bỏ khoảng trống
                type='category',
                # Hiển thị ngày tháng thông minh
                tickmode='array',
                tickvals=[d.strftime('%Y-%m-%d') for d in tick_dates],
                ticktext=tick_labels,
                tickangle=-45,  # Xoay 45 độ để tránh chồng chéo
                tickfont=dict(
                    family="Inter",
                    size=10,
                    color=colors['text_secondary']
                ),
                row=i, col=1
            )
        
        fig.update_yaxes(
            gridcolor=colors['grid_color'],
            gridwidth=0.5,
            showspikes=True,
            spikethickness=1,
            spikedash="dot",
            spikecolor=colors['text_secondary'],
            showline=True,
            linewidth=1,
            linecolor=colors['border'],
            row=i, col=1
        )
    
    # Cấu hình đặc biệt cho RSI
    if st.session_state.get('show_rsi', False):
        rsi_row = 2 if not st.session_state.get('show_volume', True) else 3
        if rsi_row <= rows:
            fig.update_yaxes(range=[0, 100], row=rsi_row, col=1)
    
    # Tắt rangeslider
    fig.update_layout(xaxis_rangeslider_visible=False)
    
    return fig

# === HÀM TỰ ĐỘNG TẢI DỮ LIỆU ===
def auto_load_data():
    """Tự động tải dữ liệu khi khởi động ứng dụng"""
    if not st.session_state.data_loaded:
        data_date = download_latest_data()
        if data_date is not None:
            if combine_data_files():
                filename = "alldata.csv"
                df = pd.read_csv(filename)
                date_column = '<DTYYYYMMDD>'
                df[date_column] = pd.to_datetime(df[date_column], format='%Y%m%d')
                st.session_state.df = df
                st.session_state.data_loaded = True
                st.session_state.data_date = data_date
                # Thông báo nhỏ khi tải thành công
                st.toast(f"✅ Đã tải dữ liệu ({data_date.strftime('%d/%m/%Y')})", icon="✅")
            else:
                st.error("❌ Không thể xử lý dữ liệu.")
        else:
            st.error("❌ Không thể kết nối với CafeF.")

# === GIAO DIỆN ỨNG DỤNG ===
# Header chuyên nghiệp với hologram effect
st.markdown("""
<div class="header-container">
    <div>
        <h1 class="header-title"><i class="fas fa-chart-line"></i> VnStock Pro</h1>
    </div>
</div>
""", unsafe_allow_html=True)

# Khởi tạo session state
if 'show_ma' not in st.session_state:
    st.session_state.show_ma = True
if 'ma_periods' not in st.session_state:
    st.session_state.ma_periods = [20]
if 'show_volume' not in st.session_state:
    st.session_state.show_volume = True
if 'show_rsi' not in st.session_state:
    st.session_state.show_rsi = False
if 'rsi_period' not in st.session_state:
    st.session_state.rsi_period = 14
if 'show_macd' not in st.session_state:
    st.session_state.show_macd = False

# Tự động tải dữ liệu khi khởi động
auto_load_data()

# Sidebar với glassmorphism
with st.sidebar:
    st.markdown("""
    <div class="info-card">
        <h3 style="margin-top: 0; text-align: center;">⚙️ Cấu hình</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Theme toggle với style mới
    theme = st.selectbox(
        "🎨 Chọn giao diện",
        ["🌙 Tối", "☀️ Sáng"],
        index=0 if st.session_state.theme == 'dark' else 1
    )
    st.session_state.theme = 'dark' if "Tối" in theme else 'light'
    
    # Nút làm mới dữ liệu
    if st.button("🔄 Làm mới dữ liệu"):
        st.session_state.data_loaded = False
        st.rerun()
    
    # Hiển thị thông tin dữ liệu
    if st.session_state.data_loaded:
        st.success(f"📅 Dữ liệu từ CafeF: {st.session_state.data_date.strftime('%d/%m/%Y')}")
    
    # Stock selection với gợi ý
    st.markdown('<div class="section-header">📈 Thông tin cổ phiếu</div>', unsafe_allow_html=True)
    
    if st.session_state.data_loaded:
        ticker_list = st.session_state.df['<Ticker>'].unique()
        stock_symbol = st.text_input("Mã chứng khoán", value="FPT", placeholder="VD: FPT, VNM, VIC...")
    else:
        stock_symbol = st.text_input("Mã chứng khoán", value="FPT", placeholder="VD: FPT, VNM, VIC...")
    
    # Date range selection với validation
    st.markdown('<div class="section-header">📅 Khoảng thời gian</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Từ ngày",
            value=datetime.now() - timedelta(days=365),
            max_value=datetime.now().date()
        )
    with col2:
        end_date = st.date_input(
            "Đến ngày", 
            value=datetime.now(),
            max_value=datetime.now().date()
        )
    
    # Validation logic ngày
    is_valid, error_message = validate_date_range(start_date, end_date)
    if not is_valid:
        st.error(f"⚠️ {error_message}")
    
    # Technical indicators section
    st.markdown('<div class="section-header">📊 Chỉ báo kỹ thuật</div>', unsafe_allow_html=True)
    
    # Moving Averages với multiple selection
    st.session_state.show_ma = st.checkbox("📈 Đường trung bình động (MA)", value=st.session_state.show_ma)
    
    if st.session_state.show_ma:
        st.markdown("**Chọn kỳ hạn MA:**", help="Có thể chọn nhiều kỳ hạn cùng lúc")
        
        # Tạo các checkbox cho từng kỳ hạn MA
        ma_options = {
            5: st.checkbox("MA5", value=5 in st.session_state.ma_periods, key="ma5"),
            10: st.checkbox("MA10", value=10 in st.session_state.ma_periods, key="ma10"),
            20: st.checkbox("MA20", value=20 in st.session_state.ma_periods, key="ma20"),
            50: st.checkbox("MA50", value=50 in st.session_state.ma_periods, key="ma50"),
            100: st.checkbox("MA100", value=100 in st.session_state.ma_periods, key="ma100"),
            200: st.checkbox("MA200", value=200 in st.session_state.ma_periods, key="ma200")
        }
        
        # Cập nhật danh sách MA periods
        selected_ma_periods = [period for period, selected in ma_options.items() if selected]
        st.session_state.ma_periods = selected_ma_periods if selected_ma_periods else [20]
    
    # Volume
    st.session_state.show_volume = st.checkbox("📊 Hiển thị khối lượng", value=st.session_state.show_volume)
    
    # RSI
    st.session_state.show_rsi = st.checkbox("📉 Chỉ số RSI", value=st.session_state.show_rsi)
    if st.session_state.show_rsi:
        st.session_state.rsi_period = st.selectbox(
            "Kỳ hạn RSI",
            [9, 14, 21, 25],
            index=1,  # Default to 14
            key="rsi_period_select"
        )
    
    # MACD
    st.session_state.show_macd = st.checkbox("📈 Chỉ số MACD", value=st.session_state.show_macd)

# Main content area
if st.session_state.data_loaded and is_valid:
    # Tạo container cho biểu đồ
    chart_container = st.container()
    
    with chart_container:
        df_total = st.session_state.df
        # SỬ LỖI QUAN TRỌNG: Sử dụng get_stock_data() thay vì generate_sample_data()
        df = get_stock_data(df_total, stock_symbol.upper(), start_date, end_date)
        
        if df is None or df.empty:
            st.error(f"Không tìm thấy dữ liệu cho mã {stock_symbol.upper()} trong khoảng thời gian đã chọn.")
        else:
            # Tạo và hiển thị biểu đồ
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            
            fig = create_fireant_candlestick(df, f"Biểu đồ {stock_symbol.upper()}")
            
            # Cấu hình hiển thị với các tùy chọn zoom/pan nâng cao
            config = {
                'displayModeBar': True,
                'displaylogo': False,
                'modeBarButtonsToRemove': [
                    'select2d', 'lasso2d', 'autoScale2d', 'resetScale2d',
                    'toggleSpikelines', 'hoverClosestCartesian', 'hoverCompareCartesian'
                ],
                'modeBarButtonsToAdd': [
                    'drawline', 'drawopenpath', 'drawclosedpath',
                    'drawcircle', 'drawrect', 'eraseshape'
                ],
                'scrollZoom': True,  # Zoom bằng lăn chuột
                'doubleClick': 'reset',  # Double click để reset zoom
                'showTips': True,
                'responsive': True,
                'toImageButtonOptions': {
                    'format': 'png',
                    'filename': f'{stock_symbol}_chart',
                    'height': 800,
                    'width': 1200,
                    'scale': 1
                }
            }
            
            st.plotly_chart(fig, use_container_width=True, config=config)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Advanced Analytics Dashboard
            if not df.empty:
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    high_52w = df['high'].max()
                    low_52w = df['low'].min()
                    st.markdown(f"""
                    <div class="info-card">
                        <h4 style="margin: 0 0 0.5rem 0;">📈 Biên độ giá</h4>
                        <p><strong>Cao nhất:</strong> {high_52w:.2f}</p>
                        <p><strong>Thấp nhất:</strong> {low_52w:.2f}</p>
                        <p><strong>Biên độ:</strong> {((high_52w - low_52w) / low_52w * 100):.1f}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    avg_volume = df['volume'].mean()
                    total_volume = df['volume'].sum()
                    st.markdown(f"""
                    <div class="info-card">
                        <h4 style="margin: 0 0 0.5rem 0;">📊 Thống kê khối lượng</h4>
                        <p><strong>TB mỗi ngày:</strong> {avg_volume:,.0f}</p>
                        <p><strong>Tổng khối lượng:</strong> {total_volume:,.0f}</p>
                        <p><strong>Xu hướng:</strong> {'📈' if df['volume'].iloc[-1] > avg_volume else '📉'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    volatility = df['close'].pct_change().std() * 100
                    trend = "Tăng" if df['close'].iloc[-1] > df['close'].iloc[0] else "Giảm"
                    st.markdown(f"""
                    <div class="info-card">
                        <h4 style="margin: 0 0 0.5rem 0;">⚡ Phân tích xu hướng</h4>
                        <p><strong>Xu hướng:</strong> {trend} {'📈' if trend == 'Tăng' else '📉'}</p>
                        <p><strong>Độ biến động:</strong> {volatility:.2f}%</p>
                        <p><strong>Đánh giá:</strong> {'Cao' if volatility > 3 else 'Trung bình' if volatility > 1.5 else 'Thấp'}</p>
                    </div>
                    """, unsafe_allow_html=True)
            
            # Hiển thị dữ liệu gốc
            with st.expander("📋 Dữ liệu gốc"):
                st.dataframe(df, use_container_width=True)
            
            # Hướng dẫn sử dụng - Cách tiếp cận mới
            with st.expander("🔧 Hướng dẫn sử dụng biểu đồ"):
                colors = get_theme_colors()
                st.markdown(f"""
                <div style="color: {colors['text']};">
                <h3 style="color: {colors['text']}; font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid {colors['primary']};">Các thao tác trên biểu đồ:</h3>
                
                <ul style="color: {colors['text']}; margin-bottom: 1rem;">
                    <li style="color: {colors['text']}; margin-bottom: 0.5rem;"><strong style="color: {colors['text']};">🖱️ Lăn chuột</strong>: Zoom in/out biểu đồ</li>
                    <li style="color: {colors['text']}; margin-bottom: 0.5rem;"><strong style="color: {colors['text']};">✋ Kéo thả</strong>: Di chuyển biểu đồ theo chiều ngang</li>
                    <li style="color: {colors['text']}; margin-bottom: 0.5rem;"><strong style="color: {colors['text']};">🖱️ Double click</strong>: Reset về view mặc định</li>
                    <li style="color: {colors['text']}; margin-bottom: 0.5rem;"><strong style="color: {colors['text']};">📱 Hover</strong>: Xem thông tin chi tiết tại điểm đó</li>
                    <li style="color: {colors['text']}; margin-bottom: 0.5rem;"><strong style="color: {colors['text']};">🔧 Toolbar</strong>: Sử dụng các công cụ vẽ và phân tích</li>
                </ul>
                
                <h3 style="color: {colors['text']}; font-size: 1.25rem; font-weight: 700; margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 2px solid {colors['primary']};">Chỉ báo kỹ thuật:</h3>
                
                <ul style="color: {colors['text']}; margin-bottom: 1rem;">
                    <li style="color: {colors['text']}; margin-bottom: 0.5rem;"><strong style="color: {colors['text']};">MA (Moving Average)</strong>: Đường trung bình động, có thể chọn nhiều kỳ hạn</li>
                    <li style="color: {colors['text']}; margin-bottom: 0.5rem;"><strong style="color: {colors['text']};">RSI</strong>: Chỉ số sức mạnh tương đối (30-70 là vùng bình thường)</li>
                    <li style="color: {colors['text']}; margin-bottom: 0.5rem;"><strong style="color: {colors['text']};">MACD</strong>: Hội tụ phân kỳ trung bình động</li>
                    <li style="color: {colors['text']}; margin-bottom: 0.5rem;"><strong style="color: {colors['text']};">Volume</strong>: Khối lượng giao dịch (màu xanh = tăng, đỏ = giảm)</li>
                </ul>
                </div>
                """, unsafe_allow_html=True)
elif not st.session_state.data_loaded:
    st.info("Đang tải dữ liệu...")
elif not is_valid:
    st.error("Vui lòng kiểm tra lại khoảng thời gian đã chọn.")

# Footer
st.markdown("""
---
<div style="text-align: center; padding: 1rem; color: #64748b;">
    <p>📊 <strong>VnStock Pro</strong> - Nền tảng Phân tích Chứng khoán Chuyên nghiệp</p>
    <p style="font-size: 0.8em;">Dữ liệu được cập nhật từ CafeF • Dành cho mục đích tham khảo</p>
</div>
""", unsafe_allow_html=True)