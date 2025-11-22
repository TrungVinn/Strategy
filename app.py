"""Streamlit app for Crypto Market Analysis Agent"""
import streamlit as st
import time
from datetime import datetime
import config
from agent import get_agent
import pandas as pd


# Page configuration
st.set_page_config(
    page_title="Crypto Market Analysis Agent",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .report-container {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 5px solid #1f77b4;
    }
    .status-running {
        color: #ff9800;
        font-weight: bold;
    }
    .status-success {
        color: #4caf50;
        font-weight: bold;
    }
    .status-error {
        color: #f44336;
        font-weight: bold;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        border-radius: 0.5rem;
        padding: 0.5rem 1rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #1565c0;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables"""
    if 'agent' not in st.session_state:
        st.session_state.agent = None
    if 'reports' not in st.session_state:
        st.session_state.reports = {}
    if 'last_update' not in st.session_state:
        st.session_state.last_update = None
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = False
    if 'selected_symbols' not in st.session_state:
        st.session_state.selected_symbols = config.DEFAULT_SYMBOLS


def load_agent():
    """Load the agent instance"""
    if st.session_state.agent is None:
        with st.spinner("🚀 Đang khởi tạo Agent..."):
            try:
                st.session_state.agent = get_agent()
                st.success("✅ Agent đã sẵn sàng!")
            except Exception as e:
                st.error(f"❌ Lỗi khởi tạo Agent: {str(e)}")
                st.session_state.agent = None


def analyze_markets(symbols):
    """Analyze selected markets"""
    if st.session_state.agent is None:
        st.error("❌ Agent chưa được khởi tạo. Vui lòng khởi động lại ứng dụng.")
        return
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, symbol in enumerate(symbols):
        status_text.text(f"📊 Đang phân tích {symbol}... ({idx + 1}/{len(symbols)})")
        
        try:
            report = st.session_state.agent.analyze_symbol(symbol)
            st.session_state.reports[symbol] = {
                'report': report,
                'timestamp': datetime.now()
            }
        except Exception as e:
            st.session_state.reports[symbol] = {
                'report': f"❌ Lỗi: {str(e)}\n\nChưa đủ dữ liệu — đang chờ cập nhật.",
                'timestamp': datetime.now()
            }
        
        progress_bar.progress((idx + 1) / len(symbols))
    
    status_text.text("✅ Hoàn thành phân tích!")
    st.session_state.last_update = datetime.now()
    time.sleep(1)
    progress_bar.empty()
    status_text.empty()


def main():
    """Main application"""
    initialize_session_state()
    
    # Header
    st.markdown('<div class="main-header">📊 Crypto Market Analysis Agent</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Phân tích thị trường crypto theo thời gian thực với LangGraph</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Cấu hình")
        
        # Symbol selection
        st.subheader("Chọn cặp coin")
        available_symbols = [
            "BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT",
            "XRP/USDT", "ADA/USDT", "DOGE/USDT", "MATIC/USDT",
            "DOT/USDT", "AVAX/USDT", "LINK/USDT", "UNI/USDT"
        ]
        
        st.session_state.selected_symbols = st.multiselect(
            "Chọn các cặp coin để phân tích:",
            options=available_symbols,
            default=st.session_state.selected_symbols
        )
        
        st.divider()
        
        # Refresh interval
        st.subheader("Tự động cập nhật")
        auto_refresh = st.checkbox("Bật tự động cập nhật", value=st.session_state.auto_refresh)
        st.session_state.auto_refresh = auto_refresh
        
        if auto_refresh:
            refresh_interval = st.slider(
                "Khoảng thời gian (giây):",
                min_value=30,
                max_value=300,
                value=60,
                step=30
            )
        
        st.divider()
        
        # Agent info
        st.subheader("ℹ️ Thông tin")
        if st.session_state.last_update:
            st.write(f"**Cập nhật lần cuối:**")
            st.write(st.session_state.last_update.strftime("%H:%M:%S %d/%m/%Y"))
        
        st.write(f"**Số coin đang theo dõi:**")
        st.write(len(st.session_state.selected_symbols))
        
        st.divider()
        
        # About
        with st.expander("📖 Về ứng dụng"):
            st.markdown("""
            **Crypto Market Analysis Agent** sử dụng:
            - 🤖 **LangGraph** cho workflow phân tích
            - 📊 **CCXT & Binance API** cho dữ liệu
            - 🎨 **Streamlit** cho giao diện
            
            **Chức năng:**
            - Thu thập dữ liệu real-time
            - Phân tích xu hướng và volume
            - Phát hiện bất thường
            - Cảnh báo funding rate
            - Gợi ý định hướng giao dịch
            """)
    
    # Main content
    if not st.session_state.selected_symbols:
        st.warning("⚠️ Vui lòng chọn ít nhất một cặp coin để phân tích.")
        return
    
    # Initialize agent
    load_agent()
    
    if st.session_state.agent is None:
        st.error("❌ Không thể khởi tạo Agent. Vui lòng kiểm tra cấu hình và thử lại.")
        return
    
    # Control buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        if st.button("🔄 Phân tích ngay", use_container_width=True):
            analyze_markets(st.session_state.selected_symbols)
    
    with col2:
        if st.button("🗑️ Xóa báo cáo", use_container_width=True):
            st.session_state.reports = {}
            st.session_state.last_update = None
            st.rerun()
    
    with col3:
        if st.button("🔃 Làm mới", use_container_width=True):
            st.rerun()
    
    st.divider()
    
    # Display reports
    if st.session_state.reports:
        # Create tabs for different views
        tab1, tab2 = st.tabs(["📊 Báo cáo chi tiết", "📋 Tổng quan"])
        
        with tab1:
            # Detailed reports
            for symbol in st.session_state.selected_symbols:
                if symbol in st.session_state.reports:
                    report_data = st.session_state.reports[symbol]
                    
                    with st.container():
                        st.markdown(f'<div class="report-container">', unsafe_allow_html=True)
                        st.markdown(report_data['report'])
                        
                        # Timestamp
                        timestamp = report_data['timestamp'].strftime("%H:%M:%S %d/%m/%Y")
                        st.caption(f"_Cập nhật lúc: {timestamp}_")
                        st.markdown('</div>', unsafe_allow_html=True)
        
        with tab2:
            # Summary view
            summary_data = []
            
            for symbol in st.session_state.selected_symbols:
                if symbol in st.session_state.reports:
                    report_data = st.session_state.reports[symbol]
                    
                    # Extract key info (simplified)
                    summary_data.append({
                        'Cặp coin': symbol,
                        'Thời gian': report_data['timestamp'].strftime("%H:%M:%S"),
                        'Trạng thái': '✅ Đã phân tích'
                    })
            
            if summary_data:
                df = pd.DataFrame(summary_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ Chưa có báo cáo. Nhấn nút **Phân tích ngay** để bắt đầu.")
    
    # Auto-refresh logic
    if st.session_state.auto_refresh and st.session_state.reports:
        time.sleep(refresh_interval)
        st.rerun()


if __name__ == "__main__":
    main()
