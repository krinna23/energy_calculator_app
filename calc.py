import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Energy Usage Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    .metric-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 5px;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
    }
    .stButton > button:hover {
        background: linear-gradient(45deg, #2980b9, #3498db);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">⚡ Energy Usage Calculator</h1>', unsafe_allow_html=True)

# Sidebar for navigation
st.sidebar.title("📊 Navigation")
page = st.sidebar.selectbox("Choose a section:", ["Calculator", "Energy Tips", "About"])

if page == "Calculator":
    # Create two columns for better layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h2 class="section-header">👤 Personal Information</h2>', unsafe_allow_html=True)
        
        # Personal information form
        with st.form("personal_info"):
            name = st.text_input("Enter your name:", placeholder="John Doe")
            age = st.number_input("Enter your age:", min_value=1, max_value=120, value=25)
            city = st.text_input("Enter your city:", placeholder="Mumbai")
            area = st.text_input("Enter your area name:", placeholder="Bandra West")
            
            st.markdown('<h2 class="section-header">🏠 Housing Information</h2>', unsafe_allow_html=True)
            
            flat_tenament = st.selectbox("Are you living in:", ["Flat", "Tenement"])
            facility = st.selectbox("Select your facility type:", ["1BHK", "2BHK", "3BHK"])
            
            st.markdown('<h2 class="section-header">🔌 Appliances</h2>', unsafe_allow_html=True)
            
            ac = st.checkbox("Air Conditioner (AC)")
            fridge = st.checkbox("Refrigerator")
            wm = st.checkbox("Washing Machine")
            
            # Submit button
            submitted = st.form_submit_button("Calculate Energy Usage")
    
    with col2:
        if submitted and name and city and area:
            # Energy calculation logic
            cal_energy = 0
            
            # Base energy for lighting and fans
            if facility == "1BHK":
                cal_energy += 2 * 0.4 + 2 * 0.8  # 2 lights + 2 fans
                rooms = 1
            elif facility == "2BHK":
                cal_energy += 3 * 0.4 + 3 * 0.8  # 3 lights + 3 fans
                rooms = 2
            elif facility == "3BHK":
                cal_energy += 4 * 0.4 + 4 * 0.8  # 4 lights + 4 fans
                rooms = 3
            
            # Additional appliances
            appliances_energy = 0
            appliances_list = []
            
            if ac:
                appliances_energy += 3
                appliances_list.append("AC")
            if fridge:
                appliances_energy += 3
                appliances_list.append("Refrigerator")
            if wm:
                appliances_energy += 3
                appliances_list.append("Washing Machine")
            
            cal_energy += appliances_energy
            
            # Display results
            st.markdown('<h2 class="section-header">📊 Energy Usage Summary</h2>', unsafe_allow_html=True)
            
            # User information card
            st.markdown(f"""
            <div class="info-box">
                <h3>👤 Personal Details</h3>
                <p><strong>Name:</strong> {name}</p>
                <p><strong>Age:</strong> {age} years</p>
                <p><strong>Location:</strong> {area}, {city}</p>
                <p><strong>Housing:</strong> {facility} {flat_tenament}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Energy metrics
            st.markdown(f"""
            <div class="metric-container">
                <h2>Total Energy Consumption</h2>
                <h1>{cal_energy:.1f} kWh/day</h1>
                <p>Estimated Monthly: {cal_energy * 30:.1f} kWh</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Breakdown visualization
            st.markdown('<h3 class="section-header">📈 Energy Breakdown</h3>', unsafe_allow_html=True)
            
            # Create breakdown data
            base_energy = cal_energy - appliances_energy
            breakdown_data = {
                'Category': ['Lighting & Fans', 'Appliances'],
                'Energy (kWh/day)': [base_energy, appliances_energy],
                'Percentage': [
                    (base_energy / cal_energy) * 100 if cal_energy > 0 else 0,
                    (appliances_energy / cal_energy) * 100 if cal_energy > 0 else 0
                ]
            }
            
            # Pie chart
            fig = px.pie(
                values=breakdown_data['Energy (kWh/day)'],
                names=breakdown_data['Category'],
                title="Energy Consumption Breakdown",
                color_discrete_sequence=['#3498db', '#e74c3c']
            )
            fig.update_layout(
                font=dict(size=14),
                showlegend=True,
                height=400
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Appliances list
            if appliances_list:
                st.markdown('<h3 class="section-header">🔌 Active Appliances</h3>', unsafe_allow_html=True)
                for appliance in appliances_list:
                    st.markdown(f"✅ {appliance}")
            
            # Cost estimation
            st.markdown('<h3 class="section-header">💰 Cost Estimation</h3>', unsafe_allow_html=True)
            
            # Assuming average electricity rate in India
            rate_per_unit = 5.0  # Rs per kWh
            daily_cost = cal_energy * rate_per_unit
            monthly_cost = daily_cost * 30
            
            cost_col1, cost_col2 = st.columns(2)
            
            with cost_col1:
                st.metric("Daily Cost", f"₹{daily_cost:.2f}")
            
            with cost_col2:
                st.metric("Monthly Cost", f"₹{monthly_cost:.2f}")
            
            # Energy efficiency tips
            st.markdown('<h3 class="section-header">💡 Energy Saving Tips</h3>', unsafe_allow_html=True)
            
            tips = [
                "Use LED bulbs instead of incandescent bulbs",
                "Set AC temperature to 24°C for optimal efficiency",
                "Use ceiling fans along with AC to circulate air",
                "Unplug appliances when not in use",
                "Use natural light during daytime",
                "Regular maintenance of appliances improves efficiency"
            ]
            
            for tip in tips:
                st.markdown(f"• {tip}")
        
        elif submitted:
            st.warning("Please fill in all required fields (Name, City, Area)")

elif page == "Energy Tips":
    st.markdown('<h2 class="section-header">💡 Energy Saving Tips</h2>', unsafe_allow_html=True)
    
    tips_data = {
        "Appliance": ["Air Conditioner", "Refrigerator", "Washing Machine", "Lighting", "Water Heater"],
        "Energy Saving Tip": [
            "Set temperature to 24°C and use ceiling fans",
            "Keep door closed and maintain proper temperature",
            "Use cold water for washing when possible",
            "Switch to LED bulbs and use natural light",
            "Use solar water heater or reduce usage time"
        ],
        "Potential Savings": ["20-30%", "10-15%", "15-20%", "80%", "30-40%"]
    }
    
    df = pd.DataFrame(tips_data)
    st.dataframe(df, use_container_width=True)
    
    # Energy comparison chart
    st.markdown('<h3 class="section-header">📊 Appliance Energy Comparison</h3>', unsafe_allow_html=True)
    
    appliance_data = {
        'Appliance': ['AC', 'Refrigerator', 'Washing Machine', 'LED Lights', 'Ceiling Fan'],
        'Power (kW)': [1.5, 0.15, 0.5, 0.01, 0.075],
        'Hours/Day': [8, 24, 1, 6, 12]
    }
    
    appliance_df = pd.DataFrame(appliance_data)
    appliance_df['Energy (kWh/day)'] = appliance_df['Power (kW)'] * appliance_df['Hours/Day']
    
    fig = px.bar(
        appliance_df,
        x='Appliance',
        y='Energy (kWh/day)',
        title='Daily Energy Consumption by Appliance',
        color='Energy (kWh/day)',
        color_continuous_scale='viridis'
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif page == "About":
    st.markdown('<h2 class="section-header">ℹ️ About This App</h2>', unsafe_allow_html=True)
    
    st.markdown("""
    This Energy Usage Calculator helps you estimate your daily electricity consumption based on:
    
    - **Housing Type**: Different BHK configurations have different baseline energy needs
    - **Appliances**: Major appliances like AC, refrigerator, and washing machine
    - **Usage Patterns**: Estimates based on typical Indian household usage
    
    ### How It Works:
    
    1. **Base Energy**: Calculated based on lighting and fans for your BHK type
    2. **Appliance Energy**: Added based on selected appliances
    3. **Cost Estimation**: Uses average electricity rates in India
    
    ### Energy Calculation Formula:
    
    - **1BHK**: 2 lights (0.4 kW) + 2 fans (0.8 kW)
    - **2BHK**: 3 lights (0.4 kW) + 3 fans (0.8 kW)
    - **3BHK**: 4 lights (0.4 kW) + 4 fans (0.8 kW)
    - **Each Major Appliance**: +3 kWh/day
    
    ### Note:
    These are estimates based on typical usage patterns. Actual consumption may vary based on:
    - Appliance efficiency ratings
    - Usage hours
    - Local climate conditions
    - Personal habits
    """)
    
    st.markdown('<h3 class="section-header">🌱 Environmental Impact</h3>', unsafe_allow_html=True)
    
    st.markdown("""
    **Did you know?**
    - 1 kWh of electricity produces approximately 0.82 kg of CO₂
    - Reducing energy consumption by 20% can save hundreds of kg of CO₂ annually
    - LED bulbs use 80% less energy than incandescent bulbs
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit | Energy Usage Calculator v1.0")