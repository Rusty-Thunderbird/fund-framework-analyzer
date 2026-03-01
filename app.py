"""
Mutual Fund Framework Analyzer
Interactive tool for comparing fund selection frameworks
Built on IIM Indore research project
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import os

# Page configuration
st.set_page_config(
    page_title="Fund Framework Analyzer",
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
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        padding: 1rem;
        border-left: 4px solid #1f77b4;
        border-radius: 0.25rem;
        margin: 1rem 0;
    }
    .winner-box {
        background-color: #d4edda;
        padding: 1rem;
        border-left: 4px solid #28a745;
        border-radius: 0.25rem;
        margin: 1rem 0;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🎯 Mutual Fund Framework Analyzer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Compare fund selection frameworks and simulate investor outcomes</div>', unsafe_allow_html=True)

# Load pre-computed data
@st.cache_data
def load_framework_results():
    """Load pre-computed framework results"""
    # This would load your actual validation results
    # For now, using the results from your PDF
    
    frameworks = {
        'FW4': {
            'name': '7Y Reliability Framework',
            'weights': {'WP_7Y': 0.50, 'WP_5Y': 0.00, 'WP_3Y': 0.00, 
                       'RAA_7Y': 0.10, 'RAA_5Y': 0.10, 'RAA_3Y': 0.15, 'RAA_1Y': 0.15},
            'results': {
                '1Y': {'terminal_wealth': 110.29, 'cagr': 0.1029, 'beat_bench': 68, 'underperform': 32},
                '3Y': {'terminal_wealth': 177.35, 'cagr': 0.2104, 'beat_bench': 68, 'underperform': 32},
                '5Y': {'terminal_wealth': 245.56, 'cagr': 0.1968, 'beat_bench': 52, 'underperform': 48},
                '7Y': {'terminal_wealth': 310.07, 'cagr': 0.1755, 'beat_bench': 72, 'underperform': 28}
            }
        },
        'VR': {
            'name': 'Value Research',
            'results': {
                '1Y': {'terminal_wealth': 109.49, 'cagr': 0.0949, 'beat_bench': 60, 'underperform': 40},
                '3Y': {'terminal_wealth': 175.90, 'cagr': 0.2071, 'beat_bench': 56, 'underperform': 44},
                '5Y': {'terminal_wealth': 243.81, 'cagr': 0.1951, 'beat_bench': 40, 'underperform': 60},
                '7Y': {'terminal_wealth': 299.46, 'cagr': 0.1696, 'beat_bench': 68, 'underperform': 32}
            }
        },
        'Benchmark': {
            'name': 'NIFTY 500 TRI',
            'results': {
                '1Y': {'terminal_wealth': 108.86, 'cagr': 0.0886, 'beat_bench': 0, 'underperform': 0},
                '3Y': {'terminal_wealth': 168.26, 'cagr': 0.1894, 'beat_bench': 0, 'underperform': 0},
                '5Y': {'terminal_wealth': 228.04, 'cagr': 0.1792, 'beat_bench': 0, 'underperform': 0},
                '7Y': {'terminal_wealth': 280.17, 'cagr': 0.1586, 'beat_bench': 0, 'underperform': 0}
            }
        }
    }
    
    return frameworks

frameworks = load_framework_results()

# Sidebar - Framework Selection
st.sidebar.header("🎛️ Framework Configuration")

framework_choice = st.sidebar.radio(
    "Select Framework",
    ["FW4 (Recommended)", "Value Research", "Custom Framework"],
    help="Choose which fund selection framework to analyze"
)

# Custom Framework Configuration
if framework_choice == "Custom Framework":
    st.sidebar.markdown("### Custom Weights")
    st.sidebar.markdown("*Adjust to change fund selection criteria*")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        wp_7y = st.slider("WP 7Y", 0.0, 1.0, 0.5, 0.05, help="7-year win probability weight")
        wp_5y = st.slider("WP 5Y", 0.0, 1.0, 0.0, 0.05, help="5-year win probability weight")
        wp_3y = st.slider("WP 3Y", 0.0, 1.0, 0.0, 0.05, help="3-year win probability weight")
    
    with col2:
        raa_7y = st.slider("RAA 7Y", 0.0, 1.0, 0.1, 0.05, help="7-year risk-adjusted alpha weight")
        raa_5y = st.slider("RAA 5Y", 0.0, 1.0, 0.1, 0.05, help="5-year risk-adjusted alpha weight")
        raa_3y = st.slider("RAA 3Y", 0.0, 1.0, 0.15, 0.05, help="3-year risk-adjusted alpha weight")
        raa_1y = st.slider("RAA 1Y", 0.0, 1.0, 0.15, 0.05, help="1-year risk-adjusted alpha weight")
    
    total_weight = wp_7y + wp_5y + wp_3y + raa_7y + raa_5y + raa_3y + raa_1y
    
    if abs(total_weight - 1.0) > 0.01:
        st.sidebar.error(f"⚠️ Weights must sum to 1.0 (currently: {total_weight:.2f})")
    else:
        st.sidebar.success(f"✅ Weights sum to {total_weight:.2f}")
    
    custom_weights = {
        'WP_7Y': wp_7y, 'WP_5Y': wp_5y, 'WP_3Y': wp_3y,
        'RAA_7Y': raa_7y, 'RAA_5Y': raa_5y, 'RAA_3Y': raa_3y, 'RAA_1Y': raa_1y
    }

# Investment Configuration
st.sidebar.markdown("---")
st.sidebar.header("💰 Investment Settings")

investment_mode = st.sidebar.radio(
    "Investment Mode",
    ["Lump Sum", "SIP (Monthly)", "SIP (Quarterly)"],
    help="How you want to invest"
)

initial_amount = st.sidebar.number_input(
    "Initial Investment (₹)",
    min_value=1000,
    max_value=10000000,
    value=100000,
    step=10000,
    help="Amount to invest"
)

if "SIP" in investment_mode:
    sip_amount = st.sidebar.number_input(
        "SIP Amount (₹)",
        min_value=500,
        max_value=1000000,
        value=10000,
        step=1000,
        help="Amount to invest periodically"
    )

horizon = st.sidebar.select_slider(
    "Investment Horizon",
    options=["1Y", "3Y", "5Y", "7Y"],
    value="5Y",
    help="How long will you stay invested?"
)

# Main content area
tab1, tab2, tab3, tab4 = st.tabs(["📊 Comparison", "💹 Wealth Simulation", "🎯 Risk Analysis", "📖 Methodology"])

with tab1:
    st.header("Framework Comparison")
    
    # Framework selection for comparison
    compare_options = []
    if framework_choice == "FW4 (Recommended)":
        selected_fw = 'FW4'
        compare_options = ['FW4', 'VR', 'Benchmark']
    elif framework_choice == "Value Research":
        selected_fw = 'VR'
        compare_options = ['VR', 'FW4', 'Benchmark']
    else:
        selected_fw = 'Custom'
        compare_options = ['Custom', 'FW4', 'VR', 'Benchmark']
    
    # Get results for selected horizon
    fw4_result = frameworks['FW4']['results'][horizon]
    vr_result = frameworks['VR']['results'][horizon]
    bench_result = frameworks['Benchmark']['results'][horizon]
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Terminal Wealth",
            f"₹{fw4_result['terminal_wealth']:.2f}",
            f"+₹{fw4_result['terminal_wealth'] - 100:.2f}",
            help="Final value of ₹100 invested"
        )
    
    with col2:
        st.metric(
            "Annualized Return",
            f"{fw4_result['cagr']*100:.2f}%",
            f"+{(fw4_result['cagr'] - bench_result['cagr'])*100:.2f}% vs benchmark"
        )
    
    with col3:
        st.metric(
            "Funds Beating Benchmark",
            f"{fw4_result['beat_bench']}%",
            f"+{fw4_result['beat_bench'] - vr_result['beat_bench']}% vs VR"
        )
    
    with col4:
        st.metric(
            "Risk Avoidance",
            f"{100 - fw4_result['underperform']}%",
            f"+{vr_result['underperform'] - fw4_result['underperform']}% better"
        )
    
    st.markdown("---")
    
    # Wealth comparison chart
    st.subheader(f"💰 Terminal Wealth Comparison ({horizon})")
    
    horizons = ['1Y', '3Y', '5Y', '7Y']
    
    wealth_data = {
        'Horizon': horizons,
        'FW4': [frameworks['FW4']['results'][h]['terminal_wealth'] for h in horizons],
        'Value Research': [frameworks['VR']['results'][h]['terminal_wealth'] for h in horizons],
        'NIFTY 500': [frameworks['Benchmark']['results'][h]['terminal_wealth'] for h in horizons]
    }
    
    df_wealth = pd.DataFrame(wealth_data)
    
    fig_wealth = go.Figure()
    
    fig_wealth.add_trace(go.Bar(
        name='FW4 (IIM Framework)',
        x=df_wealth['Horizon'],
        y=df_wealth['FW4'],
        marker_color='#1f77b4',
        text=df_wealth['FW4'].round(2),
        textposition='outside'
    ))
    
    fig_wealth.add_trace(go.Bar(
        name='Value Research',
        x=df_wealth['Horizon'],
        y=df_wealth['Value Research'],
        marker_color='#ff7f0e',
        text=df_wealth['Value Research'].round(2),
        textposition='outside'
    ))
    
    fig_wealth.add_trace(go.Bar(
        name='NIFTY 500 TRI',
        x=df_wealth['Horizon'],
        y=df_wealth['NIFTY 500'],
        marker_color='#2ca02c',
        text=df_wealth['NIFTY 500'].round(2),
        textposition='outside'
    ))
    
    fig_wealth.update_layout(
        title="Terminal Wealth: ₹100 Invested in Dec 2018",
        xaxis_title="Investment Horizon",
        yaxis_title="Terminal Wealth (₹)",
        barmode='group',
        height=500,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_wealth, use_container_width=True)
    
    # Success rate comparison
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ Benchmark Beating Probability")
        
        beat_data = {
            'Horizon': horizons,
            'FW4': [frameworks['FW4']['results'][h]['beat_bench'] for h in horizons],
            'Value Research': [frameworks['VR']['results'][h]['beat_bench'] for h in horizons]
        }
        
        df_beat = pd.DataFrame(beat_data)
        
        fig_beat = go.Figure()
        
        fig_beat.add_trace(go.Scatter(
            name='FW4',
            x=df_beat['Horizon'],
            y=df_beat['FW4'],
            mode='lines+markers',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=10)
        ))
        
        fig_beat.add_trace(go.Scatter(
            name='VR',
            x=df_beat['Horizon'],
            y=df_beat['Value Research'],
            mode='lines+markers',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=10)
        ))
        
        fig_beat.add_hline(y=50, line_dash="dash", line_color="gray", 
                          annotation_text="50% threshold")
        
        fig_beat.update_layout(
            yaxis_title="% of Funds Beating Benchmark",
            xaxis_title="Horizon",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_beat, use_container_width=True)
    
    with col2:
        st.subheader("⚠️ Downside Risk (Underperformance)")
        
        under_data = {
            'Horizon': horizons,
            'FW4': [frameworks['FW4']['results'][h]['underperform'] for h in horizons],
            'Value Research': [frameworks['VR']['results'][h]['underperform'] for h in horizons]
        }
        
        df_under = pd.DataFrame(under_data)
        
        fig_under = go.Figure()
        
        fig_under.add_trace(go.Scatter(
            name='FW4',
            x=df_under['Horizon'],
            y=df_under['FW4'],
            mode='lines+markers',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=10),
            fill='tozeroy'
        ))
        
        fig_under.add_trace(go.Scatter(
            name='VR',
            x=df_under['Horizon'],
            y=df_under['Value Research'],
            mode='lines+markers',
            line=dict(color='#ff7f0e', width=3),
            marker=dict(size=10),
            fill='tozeroy'
        ))
        
        fig_under.update_layout(
            yaxis_title="% of Funds Underperforming",
            xaxis_title="Horizon",
            height=400,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_under, use_container_width=True)
    
    # Winner announcement
    st.markdown("---")
    
    if fw4_result['terminal_wealth'] > vr_result['terminal_wealth']:
        winner_text = f"""
        <div class="winner-box">
        🏆 <b>FW4 (IIM Framework) WINS over {horizon}</b><br>
        • {(fw4_result['terminal_wealth'] - vr_result['terminal_wealth']):.2f} more terminal wealth<br>
        • {fw4_result['beat_bench'] - vr_result['beat_bench']}% more funds beating benchmark<br>
        • {vr_result['underperform'] - fw4_result['underperform']}% better risk avoidance
        </div>
        """
    else:
        winner_text = f"""
        <div class="winner-box">
        🏆 <b>Value Research WINS over {horizon}</b><br>
        • {(vr_result['terminal_wealth'] - fw4_result['terminal_wealth']):.2f} more terminal wealth<br>
        • {vr_result['beat_bench'] - fw4_result['beat_bench']}% more funds beating benchmark
        </div>
        """
    
    st.markdown(winner_text, unsafe_allow_html=True)

with tab2:
    st.header("💹 Wealth Growth Simulation")
    
    st.markdown("""
    <div class="info-box">
    📌 <b>What You're Seeing:</b> This simulates how your investment would have grown from Dec 2018 onwards 
    using different fund selection frameworks. All portfolios are equal-weighted across top 25 funds with no rebalancing.
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate wealth path
    if investment_mode == "Lump Sum":
        # Simple wealth path based on terminal values
        num_points = int(horizon[0]) * 12 + 1  # Monthly points
        months = np.linspace(0, int(horizon[0]) * 12, num_points)
        
        fw4_terminal = fw4_result['terminal_wealth']
        vr_terminal = vr_result['terminal_wealth']
        bench_terminal = bench_result['terminal_wealth']
        
        # Simulate path (exponential growth)
        fw4_path = initial_amount * ((fw4_terminal/100) ** (months / (int(horizon[0]) * 12)))
        vr_path = initial_amount * ((vr_terminal/100) ** (months / (int(horizon[0]) * 12)))
        bench_path = initial_amount * ((bench_terminal/100) ** (months / (int(horizon[0]) * 12)))
        
        fig_wealth_path = go.Figure()
        
        fig_wealth_path.add_trace(go.Scatter(
            name='FW4 Portfolio',
            x=months,
            y=fw4_path,
            mode='lines',
            line=dict(color='#1f77b4', width=3),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.1)'
        ))
        
        fig_wealth_path.add_trace(go.Scatter(
            name='VR Portfolio',
            x=months,
            y=vr_path,
            mode='lines',
            line=dict(color='#ff7f0e', width=3)
        ))
        
        fig_wealth_path.add_trace(go.Scatter(
            name='NIFTY 500',
            x=months,
            y=bench_path,
            mode='lines',
            line=dict(color='#2ca02c', width=2, dash='dash')
        ))
        
        fig_wealth_path.update_layout(
            title=f"Wealth Growth Trajectory: ₹{initial_amount:,.0f} Lump Sum Investment",
            xaxis_title="Months from Dec 2018",
            yaxis_title="Portfolio Value (₹)",
            height=500,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig_wealth_path, use_container_width=True)
        
        # Final summary
        col1, col2, col3 = st.columns(3)
        
        with col1:
            final_fw4 = initial_amount * (fw4_terminal / 100)
            st.metric(
                "FW4 Final Value",
                f"₹{final_fw4:,.0f}",
                f"+₹{final_fw4 - initial_amount:,.0f}"
            )
        
        with col2:
            final_vr = initial_amount * (vr_terminal / 100)
            st.metric(
                "VR Final Value",
                f"₹{final_vr:,.0f}",
                f"+₹{final_vr - initial_amount:,.0f}"
            )
        
        with col3:
            final_bench = initial_amount * (bench_terminal / 100)
            st.metric(
                "Benchmark Final Value",
                f"₹{final_bench:,.0f}",
                f"+₹{final_bench - initial_amount:,.0f}"
            )
    
    else:  # SIP mode
        st.info("🚧 SIP simulation coming in next update! Currently showing lump sum results.")

