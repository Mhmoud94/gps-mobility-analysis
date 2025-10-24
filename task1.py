"""
GPS Data Processing - Task 1
Course: AMI23K - Lab 2
"""

import pandas as pd
import numpy as np
from pathlib import Path
import re
from math import radians, sin, cos, sqrt, atan2

# ============================================================================
# CONFIGURATION
# ============================================================================

INPUT_FOLDER = r"C:\Users\Mhmou\Desktop\Lab report2 D.collection\data-1\data"
OUTPUT_FOLDER = r"C:\Users\Mhmou\Desktop\Lab report2 D.collection\data-1\results"

# ============================================================================


def parse_gsd_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    trip_pattern = r'\[(\d+),(\d{4}-\d{2}-\d{2}:\d{2}:\d{2}:\d{2})\]'
    all_data = []
    
    for trip_match in re.finditer(trip_pattern, content):
        trip_id = trip_match.group(1)
        trip_start_time = trip_match.group(2)
        
        start_pos = trip_match.end()
        next_trip = re.search(trip_pattern, content[start_pos:])
        if next_trip:
            end_pos = start_pos + next_trip.start()
        else:
            end_pos = len(content)
        
        trip_data = content[start_pos:end_pos]
        point_pattern = r'(\d+)=(\d+),(\d+),(\d+),(\d+),(-?\d+),(-?\d+)'
        
        for point_match in re.finditer(point_pattern, trip_data):
            point_id = point_match.group(1)
            lat_raw = int(point_match.group(2))
            lon_raw = int(point_match.group(3))
            time_raw = point_match.group(4)
            date_raw = point_match.group(5)
            speed_raw = int(point_match.group(6))
            altitude_raw = int(point_match.group(7))
            
            lat_degrees = lat_raw // 100000
            lat_minutes = (lat_raw % 100000) / 1000
            latitude = lat_degrees + (lat_minutes / 60)
            
            lon_degrees = lon_raw // 100000
            lon_minutes = (lon_raw % 100000) / 1000
            longitude = lon_degrees + (lon_minutes / 60)
            
            time_str = time_raw.zfill(6)
            time_formatted = f"{time_str[0:2]}:{time_str[2:4]}:{time_str[4:6]}"
            
            date_str = date_raw.zfill(6)
            year = "20" + date_str[4:6]
            month = date_str[2:4]
            day = date_str[0:2]
            date_formatted = f"{year}-{month}-{day}"
            
            speed_kmh = speed_raw / 100
            altitude = altitude_raw if altitude_raw != -1 else None
            
            all_data.append({
                'TRIP_ID': trip_id,
                'POINT_ID': point_id,
                'USER_ID': Path(file_path).stem,
                'Y_COORDINA': latitude,
                'X_COORDINA': longitude,
                'TIME': time_formatted,
                'DATE': date_formatted,
                'SPEED': speed_kmh,
                'HEIGHT': altitude,
                'DATETIME': f"{date_formatted} {time_formatted}"
            })
    
    return pd.DataFrame(all_data)


