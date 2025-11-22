"""LangGraph agent for crypto market analysis"""
from typing import TypedDict, Annotated, Optional
from langgraph.graph import StateGraph, END
import asyncio
from models import MarketData, MarketAnalysis
from data_collector import get_data_collector
from market_analyzer import get_market_analyzer
from report_generator import get_report_generator


# Define state as TypedDict for LangGraph
class GraphState(TypedDict):
    """State dictionary for LangGraph"""
    symbol: str
    raw_data: Optional[MarketData]
    analysis: Optional[MarketAnalysis]
    report: str
    error: Optional[str]


class CryptoAnalysisAgent:
    """Main agent orchestrating the analysis workflow"""
    
    def __init__(self):
        self.data_collector = get_data_collector()
        self.market_analyzer = get_market_analyzer()
        self.report_generator = get_report_generator()
        self.graph = self._build_graph()
    
    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow"""
        
        # Define the workflow graph
        workflow = StateGraph(GraphState)
        
        # Add nodes
        workflow.add_node("collect_data", self.collect_data_node)
        workflow.add_node("analyze_market", self.analyze_market_node)
        workflow.add_node("generate_report", self.generate_report_node)
        
        # Define edges
        workflow.set_entry_point("collect_data")
        workflow.add_edge("collect_data", "analyze_market")
        workflow.add_edge("analyze_market", "generate_report")
        workflow.add_edge("generate_report", END)
        
        return workflow.compile()
    
    def collect_data_node(self, state: GraphState) -> GraphState:
        """Node: Collect market data"""
        try:
            print(f"📊 Collecting data for {state['symbol']}...")
            
            # Run async data collection in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            market_data = loop.run_until_complete(
                self.data_collector.collect_market_data(state['symbol'])
            )
            loop.close()
            
            state['raw_data'] = market_data
            print(f"✅ Data collected for {state['symbol']}")
            
        except Exception as e:
            print(f"❌ Error collecting data: {e}")
            state['error'] = f"Lỗi thu thập dữ liệu: {str(e)}"
        
        return state
    
    def analyze_market_node(self, state: GraphState) -> GraphState:
        """Node: Analyze market data"""
        try:
            if state.get('error') or not state.get('raw_data'):
                return state
            
            print(f"🔍 Analyzing market for {state['symbol']}...")
            
            analysis = self.market_analyzer.analyze_market(state['raw_data'])
            state['analysis'] = analysis
            
            print(f"✅ Analysis completed for {state['symbol']}")
            
        except Exception as e:
            print(f"❌ Error analyzing market: {e}")
            state['error'] = f"Lỗi phân tích: {str(e)}"
        
        return state
    
    def generate_report_node(self, state: GraphState) -> GraphState:
        """Node: Generate analysis report"""
        try:
            if state.get('error'):
                state['report'] = f"❌ {state['error']}\n\nChưa đủ dữ liệu — đang chờ cập nhật."
                return state
            
            if not state.get('analysis'):
                state['report'] = "❌ Chưa có phân tích.\n\nChưa đủ dữ liệu — đang chờ cập nhật."
                return state
            
            print(f"📝 Generating report for {state['symbol']}...")
            
            report = self.report_generator.format_report(state['analysis'])
            state['report'] = report
            
            print(f"✅ Report generated for {state['symbol']}")
            
        except Exception as e:
            print(f"❌ Error generating report: {e}")
            state['report'] = f"❌ Lỗi tạo báo cáo: {str(e)}\n\nChưa đủ dữ liệu — đang chờ cập nhật."
        
        return state
    
    def analyze_symbol(self, symbol: str) -> str:
        """Run complete analysis for a symbol"""
        try:
            # Create initial state as dict
            initial_state: GraphState = {
                'symbol': symbol,
                'raw_data': None,
                'analysis': None,
                'report': '',
                'error': None
            }
            
            # Run the graph
            final_state = self.graph.invoke(initial_state)
            
            return final_state['report']
            
        except Exception as e:
            print(f"❌ Error in agent workflow: {e}")
            return f"❌ Lỗi: {str(e)}\n\nChưa đủ dữ liệu — đang chờ cập nhật."
    
    def analyze_multiple_symbols(self, symbols: list) -> dict:
        """Run analysis for multiple symbols"""
        results = {}
        
        for symbol in symbols:
            print(f"\n{'='*60}")
            print(f"Analyzing {symbol}...")
            print('='*60)
            
            try:
                report = self.analyze_symbol(symbol)
                results[symbol] = report
            except Exception as e:
                results[symbol] = f"❌ Lỗi: {str(e)}\n\nChưa đủ dữ liệu — đang chờ cập nhật."
        
        return results


def get_agent() -> CryptoAnalysisAgent:
    """Factory function to get agent instance"""
    return CryptoAnalysisAgent()
