"""Report generation module"""
from models import MarketAnalysis
from datetime import datetime


class ReportGenerator:
    """Generates formatted market analysis reports"""
    
    def __init__(self):
        pass
    
    def format_report(self, analysis: MarketAnalysis) -> str:
        """Format analysis into a readable report"""
        
        # Check if we have sufficient data
        if not analysis.market_data:
            return "❌ Chưa đủ dữ liệu — đang chờ cập nhật."
        
        # Header
        time_str = analysis.timestamp.strftime("%H:%M:%S %d/%m/%Y")
        report = f"🕒 **{time_str}** — **{analysis.symbol}**\n\n"
        
        # Trend
        report += f"**Xu hướng:** {analysis.trend_emoji} {analysis.trend_description}\n\n"
        
        # Volume
        volume_emoji = "📊" if abs(analysis.volume_change_pct) > 20 else "📈"
        volume_text = f"+{analysis.volume_change_pct:.1f}%" if analysis.volume_change_pct > 0 else f"{analysis.volume_change_pct:.1f}%"
        report += f"**Volume:** {volume_emoji} {volume_text} so với trung bình 7 ngày\n\n"
        
        # Funding rate
        fr_emoji = "⚠️" if analysis.funding_rate_status == "nguy hiểm" else ("⚡" if analysis.funding_rate_status == "cao" else "✅")
        report += f"**Funding rate:** {fr_emoji} {analysis.funding_rate_status}"
        if analysis.market_data.funding_rate:
            report += f" ({analysis.market_data.funding_rate * 100:.4f}%)"
        report += "\n\n"
        
        # Volatility
        vol_emoji = "🔥" if analysis.volatility_status == "mạnh" else ("💨" if analysis.volatility_status == "trung bình" else "😴")
        report += f"**Biến động:** {vol_emoji} {analysis.volatility_status}\n\n"
        
        # Anomalies
        if analysis.anomalies:
            report += "**⚠️ Bất thường phát hiện:**\n"
            for anomaly in analysis.anomalies[:3]:  # Limit to 3 anomalies
                severity_emoji = "🔴" if anomaly.severity == "high" else ("🟡" if anomaly.severity == "medium" else "🟢")
                report += f"  {severity_emoji} {anomaly.description}\n"
            report += "\n"
        
        # Key levels
        if analysis.key_levels:
            report += "**📍 Vùng giá quan trọng:**\n"
            current_price = analysis.market_data.price
            
            if 'resistance' in analysis.key_levels:
                dist_to_res = ((analysis.key_levels['resistance'] - current_price) / current_price) * 100
                report += f"  • Kháng cự: ${analysis.key_levels['resistance']:.2f} (+{dist_to_res:.1f}%)\n"
            
            if 'support' in analysis.key_levels:
                dist_to_sup = ((current_price - analysis.key_levels['support']) / current_price) * 100
                report += f"  • Hỗ trợ: ${analysis.key_levels['support']:.2f} (-{dist_to_sup:.1f}%)\n"
            
            if 'ma_200' in analysis.key_levels:
                report += f"  • MA200: ${analysis.key_levels['ma_200']:.2f}\n"
            
            report += "\n"
        
        # Trading direction
        report += f"**📌 Định hướng giao dịch:**\n"
        report += f"_{analysis.trading_direction}_\n"
        
        return report
    
    def format_compact_report(self, analysis: MarketAnalysis) -> str:
        """Format a compact version of the report"""
        if not analysis.market_data:
            return f"{analysis.symbol}: ❌ Chưa đủ dữ liệu"
        
        time_str = analysis.timestamp.strftime("%H:%M")
        price = analysis.market_data.price
        
        report = f"{analysis.trend_emoji} **{analysis.symbol}** @ ${price:.2f} | "
        report += f"Vol: {analysis.volume_change_pct:+.0f}% | "
        report += f"FR: {analysis.funding_rate_status} | "
        
        if analysis.anomalies:
            report += f"⚠️ {len(analysis.anomalies)} cảnh báo"
        else:
            report += "✅ Bình thường"
        
        return report


def get_report_generator() -> ReportGenerator:
    """Factory function to get ReportGenerator instance"""
    return ReportGenerator()