def haversine_distance(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    r = 6371
    return r * c


def calculate_metrics(df):
    df['DATETIME_OBJ'] = pd.to_datetime(df['DATETIME'])
    df['DISTANCE_KM'] = 0.0
    df['TIME_DIFF_SEC'] = 0.0
    df['SPEED_CALC'] = 0.0
    df['ACCELERATION'] = 0.0
    
    for trip_id in df['TRIP_ID'].unique():
        trip_mask = df['TRIP_ID'] == trip_id
        trip_indices = df[trip_mask].index
        
        for i in range(len(trip_indices) - 1):
            curr_idx = trip_indices[i]
            next_idx = trip_indices[i + 1]
            
            distance = haversine_distance(
                df.loc[curr_idx, 'Y_COORDINA'],
                df.loc[curr_idx, 'X_COORDINA'],
                df.loc[next_idx, 'Y_COORDINA'],
                df.loc[next_idx, 'X_COORDINA']
            )
            df.loc[next_idx, 'DISTANCE_KM'] = distance
            
            time_diff = (df.loc[next_idx, 'DATETIME_OBJ'] - 
                        df.loc[curr_idx, 'DATETIME_OBJ']).total_seconds()
            df.loc[next_idx, 'TIME_DIFF_SEC'] = time_diff
            
            if time_diff > 0:
                speed_calc = (distance / time_diff) * 3600
                df.loc[next_idx, 'SPEED_CALC'] = speed_calc
            
            if time_diff > 0:
                speed_diff = df.loc[next_idx, 'SPEED'] - df.loc[curr_idx, 'SPEED']
                acceleration = speed_diff / time_diff
                df.loc[next_idx, 'ACCELERATION'] = acceleration
    
    return df


def calculate_trip_summary(df):
    trip_summary = []
    
    for trip_id in df['TRIP_ID'].unique():
        trip_data = df[df['TRIP_ID'] == trip_id].copy()
        total_distance = trip_data['DISTANCE_KM'].sum()
        
        if len(trip_data) > 1:
            start_time = trip_data['DATETIME_OBJ'].min()
            end_time = trip_data['DATETIME_OBJ'].max()
            duration_sec = (end_time - start_time).total_seconds()
            duration_min = duration_sec / 60
        else:
            duration_sec = 0
            duration_min = 0
        
        avg_speed = trip_data['SPEED'].mean()
        avg_acceleration = trip_data['ACCELERATION'].mean()
        max_speed = trip_data['SPEED'].max()
        
        trip_summary.append({
            'TRIP_ID': trip_id,
            'USER_ID': trip_data['USER_ID'].iloc[0],
            'NUM_POINTS': len(trip_data),
            'TOTAL_DISTANCE_KM': round(total_distance, 3),
            'DURATION_SEC': round(duration_sec, 2),
            'DURATION_MIN': round(duration_min, 2),
            'AVG_SPEED_KMH': round(avg_speed, 2),
            'MAX_SPEED_KMH': round(max_speed, 2),
            'AVG_ACCELERATION': round(avg_acceleration, 4),
            'START_TIME': trip_data['DATETIME'].min(),
            'END_TIME': trip_data['DATETIME'].max()
        })
    
    return pd.DataFrame(trip_summary)


def process_all_gsd_files(input_folder, output_folder):
    input_path = Path(input_folder)
    output_path = Path(output_folder)
    output_path.mkdir(exist_ok=True, parents=True)
    
    all_processed_data = []
    gsd_files = list(input_path.glob('*.gsd'))
    print(f"Found {len(gsd_files)} .gsd files to process")
    print()
    
    if len(gsd_files) == 0:
        print("ERROR: No .gsd files found!")
        print(f"Please check the INPUT_FOLDER path: {input_folder}")
        return None, None
    
    for gsd_file in gsd_files:
        print(f"Processing {gsd_file.name}...")
        try:
            df = parse_gsd_file(gsd_file)
            if len(df) > 0:
                df = calculate_metrics(df)
                all_processed_data.append(df)
                print(f"  ✓ Processed {len(df)} GPS points from {df['TRIP_ID'].nunique()} trips")
            else:
                print(f"  ⚠ No data found in {gsd_file.name}")
        except Exception as e:
            print(f"  ✗ Error processing {gsd_file.name}: {e}")
    
    print()
    
    if all_processed_data:
        combined_df = pd.concat(all_processed_data, ignore_index=True)
        combined_df = combined_df.sort_values(['USER_ID', 'TRIP_ID', 'POINT_ID'])
        combined_df = combined_df.reset_index(drop=True)
        combined_df.insert(0, 'ID', range(1, len(combined_df) + 1))
        
        output_columns = [
            'ID', 'TRIP_ID', 'USER_ID', 'Y_COORDINA', 'X_COORDINA', 
            'TIME', 'DATE', 'SPEED', 'HEIGHT', 'SPEED_CALC', 'DISTANCE_KM',
            'TIME_DIFF_SEC', 'ACCELERATION'
        ]
        
        output_file = output_path / 'gps_processed_data.csv'
        combined_df[output_columns].to_csv(output_file, index=False)
        print(f"✓ Saved detailed GPS data to: {output_file}")
        print(f"  Total records: {len(combined_df)}")
        
        excel_file = output_path / 'gps_processed_data.xlsx'
        combined_df[output_columns].to_excel(excel_file, index=False)
        print(f"✓ Saved Excel file to: {excel_file}")
        
        trip_summary = calculate_trip_summary(combined_df)
        summary_file = output_path / 'trip_summary.csv'
        trip_summary.to_csv(summary_file, index=False)
        print(f"✓ Saved trip summary to: {summary_file}")
        print(f"  Total trips: {len(trip_summary)}")
        
        print("\n" + "="*80)
        print("SAMPLE OF PROCESSED DATA (first 10 rows):")
        print("="*80)
        print(combined_df[output_columns].head(10).to_string())
        
        print("\n" + "="*80)
        print("TRIP SUMMARY (first 5 trips):")
        print("="*80)
        print(trip_summary.head(5).to_string())
        
        return combined_df, trip_summary
    else:
        print("ERROR: No data was processed!")
        return None, None


def main():
    print("="*80)
    print("GPS DATA PROCESSING - TASK 1")
    print("Course: AMI23K - Lab 2")
    print("="*80)
    print()
    print("Configured paths:")
    print(f"  INPUT:  {INPUT_FOLDER}")
    print(f"  OUTPUT: {OUTPUT_FOLDER}")
    print()
    
    df, summary = process_all_gsd_files(INPUT_FOLDER, OUTPUT_FOLDER)
    
    if df is not None:
        print("\n" + "="*80)
        print("PROCESSING COMPLETE! ✓")
        print("="*80)
        print()
        print("Your results have been saved to:")
        print(f"  • {OUTPUT_FOLDER}")
        print()
        print("Files created:")
        print("  1. gps_processed_data.csv")
        print("  2. gps_processed_data.xlsx")
        print("  3. trip_summary.csv")
        print()
        print("Next step: Run task2_gps_visualization.py")
    else:
        print("\n" + "="*80)
        print("PROCESSING FAILED ✗")
        print("="*80)
    
    print()
    input("Press Enter to close...")


if __name__ == "__main__":
    main()