import streamlit as st
from typing import List, Optional

def render_key_insights(
    title: str = "💡 Key Insights",
    insights: Optional[List[str]] = None,
    badge_text: str = "⚡ AI STRATEGIC ANALYSIS",
    border_color: str = "#00E676"
):
    """
    Renders an interactive, innovative, and unique Key Insights panel with glassmorphism,
    neon glowing accents, dynamic hover state cards, and high-contrast readable text.
    """
    if not insights:
        insights = ["No key insights available for the current selection."]
        
    # CSS styles for interactive key insights card
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
        padding: 24px !important;
        margin-top: 20px !important;
        margin-bottom: 24px !important;
        backdrop-filter: blur(16px) !important;
        -webkit-backdrop-filter: blur(16px) !important;
        box-shadow: 0 12px 35px -10px rgba(0, 0, 0, 0.6), inset 0 1px 1px rgba(255, 255, 255, 0.1) !important;
        position: relative !important;
        overflow: hidden !important;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }}
    
    .key-insights-container:hover {{
        border-color: {border_color} !important;
        box-shadow: 0 16px 40px -10px rgba(0, 230, 118, 0.3), inset 0 1px 2px rgba(255, 255, 255, 0.2) !important;
        transform: translateY(-2px) !important;
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
        margin-bottom: 18px !important;
        padding-bottom: 12px !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
    }}
    
    .key-insights-title {{
        font-size: 1.3rem !important;
        font-weight: 800 !important;
        background: linear-gradient(90deg, #38BDF8 0%, #34D399 50%, {border_color} 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        margin: 0 !important;
        letter-spacing: -0.3px !important;
    }}
    
    .key-insights-badge {{
        background: rgba(56, 189, 248, 0.12) !important;
        border: 1px solid rgba(56, 189, 248, 0.4) !important;
        color: #38BDF8 !important;
        font-size: 0.72rem !important;
        font-weight: 700 !important;
        padding: 5px 13px !important;
        border-radius: 20px !important;
        letter-spacing: 0.8px !important;
        text-transform: uppercase !important;
        display: inline-flex !important;
        align-items: center !important;
        gap: 7px !important;
        box-shadow: 0 0 12px rgba(56, 189, 248, 0.2) !important;
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
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)) !important;
        gap: 14px !important;
    }}
    
    .insight-card {{
        background: rgba(30, 41, 59, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-left: 4px solid #38BDF8 !important;
        border-radius: 12px !important;
        padding: 16px 18px !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        color: #F8FAFC !important;
        font-size: 0.95rem !important;
        line-height: 1.65 !important;
    }}
    
    .insight-card:hover {{
        background: rgba(30, 41, 59, 0.95) !important;
        border-color: rgba(56, 189, 248, 0.5) !important;
        border-left-color: {border_color} !important;
        transform: translateY(-3px) scale(1.01) !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.4), 0 0 15px rgba(0, 230, 118, 0.2) !important;
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
    
    # Build list of insight cards
    cards_html = ""
    accent_colors = ["#38BDF8", "#00E676", "#FBBF24", "#C084FC", "#F43F5E"]
    
    for idx, item in enumerate(insights):
        accent = accent_colors[idx % len(accent_colors)]
        cards_html += f"""
        <div class="insight-card" style="border-left-color: {accent} !important;">
            {item}
        </div>
        """
        
    content = f"""
    <div class="key-insights-container">
        <div class="key-insights-header">
            <h3 class="key-insights-title">
                {title}
            </h3>
            <div class="key-insights-badge">
                <span class="key-insights-badge-dot"></span>
                {badge_text}
            </div>
        </div>
        <div class="key-insights-grid">
            {cards_html}
        </div>
    </div>
    """

    # Build full HTML document with explicit UTF-8 charset to avoid mojibake
    html_document = f"""<!doctype html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      {custom_css}
      <style>body{{margin:0;padding:12px;background:transparent;color:inherit;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial;}}</style>
    </head>
    <body>
      {content}
    </body>
    </html>
    """

    import base64
    try:
        # Encode HTML document as a base64 data URI with charset
        html_bytes = html_document.encode('utf-8')
        b64 = base64.b64encode(html_bytes).decode('ascii')
        data_uri = f"data:text/html;charset=utf-8;base64,{b64}"
        st.iframe(data_uri, height=300)
    except Exception:
        # Fallback to legacy markdown rendering if iframe/data URI isn't available
        st.markdown(html_document, unsafe_allow_html=True)

