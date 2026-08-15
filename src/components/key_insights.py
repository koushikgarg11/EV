import streamlit as st
from typing import List, Optional

def render_key_insights(
    title: str = "💡 Key Insights",
    insights: Optional[List[str]] = None,
    badge_text: str = "⚡ AI STRATEGIC ANALYSIS",
    border_color: str = "#00E676",
    height: Optional[int] = None,
    **kwargs
):
    """
    Renders an interactive Key Insights panel with glassmorphism, neon glowing accents,
    full-width layout, and smooth horizontal scrolling across all Streamlit pages.
    """
    if not insights:
        insights = ["No key insights available for the current selection."]
        
    custom_css = f"""
<style>
@keyframes pulseDot {{
    0%, 100% {{ transform: scale(1); opacity: 1; }}
    50% {{ transform: scale(1.4); opacity: 0.5; }}
}}

@keyframes gradientMove {{
    0% {{ background-position: 0% 0%; }}
    100% {{ background-position: 200% 0%; }}
}}

.key-insights-container {{
    background: linear-gradient(135deg, rgba(15, 23, 42, 0.96) 0%, rgba(24, 37, 66, 0.92) 50%, rgba(15, 23, 42, 0.96) 100%) !important;
    border: 1px solid rgba(56, 189, 248, 0.35) !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    backdrop-filter: blur(16px) !important;
    box-shadow: 0 12px 35px -10px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
    position: relative !important;
    overflow: hidden !important;
    box-sizing: border-box !important;
    width: 100% !important;
    margin-top: 16px !important;
    margin-bottom: 20px !important;
}}

.key-insights-container::before {{
    content: '' !important;
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    height: 3px !important;
    background: linear-gradient(90deg, {border_color}, #38BDF8, #A78BFA, {border_color}) !important;
    background-size: 200% 100% !important;
    animation: gradientMove 4s linear infinite !important;
}}

.key-insights-header {{
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-bottom: 16px !important;
    padding-bottom: 10px !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
    flex-wrap: wrap !important;
    gap: 10px !important;
}}

.key-insights-title {{
    font-size: 1.25rem !important;
    font-weight: 800 !important;
    background: linear-gradient(90deg, #38BDF8 0%, #34D399 50%, {border_color} 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    margin: 0 !important;
}}

.key-insights-badge {{
    background: rgba(56, 189, 248, 0.12) !important;
    border: 1px solid rgba(56, 189, 248, 0.4) !important;
    color: #38BDF8 !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    letter-spacing: 0.8px !important;
    text-transform: uppercase !important;
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
}}

.key-insights-badge-dot {{
    width: 7px !important;
    height: 7px !important;
    border-radius: 50% !important;
    background-color: {border_color} !important;
    box-shadow: 0 0 8px {border_color} !important;
    animation: pulseDot 1.5s infinite ease-in-out !important;
}}

.key-insights-grid {{
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    overflow-x: auto !important;
    overflow-y: hidden !important;
    gap: 16px !important;
    padding-bottom: 10px !important;
    scroll-behavior: smooth !important;
    -webkit-overflow-scrolling: touch !important;
    width: 100% !important;
}}

.key-insights-grid::-webkit-scrollbar {{
    height: 6px !important;
}}

.key-insights-grid::-webkit-scrollbar-track {{
    background: rgba(15, 23, 42, 0.6) !important;
    border-radius: 10px !important;
}}

.key-insights-grid::-webkit-scrollbar-thumb {{
    background: rgba(56, 189, 248, 0.4) !important;
    border-radius: 10px !important;
}}

.key-insights-grid::-webkit-scrollbar-thumb:hover {{
    background: #00E676 !important;
}}

.insight-card {{
    flex: 0 0 calc(33.333% - 11px) !important;
    min-width: 280px !important;
    background: rgba(30, 41, 59, 0.65) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-left: 4px solid #38BDF8 !important;
    border-radius: 12px !important;
    padding: 14px 16px !important;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    color: #F8FAFC !important;
    font-size: 0.92rem !important;
    line-height: 1.6 !important;
    box-sizing: border-box !important;
}}

.insight-card:hover {{
    background: rgba(30, 41, 59, 0.95) !important;
    border-color: rgba(56, 189, 248, 0.5) !important;
    border-left-color: {border_color} !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.4), 0 0 12px rgba(0, 230, 118, 0.2) !important;
}}

.insight-card strong, .insight-card b {{
    color: #38BDF8 !important;
    font-weight: 700 !important;
}}

.insight-card .highlight-emerald {{
    color: #00E676 !important;
    font-weight: 700 !important;
}}

.insight-card .highlight-amber {{
    color: #FBBF24 !important;
    font-weight: 700 !important;
}}

.insight-card .highlight-purple {{
    color: #C084FC !important;
    font-weight: 700 !important;
}}
</style>
"""
    cards_html = ""
    accent_colors = ["#38BDF8", "#00E676", "#FBBF24", "#C084FC", "#F43F5E"]
    
    for idx, item in enumerate(insights):
        accent = accent_colors[idx % len(accent_colors)]
        cards_html += f'<div class="insight-card" style="border-left-color: {accent} !important;">{item}</div>'
        
    content = f'<div class="key-insights-container"><div class="key-insights-header"><h3 class="key-insights-title">{title}</h3><div class="key-insights-badge"><span class="key-insights-badge-dot"></span>{badge_text}</div></div><div class="key-insights-grid">{cards_html}</div></div>'

    st.markdown(f"{custom_css}\n{content}", unsafe_allow_html=True)

