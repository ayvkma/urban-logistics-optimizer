import random
import numpy as np
import pandas as pd

def generate_data():
    """Generates synthetic order data for Tokyo deliveries."""
    
    data = []
    ord_cnt = 1
    NUMBER_OF_ROWS = 100
    MIN_LATITUDE = 35.6805
    MAX_LATITUDE = 35.6895
    MIN_LONGITUDE = 139.6806
    MAX_LONGITUDE = 139.7028
    
    for i in range(NUMBER_OF_ROWS):
        data.append({
            'order_id': f'ORD-{ord_cnt:04d}',
            'latitude': round(random.uniform(MIN_LATITUDE, MAX_LATITUDE), 4),
            'longitude': round(random.uniform(MIN_LONGITUDE, MAX_LONGITUDE), 4),
            'package_weight_kg': round(random.uniform(0.5, 20), 2),
            'priority': random.choice(["Low", "Medium", "High"]),
        })
        ord_cnt += 1
    return pd.DataFrame(data)

data = generate_data()
# Introduce some NaN values in the latitude and longitude columns and a outlier in the latitude column.
nan_indices = data.sample(frac=0.05).index
data.loc[nan_indices, 'latitude'] = np.nan
data.loc[data.sample(n=1).index, 'longitude'] = np.nan
data.loc[data.sample(n=1).index, 'latitude'] = 999.99
# A duplicate row to test data cleaning steps later on.
random_row = data.sample(n=1)
final_data = pd.concat([data, random_row], ignore_index=True)
# Export the generated data to a CSV file.
final_data.to_csv('../data/raw/tokyo_orders_raw.csv', index=False)