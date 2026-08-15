import streamlit as st

def fix_plotly_dark(fig):
    """
    Ensures Plotly figures have transparent / dark background, white text,
    visible grid lines, and proper legend & axis contrast across all plot types
    (Cartesian, Pie, Treemap, Map, Polar).
    """
    if fig is not None:
        axis_config = dict(
            color="#FFFFFF",
            title_font=dict(color="#FFFFFF", size=13),
            tickfont=dict(color="#FFFFFF", size=11),
            gridcolor="rgba(255, 255, 255, 0.15)",
            zerolinecolor="rgba(255, 255, 255, 0.2)"
        )
        
        layout_update = dict(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#FFFFFF", family="Inter, sans-serif"),
            title_font=dict(color="#FFFFFF", size=16),
            legend=dict(
                font=dict(color="#FFFFFF", size=11),
                title_font=dict(color="#FFFFFF", size=12),
                bgcolor="rgba(14, 17, 23, 0.6)"
            ),
            hoverlabel=dict(
                bgcolor="#161B22",
                font_color="#FFFFFF",
                bordercolor="rgba(56, 189, 248, 0.5)"
            )
        )

        # Detect trace types to check if plot is Cartesian
        trace_types = set()
        if hasattr(fig, "data") and fig.data:
            trace_types = {getattr(t, "type", "") for t in fig.data}

        non_cartesian_types = {"pie", "treemap", "sunburst", "densitymapbox", "scattermapbox", "densitymap", "scattermap", "scatterpolar", "pie"}
        is_cartesian = bool(trace_types) and not trace_types.issubset(non_cartesian_types)
        
        # Only add xaxis/yaxis if chart is Cartesian or already has axes defined
        fig_dict = fig.to_dict() if hasattr(fig, "to_dict") else {}
        existing_layout = fig_dict.get("layout", {})
        if is_cartesian or "xaxis" in existing_layout or "yaxis" in existing_layout:
            layout_update["xaxis"] = axis_config
            layout_update["yaxis"] = axis_config

        fig.update_layout(**layout_update)

        try:
            fig.update_coloraxes(
                colorbar=dict(
                    title_font=dict(color="#FFFFFF"),
                    tickfont=dict(color="#FFFFFF"),
                    outlinecolor="rgba(255, 255, 255, 0.2)"
                )
            )
        except Exception:
            pass

        try:
            fig.update_scenes(
                xaxis=axis_config,
                yaxis=axis_config,
                zaxis=axis_config,
                bgcolor="rgba(0,0,0,0)"
            )
        except Exception:
            pass

        try:
            fig.update_polars(
                radialaxis=axis_config,
                angularaxis=axis_config,
                bgcolor="rgba(0,0,0,0)"
            )
        except Exception:
            pass

    return fig

