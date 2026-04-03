from utils.haversine import calculate_distance

# Define the depot location (Shinjuku Station, Tokyo)
DEPOT_LOCATION = {'latitude': 35.6901, 'longitude': 139.7004}

def calculate_route(df, depot_location=DEPOT_LOCATION):
    """Calculate the delivery route using a nearest neighbor heuristic."""
    
    visited_locations = set()
    total_distance_traveled = 0.0
    route_sequence = []
    current_location = depot_location
    
    while len(visited_locations) < len(df):
        min_distance = float('inf')
        next_location_index = None
        for index, row in df.iterrows():
            if index not in visited_locations:
                distance_to_location = calculate_distance(
                    current_location['latitude'], current_location['longitude'],
                    row['latitude'], row['longitude']
                )
                if distance_to_location < min_distance:
                    min_distance = distance_to_location
                    next_location_index = index
                    
        if next_location_index is not None:
            visited_locations.add(next_location_index)
            total_distance_traveled += min_distance
            route_sequence.append(df.loc[next_location_index, 'order_id'])
            current_location = {'latitude': df.loc[next_location_index, 'latitude'], 'longitude': df.loc[next_location_index, 'longitude']}  
        else:
            break
        
    # Return to the depot
    total_distance_traveled += calculate_distance(
        current_location['latitude'], current_location['longitude'],
        depot_location['latitude'], depot_location['longitude']
    )
    
    return {"route_sequence": route_sequence, "total_distance_traveled": total_distance_traveled}

# Example usage:
# if __name__ == "__main__":
#     import pandas as pd
    
#     df = pd.read_csv("data/processed/tokyo_orders_clean.csv")
#     result = calculate_route(df)
#     print(result['route_sequence'][:5])
#     print(f"{result['total_distance_traveled'] / 1000:.2f} km")