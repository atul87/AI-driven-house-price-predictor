import streamlit as st
import pickle
import json
import numpy as np
import pandas as pd
import altair as alt
from data import create_usertable, add_userdata, login_user
import sqlite3

# --- Global variables ---
__model = None
__data_columns = None
__locations = None
__cleaned_data = None

def load_artifacts():
    """
    Model aur data files ko load karne wala function.
    """
    global __model, __data_columns, __locations, __cleaned_data
    if __model and __data_columns and __cleaned_data is not None:
        return

    # st.spinner("Application resources load ") # Removed spinner to avoid UI flicker on reload
    try:
        with open('banglore_home_prices_model.pickle', 'rb') as f:
            __model = pickle.load(f)

        with open('columns.json', 'r') as f:
            data = json.load(f)
            __data_columns = data['columns']
            __locations = __data_columns[3:]
            
        __cleaned_data = pd.read_csv('cleaned_house_data.csv')
    
    except FileNotFoundError as e:
        st.error(f"Critical Error: Resource file missing: {e}.")
        st.stop()

def predict_price(location, sqft, bath, bhk):
    """
    User ke input ke aadhar par ghar ki keemat predict karta hai.
    """
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0], x[1], x[2] = sqft, bath, bhk
    if loc_index >= 0:
        x[loc_index] = 1

    return round(__model.predict([x])[0], 2)

def view_all_users():
    """
    Database se saare users ki jaankari nikalta hai.
    """
    conn = sqlite3.connect('user_data.db')
    df = pd.read_sql_query("SELECT id, username, password FROM users", conn)
    conn.close()
    return df

# =====================================================================
# --- CUSTOM STYLING ---
# =====================================================================