def apply_custom_theme():
    """
    Applies unified Dark Mode Glassmorphic Styling with pure white text (#FFFFFF),
    black sidebar (#000000), dark multiselect widgets (#161B22), and crisp Plotly background (#0E1117).
    """
    st.markdown("""
    <style>
        /* Base App & Dark Theme Customization */
        .stApp, [data-testid="stAppViewContainer"], .main {
            background-color: #0E1117 !important;
            color: #FFFFFF !important;
        }
        
        /* Body text, paragraphs, list items, and headings */
        p, label, li, h1, h2, h3, h4, h5, h6, td, th {
            color: #FFFFFF !important;
        }
        
        /* Streamlit Top Header & Toolbar Background Override */
        header[data-testid="stHeader"],
        [data-testid="stHeader"],
        .stAppHeader,
        .stHeader,
        div[data-testid="stHeader"],
        div[data-testid="stToolbar"],
        .stApp > header {
            background-color: #0E1117 !important;
            background: #0E1117 !important;
            color: #FFFFFF !important;
        }
        
        /* Remove top decoration strip */
        div[data-testid="stDecoration"] {
            background-image: none !important;
            background-color: #0E1117 !important;
        }
        
        /* Header icons & text styling */
        [data-testid="stHeader"] button,
        [data-testid="stHeader"] svg,
        [data-testid="stHeader"] span,
        [data-testid="stHeader"] a {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }
        
        /* Sidebar Customization - Sleek Pure Black */
        section[data-testid="stSidebar"] {
            background-color: #000000 !important;
            background: #000000 !important;
            border-right: 1px solid rgba(255, 255, 255, 0.15) !important;
            box-shadow: 6px 0 30px rgba(0, 0, 0, 0.9) !important;
        }
        
        section[data-testid="stSidebar"] * {
            color: #FFFFFF !important;
        }
        
        /* BaseWeb Selectbox / Multiselect Dropdown Controls (Dark Theme Fix) */
        [data-testid="stMultiSelect"],
        [data-testid="stSelectbox"],
        div[data-baseweb="select"],
        div[data-baseweb="select"] > div,
        div[data-baseweb="select"] *,
        div[data-baseweb="base-input"] {
            background-color: #161B22 !important;
            background: #161B22 !important;
            color: #FFFFFF !important;
        }

        div[data-baseweb="select"] {
            border: 1px solid rgba(56, 189, 248, 0.4) !important;
            border-radius: 10px !important;
        }

        /* Selected tags / pills inside Multiselect */
        span[data-baseweb="tag"],
        div[data-baseweb="tag"] {
            background: #EF4444 !important;
            background-color: #EF4444 !important;
            border: 1px solid #F87171 !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            margin: 2px !important;
        }

        span[data-baseweb="tag"] *,
        div[data-baseweb="tag"] * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }

        /* Dropdown Popup Menu */
        ul[data-baseweb="menu"],
        div[data-baseweb="popover"],
        div[data-baseweb="popover"] * {
            background-color: #161B22 !important;
            background: #161B22 !important;
            color: #FFFFFF !important;
        }

        li[data-baseweb="option"] {
            background-color: #161B22 !important;
            color: #FFFFFF !important;
        }

        li[data-baseweb="option"]:hover {
            background-color: rgba(56, 189, 248, 0.25) !important;
            color: #FFFFFF !important;
        }

        /* Plotly Chart Container Styling */
        .stPlotlyChart,
        div[data-testid="stPlotlyChart"] {
            background-color: #0E1117 !important;
            background: #0E1117 !important;
            border-radius: 14px !important;
            border: 1px solid rgba(56, 189, 248, 0.25) !important;
            padding: 6px !important;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4) !important;
            width: 100% !important;
            overflow: visible !important;
        }

        /* Folium Map Popup Content Fix */
        .leaflet-popup-content, .leaflet-popup-content * {
            color: #1E293B !important;
        }

        /* Navigation Items Styling */
        section[data-testid="stSidebar"] ul[data-testid="stSidebarNavItems"] li a,
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a,
        section[data-testid="stSidebar"] .stRadio label {
            border-radius: 12px !important;
            margin: 4px 6px !important;
            padding: 10px 14px !important;
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            background: rgba(255, 255, 255, 0.05) !important;
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }

        section[data-testid="stSidebar"] ul[data-testid="stSidebarNavItems"] li a:hover,
        section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
            background: linear-gradient(90deg, rgba(56, 189, 248, 0.25) 0%, rgba(0, 230, 118, 0.2) 100%) !important;
            border-color: #00E676 !important;
            transform: translateX(6px) !important;
            box-shadow: 0 4px 20px rgba(0, 230, 118, 0.3) !important;
            color: #FFFFFF !important;
        }

        section[data-testid="stSidebar"] [aria-current="page"],
        section[data-testid="stSidebar"] ul[data-testid="stSidebarNavItems"] li a[aria-current="page"] {
            background: linear-gradient(90deg, rgba(0, 230, 118, 0.3) 0%, rgba(56, 189, 248, 0.25) 100%) !important;
            border: 1px solid #00E676 !important;
            border-left: 6px solid #00E676 !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            box-shadow: 0 6px 25px rgba(0, 230, 118, 0.35) !important;
        }
        
        /* Metric Cards */
        div[data-testid="metric-container"], [data-testid="stMetric"] {
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03)) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 14px !important;
            padding: 16px 20px !important;
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4) !important;
            backdrop-filter: blur(12px) !important;
        }
        
        [data-testid="stMetricLabel"], [data-testid="stMetricLabel"] *, [data-testid="stMetricLabel"] label, [data-testid="stMetricLabel"] p, div[data-testid="metric-container"] label {
            color: #FFFFFF !important;
            font-size: 0.95rem !important;
            font-weight: 700 !important;
            opacity: 1 !important;
        }
        
        [data-testid="stMetricValue"], [data-testid="stMetricValue"] *, [data-testid="stMetricValue"] div, [data-testid="stMetricValue"] span, div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
            color: #FFFFFF !important;
            font-size: 1.9rem !important;
            font-weight: 800 !important;
            opacity: 1 !important;
        }
        
        /* Section Cards */
        .glass-card {
            background: rgba(22, 27, 34, 0.85);
            border: 1px solid rgba(56, 189, 248, 0.3);
            border-radius: 16px;
            padding: 26px;
            margin-bottom: 22px;
            box-shadow: 0 8px 28px rgba(0, 0, 0, 0.5);
            color: #FFFFFF !important;
        }
        
        .glass-card p, .glass-card li, .glass-card ul, .glass-card b, .glass-card strong {
            color: #FFFFFF !important;
        }
        
        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #FFFFFF !important;
            font-weight: 800 !important;
        }
        
        .stButton>button {
            background: linear-gradient(90deg, #00C853, #00E676);
            color: #000000 !important;
            font-weight: 800;
            border-radius: 10px;
            border: none;
            padding: 10px 24px;
            box-shadow: 0 4px 15px rgba(0, 230, 118, 0.4);
        }
    </style>
    """, unsafe_allow_html=True)