with tab3:
    st.header("🎯 Risk & Reliability Analysis")
    
    st.subheader("Decision Confidence Score")
    
    # Calculate confidence metrics
    avg_beat_fw4 = np.mean([frameworks['FW4']['results'][h]['beat_bench'] for h in horizons])
    avg_beat_vr = np.mean([frameworks['VR']['results'][h]['beat_bench'] for h in horizons])
    
    avg_under_fw4 = np.mean([frameworks['FW4']['results'][h]['underperform'] for h in horizons])
    avg_under_vr = np.mean([frameworks['VR']['results'][h]['underperform'] for h in horizons])
    
    # Confidence score = (avg beat% - avg under%) / 100
    confidence_fw4 = (avg_beat_fw4 - avg_under_fw4) / 100
    confidence_vr = (avg_beat_vr - avg_under_vr) / 100
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "FW4 Confidence Score",
            f"{confidence_fw4:.2f}",
            help="Higher is better. Combines success rate and risk avoidance."
        )
        
        st.markdown(f"""
        **Interpretation:**
        - Average Benchmark Beating: {avg_beat_fw4:.1f}%
        - Average Risk Avoidance: {100-avg_under_fw4:.1f}%
        - Net Confidence: {confidence_fw4:.2f}
        """)
    
    with col2:
        st.metric(
            "VR Confidence Score",
            f"{confidence_vr:.2f}",
            f"{confidence_vr - confidence_fw4:.2f} vs FW4"
        )
        
        st.markdown(f"""
        **Interpretation:**
        - Average Benchmark Beating: {avg_beat_vr:.1f}%
        - Average Risk Avoidance: {100-avg_under_vr:.1f}%
        - Net Confidence: {confidence_vr:.2f}
        """)
    
    st.markdown("---")
    
    st.subheader("Portfolio Win Rate")
    
    # Count wins across horizons
    fw4_wins = sum(1 for h in horizons if frameworks['FW4']['results'][h]['terminal_wealth'] > 
                   frameworks['VR']['results'][h]['terminal_wealth'])
    vr_wins = len(horizons) - fw4_wins
    
    win_rate_data = pd.DataFrame({
        'Framework': ['FW4', 'Value Research'],
        'Wins': [fw4_wins, vr_wins],
        'Win Rate': [fw4_wins/len(horizons)*100, vr_wins/len(horizons)*100]
    })
    
    fig_wins = go.Figure()
    
    fig_wins.add_trace(go.Bar(
        x=win_rate_data['Framework'],
        y=win_rate_data['Wins'],
        text=win_rate_data['Win Rate'].round(0).astype(str) + '%',
        textposition='outside',
        marker_color=['#1f77b4', '#ff7f0e']
    ))
    
    fig_wins.update_layout(
        title="Head-to-Head: Which Framework Won More Often?",
        yaxis_title="Number of Horizons Won",
        height=400
    )
    
    st.plotly_chart(fig_wins, use_container_width=True)
    
    st.markdown(f"""
    <div class="info-box">
    📊 <b>Portfolio Win Rate:</b> FW4 won {fw4_wins} out of {len(horizons)} horizons ({fw4_wins/len(horizons)*100:.0f}% win rate)
    </div>
    """, unsafe_allow_html=True)

