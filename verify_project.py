import unittest
import os
import sqlite3
import pickle
import json
import numpy as np
import pandas as pd
from data import create_usertable, add_userdata, login_user

class TestHousePriceProject(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Setup temporary test database
        if os.path.exists('user_data.db.bak'):
            os.remove('user_data.db.bak')
        if os.path.exists('user_data.db'):
            # Backup existing db
            os.rename('user_data.db', 'user_data.db.bak')
        
        create_usertable()
        
        # Load Model Artifacts
        with open('banglore_home_prices_model.pickle', 'rb') as f:
            cls.model = pickle.load(f)
        with open('columns.json', 'r') as f:
            cls.data_columns = json.load(f)['columns']

    @classmethod
    def tearDownClass(cls):
        # Restore original db
        if os.path.exists('user_data.db'):
            os.remove('user_data.db')
        if os.path.exists('user_data.db.bak'):
            os.rename('user_data.db.bak', 'user_data.db')

    def test_01_database_operations(self):
        print("\nTesting Database Operations...")
        # Test Add User
        self.assertTrue(add_userdata('testuser', 'testpass'), "Failed to add user")
        self.assertFalse(add_userdata('testuser', 'newpass'), "Should not allow duplicate username")
        
        # Test Login
        self.assertTrue(login_user('testuser', 'testpass'), "Login failed with correct credentials")
        self.assertFalse(login_user('testuser', 'wrongpass'), "Login succeeded with wrong credentials")
        print("Database Operations: PASS")

    def test_02_model_prediction(self):
        print("\nTesting Model Prediction...")
        
        def predict(location, sqft, bath, bhk):
            try:
                loc_index = self.data_columns.index(location.lower())
            except ValueError:
                loc_index = -1

            x = np.zeros(len(self.data_columns))
            x[0], x[1], x[2] = sqft, bath, bhk
            if loc_index >= 0:
                x[loc_index] = 1

            return self.model.predict([x])[0]

        # Test case 1: Electronic City Phase II, 1000 sqft, 2 bath, 2 bhk
        # We expect a positive price
        price = predict('1st Phase JP Nagar', 1000, 2, 2)
        print(f"Predicted price for 1st Phase JP Nagar (1000sqft, 2bath, 2bhk): {price}")
        self.assertTrue(price > 0, "Predicted price should be positive")
        
        # Test case 2: Different location
        price2 = predict('Indira Nagar', 1000, 2, 2)
        print(f"Predicted price for Indira Nagar (1000sqft, 2bath, 2bhk): {price2}")
        self.assertTrue(price2 > 0, "Predicted price should be positive")
        
        # Logic check: Indira Nagar is generally more expensive than 1st Phase JP Nagar for same config
        # This is a loose check based on domain knowledge, but good for sanity
        # self.assertTrue(price2 > price, "Indira Nagar should be more expensive") 
        
        print("Model Prediction: PASS")

if __name__ == '__main__':
    unittest.main()
