# 📊 Crypto Market Analysis Agent

Agent Phân tích Thị trường Crypto sử dụng **LangGraph** và giao diện **Streamlit** - Thu thập dữ liệu, phân tích thị trường theo thời gian thực, và tạo ra báo cáo ngắn gọn, dễ hiểu với tính định hướng giao dịch.

## 🌟 Tính năng

### 1️⃣ Thu thập dữ liệu
- ✅ Giá và volume từ Binance/CCXT
- ✅ Open Interest (OI)
- ✅ Funding Rate
- ✅ Liquidation Map
- ✅ Market Sentiment (có thể mở rộng)
- ✅ Whale Wallet Activity (có thể mở rộng)

### 2️⃣ Phân tích thị trường
- 📈 Xu hướng (MA20/50/200)
- 📊 So sánh volume hiện tại với trung bình 7 ngày
- 💨 Trạng thái biến động (thấp / trung bình / mạnh)
- ⚠️ Funding rate cực đoan → squeeze risk
- 🔄 Divergence giữa Spot và Futures

### 3️⃣ Phát hiện bất thường
- 🚨 Spike bất thường ở OI hoặc volume
- 🐋 Cá voi chuyển coin lên sàn (có thể mở rộng)
- 💥 Dump/Pump không theo giá trị thực
- ⚡ Liquidation cluster bị chạm hoặc bị đe dọa

### 4️⃣ Sinh báo cáo
Báo cáo theo format chuẩn:
- 🕒 Thời gian và cặp coin
- 📈/📉 Xu hướng với mô tả ngắn
- 📊 Volume % chênh lệch
- ⚡ Funding rate status
- ⚠️ Ghi chú bất thường
- 📍 Vùng giá quan trọng
- 📌 Định hướng giao dịch (không có lệnh BUY/SELL trực tiếp)

## 🚀 Cài đặt

### Yêu cầu
- Python 3.8+
- pip hoặc conda

### Bước 1: Clone repository
```bash
git clone <repository-url>
cd workspace
```

### Bước 2: Tạo virtual environment (khuyến nghị)
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate  # Windows
```

### Bước 3: Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Bước 4: Cấu hình (Tùy chọn)
Sao chép file `.env.example` thành `.env` và cấu hình:
```bash
cp .env.example .env
```

Chỉnh sửa file `.env`:
```env
# Binance API (Tùy chọn - cho endpoints cần xác thực)
BINANCE_API_KEY=your_key_here
BINANCE_API_SECRET=your_secret_here

# OpenAI API (Tùy chọn - cho tính năng nâng cao)
OPENAI_API_KEY=your_openai_key_here
```

**Lưu ý:** Ứng dụng có thể chạy mà không cần API keys, sử dụng public endpoints của Binance.

## 📱 Sử dụng

### Chạy ứng dụng Streamlit
```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: `http://localhost:8501`

### Giao diện chính

1. **Sidebar - Cấu hình:**
   - Chọn các cặp coin để phân tích
   - Bật/tắt tự động cập nhật
   - Điều chỉnh khoảng thời gian refresh

2. **Main Panel:**
   - Nút **"Phân tích ngay"**: Chạy phân tích cho các cặp coin đã chọn
   - Nút **"Xóa báo cáo"**: Xóa tất cả báo cáo hiện tại
   - Nút **"Làm mới"**: Refresh giao diện

3. **Tabs hiển thị:**
   - **Báo cáo chi tiết**: Hiển thị phân tích đầy đủ cho từng coin
   - **Tổng quan**: Hiển thị bảng tóm tắt trạng thái

## 🏗️ Kiến trúc

### Cấu trúc project
```
workspace/
├── app.py                  # Streamlit UI
├── agent.py                # LangGraph Agent chính
├── data_collector.py       # Module thu thập dữ liệu
├── market_analyzer.py      # Module phân tích thị trường
├── report_generator.py     # Module tạo báo cáo
├── models.py              # Data models
├── config.py              # Configuration
├── requirements.txt       # Dependencies
├── .env.example          # Environment variables template
└── README.md             # Documentation
```

### LangGraph Workflow

```
┌─────────────────┐
│  Collect Data   │  ← Thu thập dữ liệu từ API
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Analyze Market  │  ← Phân tích xu hướng, anomalies
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Generate Report │  ← Tạo báo cáo định dạng
└─────────────────┘
```

## 🔧 Cấu hình nâng cao

### Chỉnh sửa `config.py`

```python
# Các cặp coin mặc định
DEFAULT_SYMBOLS = ["BTC/USDT", "ETH/USDT", "BNB/USDT", "SOL/USDT"]

# Các tham số phân tích
MA_PERIODS = [20, 50, 200]  # Các chu kỳ MA
VOLUME_LOOKBACK = 7  # Số ngày tính trung bình volume
FUNDING_RATE_THRESHOLD = 0.01  # 1% - ngưỡng funding rate
OI_SPIKE_THRESHOLD = 0.15  # 15% - ngưỡng spike OI
VOLUME_SPIKE_THRESHOLD = 0.30  # 30% - ngưỡng spike volume

# Khoảng thời gian refresh (giây)
REFRESH_INTERVAL = 60

# Timeframe nến
TIMEFRAME = "1h"  # 1 giờ
```

## 📊 Ví dụ báo cáo

```
🕒 14:30:15 22/11/2024 — BTC/USDT

Xu hướng: 📈 Xu hướng tăng mạnh, giá trên các MA chính

Volume: 📊 +35.2% so với trung bình 7 ngày

Funding rate: ⚡ cao (0.0152%)

Biến động: 💨 trung bình

⚠️ Bất thường phát hiện:
  🟡 Volume tăng đột biến 35.2% so với trung bình

📍 Vùng giá quan trọng:
  • Kháng cự: $38,500.00 (+2.1%)
  • Hỗ trợ: $36,800.00 (-2.4%)
  • MA200: $35,200.00

📌 Định hướng giao dịch:
_Momentum tăng đang mạnh_
```

## ⚠️ Lưu ý quan trọng

1. **Không phải tư vấn tài chính:**
   - Ứng dụng chỉ cung cấp thông tin phân tích
   - Không đưa ra lệnh BUY/SELL trực tiếp
   - Người dùng tự chịu trách nhiệm về quyết định giao dịch

2. **Rate Limits:**
   - Binance API có giới hạn số requests
   - Tránh refresh quá nhanh (khuyến nghị >= 30 giây)

3. **Dữ liệu:**
   - Sử dụng public endpoints, có thể thiếu một số dữ liệu
   - API keys giúp truy cập đầy đủ hơn (nhưng không bắt buộc)

## 🔮 Mở rộng tương lai

- [ ] Tích hợp sentiment analysis từ Twitter/Reddit
- [ ] Theo dõi ví cá voi real-time
- [ ] Thêm các chỉ báo kỹ thuật (RSI, MACD, Bollinger Bands)
- [ ] Cảnh báo qua Telegram/Discord
- [ ] Export báo cáo PDF
- [ ] Backtesting với dữ liệu lịch sử
- [ ] Machine Learning predictions
- [ ] Multi-exchange support

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng:
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Tạo Pull Request

## 📝 License

Dự án này được phân phối dưới MIT License.

## 📧 Liên hệ

Nếu có câu hỏi hoặc góp ý, vui lòng tạo issue trên GitHub.

---

**Disclaimer:** Ứng dụng này chỉ phục vụ mục đích giáo dục và nghiên cứu. Không phải là tư vấn tài chính. Luôn DYOR (Do Your Own Research) trước khi giao dịch.
