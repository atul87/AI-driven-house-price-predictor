# 🏡 Bangalore House Price Predictor

An end-to-end machine learning web application that predicts house prices in Bangalore, India using Linear Regression.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red.svg)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-Latest-orange.svg)

## ✨ Features

- **AI-Powered Predictions**: Get instant house price estimates based on location, size, and amenities
- **Interactive UI**: Modern, responsive design with custom styling
- **User Authentication**: Secure login and signup system with SQLite database
- **Data Visualization**: Interactive charts showing price trends across different configurations
- **Admin Dashboard**: Special admin panel to view registered users
- **Real-time Updates**: Dynamic predictions based on user input

## 🚀 Demo

The application provides:

- Price prediction for 240+ locations in Bangalore
- Configurable parameters: Square feet, BHK, Bathrooms
- Visual price comparison charts
- Clean, modern interface with glassmorphism design

## 📋 Prerequisites

- Python 3.8 or higher
- pip package manager

## 🛠️ Installation

1. **Clone or download the repository**

   ```bash
   cd AI-Driven-House-Price-Estimator-main
   ```

2. **Install required dependencies**

   ```bash
   pip install streamlit pandas numpy scikit-learn altair
   ```

3. **Verify all files are present**
   - `app.py` - Main Streamlit application
   - `data.py` - Database helper functions
   - `banglore_home_prices_model.pickle` - Trained ML model
   - `columns.json` - Feature columns for the model
   - `cleaned_house_data.csv` - Cleaned dataset
   - `bengaluru_house_prices (1).csv` - Original dataset
   - `house_price.ipynb` - Jupyter notebook with model training code

## 🎯 Usage

1. **Start the application**

   ```bash
   streamlit run app.py
   ```

2. **Access the app**

   - Open your browser and navigate to `http://localhost:8501`

3. **Create an account**

   - Click on "Sign Up"
   - Enter a username and password
   - Click "Create Account"

4. **Login**

   - Enter your credentials
   - Click "Login"

5. **Get predictions**
   - Select a location from the dropdown
   - Enter the total square feet
   - Adjust BHK and bathrooms using sliders
   - Click "✨ Predict Price"

## 👥 User Roles

### Regular User

- Access to price prediction
- View dataset
- Read about the project

### Admin User

- All regular user features
- Access to admin dashboard
- View all registered users

**Admin Credentials:**

- Username: `admin`
- Password: `admin123`

## 📊 Dataset

The model is trained on the "Bengaluru House Price Data" from Kaggle, which includes:

- 13,000+ property listings
- Features: Location, size, total square feet, bathrooms, price
- 240+ unique locations in Bangalore

## 🧠 Model Information

- **Algorithm**: Linear Regression
- **Training Score**: ~80% accuracy
- **Features**:
  - Total square feet (numeric)
  - Number of bathrooms (numeric)
  - Number of bedrooms/BHK (numeric)
  - Location (one-hot encoded - 240+ categories)

## 📁 Project Structure

```
AI-Driven-House-Price-Estimator-main/
│
├── app.py                              # Main Streamlit application
├── data.py                             # Database operations
├── banglore_home_prices_model.pickle   # Trained ML model
├── columns.json                        # Model feature columns
├── cleaned_house_data.csv              # Processed dataset
├── bengaluru_house_prices (1).csv      # Original dataset
├── house_price.ipynb                   # Model training notebook
├── user_data.db                        # SQLite database (auto-created)
└── README.md                           # This file
```

## 🎨 UI/UX Features

- **Modern Design**: Custom CSS with Google Fonts (Outfit)
- **Responsive Layout**: Works on desktop and mobile
- **Color Scheme**: Professional purple and green gradient theme
- **Interactive Elements**: Hover effects, smooth transitions
- **Visual Feedback**: Loading spinners, success messages
- **Data Visualization**: Altair charts with custom styling

## 🔧 Technical Details

### Frontend

- **Framework**: Streamlit
- **Styling**: Custom CSS with modern design principles
- **Charts**: Altair for interactive visualizations

### Backend

- **Language**: Python 3.8+
- **ML Library**: Scikit-learn
- **Database**: SQLite3
- **Data Processing**: Pandas, NumPy

### Model Training

The model was trained using:

1. Data cleaning (removing nulls, outliers)
2. Feature engineering (extracting BHK, standardizing sqft)
3. One-hot encoding for location
4. Linear Regression with GridSearchCV for hyperparameter tuning

## 🐛 Troubleshooting

### App won't start

- Ensure all dependencies are installed: `pip install streamlit pandas numpy scikit-learn altair`
- Check Python version: `python --version` (should be 3.8+)

### Model/Data files missing

- Verify all files listed in Project Structure are present
- Re-run the Jupyter notebook to regenerate model files

### Login issues

- Database is created automatically on first run
- Check if `user_data.db` exists in the project directory

### Predictions seem incorrect

- Model is trained on Bangalore data from a specific time period
- Predictions are estimates based on historical data
- Outliers may affect predictions for very large/small properties

## 📝 License

This project is for educational purposes.

## 🤝 Contributing

This is a demonstration project. Feel free to fork and modify for your own use.

## 📧 Contact

For questions or issues, please refer to the project documentation.

## 🙏 Acknowledgments

- Dataset: Kaggle - Bengaluru House Price Data
- Framework: Streamlit
- ML Library: Scikit-learn
- Visualization: Altair

---

**Note**: This application provides price estimates based on historical data and should not be used as the sole basis for real estate decisions. Always consult with real estate professionals for accurate, current pricing information.