def local_css():
    st.markdown("""
    <style>
        /* Import Google Font */
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

        html, body, [class*="css"]  {
            font-family: 'Outfit', sans-serif;
        }
        
        /* Global Background & Text */
        .stApp {
            background-color: #f8f9fa;
            color: #1f2937;
        }

        /* Headings */
        h1, h2, h3 {
            color: #111827;
            font-weight: 700;
        }
        
        /* Sidebar */
        [data-testid="stSidebar"] {
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
        }
        
        /* Buttons */
        .stButton > button {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.1), 0 2px 4px -1px rgba(79, 70, 229, 0.06);
        }
        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.2), 0 4px 6px -2px rgba(79, 70, 229, 0.1);
            background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        }

        /* Inputs */
        .stTextInput > div > div > input, .stNumberInput > div > div > input, .stSelectbox > div > div > div {
            border-radius: 8px;
            border: 1px solid #d1d5db;
            background-color: white;
            color: #374151;
        }
        .stTextInput > div > div > input:focus, .stNumberInput > div > div > input:focus {
            border-color: #6366f1;
            box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.2);
        }

        /* Cards/Containers */
        .css-1r6slb0 {
            background-color: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
            border: 1px solid #f3f4f6;
        }
        
        /* Custom Success Message */
        .stSuccess {
            background-color: #ecfdf5;
            color: #065f46;
            border: 1px solid #a7f3d0;
            border-radius: 8px;
        }
        
        /* Custom Info Message */
        .stInfo {
            background-color: #eff6ff;
            color: #1e40af;
            border: 1px solid #bfdbfe;
            border-radius: 8px;
        }

    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# --- APPLICATION PAGES ---
# =====================================================================

def home_page():
    st.markdown("<h1 style='text-align: center; margin-bottom: 2rem;'>🏡 Bangalore House Price Predictor</h1>", unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; margin-bottom: 3rem; color: #6b7280; max-width: 600px; margin-left: auto; margin-right: auto;'>
        Get an instant, AI-powered estimate for your dream home in Bangalore. 
        Simply enter the details below to get started.
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns(2, gap="large")
        
        with col1:
            st.markdown("### 📍 Property Details")
            location = st.selectbox("Location", __locations, help="Select the locality in Bangalore")
            sqft = st.number_input("Total Square Feet", min_value=300, max_value=50000, value=1200, step=50, help="Total super built-up area")
        
        with col2:
            st.markdown("### 🏠 Configuration")
            bhk = st.slider("Bedrooms (BHK)", 1, 10, 2, help="Number of bedrooms")
            bath = st.slider("Bathrooms", 1, 10, 2, help="Number of bathrooms")

        st.markdown("---")
        
        # Center the button
        col_spacer_l, col_btn, col_spacer_r = st.columns([1, 2, 1])
        with col_btn:
            predict_btn = st.button("✨ Predict Price", type="primary", use_container_width=True)

    if predict_btn:
        with st.spinner('Crunching the numbers...'):
            predicted_price = predict_price(location, sqft, bath, bhk)
            
            st.markdown(f"""
            <div style='background: linear-gradient(135deg, #10b981 0%, #059669 100%); padding: 2rem; border-radius: 12px; color: white; text-align: center; margin-top: 2rem; box-shadow: 0 10px 15px -3px rgba(16, 185, 129, 0.3);'>
                <h3 style='color: white; margin: 0; font-weight: 400;'>Estimated Price</h3>
                <h1 style='color: white; font-size: 3.5rem; margin: 0.5rem 0;'>₹ {predicted_price} Lakhs</h1>
                <p style='margin: 0; opacity: 0.9;'>for a {bhk} BHK in {location}</p>
            </div>
            """, unsafe_allow_html=True)
            
            if __cleaned_data is not None:
                st.markdown("### 📊 Price Trends")
                location_data = __cleaned_data[__cleaned_data['location'] == location]
                
                if not location_data.empty:
                    avg_prices_by_bhk = location_data.groupby('bhk')['price'].mean().reset_index()
                    avg_prices_by_bhk['Color'] = avg_prices_by_bhk['bhk'].apply(lambda x: 'Your Selection' if x == bhk else 'Average')
                    
                    chart = alt.Chart(avg_prices_by_bhk).mark_bar(cornerRadiusTopLeft=5, cornerRadiusTopRight=5).encode(
                        x=alt.X('bhk:O', title='Number of Bedrooms (BHK)', axis=alt.Axis(labelAngle=0)),
                        y=alt.Y('price', title='Average Price (Lakhs)'),
                        color=alt.Color('Color', scale={'domain': ['Average', 'Your Selection'], 'range': ['#cbd5e1', '#10b981']}, legend=None),
                        tooltip=[alt.Tooltip('bhk', title='BHK'), alt.Tooltip('price', title='Avg. Price (Lakhs)', format='$.2f')]
                    ).properties(
                        title=f"Average Property Prices in {location}",
                        height=300
                    ).configure_axis(
                        grid=False,
                        labelFont='Outfit',
                        titleFont='Outfit'
                    ).configure_view(
                        strokeWidth=0
                    )
                    
                    st.altair_chart(chart, use_container_width=True)
                else:
                    st.info(f"Not enough data to show price trends for '{location}'.")

def dataset_page():
    st.title("📖 Dataset Explorer")
    st.markdown("Explore the cleaned dataset used to train our prediction model.")
    
    if __cleaned_data is not None:
        st.dataframe(__cleaned_data, use_container_width=True, height=600)
        st.caption(f"Showing **{__cleaned_data.shape[0]}** rows and **{__cleaned_data.shape[1]}** columns.")
    else:
        st.warning("Dataset could not be loaded.")

def about_page():
    st.title("ℹ️ About This Project")
    
    st.markdown("""
    <div style='background-color: white; padding: 2rem; border-radius: 12px; border: 1px solid #e5e7eb;'>
        <p style='font-size: 1.1rem; line-height: 1.6;'>
            This application is an end-to-end data science project designed to predict house prices in Bangalore, India. 
            It leverages machine learning to provide accurate estimates based on real-world data.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 How It Works")
    st.markdown("""
    1. **Data Collection:** We use the "Bengaluru House Price Data" from Kaggle.
    2. **Data Cleaning:** The raw data is processed to handle missing values, remove outliers, and standardize features.
    3. **Model Training:** A Linear Regression model is trained to understand the relationship between location, size, and price.
    4. **Prediction:** This app uses the trained model to generate instant price estimates for you.
    """)
    
    st.markdown("### 🛠️ Tech Stack")
    
    # Create columns for tech stack badges
    cols = st.columns(5)
    
    with cols[0]:
        st.markdown("""
        <div style='background-color: #eff6ff; color: #1d4ed8; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500; text-align: center; margin-bottom: 0.5rem;'>
            Python
        </div>
        """, unsafe_allow_html=True)
    
    with cols[1]:
        st.markdown("""
        <div style='background-color: #ecfdf5; color: #047857; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500; text-align: center; margin-bottom: 0.5rem;'>
            Scikit-learn
        </div>
        """, unsafe_allow_html=True)
    
    with cols[2]:
        st.markdown("""
        <div style='background-color: #fff7ed; color: #c2410c; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500; text-align: center; margin-bottom: 0.5rem;'>
            Streamlit
        </div>
        """, unsafe_allow_html=True)
    
    with cols[3]:
        st.markdown("""
        <div style='background-color: #f5f3ff; color: #6d28d9; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500; text-align: center; margin-bottom: 0.5rem;'>
            Altair
        </div>
        """, unsafe_allow_html=True)
    
    with cols[4]:
        st.markdown("""
        <div style='background-color: #fdf2f8; color: #be185d; padding: 0.5rem 1rem; border-radius: 20px; font-weight: 500; text-align: center; margin-bottom: 0.5rem;'>
            Pandas
        </div>
        """, unsafe_allow_html=True)


def admin_page():
    st.title("🔑 Admin Dashboard")
    st.markdown("Manage and view registered users.")
    
    user_data = view_all_users()
    st.dataframe(user_data, use_container_width=True)

# =====================================================================
# --- MAIN APP LOGIC AND ROUTING ---
# =====================================================================

def main():
    st.set_page_config(page_title="Bangalore House Price Predictor", page_icon="🏡", layout="wide")
    local_css()

    # --- Session State Initialization ---
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = ''
        st.session_state['role'] = '' 
    if 'page' not in st.session_state:
        st.session_state['page'] = 'Home'

    # --- Routing Logic ---
    if st.session_state['logged_in']:
        load_artifacts()

        # --- Sidebar Navigation ---
        with st.sidebar:
            st.markdown(f"### 👋 Hi, {st.session_state['username']}!")
            st.markdown("---")
            
            if st.button("🏠 Home", use_container_width=True): st.session_state.page = "Home"
            if st.button("📖 Dataset", use_container_width=True): st.session_state.page = "Data Set"
            if st.button("ℹ️ About", use_container_width=True): st.session_state.page = "About"
            
            if st.session_state['role'] == 'admin':
                st.markdown("---")
                if st.button("🔑 Admin Panel", use_container_width=True):
                    st.session_state.page = "Admin"
            
            st.markdown("---")
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state['logged_in'] = False
                st.session_state['username'] = ''
                st.session_state['role'] = ''
                st.session_state['page'] = 'Home'
                st.rerun()

        # --- Page Display ---
        if st.session_state.page == "Home": home_page()
        elif st.session_state.page == "Data Set": dataset_page()
        elif st.session_state.page == "About": about_page()
        elif st.session_state.page == "Admin": admin_page()

    else:
        # --- LOGIN/SIGNUP VIEW ---
        col1, col2 = st.columns([1, 1.5])
        
        with col1:
            st.markdown("""
            <div style='margin-top: 4rem;'>
                <h1 style='font-size: 3rem; line-height: 1.2;'>Welcome to <br><span style='color: #4f46e5;'>House Price Predictor</span></h1>
                <p style='font-size: 1.2rem; color: #6b7280; margin-top: 1rem;'>
                    Discover the true value of properties in Bangalore with our advanced AI model.
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("<div style='background-color: white; padding: 2rem; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06); margin-top: 2rem; max-width: 400px; margin-left: auto; margin-right: auto;'>", unsafe_allow_html=True)
            
            choice = st.radio("Select Action", ["Login", "Sign Up"], horizontal=True, label_visibility="collapsed")
            st.markdown("---")
            
            create_usertable()

            if choice == "Login":
                st.subheader("Welcome Back")
                username = st.text_input("Username", placeholder="Enter your username")
                password = st.text_input("Password", type='password', placeholder="Enter your password")
                
                if st.button("Login", use_container_width=True, type="primary"):
                    if login_user(username, password):
                        st.session_state['logged_in'] = True
                        st.session_state['username'] = username
                        if username == 'admin' and password == 'admin123':
                            st.session_state['role'] = 'admin'
                        else:
                            st.session_state['role'] = 'user'
                        st.rerun()
                    else:
                        st.error("Invalid username or password")

            elif choice == "Sign Up":
                st.subheader("Create Account")
                new_user = st.text_input("Choose Username", placeholder="e.g., john_doe")
                new_password = st.text_input("Choose Password", type='password', placeholder="Minimum 6 characters")
                
                if st.button("Create Account", use_container_width=True, type="primary"):
                    if add_userdata(new_user, new_password):
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists. Please try another.")
            
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == '__main__':
    main()



