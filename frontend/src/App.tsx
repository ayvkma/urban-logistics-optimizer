import React, { useMemo } from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline, CircleMarker } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import routeDataRaw from './route_data.json';
import "./App.css";

import L from 'leaflet';
import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
});

L.Marker.prototype.options.icon = DefaultIcon;

// 1. Define the Data Contract (TypeScript)
interface Order {
  order_id: string;
  trip_id: number;
  latitude: number;
  longitude: number;
  priority: string;
}

const routeData = routeDataRaw as Order[];
const DEPOT = { lat: 35.6901, lng: 139.7004 };

// A distinct color palette for our different trips
const TRIP_COLORS = ['#e6194B', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#42d4f4', '#f032e6', '#bfef45'];

const App: React.FC = () => {
  // Group orders by trip_id so we can draw separate polylines
  const trips = useMemo(() => {
    const grouped = new Map<number, [number, number][]>();
    
    routeData.forEach((order) => {
      if (!grouped.has(order.trip_id)) {
        // Start each new trip at the Depot
        grouped.set(order.trip_id, [[DEPOT.lat, DEPOT.lng]]);
      }
      grouped.get(order.trip_id)?.push([order.latitude, order.longitude]);
    });

    // Ensure every trip returns back to the Depot at the end
    grouped.forEach((coords) => {
      coords.push([DEPOT.lat, DEPOT.lng]);
    });

    return Array.from(grouped.entries());
  }, []);

  return (
    <div style={{ height: '100vh', width: '100vw' }}>
      {/* 3. Render the Map centered on Shinjuku */}
      <MapContainer center={[DEPOT.lat, DEPOT.lng]} zoom={13} scrollWheelZoom={true}>
       <TileLayer
          attribution='&copy; <a href="https://carto.com/attributions">CARTO</a>'
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
        />

        {/* 4. Mark the Depot clearly */}
        <Marker position={[DEPOT.lat, DEPOT.lng]}>
          <Popup>
            <strong>Distribution Center (Depot)</strong><br />
            Shinjuku, Tokyo
          </Popup>
        </Marker>

        {/* 5. Draw the colored routes for each Trip */}
        {trips.map(([tripId, coords], index) => (
          <Polyline 
            key={`trip-${tripId}`} 
            positions={coords} 
            pathOptions={{ color: TRIP_COLORS[index % TRIP_COLORS.length], weight: 4, opacity: 0.8 }} 
          />
        ))}

        {/* 6. Plot the individual delivery points */}
       {routeData.map((order) => {
          // Get the color for this specific trip
          const tripColor = TRIP_COLORS[(order.trip_id - 1) % TRIP_COLORS.length];
          
          return (
            <CircleMarker 
              key={order.order_id} 
              center={[order.latitude, order.longitude]}
              radius={6}
              pathOptions={{ 
                color: tripColor, 
                fillColor: tripColor, 
                fillOpacity: 0.8, 
                weight: 2 
              }}
            >
              <Popup>
                <strong>{order.order_id}</strong><br />
                Trip ID: {order.trip_id}<br />
                Priority: {order.priority}<br />
              </Popup>
            </CircleMarker>
          );
        })}
      </MapContainer>
    </div>
  );
};

export default App;