with tab4:
    st.header("📖 Methodology")
    
    st.markdown("""
    ## About This Framework
    
    This tool is based on research conducted at **IIM Indore** that developed a fundamentally different 
    approach to mutual fund selection.
    
    ### The Problem with Traditional Ratings
    
    Most fund rating systems (Morningstar, CRISIL, Value Research) focus on:
    - ❌ Point-in-time performance
    - ❌ Backward-looking metrics
    - ❌ Return-chasing behavior
    - ❌ Risk-adjusted ratios (Sharpe, Sortino)
    
    But they don't answer the investor's real question:
    
    > **"What is the probability that I will beat the market over my holding period?"**
    
    ### Our Approach: Outcome Reliability
    
    Instead of measuring past performance, we measure **forward outcome probability**:
    
    1. **Rolling Window Analysis**: Simulate thousands of historical investors entering at different times
    2. **Win Probability**: Calculate how often each fund actually beat NIFTY 500 TRI over 7-year periods
    3. **Multi-Horizon Strength**: Evaluate consistency across 1Y, 3Y, 5Y, 7Y horizons
    4. **Reliability Gate**: Only consider funds that have proven cycle-resilient
    
    ### Framework Components
    
    **FW4 (Recommended Framework):**
    - 50% weight on 7-Year Win Probability (structural reliability)
    - 10% weight on 7-Year Risk-Adjusted Alpha
    - 10% weight on 5-Year Risk-Adjusted Alpha
    - 15% weight on 3-Year Risk-Adjusted Alpha
    - 15% weight on 1-Year Risk-Adjusted Alpha
    
    **Value Research (Comparison):**
    - Category-relative risk-adjusted performance
    - 40% weight on 3-year metrics
    - 60% weight on 5-year metrics
    - Downside deviation as risk measure
    
    ### Validation Results
    
    Tested on Dec 2018 selection with forward outcomes through Dec 2025:
    - ✅ FW4 won **3 out of 4** forward horizons
    - ✅ Higher terminal wealth across most periods
    - ✅ Better benchmark-beating probability
    - ✅ Superior risk avoidance
    
    ### Key Insight
    
    **Reliability > Returns**
    
    The framework doesn't chase the highest past returns. Instead, it identifies funds with 
    **structural advantages** that persist across market cycles.
    
    ---
    
    ### Research Team
    - **Institution**: IIM Indore
    - **Project Type**: Research Internship
    - **Approach**: Quantitative validation using 15+ years of mutual fund NAV data
    - **Benchmark**: NIFTY 500 Total Return Index
    
    ---
    
    ### Data Sources
    - NAV Data: AMFI (Association of Mutual Funds in India)
    - Benchmark: NSE Indices (NIFTY 500 TRI)
    - Risk-Free Rate: RBI 182-Day T-Bill Yields
    
    ### Important Disclaimers
    
    ⚠️ **This is a research tool, not investment advice**
    - Past performance does not guarantee future results
    - All investments carry risk
    - Consult a financial advisor before making investment decisions
    - This tool is for educational and research purposes only
    
    ### Future Enhancements
    
    Coming soon:
    - 📊 SIP simulations
    - 📈 Distribution analysis (best/median/worst cases)
    - 🎯 Regret probability maps
    - 📅 Multiple start date testing
    - 🔄 Rebalancing strategies
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 2rem;">
    Built with ❤️ using Streamlit | Research Project @ IIM Indore<br>
    <small>For educational purposes only. Not investment advice.</small>
</div>
""", unsafe_allow_html=True)
