import json
import os
from datetime import datetime
import pandas as pd


class DataManager:
    def __init__(self):
        self.data_dir = 'data/user_data'
        os.makedirs(self.data_dir, exist_ok=True)

    def save_user_data(self, user_id, data_type, data):
        """Save user data to JSON file"""
        filename = f"{self.data_dir}/{user_id}_{data_type}.json"

        # Convert data to serializable format
        if isinstance(data, pd.DataFrame):
            data = data.to_dict('records')

        with open(filename, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'data': data
            }, f)

    def load_user_data(self, user_id, data_type):
        """Load user data from JSON file"""
        filename = f"{self.data_dir}/{user_id}_{data_type}.json"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                if data_type in ['progress', 'analytics']:
                    return pd.DataFrame(data['data'])
                return data['data']
        return None
