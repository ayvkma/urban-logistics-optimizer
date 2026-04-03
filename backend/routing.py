import json
from utils.haversine import calculate_distance

# Define the depot location (Shinjuku Station, Tokyo)
DEPOT_LOCATION = {'latitude': 35.6901, 'longitude': 139.7004}
TRUCK_CAPACITY_KG = 100.00

def calculate_route(df, depot_location=DEPOT_LOCATION):
    """Calculate the delivery route using a nearest neighbor heuristic."""
    
    visited_locations = set()
    total_distance_traveled = 0.0
    route_sequence = []
    current_location = depot_location
    truck_capacity_used = 0.0
    current_trip_id = 1
    
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
            if truck_capacity_used + df.loc[next_location_index, 'package_weight_kg'] <= TRUCK_CAPACITY_KG:
                truck_capacity_used += df.loc[next_location_index, 'package_weight_kg']
            else:
                total_distance_traveled += calculate_distance(
                    current_location['latitude'], current_location['longitude'],
                    depot_location['latitude'], depot_location['longitude']
                )
                current_location = depot_location
                truck_capacity_used = 0.0
                current_trip_id += 1
                continue
            visited_locations.add(next_location_index)
            total_distance_traveled += min_distance
            route_sequence.append({"order_id": df.loc[next_location_index, 'order_id'], "trip_id": current_trip_id})
            current_location = {'latitude': df.loc[next_location_index, 'latitude'], 'longitude': df.loc[next_location_index, 'longitude']}  
        else:
            break
        
    # Return to the depot
    total_distance_traveled += calculate_distance(
        current_location['latitude'], current_location['longitude'],
        depot_location['latitude'], depot_location['longitude']
    )
    
    return {"route_sequence": route_sequence, "total_distance_traveled": total_distance_traveled}


if __name__ == "__main__":
    import pandas as pd
    
    df = pd.read_csv("data/processed/tokyo_orders_clean.csv")
    result = calculate_route(df)
   
    # Create a clean list of dictionaries for the frontend
    frontend_data = []
    for item in result['route_sequence']:
        order_id = item['order_id']
        trip_id = item['trip_id']
        row = df[df['order_id'] == order_id].iloc[0]
        frontend_data.append({
            "order_id": order_id,
            "trip_id": trip_id,
            "latitude": row['latitude'],
            "longitude": row['longitude'],
            "priority": row['priority']
        })

    # Save to the React src folder
    output_path = "frontend/src/route_data.json"
    with open(output_path, "w") as f:
        json.dump(frontend_data, f, indent=4)

    print(f"Route data saved to {output_path}")