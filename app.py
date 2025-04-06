import os
import sys
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime
import json
import plotly.express as px
from typing import List, Dict, Any, Optional
import random

# Create necessary directories
os.makedirs('data/charts', exist_ok=True)
os.makedirs('data/news', exist_ok=True)
os.makedirs('data/recommendations', exist_ok=True)

class FinancialPlatform:
    """Financial Intelligence Analysis Platform - Optimized Version"""
    
    def __init__(self):
        """Initialize the platform"""
        # Set theme colors
        self.theme = {
            'primary': '#1E88E5',    # Primary (blue)
            'secondary': '#26A69A',  # Secondary (teal)
            'accent': '#FF8F00',     # Accent (orange)
            'warning': '#E53935',    # Warning (red)
            'success': '#43A047',    # Success (green)
            'background': '#F5F5F5', # Background (light gray)
            'text': '#212121',       # Text (dark gray)
            'text_secondary': '#757575', # Secondary text (mid gray)
            'border': '#BDBDBD',     # Border (gray)
            'chart_colors': ['#1E88E5', '#26A69A', '#FF8F00', '#E53935', '#43A047', 
                            '#7E57C2', '#D81B60', '#FFC107', '#5D4037', '#00ACC1']
        }
        
        # Sample stock data
        self.default_stocks = [
            'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 
            'TSLA', 'NVDA', 'JPM', 'V', 'PG'
        ]
        
        # Cache for stock data
        self.stock_data = {}
        
    def generate_css(self) -> str:
        """Generate CSS styles
        
        Returns:
            CSS style string
        """
        css = f"""
        <style>
            /* Global styles */
            body {{
                font-family: 'Arial', sans-serif;
                color: {self.theme['text']};
                background-color: {self.theme['background']};
            }}
            
            /* Header styles */
            h1, h2, h3, h4, h5, h6 {{
                color: {self.theme['primary']};
                font-weight: bold;
            }}
            
            /* Card styles */
            .card {{
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }}
            
            /* Primary button */
            .button-primary {{
                background-color: {self.theme['primary']};
                color: white;
                border: none;
                border-radius: 4px;
                padding: 10px 20px;
                font-weight: bold;
                cursor: pointer;
                transition: background-color 0.3s;
            }}
            .button-primary:hover {{
                background-color: #1976D2;
            }}
            
            /* Stock styles */
            .stock-up {{
                color: {self.theme['warning']};
                font-weight: bold;
            }}
            .stock-down {{
                color: {self.theme['success']};
                font-weight: bold;
            }}
            
            /* Stock card */
            .stock-card {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px;
                border: 1px solid {self.theme['border']};
                border-radius: 8px;
                margin-bottom: 10px;
                transition: transform 0.3s;
            }}
            .stock-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            }}
            .stock-info {{
                flex: 1;
            }}
            .stock-name {{
                font-weight: bold;
                font-size: 18px;
            }}
            .stock-price {{
                font-size: 24px;
                font-weight: bold;
                margin-left: 20px;
            }}
            
            /* News card */
            .news-card {{
                padding: 15px;
                border: 1px solid {self.theme['border']};
                border-radius: 8px;
                margin-bottom: 15px;
                transition: transform 0.3s;
            }}
            .news-card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            }}
            .news-title {{
                font-weight: bold;
                font-size: 18px;
                margin-bottom: 10px;
            }}
            .news-meta {{
                color: {self.theme['text_secondary']};
                font-size: 14px;
                margin-bottom: 10px;
            }}
            
            /* Stat card */
            .stat-card {{
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                text-align: center;
            }}
            .stat-value {{
                font-size: 36px;
                font-weight: bold;
                margin-bottom: 10px;
            }}
            .stat-label {{
                color: {self.theme['text_secondary']};
                font-size: 14px;
            }}
            
            /* Hot topic */
            .hot-topic {{
                display: inline-block;
                padding: 8px 16px;
                margin: 5px;
                background-color: {self.theme['primary']};
                color: white;
                border-radius: 20px;
                font-weight: bold;
                cursor: pointer;
                transition: transform 0.3s;
            }}
            .hot-topic:hover {{
                transform: scale(1.1);
            }}
            
            /* Footer */
            .footer {{
                text-align: center;
                margin-top: 50px;
                padding-top: 20px;
                border-top: 1px solid #eee;
                font-size: 0.8em;
                color: #666;
            }}
        </style>
        """
        
        return css
    
    def fetch_stock_data(self, symbol: str, period: str = '1y', interval: str = '1d') -> pd.DataFrame:
        """Generate simulated stock data
        
        Args:
            symbol: Stock symbol
            period: Data period
            interval: Data interval
            
        Returns:
            Stock data DataFrame
        """
        cache_key = f"{symbol}_{period}_{interval}"
        if cache_key in self.stock_data:
            return self.stock_data[cache_key]
            
        # Generate simulated data
        dates = pd.date_range(end=datetime.datetime.now(), periods=252, freq='B')
        np.random.seed(hash(symbol) % 10000)
        
        # Generate random price trend
        close = np.random.randn(len(dates)).cumsum() + 100
        # Ensure positive prices
        close = np.maximum(close, 1)
        
        # Generate other price data
        high = close * (1 + 0.02 * np.random.rand(len(dates)))
        low = close * (1 - 0.02 * np.random.rand(len(dates)))
        open_price = low + np.random.rand(len(dates)) * (high - low)
        volume = np.random.randint(100000, 10000000, size=len(dates))
        
        df = pd.DataFrame({
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        }, index=dates)
        
        # Store in cache
        self.stock_data[cache_key] = df
        
        return df
    
    def calculate_technical_indicators(self, df: pd.DataFrame) -> Dict[str, np.ndarray]:
        """Calculate technical indicators
        
        Args:
            df: Stock data DataFrame
            
        Returns:
            Dictionary of technical indicators
        """
        # Calculate moving averages
        ma5 = df['close'].rolling(window=5).mean()
        ma20 = df['close'].rolling(window=20).mean()
        ma60 = df['close'].rolling(window=60).mean()
        
        # Calculate MACD
        ema12 = df['close'].ewm(span=12, adjust=False).mean()
        ema26 = df['close'].ewm(span=26, adjust=False).mean()
        macd = ema12 - ema26
        signal = macd.ewm(span=9, adjust=False).mean()
        histogram = macd - signal
        
        # Calculate RSI
        delta = df['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=14).mean()
        avg_loss = loss.rolling(window=14).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        
        # Store indicators
        indicators = {
            'ma5': ma5,
            'ma20': ma20,
            'ma60': ma60,
            'macd': macd,
            'macd_signal': signal,
            'macd_histogram': histogram,
            'rsi': rsi
        }
        
        return indicators
    
    def plot_stock_chart(self, symbol: str) -> str:
        """Plot stock chart
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Path to saved chart image
        """
        # Get stock data
        df = self.fetch_stock_data(symbol)
        
        # Calculate indicators
        indicators = self.calculate_technical_indicators(df)
        
        # Create figure
        fig, axes = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]})
        
        # Plot price
        axes[0].plot(df.index, df['close'], label='Close Price')
        axes[0].plot(df.index, indicators['ma5'], label='MA5', alpha=0.7)
        axes[0].plot(df.index, indicators['ma20'], label='MA20', alpha=0.7)
        
        # Set chart properties
        axes[0].set_title(f"{symbol} Stock Chart")
        axes[0].set_ylabel("Price")
        axes[0].legend()
        axes[0].grid(True)
        
        # Plot MACD
        axes[1].plot(df.index, indicators['macd'], label='MACD')
        axes[1].plot(df.index, indicators['macd_signal'], label='Signal')
        axes[1].bar(df.index, indicators['macd_histogram'], label='Histogram', alpha=0.5)
        
        axes[1].set_xlabel("Date")
        axes[1].set_ylabel("MACD")
        axes[1].legend()
        axes[1].grid(True)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save chart
        chart_file = f"data/charts/{symbol}_chart_{datetime.datetime.now().strftime('%Y%m%d')}.png"
        plt.savefig(chart_file)
        plt.close()
        
        return chart_file
    
    def recommend_stocks(self, n: int = 5) -> List[Dict[str, Any]]:
        """Generate stock recommendations
        
        Args:
            n: Number of recommendations
            
        Returns:
            List of stock recommendations
        """
        recommendations = []
        
        for symbol in self.default_stocks[:n]:
            # Get stock data
            df = self.fetch_stock_data(symbol)
            
            # Latest price
            latest_price = df['close'].iloc[-1]
            prev_price = df['close'].iloc[-2]
            change_percent = (latest_price - prev_price) / prev_price * 100
            
            # Generate recommendation
            recommendation = {
                'symbol': symbol,
                'name': self.get_company_name(symbol),
                'current_price': latest_price,
                'change_percent': change_percent,
                'volume': int(df['volume'].iloc[-1]),
                'win_rate': random.uniform(65, 95),
                'potential_upside': random.uniform(5, 20),
                'recommendation_reason': self.generate_recommendation_reason(),
                'industry': random.choice(['Technology', 'Finance', 'Healthcare', 'Consumer', 'Energy'])
            }
            
            recommendations.append(recommendation)
        
        # Sort by win rate
        recommendations.sort(key=lambda x: x['win_rate'], reverse=True)
        
        return recommendations
    
    def get_company_name(self, symbol: str) -> str:
        """Get company name for symbol
        
        Args:
            symbol: Stock symbol
            
        Returns:
            Company name
        """
        companies = {
            'AAPL': 'Apple Inc.',
            'MSFT': 'Microsoft Corporation',
            'AMZN': 'Amazon.com, Inc.',
            'GOOGL': 'Alphabet Inc.',
            'META': 'Meta Platforms, Inc.',
            'TSLA': 'Tesla, Inc.',
            'NVDA': 'NVIDIA Corporation',
            'JPM': 'JPMorgan Chase & Co.',
            'V': 'Visa Inc.',
            'PG': 'Procter & Gamble Co.'
        }
        
        return companies.get(symbol, f"{symbol} Inc.")
    
    def generate_recommendation_reason(self) -> str:
        """Generate recommendation reason
        
        Returns:
            Recommendation reason
        """
        reasons = [
            "Strong technical breakout with increasing volume",
            "Positive earnings momentum and analyst upgrades",
            "Attractive valuation with strong growth prospects",
            "Recent dip presents buying opportunity",
            "Industry leader with competitive advantage",
            "New product launches expected to drive growth",
            "Technical indicators show potential reversal",
            "Strong support level with high win rate",
            "Consistent revenue growth with expanding margins",
            "Positive sector trends and favorable position"
        ]
        
        return random.choice(reasons)
    
    def generate_financial_news(self, count: int = 5) -> List[Dict[str, Any]]:
        """Generate simulated financial news
        
        Args:
            count: Number of news items
            
        Returns:
            List of news items
        """
        news_list = []
        
        # News title templates
        title_templates = [
            "{}股市{}：{}板块领涨，{}概念受关注",
            "央行{}政策出台，{}市场{}反应",
            "{}季度GDP增长{}%，经济{}预期",
            "{}公司发布{}财报，净利润同比{}{}%",
            "{}指数{}点，{}板块{}表现"
        ]
        
        # Placeholder variables
        directions = ["上涨", "下跌", "震荡", "反弹", "回调", "走强", "走弱"]
        sectors = ["科技", "金融", "医药", "消费", "新能源", "半导体", "人工智能"]
        concepts = ["ChatGPT", "AIGC", "光伏", "储能", "氢能", "碳中和"]
        companies = ["阿里巴巴", "腾讯", "百度", "京东", "美团", "拼多多", "比亚迪"]
        indices = ["上证指数", "深证成指", "创业板指", "科创50", "沪深300"]
        
        # Sources
        sources = ["东方财富网", "新浪财经", "华尔街见闻", "财联社", "证券时报"]
        
        # Generate news
        for i in range(count):
            # Generate title
            title_template = random.choice(title_templates)
            title = title_template.format(
                random.choice(["今日", "昨日", "本周", "本月", "Q1", "Q2", "Q3", "Q4"]),
                random.choice(directions),
                random.choice(sectors),
                random.choice(concepts)
            )
            
            # Generate content (simplified for demo)
            content = f"This is simulated financial news content for: {title}"
            
            # Generate date (recent date)
            days_ago = random.randint(0, 5)
            date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).strftime("%Y-%m-%d %H:%M")
            
            # Generate news item
            news_item = {
                'title': title,
                'content': content,
                'date': date,
                'source': random.choice(sources),
                'keywords': random.sample(sectors + concepts + companies, 3)
            }
            
            news_list.append(news_item)
        
        # Sort by date (newest first)
        news_list.sort(key=lambda x: x['date'], reverse=True)
        
        return news_list
    
    def analyze_hot_topics(self, news_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Analyze hot topics from news
        
        Args:
            news_data: News data
            
        Returns:
            List of hot topics
        """
        # Extract keywords
        all_keywords = []
        for news in news_data:
            all_keywords.extend(news.get('keywords', []))
        
        # Count keywords
        keyword_counts = {}
        for keyword in all_keywords:
            if keyword in keyword_counts:
                keyword_counts[keyword] += 1
            else:
                keyword_counts[keyword] = 1
        
        # Create hot topics
        hot_topics = []
        for keyword, count in sorted(keyword_counts.items(), key=lambda x: x[1], reverse=True):
            # Find related news
            related_news = []
            for news in news_data:
                if keyword in news.get('keywords', []):
                    related_news.append({
                        'title': news['title'],
                        'date': news['date'],
                        'source': news['source']
                    })
            
            hot_topics.append({
                'keyword': keyword,
                'count': count,
                'related_news': related_news[:3]  # Max 3 related news
            })
        
        return hot_topics
    
    def generate_market_overview(self) -> Dict[str, Any]:
        """Generate market overview
        
        Returns:
            Market overview data
        """
        # Main indices
        indices = {
            '^GSPC': {'name': 'S&P 500'},
            '^DJI': {'name': 'Dow Jones'},
            '^IXIC': {'name': 'NASDAQ'},
            '000001.SS': {'name': 'Shanghai Composite'},
            '399001.SZ': {'name': 'Shenzhen Component'}
        }
        
        # Sectors
        sectors = [
            {'name': 'Technology', 'change': random.uniform(-2, 5)},
            {'name': 'Finance', 'change': random.uniform(-2, 3)},
            {'name': 'Healthcare', 'change': random.uniform(-1, 4)},
            {'name': 'Consumer', 'change': random.uniform(-2, 3)},
            {'name': 'Energy', 'change': random.uniform(-3, 3)},
            {'name': 'Materials', 'change': random.uniform(-2, 2)},
            {'name': 'Real Estate', 'change': random.uniform(-3, 2)}
        ]
        
        # Generate index changes
        index_changes = {}
        market_trend = "震荡"
        total_pct = 0
        
        for symbol, info in indices.items():
            change_pct = random.uniform(-2, 2.5)
            total_pct += change_pct
            
            index_changes[symbol] = {
                'name': info['name'],
                'latest_close': random.randint(2000, 35000) if 'Dow' in info['name'] else random.randint(1000, 5000),
                'change_pct': change_pct,
                'direction': 'up' if change_pct > 0 else 'down'
            }
        
        # Determine market trend
        avg_change = total_pct / len(indices)
        if avg_change > 1:
            market_trend = "上涨"
        elif avg_change > 0.3:
            market_trend = "小幅上涨"
        elif avg_change > -0.3:
            market_trend = "震荡"
        elif avg_change > -1:
            market_trend = "小幅下跌"
        else:
            market_trend = "下跌"
        
        # Sort sectors
        sorted_sectors = sorted(sectors, key=lambda x: x['change'], reverse=True)
        
        return {
            'date': datetime.datetime.now().strftime('%Y-%m-%d'),
            'market_trend': market_trend,
            'index_changes': index_changes,
            'sectors': sorted_sectors,
            'top_sectors': [s['name'] for s in sorted_sectors[:3]],
            'bottom_sectors': [s['name'] for s in sorted_sectors[-3:]]
        }
    
    def create_streamlit_app(self):
        """Create Streamlit application"""
        # Page config
        st.set_page_config(
            page_title="Financial Intelligence Platform",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Inject CSS
        st.markdown(self.generate_css(), unsafe_allow_html=True)
        
        # Create header
        col1, col2 = st.columns([1, 6])
        with col1:
            # Logo placeholder
            st.image("https://via.placeholder.com/100x100.png?text=FIP", width=100)
        with col2:
            st.title("Financial Intelligence Platform")
            st.markdown("AI-powered stock analysis, market news, and intelligent advisory")
        
        # Create sidebar navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio(
            "Select Function",
            ["Home", "Stock Recommendations", "Chart Analysis", "Market News", "Smart Advisor"]
        )
        
        # Display page content
        if page == "Home":
            self.render_home_page()
        elif page == "Stock Recommendations":
            self.render_stock_recommendation_page()
        elif page == "Chart Analysis":
            self.render_chart_analysis_page()
        elif page == "Market News":
            self.render_news_page()
        elif page == "Smart Advisor":
            self.render_advisor_page()
        
        # Add footer
        st.markdown("""
        <div class="footer">
            <p>© 2023 Financial Intelligence Platform | All Rights Reserved</p>
            <p>Disclaimer: This platform provides information for reference only and does not constitute investment advice. Investment involves risks.</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_home_page(self):
        """Render home page"""
        # Welcome message
        st.header("Welcome to Financial Intelligence Platform")
        st.markdown("""
        <div class="card">
            <h3>Platform Highlights</h3>
            <p>Financial Intelligence Platform integrates various advanced AI technologies to provide comprehensive financial market analysis and investment decision support.</p>
            <ul>
                <li>Stock recommendation system based on historical trends</li>
                <li>Intelligent chart analysis and technical pattern recognition</li>
                <li>Real-time hot news and market review</li>
                <li>Personalized smart advisory service</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        # Market overview
        st.subheader("Today's Market Overview")
        
        # Get market data
        market_data = self.generate_market_overview()
        
        # Display main indices
        col1, col2, col3 = st.columns(3)
        
        index_map = {
            '^GSPC': {'name': 'S&P 500', 'col': col1},
            '^DJI': {'name': 'Dow Jones', 'col': col1},
            '000001.SS': {'name': 'Shanghai Composite', 'col': col2},
            '399001.SZ': {'name': 'Shenzhen Component', 'col': col2},
            '^IXIC': {'name': 'NASDAQ', 'col': col3}
        }
        
        for symbol, info in index_map.items():
            if symbol in market_data['index_changes']:
                index_data = market_data['index_changes'][symbol]
                direction_class = 'stock-up' if index_data['direction'] == 'up' else 'stock-down'
                change_sign = '+' if index_data['direction'] == 'up' else ''
                
                with info['col']:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">{info['name']}</div>
                        <div class="stat-value">{index_data['latest_close']:.2f}</div>
                        <div class="{direction_class}">{change_sign}{index_data['change_pct']:.2f}%</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Sector performance
        st.subheader("Sector Performance")
        
        # Create bar chart
        sector_names = [s['name'] for s in market_data['sectors']]
        sector_changes = [s['change'] for s in market_data['sectors']]
        
        fig = px.bar(
            x=sector_changes, 
            y=sector_names, 
            orientation='h',
            labels={"x": "Change (%)", "y": "Sector"},
            title="Sector Performance",
            color=sector_changes,
            color_continuous_scale=["red", "green"],
            range_color=[-max(abs(min(sector_changes)), abs(max(sector_changes))), max(abs(min(sector_changes)), abs(max(sector_changes)))]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Hot topics
        st.subheader("Today's Hot Topics")
        
        # Generate news
        news_data = self.generate_financial_news(10)
        
        # Analyze hot topics
        hot_topics = self.analyze_hot_topics(news_data)
        
        # Display hot topics
        hot_topics_html = '<div style="margin-bottom: 20px;">'
        for topic in hot_topics[:8]:
            size = min(24, max(16, 16 + topic['count']))
            hot_topics_html += f'<span class="hot-topic" style="font-size: {size}px;">{topic["keyword"]} ({topic["count"]})</span>'
        hot_topics_html += '</div>'
        
        st.markdown(hot_topics_html, unsafe_allow_html=True)
        
        # Stock recommendations
        st.subheader("Today's Stock Recommendations")
        
        # Get stock recommendations
        recommended_stocks = self.recommend_stocks(3)
        
        # Display recommendations
        for stock in recommended_stocks:
            direction_class = 'stock-up' if stock['change_percent'] > 0 else 'stock-down'
            change_sign = '+' if stock['change_percent'] > 0 else ''
            
            st.markdown(f"""
            <div class="stock-card">
                <div class="stock-info">
                    <div class="stock-name">{stock['name']} ({stock['symbol']})</div>
                    <div>Recommendation: {stock['recommendation_reason']}</div>
                    <div>Win Rate: {stock['win_rate']:.2f}%</div>
                </div>
                <div>
                    <div class="stock-price">{stock['current_price']:.2f}</div>
                    <div class="{direction_class}">{change_sign}{stock['change_percent']:.2f}%</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Latest news
        st.subheader("Latest Financial News")
        
        # Display news
        for news in news_data[:3]:
            st.markdown(f"""
            <div class="news-card">
                <div class="news-title">{news['title']}</div>
                <div class="news-meta">{news['source']} | {news['date']}</div>
            </div>
            """, unsafe_allow_html=True)
    
    def render_stock_recommendation_page(self):
        """Render stock recommendation page"""
        st.header("Stock Recommendation System")
        st.markdown("""
        <div class="card">
            <p>Based on historical trends and technical indicators, we recommend stocks with high win rates. The system considers multiple factors including price trends, volume, technical indicators, and market sentiment.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        with col1:
            market = st.selectbox("Select Market", ["All", "US Stocks", "China A-Shares", "Hong Kong"])
        with col2:
            industry = st.selectbox("Select Industry", ["All", "Technology", "Finance", "Healthcare", "Consumer", "Energy"])
        with col3:
            sort_by = st.selectbox("Sort By", ["Win Rate", "Potential Upside", "Latest Price", "Volume"])
        
        # Get recommendations
        recommended_stocks = self.recommend_stocks(10)
        
        # Sort stocks
        if sort_by == "Win Rate":
            recommended_stocks.sort(key=lambda x: x['win_rate'], reverse=True)
        elif sort_by == "Potential Upside":
            recommended_stocks.sort(key=lambda x: x['potential_upside'], reverse=True)
        elif sort_by == "Latest Price":
            recommended_stocks.sort(key=lambda x: x['current_price'], reverse=True)
        elif sort_by == "Volume":
            recommended_stocks.sort(key=lambda x: x['volume'], reverse=True)
        
        # Display recommendations
        st.subheader(f"Recommended Stocks (Total: {len(recommended_stocks)})")
        
        # Create table
        table_html = """
        <table>
            <tr>
                <th>Stock</th>
                <th>Symbol</th>
                <th>Price</th>
                <th>Change</th>
                <th>Win Rate</th>
                <th>Potential</th>
                <th>Recommendation</th>
            </tr>
        """
        
        for stock in recommended_stocks:
            direction_class = 'stock-up' if stock['change_percent'] > 0 else 'stock-down'
            change_sign = '+' if stock['change_percent'] > 0 else ''
            
            table_html += f"""
            <tr>
                <td>{stock['name']}</td>
                <td>{stock['symbol']}</td>
                <td>{stock['current_price']:.2f}</td>
                <td class="{direction_class}">{change_sign}{stock['change_percent']:.2f}%</td>
                <td>{stock['win_rate']:.2f}%</td>
                <td>{stock['potential_upside']:.2f}%</td>
                <td>{stock['recommendation_reason']}</td>
            </tr>
            """
        
        table_html += "</table>"
        st.markdown(table_html, unsafe_allow_html=True)
        
        # Stock details
        st.subheader("Stock Detailed Analysis")
        selected_stock = st.selectbox("Select stock to view detailed analysis", 
                                     [f"{stock['name']} ({stock['symbol']})" for stock in recommended_stocks])
        
        if selected_stock:
            # Extract symbol
            symbol = selected_stock.split('(')[1].split(')')[0]
            
            # Find selected stock
            stock_detail = None
            for stock in recommended_stocks:
                if stock['symbol'] == symbol:
                    stock_detail = stock
                    break
            
            if stock_detail:
                # Display stock details
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Display stock chart
                    st.markdown("### Stock Chart")
                    chart_img = self.plot_stock_chart(symbol)
                    if chart_img:
                        st.image(chart_img)
                
                with col2:
                    # Display stock info
                    st.markdown("### Stock Information")
                    st.markdown(f"""
                    <div class="card">
                        <p><strong>Stock Name:</strong> {stock_detail['name']}</p>
                        <p><strong>Symbol:</strong> {stock_detail['symbol']}</p>
                        <p><strong>Current Price:</strong> {stock_detail['current_price']:.2f}</p>
                        <p><strong>Change:</strong> <span class="{direction_class}">{change_sign}{stock_detail['change_percent']:.2f}%</span></p>
                        <p><strong>Volume:</strong> {stock_detail['volume']:,}</p>
                        <p><strong>Industry:</strong> {stock_detail.get('industry', 'N/A')}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Display recommendation indicators
                    st.markdown("### Recommendation Indicators")
                    st.markdown(f"""
                    <div class="card">
                        <p><strong>Win Rate:</strong> {stock_detail['win_rate']:.2f}%</p>
                        <p><strong>Potential Upside:</strong> {stock_detail['potential_upside']:.2f}%</p>
                        <p><strong>Recommendation:</strong> {stock_detail['recommendation_reason']}</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    def render_chart_analysis_page(self):
        """Render chart analysis page"""
        st.header("Chart Analysis System")
        st.markdown("""
        <div class="card">
            <p>The intelligent chart analysis system can automatically identify key technical patterns, support/resistance levels, and trend lines to help you better understand market trends and make investment decisions.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Stock selection
        col1, col2 = st.columns([3, 1])
        with col1:
            stock_input = st.text_input("Enter stock symbol or name", "AAPL")
        with col2:
            time_frame = st.selectbox("Select time frame", ["Daily", "Weekly", "Monthly"])
        
        # Analysis button
        analyze_button = st.button("Analyze Chart")
        
        if analyze_button or stock_input:
            # For demo, always use the entered symbol
            symbol = stock_input
            
            # Display stock information
            st.subheader(f"{self.get_company_name(symbol)} ({symbol}) Chart Analysis")
            
            # Display chart
            st.markdown("### Technical Pattern Recognition")
            chart_img = self.plot_stock_chart(symbol)
            if chart_img:
                st.image(chart_img)
            
            # Get stock data
            df = self.fetch_stock_data(symbol)
            
            # Calculate indicators
            indicators = self.calculate_technical_indicators(df)
            
            # Display analysis results
            st.subheader("Analysis Results")
            
            # Technical patterns (simulated)
            st.markdown("### Identified Technical Patterns")
            
            # Generate random patterns
            patterns = [
                {"name": "Double Bottom", "confidence": random.uniform(0.7, 0.95), "signal": "Bullish"},
                {"name": "Rising Wedge", "confidence": random.uniform(0.6, 0.9), "signal": "Bearish"},
                {"name": "MACD Crossover", "confidence": random.uniform(0.75, 0.95), "signal": "Bullish"}
            ]
            
            for pattern in patterns:
                confidence = pattern['confidence'] * 100
                confidence_class = 'tag-success' if confidence >= 70 else 'tag-warning'
                
                st.markdown(f"""
                <div class="card">
                    <h4>{pattern['name']}</h4>
                    <p><strong>Signal Type:</strong> {pattern['signal']}</p>
                    <p><strong>Confidence:</strong> <span class="{confidence_class}">{confidence:.1f}%</span></p>
                </div>
                """, unsafe_allow_html=True)
            
            # Support and resistance (simulated)
            st.markdown("### Support and Resistance Levels")
            
            latest_price = df['close'].iloc[-1]
            
            # Generate support levels
            supports = [
                {"price": latest_price * 0.9, "strength": 0.85},
                {"price": latest_price * 0.85, "strength": 0.75}
            ]
            
            # Generate resistance levels
            resistances = [
                {"price": latest_price * 1.1, "strength": 0.8},
                {"price": latest_price * 1.15, "strength": 0.7}
            ]
            
            # Display support levels
            st.markdown("#### Support Levels")
            for level in supports:
                st.markdown(f"- Price: {level['price']:.2f}, Strength: {level['strength']:.2f}")
            
            # Display resistance levels
            st.markdown("#### Resistance Levels")
            for level in resistances:
                st.markdown(f"- Price: {level['price']:.2f}, Strength: {level['strength']:.2f}")
            
            # Comprehensive analysis
            st.subheader("Comprehensive Analysis")
            
            # Generate analysis
            short_term = random.choice(["Bullish", "Bearish", "Neutral"])
            medium_term = random.choice(["Bullish", "Bearish", "Neutral"])
            long_term = random.choice(["Bullish", "Bearish", "Neutral"])
            
            st.markdown(f"""
            <div class="card">
                <h4>Market State: {random.choice(["Trending", "Ranging", "Consolidating"])}</h4>
                <p><strong>Short-term Trend:</strong> {short_term}</p>
                <p><strong>Medium-term Trend:</strong> {medium_term}</p>
                <p><strong>Long-term Trend:</strong> {long_term}</p>
                <p><strong>Volatility:</strong> {random.choice(["Low", "Medium", "High"])}</p>
                <p><strong>Volume Analysis:</strong> {random.choice(["Increasing", "Decreasing", "Stable"])}</p>
                <p><strong>Key Price Levels:</strong> Support at {latest_price * 0.9:.2f}, Resistance at {latest_price * 1.1:.2f}</p>
                <p><strong>Recommendation:</strong> {random.choice(["Hold and monitor", "Consider buying on dips", "Consider selling on rallies", "Await clearer signals"])}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Risk warning
            st.markdown("""
            <div class="card" style="background-color: #FFF3E0; border-left: 5px solid #FF8F00;">
                <h4>Risk Warning</h4>
                <p>The above analysis is for reference only and does not constitute investment advice. Technical analysis has limitations and cannot predict the impact of sudden events and fundamental changes. Investment involves risk, please be cautious.</p>
            </div>
            """, unsafe_allow_html=True)
    
    def render_news_page(self):
        """Render news page"""
        st.header("Hot News & Market Review")
        st.markdown("""
        <div class="card">
            <p>Get real-time financial news, analyze market hot topics, and provide daily market reviews to help you grasp market pulse and investment opportunities.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs
        tab1, tab2, tab3 = st.tabs(["Hot News", "Market Review", "Hot Topics"])
        
        # Hot News tab
        with tab1:
            # Generate news
            news_data = self.generate_financial_news(15)
            
            # Filter options
            col1, col2 = st.columns(2)
            with col1:
                news_source = st.selectbox("News Source", ["All", "东方财富网", "新浪财经", "华尔街见闻", "财联社", "证券时报"])
            with col2:
                news_category = st.selectbox("News Category", ["All", "Macro Economy", "Stock Market", "Bond Market", "Forex", "Commodity", "Company News"])
            
            # Search box
            search_query = st.text_input("Search Keywords")
            
            # Filter news (simplified for demo)
            filtered_news = news_data
            
            # Display news
            st.subheader(f"Latest News (Total: {len(filtered_news)})")
            
            for news in filtered_news:
                st.markdown(f"""
                <div class="news-card">
                    <div class="news-title">{news['title']}</div>
                    <div class="news-meta">{news['source']} | {news['date']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Market Review tab
        with tab2:
            # Generate market data
            market_data = self.generate_market_overview()
            
            # Date selection
            selected_date = st.date_input("Select Date", datetime.datetime.now())
            
            # Market trend
            st.subheader("Market Trend")
            st.markdown(f"""
            <div class="card">
                <h3>Today's Market: {market_data.get('market_trend', 'Unknown')}</h3>
                <p>Date: {market_data.get('date', selected_date.strftime('%Y-%m-%d'))}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Main indices
            st.subheader("Main Indices Performance")
            
            # Create table
            table_html = """
            <table>
                <tr>
                    <th>Index</th>
                    <th>Latest Close</th>
                    <th>Change</th>
                </tr>
            """
            
            for symbol, data in market_data['index_changes'].items():
                direction_class = 'stock-up' if data['direction'] == 'up' else 'stock-down'
                change_sign = '+' if data['direction'] == 'up' else ''
                
                table_html += f"""
                <tr>
                    <td>{data['name']}</td>
                    <td>{data['latest_close']:.2f}</td>
                    <td class="{direction_class}">{change_sign}{data['change_pct']:.2f}%</td>
                </tr>
                """
            
            table_html += "</table>"
            st.markdown(table_html, unsafe_allow_html=True)
            
            # Sector performance
            st.subheader("Sector Performance")
            
            fig = px.bar(
                x=[s['change'] for s in market_data['sectors']], 
                y=[s['name'] for s in market_data['sectors']], 
                orientation='h',
                labels={"x": "Change (%)", "y": "Sector"},
                title="Sector Performance",
                color=[s['change'] for s in market_data['sectors']],
                color_continuous_scale=["red", "green"],
                range_color=[-max(abs(min(s['change'] for s in market_data['sectors'])), abs(max(s['change'] for s in market_data['sectors']))), 
                             max(abs(min(s['change'] for s in market_data['sectors'])), abs(max(s['change'] for s in market_data['sectors'])))]
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Market highlights
            st.subheader("Market Highlights")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Best Performing Sectors")
                for sector in market_data['top_sectors']:
                    st.markdown(f"- {sector}")
            
            with col2:
                st.markdown("#### Worst Performing Sectors")
                for sector in market_data['bottom_sectors']:
                    st.markdown(f"- {sector}")
            
            # Market summary
            st.subheader("Market Summary")
            
            st.markdown(f"""
            <div class="card">
                Today's market overall shows a {market_data['market_trend']} trend. Among the main indices,
                {"most are up" if sum(1 for data in market_data['index_changes'].values() if data['direction'] == 'up') > len(market_data['index_changes']) / 2 else "most are down"}.
                In terms of sectors, {", ".join(market_data['top_sectors'][:2])} sectors performed well, while {", ".join(market_data['bottom_sectors'][:2])} sectors underperformed.
                Trading volume is {random.choice(['expanding', 'stable', 'shrinking'])}, and
                liquidity is {random.choice(['relatively loose', 'neutral', 'slightly tight'])}.
                In the short term, the market may continue to {random.choice(['adjust', 'maintain strength', 'undergo pressure'])},
                and investors are advised to {random.choice(['pay attention to policy changes', 'seize structural opportunities', 'control positions', 'be appropriately defensive'])}.
            </div>
            """, unsafe_allow_html=True)
        
        # Hot Topics tab
        with tab3:
            # Generate news
            news_data = self.generate_financial_news(15)
            
            # Analyze hot topics
            hot_topics = self.analyze_hot_topics(news_data)
            
            # Display hot topics
            st.subheader("Hot Topics")
            
            # Display word cloud visual representation
            hot_topics_html = '<div style="margin-bottom: 20px;">'
            for topic in hot_topics:
                size = min(36, max(18, 18 + topic['count'] * 2))
                hot_topics_html += f'<span class="hot-topic" style="font-size: {size}px;">{topic["keyword"]} ({topic["count"]})</span>'
            hot_topics_html += '</div>'
            
            st.markdown(hot_topics_html, unsafe_allow_html=True)
            
            # Display hot topics list
            for topic in hot_topics[:8]:
                with st.expander(f"{topic['keyword']} (Mentions: {topic['count']})"):
                    # Related news
                    st.markdown("#### Related News")
                    for news in topic.get('related_news', []):
                        st.markdown(f"- {news['title']} - {news['source']} ({news['date']})")
                    
                    # Topic analysis
                    st.markdown("#### Topic Analysis")
                    
                    st.markdown(f"""
                    "{topic['keyword']}" related topics have recently received widespread market attention, with {topic['count']} mentions.
                    From related news, this topic is mainly related to {random.choice(['policy changes', 'industry dynamics', 'company performance', 'market sentiment', 'technological breakthroughs'])}.
                    In the short term, this topic may {random.choice(['continue to ferment', 'gradually cool down', 'cause market volatility', 'drive related sector performance'])}.
                    Investors are advised to {random.choice(['closely monitor subsequent developments', 'view related information rationally', 'pay attention to policy guidance', 'watch market reactions'])}.
                    """)
    
    def render_advisor_page(self):
        """Render advisor page"""
        st.header("Smart Advisor")
        st.markdown("""
        <div class="card">
            <p>Based on your risk preference, investment goals, and financial situation, we provide personalized investment advice and asset allocation plans to help you achieve wealth appreciation.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create tabs
        tab1, tab2 = st.tabs(["Risk Assessment", "Asset Allocation"])
        
        # Risk Assessment tab
        with tab1:
            st.subheader("Investor Risk Assessment")
            
            # Personal information
            st.markdown("### Basic Information")
            col1, col2 = st.columns(2)
            with col1:
                age = st.slider("Age", 18, 80, 35)
                income = st.selectbox("Annual Income (10,000)", ["Below 10", "10-30", "30-50", "50-100", "Above 100"])
            with col2:
                investment_horizon = st.selectbox("Investment Horizon", ["Within 1 year", "1-3 years", "3-5 years", "5-10 years", "Over 10 years"])
                financial_assets = st.selectbox("Financial Assets (10,000)", ["Below 10", "10-50", "50-100", "100-500", "Above 500"])
            
            # Risk preference questionnaire
            st.markdown("### Risk Preference Assessment")
            
            q1 = st.radio(
                "1. What is your investment experience?",
                ["No experience", "Within 1 year", "1-3 years", "3-5 years", "Over 5 years"]
            )
            
            q2 = st.radio(
                "2. What is the maximum investment loss you can accept?",
                ["Cannot accept any loss", "Within 5%", "Within 10%", "Within 20%", "Over 30%"]
            )
            
            q3 = st.radio(
                "3. If your investment falls by 20% in the short term, what would you do?",
                ["Immediately sell all", "Sell part", "Continue to hold", "Buy more"]
            )
            
            q4 = st.radio(
                "4. What type of investment do you prefer?",
                ["Capital preservation products", "Fixed income products", "Mixed products", "Stock products", "High-risk high-return products"]
            )
            
            q5 = st.radio(
                "5. What is your investment goal?",
                ["Capital preservation", "Stable appreciation", "Balanced growth", "Aggressive growth", "Maximum return"]
            )
            
            # Assessment button
            if st.button("Submit Assessment"):
                # Calculate risk score (simplified)
                risk_score = 0
                
                # Age score
                risk_score += max(0, (60 - age) / 10)
                
                # Income score
                income_scores = {"Below 10": 1, "10-30": 2, "30-50": 3, "50-100": 4, "Above 100": 5}
                risk_score += income_scores.get(income, 0)
                
                # Investment horizon score
                horizon_scores = {"Within 1 year": 1, "1-3 years": 2, "3-5 years": 3, "5-10 years": 4, "Over 10 years": 5}
                risk_score += horizon_scores.get(investment_horizon, 0)
                
                # Financial assets score
                asset_scores = {"Below 10": 1, "10-50": 2, "50-100": 3, "100-500": 4, "Above 500": 5}
                risk_score += asset_scores.get(financial_assets, 0)
                
                # Questionnaire score
                q1_scores = {"No experience": 1, "Within 1 year": 2, "1-3 years": 3, "3-5 years": 4, "Over 5 years": 5}
                risk_score += q1_scores.get(q1, 0)
                
                q2_scores = {"Cannot accept any loss": 1, "Within 5%": 2, "Within 10%": 3, "Within 20%": 4, "Over 30%": 5}
                risk_score += q2_scores.get(q2, 0)
                
                q3_scores = {"Immediately sell all": 1, "Sell part": 2, "Continue to hold": 3, "Buy more": 5}
                risk_score += q3_scores.get(q3, 0)
                
                q4_scores = {"Capital preservation products": 1, "Fixed income products": 2, "Mixed products": 3, "Stock products": 4, "High-risk high-return products": 5}
                risk_score += q4_scores.get(q4, 0)
                
                q5_scores = {"Capital preservation": 1, "Stable appreciation": 2, "Balanced growth": 3, "Aggressive growth": 4, "Maximum return": 5}
                risk_score += q5_scores.get(q5, 0)
                
                # Normalize score (0-100)
                normalized_score = min(100, max(0, risk_score * 4))
                
                # Determine risk type
                risk_type = "Conservative"
                if normalized_score >= 80:
                    risk_type = "Aggressive"
                elif normalized_score >= 60:
                    risk_type = "Growth"
                elif normalized_score >= 40:
                    risk_type = "Balanced"
                elif normalized_score >= 20:
                    risk_type = "Stable"
                
                # Display assessment results
                st.markdown("### Assessment Results")
                
                # Create gauge chart
                fig = px.pie(
                    values=[normalized_score, 100-normalized_score],
                    names=["Score", ""],
                    hole=0.7,
                    color_discrete_sequence=["blue", "lightgrey"]
                )
                
                fig.update_layout(
                    annotations=[
                        dict(
                            text=f"{normalized_score:.1f}<br>SCORE",
                            x=0.5, y=0.5,
                            font_size=20,
                            showarrow=False
                        )
                    ]
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"""
                <div class="card">
                    <h3>Your Risk Type: {risk_type}</h3>
                    <p><strong>Risk Score:</strong> {normalized_score:.1f}/100</p>
                    <p><strong>Risk Characteristics:</strong></p>
                    <ul>
                """, unsafe_allow_html=True)
                
                # Based on risk type, display characteristics
                if risk_type == "Conservative":
                    st.markdown("""
                    <li>Pursue capital safety and liquidity</li>
                    <li>Unwilling to take investment risks</li>
                    <li>Expect stable returns</li>
                    <li>Suitable for money market funds, short-term bonds, and other low-risk products</li>
                    """, unsafe_allow_html=True)
                elif risk_type == "Stable":
                    st.markdown("""
                    <li>Pursue capital safety while obtaining certain returns</li>
                    <li>Can bear small investment fluctuations</li>
                    <li>Expect returns higher than deposits</li>
                    <li>Suitable for bond funds, balanced funds, and other medium-low risk products</li>
                    """, unsafe_allow_html=True)
                elif risk_type == "Balanced":
                    st.markdown("""
                    <li>Pursue long-term capital appreciation</li>
                    <li>Can bear certain investment fluctuations</li>
                    <li>Expect balanced risk and return</li>
                    <li>Suitable for mixed funds, blue-chip stocks, and other medium-risk products</li>
                    """, unsafe_allow_html=True)
                elif risk_type == "Growth":
                    st.markdown("""
                    <li>Pursue higher capital appreciation</li>
                    <li>Can bear larger investment fluctuations</li>
                    <li>Expect higher long-term returns</li>
                    <li>Suitable for stock funds, growth stocks, and other medium-high risk products</li>
                    """, unsafe_allow_html=True)
                elif risk_type == "Aggressive":
                    st.markdown("""
                    <li>Pursue maximum capital appreciation</li>
                    <li>Can bear large investment risks</li>
                    <li>Expect returns significantly higher than market average</li>
                    <li>Suitable for high-growth stocks, options, leveraged products, and other high-risk products</li>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                </div>
                """, unsafe_allow_html=True)
        
        # Asset Allocation tab
        with tab2:
            st.subheader("Personalized Asset Allocation")
            
            # Configuration parameters
            st.markdown("### Configuration Parameters")
            col1, col2 = st.columns(2)
            with col1:
                risk_preference = st.select_slider(
                    "Risk Preference",
                    options=["Conservative", "Stable", "Balanced", "Growth", "Aggressive"]
                )
                investment_amount = st.number_input("Investment Amount (10,000)", min_value=1, max_value=10000, value=100)
            with col2:
                investment_period = st.slider("Investment Period (years)", 1, 30, 5)
                special_needs = st.multiselect(
                    "Special Needs",
                    ["Liquidity Needs", "Regular Income", "Tax Optimization", "Retirement Planning", "Children's Education"]
                )
            
            # Generate allocation button
            if st.button("Generate Asset Allocation Plan"):
                # Based on risk preference, generate asset allocation
                if risk_preference == "Conservative":
                    allocation = {
                        "Cash & Equivalents": 20,
                        "Bonds": 50,
                        "Stocks": 15,
                        "Real Estate": 10,
                        "Alternative Investments": 5
                    }
                elif risk_preference == "Stable":
                    allocation = {
                        "Cash & Equivalents": 15,
                        "Bonds": 40,
                        "Stocks": 30,
                        "Real Estate": 10,
                        "Alternative Investments": 5
                    }
                elif risk_preference == "Balanced":
                    allocation = {
                        "Cash & Equivalents": 10,
                        "Bonds": 30,
                        "Stocks": 40,
                        "Real Estate": 15,
                        "Alternative Investments": 5
                    }
                elif risk_preference == "Growth":
                    allocation = {
                        "Cash & Equivalents": 5,
                        "Bonds": 20,
                        "Stocks": 55,
                        "Real Estate": 15,
                        "Alternative Investments": 5
                    }
                else:  # Aggressive
                    allocation = {
                        "Cash & Equivalents": 5,
                        "Bonds": 10,
                        "Stocks": 65,
                        "Real Estate": 10,
                        "Alternative Investments": 10
                    }
                
                # Based on special needs, adjust allocation
                if "Liquidity Needs" in special_needs:
                    allocation["Cash & Equivalents"] += 10
                    allocation["Stocks"] -= 5
                    allocation["Alternative Investments"] -= 5
                
                if "Regular Income" in special_needs:
                    allocation["Bonds"] += 10
                    allocation["Stocks"] -= 10
                
                if "Retirement Planning" in special_needs:
                    allocation["Bonds"] += 5
                    allocation["Real Estate"] += 5
                    allocation["Stocks"] -= 10
                
                # Ensure all percentages sum to 100%
                total = sum(allocation.values())
                allocation = {k: round(v / total * 100) for k, v in allocation.items()}
                
                # Adjust to ensure total is 100
                diff = 100 - sum(allocation.values())
                if diff != 0:
                    keys = list(allocation.keys())
                    allocation[keys[0]] += diff
                
                # Display asset allocation plan
                st.markdown("### Asset Allocation Plan")
                
                # Create pie chart
                fig = px.pie(
                    values=list(allocation.values()),
                    names=list(allocation.keys()),
                    title=f"Asset Allocation for {risk_preference} Investor",
                    color_discrete_sequence=self.theme['chart_colors']
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Display specific allocation amounts
                st.markdown("### Specific Allocation Amounts")
                
                table_html = """
                <table>
                    <tr>
                        <th>Asset Class</th>
                        <th>Allocation Percentage</th>
                        <th>Allocation Amount (10,000)</th>
                    </tr>
                """
                
                for asset, percentage in allocation.items():
                    amount = investment_amount * percentage / 100
                    table_html += f"""
                    <tr>
                        <td>{asset}</td>
                        <td>{percentage}%</td>
                        <td>{amount:.2f}</td>
                    </tr>
                    """
                
                table_html += "</table>"
                st.markdown(table_html, unsafe_allow_html=True)
                
                # Display expected returns and risks
                st.markdown("### Expected Returns and Risks")
                
                # Simulate expected annual returns and volatilities for different asset classes
                expected_returns = {
                    "Cash & Equivalents": 0.02,
                    "Bonds": 0.04,
                    "Stocks": 0.08,
                    "Real Estate": 0.06,
                    "Alternative Investments": 0.10
                }
                
                volatilities = {
                    "Cash & Equivalents": 0.01,
                    "Bonds": 0.05,
                    "Stocks": 0.18,
                    "Real Estate": 0.12,
                    "Alternative Investments": 0.20
                }
                
                # Calculate portfolio expected return and volatility
                portfolio_return = sum(allocation[asset] / 100 * expected_returns[asset] for asset in allocation)
                portfolio_volatility = sum(allocation[asset] / 100 * volatilities[asset] for asset in allocation)
                
                # Calculate expected final value
                final_value = investment_amount * (1 + portfolio_return) ** investment_period
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Expected Annual Return</div>
                        <div class="stat-value">{portfolio_return:.2%}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="stat-card">
                        <div class="stat-label">Expected Annual Volatility</div>
                        <div class="stat-value">{portfolio_volatility:.2%}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown(f"""
                <div class="stat-card">
                    <div class="stat-label">Expected Total Value after {investment_period} years</div>
                    <div class="stat-value">{final_value:.2f}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Simulate investment growth curve
                years = list(range(investment_period + 1))
                values = [investment_amount * (1 + portfolio_return) ** year for year in years]
                
                fig = px.line(
                    x=years,
                    y=values,
                    labels={"x": "Investment Years", "y": "Investment Value"},
                    title="Investment Value Growth Projection"
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Investment advice
                st.markdown("### Investment Advice")
                
                st.markdown(f"""
                <div class="card">
                    <h4>Based on your risk preference and investment goals, we recommend:</h4>
                    <ul>
                """, unsafe_allow_html=True)
                
                # Based on risk preference, give advice
                if risk_preference == "Conservative":
                    st.markdown("""
                    <li>Allocate most funds to money market funds, government bonds, and other low-risk products</li>
                    <li>Allocate a small amount to quality blue-chip stocks or index funds to diversify risk</li>
                    <li>Consider inflation-protected assets, such as TIPS</li>
                    <li>Maintain adequate liquidity to meet unexpected needs</li>
                    """, unsafe_allow_html=True)
                elif risk_preference == "Stable":
                    st.markdown("""
                    <li>Allocate a certain proportion to bond funds and quality bonds for stable returns</li>
                    <li>Allocate appropriate amounts to large-cap blue-chip stocks and index funds to share in economic growth</li>
                    <li>Consider some high-dividend stocks for stable cash flow</li>
                    <li>Consider REITs and other real estate investment tools to diversify risk</li>
                    """, unsafe_allow_html=True)
                elif risk_preference == "Balanced":
                    st.markdown("""
                    <li>Balance allocations to stocks and bonds to balance returns and risks</li>
                    <li>For the stock portion, consider allocating to industry leaders and growth stocks</li>
                    <li>For the bond portion, consider allocating to some medium-high grade credit bonds to enhance returns</li>
                    <li>Consider REITs and gold as alternative assets to diversify risk</li>
                    """, unsafe_allow_html=True)
                elif risk_preference == "Growth":
                    st.markdown("""
                    <li>Allocate a higher proportion to stocks, including growth stocks and value stocks</li>
                    <li>Consider industry ETFs to capture sector rotation opportunities</li>
                    <li>Consider high-yield bonds to enhance overall returns</li>
                    <li>Consider commodity futures and other alternative assets to increase portfolio diversity</li>
                    """, unsafe_allow_html=True)
                else:  # Aggressive
                    st.markdown("""
                    <li>Allocate a high proportion to stocks, including high-growth stocks and thematic investments</li>
                    <li>Consider emerging market stocks to capture global opportunities</li>
                    <li>Consider leveraged products and options to enhance potential returns</li>
                    <li>Consider private equity and venture capital to seek excess returns</li>
                    """, unsafe_allow_html=True)
                
                st.markdown("""
                    </ul>
                    <p><strong>Risk Warning:</strong> The above suggestions are for reference only and do not constitute investment advice. Actual investments should be adjusted based on market conditions and individual needs. Investment involves risks, please be cautious.</p>
                </div>
                """, unsafe_allow_html=True)


if __name__ == "__main__":
    platform = FinancialPlatform()
    platform.create_streamlit_app()
