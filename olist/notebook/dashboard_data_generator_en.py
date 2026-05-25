#!/usr/bin/env python3
"""
Brazil Delivery Time Dashboard Data Generator (English Version)
Fetches data from BigQuery and generates JSON file for HTML dashboard
"""

import pandas as pd
import json
import datetime
from google.cloud import bigquery
import os

class DeliveryDashboardDataGenerator:
    def __init__(self, project_id=None):
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID", "brazil-olist")
        self.client = bigquery.Client(project=self.project_id)
        
    def fetch_delivery_data(self):
        """Fetch delivery time data from BigQuery"""
        print("Loading data from BigQuery...")
        
        query = f"""
        WITH delivery_data AS (
            SELECT 
                zip_code_prefix,
                avg_latitude,
                avg_longitude,
                city,
                state,
                avg_delivery_days,
                CASE 
                    WHEN avg_delivery_days <= 10 THEN 'Fast'
                    WHEN avg_delivery_days <= 15 THEN 'Medium'
                    WHEN avg_delivery_days <= 20 THEN 'Slow'
                    ELSE 'Very Slow'
                END as delivery_category,
                order_count
            FROM `{self.project_id}.dbt_output.fct_delivery_time_by_zip`
            WHERE avg_delivery_days IS NOT NULL
              AND avg_latitude IS NOT NULL
              AND avg_longitude IS NOT NULL
              AND state IS NOT NULL
              AND order_count >= 5
        ),
        revenue_data AS (
            SELECT 
                zip_code_prefix,
                total_revenue,
                order_count as revenue_order_count
            FROM `{self.project_id}.dbt_output.fct_geo_revenue`
            WHERE total_revenue IS NOT NULL
        )
        SELECT 
            d.*,
            COALESCE(r.total_revenue, 0) as total_revenue,
            CASE 
                WHEN r.total_revenue IS NULL THEN 'No Revenue'
                WHEN r.total_revenue <= 1000 THEN 'Low'
                WHEN r.total_revenue <= 5000 THEN 'Medium'
                WHEN r.total_revenue <= 20000 THEN 'High'
                ELSE 'Very High'
            END as revenue_category
        FROM delivery_data d
        LEFT JOIN revenue_data r ON d.zip_code_prefix = r.zip_code_prefix
        ORDER BY d.avg_delivery_days DESC
        """
        
        try:
            df = self.client.query(query).to_dataframe()
            print(f"Successfully loaded {len(df)} records")
            return df
        except Exception as e:
            print(f"Failed to fetch data from BigQuery: {e}")
            return self.generate_sample_data()
    
    def generate_sample_data(self):
        """Generate sample data (when BigQuery is unavailable)"""
        print("Generating sample data...")
        
        import random
        import numpy as np
        
        # Major Brazilian cities data
        cities_data = [
            {'city': 'São Paulo', 'state': 'SP', 'lat': -23.5505, 'lon': -46.6333},
            {'city': 'Rio de Janeiro', 'state': 'RJ', 'lat': -22.9068, 'lon': -43.1729},
            {'city': 'Belo Horizonte', 'state': 'MG', 'lat': -19.9191, 'lon': -43.9386},
            {'city': 'Salvador', 'state': 'BA', 'lat': -12.9714, 'lon': -38.5014},
            {'city': 'Recife', 'state': 'PE', 'lat': -8.0476, 'lon': -34.8770},
            {'city': 'Fortaleza', 'state': 'CE', 'lat': -3.7319, 'lon': -38.5267},
            {'city': 'Brasília', 'state': 'DF', 'lat': -15.8267, 'lon': -47.9218},
            {'city': 'Curitiba', 'state': 'PR', 'lat': -25.4284, 'lon': -49.2733},
            {'city': 'Porto Alegre', 'state': 'RS', 'lat': -30.0346, 'lon': -51.2177},
            {'city': 'Manaus', 'state': 'AM', 'lat': -3.1190, 'lon': -60.0217},
            {'city': 'Belém', 'state': 'PA', 'lat': -1.4558, 'lon': -48.5044},
            {'city': 'Goiânia', 'state': 'GO', 'lat': -16.6869, 'lon': -49.2648},
            {'city': 'Campinas', 'state': 'SP', 'lat': -22.9099, 'lon': -47.0626},
            {'city': 'São Luís', 'state': 'MA', 'lat': -2.5387, 'lon': -44.2825},
            {'city': 'Maceió', 'state': 'AL', 'lat': -9.6658, 'lon': -35.7353},
            {'city': 'Natal', 'state': 'RN', 'lat': -5.7945, 'lon': -35.2110},
            {'city': 'João Pessoa', 'state': 'PB', 'lat': -7.1195, 'lon': -34.8450},
            {'city': 'Aracaju', 'state': 'SE', 'lat': -10.9472, 'lon': -37.0731},
            {'city': 'Teresina', 'state': 'PI', 'lat': -5.0892, 'lon': -42.8019},
            {'city': 'Campo Grande', 'state': 'MS', 'lat': -20.4697, 'lon': -54.6201}
        ]
        
        data = []
        for i, city_info in enumerate(cities_data):
            # Generate multiple ZIP areas for each city
            for j in range(random.randint(3, 8)):
                zip_prefix = f"{(i+1)*10000 + j*1000:05d}"
                
                # Generate random coordinates around the city
                lat_offset = random.uniform(-0.5, 0.5)
                lon_offset = random.uniform(-0.5, 0.5)
                
                # Generate delivery days (remote areas have longer delivery times)
                base_days = random.uniform(5, 25)
                if city_info['state'] in ['AM', 'PA', 'AC', 'RO', 'RR', 'AP']:  # Northern states
                    base_days += random.uniform(5, 15)
                elif city_info['state'] in ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']:  # Northeastern states
                    base_days += random.uniform(2, 8)
                
                # Categorize delivery time (English categories)
                if base_days <= 10:
                    category = 'Fast'
                elif base_days <= 15:
                    category = 'Medium'
                elif base_days <= 20:
                    category = 'Slow'
                else:
                    category = 'Very Slow'
                
                data.append({
                    'zip_code_prefix': zip_prefix,
                    'avg_latitude': city_info['lat'] + lat_offset,
                    'avg_longitude': city_info['lon'] + lon_offset,
                    'city': city_info['city'],
                    'state': city_info['state'],
                    'avg_delivery_days': round(base_days, 1),
                    'delivery_category': category,
                    'order_count': random.randint(10, 200)
                })
        
        return pd.DataFrame(data)
    
    def process_data(self, df):
        """Process data and generate statistics"""
        # Ensure correct data types
        df['avg_delivery_days'] = pd.to_numeric(df['avg_delivery_days'], errors='coerce')
        df['order_count'] = pd.to_numeric(df['order_count'], errors='coerce')
        
        # Remove invalid data
        df = df.dropna(subset=['avg_delivery_days', 'avg_latitude', 'avg_longitude'])
        
        # Generate summary statistics
        stats = {
            'total_regions': len(df),
            'total_cities': len(df['city'].unique()),
            'total_states': len(df['state'].unique()),
            'avg_delivery_days': round(df['avg_delivery_days'].mean(), 1),
            'min_delivery_days': round(df['avg_delivery_days'].min(), 1),
            'max_delivery_days': round(df['avg_delivery_days'].max(), 1),
            'total_orders': int(df['order_count'].sum()),
            'last_updated': datetime.datetime.now().isoformat()
        }
        
        return df, stats
    
    def generate_dashboard_data(self, output_file='dashboard_data.json'):
        """Generate dashboard data file"""
        # Get data
        df = self.fetch_delivery_data()
        
        # Process data
        df, stats = self.process_data(df)
        
        # Convert to JSON format
        data_dict = {
            'stats': stats,
            'data': df.to_dict('records'),
            'states': sorted(df['state'].unique().tolist()),
            'cities': sorted(df['city'].unique().tolist()),
            'categories': sorted(df['delivery_category'].unique().tolist())
        }
        
        # Save to file
        output_path = os.path.join(os.path.dirname(__file__), output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=2)
        
        print(f"Data saved to: {output_path}")
        print(f"Total records: {len(df)}")
        print(f"States covered: {stats['total_states']}")
        print(f"Average delivery days: {stats['avg_delivery_days']}")
        
        return output_path

def main():
    """Main function"""
    generator = DeliveryDashboardDataGenerator()
    generator.generate_dashboard_data()

if __name__ == "__main__":
    main()