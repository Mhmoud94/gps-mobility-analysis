"""
GPS Data Visualization - Task 2
Course: AMI23K - Lab 2
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

CSV_FILE = r"C:\Users\Mhmou\Desktop\Lab report2 D.collection\data-1\results\gps_processed_data.csv"
OUTPUT_FOLDER = r"C:\Users\Mhmou\Desktop\Lab report2 D.collection\data-1\results\figures"

# ============================================================================


def visualize_gps_data(csv_file, output_folder=None):
    print("Loading GPS data...")
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"ERROR: File not found: {csv_file}")
        print("Please run Task 1 first!")
        return None
    
    print(f"✓ Loaded {len(df)} GPS points")
    print(f"  - Trips: {df['TRIP_ID'].nunique()}")
    print(f"  - Users: {df['USER_ID'].nunique()}")
    print()
    
    if output_folder is None:
        output_folder = Path(csv_file).parent / 'figures'
    else:
        output_folder = Path(output_folder)
    
    output_folder.mkdir(exist_ok=True, parents=True)
    
    # 1. LONGITUDE VS LATITUDE
    print("1. Creating longitude vs latitude plot...")
    plt.figure(figsize=(14, 10))
    scatter = plt.scatter(df['X_COORDINA'], df['Y_COORDINA'], 
                         c=df['SPEED'], cmap='viridis', 
                         alpha=0.6, s=10, edgecolors='none')
    plt.colorbar(scatter, label='Speed (km/h)')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.title('GPS Data Points - Longitude vs Latitude', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    fig_file = output_folder / 'longitude_vs_latitude.png'
    plt.savefig(fig_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {fig_file}")
    plt.close()
    
    # 2. TRIP TRAJECTORIES
    print("2. Creating trip trajectories...")
    plt.figure(figsize=(14, 10))
    trips = df['TRIP_ID'].unique()
    colors = plt.cm.tab20(np.linspace(0, 1, min(len(trips), 20)))
    for i, trip_id in enumerate(trips[:20]):
        trip_data = df[df['TRIP_ID'] == trip_id]
        color_idx = i % 20
        plt.plot(trip_data['X_COORDINA'], trip_data['Y_COORDINA'], 
                '-o', color=colors[color_idx], alpha=0.6, 
                markersize=3, linewidth=1, label=f'Trip {trip_id}')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.title('GPS Trajectories by Trip', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=8)
    plt.tight_layout()
    fig_file = output_folder / 'trips_trajectories.png'
    plt.savefig(fig_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {fig_file}")
    plt.close()
    
    # 3. HEATMAP (REQUIRED)
    print("3. Creating GPS density heatmap... (REQUIRED)")
    fig, axes = plt.subplots(1, 2, figsize=(18, 7))
    ax1 = axes[0]
    hb = ax1.hexbin(df['X_COORDINA'], df['Y_COORDINA'], 
                    gridsize=50, cmap='YlOrRd', mincnt=1)
    ax1.set_xlabel('Longitude', fontsize=12)
    ax1.set_ylabel('Latitude', fontsize=12)
    ax1.set_title('GPS Point Density Heatmap (Hexagonal)', fontsize=12, fontweight='bold')
    plt.colorbar(hb, ax=ax1, label='Number of GPS points')
    ax1.grid(True, alpha=0.3)
    
    ax2 = axes[1]
    hist, xedges, yedges = np.histogram2d(df['X_COORDINA'], df['Y_COORDINA'], bins=50)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    im = ax2.imshow(hist.T, extent=extent, origin='lower', cmap='YlOrRd', aspect='auto')
    ax2.set_xlabel('Longitude', fontsize=12)
    ax2.set_ylabel('Latitude', fontsize=12)
    ax2.set_title('GPS Point Density Heatmap (2D Histogram)', fontsize=12, fontweight='bold')
    plt.colorbar(im, ax=ax2, label='Number of GPS points')
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    fig_file = output_folder / 'gps_density_heatmap.png'
    plt.savefig(fig_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {fig_file}")
    plt.close()
    
    # 4. SPEED ANALYSIS
    print("4. Creating speed analysis...")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    ax1 = axes[0, 0]
    ax1.hist(df['SPEED'], bins=50, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Speed (km/h)', fontsize=11)
    ax1.set_ylabel('Frequency', fontsize=11)
    ax1.set_title('Speed Distribution', fontsize=11, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    ax2 = axes[0, 1]
    trip_speeds = [df[df['TRIP_ID'] == trip]['SPEED'].values for trip in trips[:20]]
    bp = ax2.boxplot(trip_speeds, patch_artist=True)
    for patch in bp['boxes']:
        patch.set_facecolor('lightblue')
    ax2.set_xlabel('Trip ID', fontsize=11)
    ax2.set_ylabel('Speed (km/h)', fontsize=11)
    ax2.set_title('Speed by Trip', fontsize=11, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')
    
    ax3 = axes[1, 0]
    ax3.scatter(df['DISTANCE_KM'], df['SPEED'], alpha=0.3, s=5)
    ax3.set_xlabel('Distance (km)', fontsize=11)
    ax3.set_ylabel('Speed (km/h)', fontsize=11)
    ax3.set_title('Speed vs Distance', fontsize=11, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    
    ax4 = axes[1, 1]
    ax4.hist(df['ACCELERATION'], bins=50, color='coral', alpha=0.7, edgecolor='black')
    ax4.set_xlabel('Acceleration (km/h/s)', fontsize=11)
    ax4.set_ylabel('Frequency', fontsize=11)
    ax4.set_title('Acceleration Distribution', fontsize=11, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    plt.tight_layout()
    fig_file = output_folder / 'speed_analysis.png'
    plt.savefig(fig_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {fig_file}")
    plt.close()
    
    # 5. TEMPORAL ANALYSIS
    print("5. Creating temporal analysis...")
    df['DATETIME'] = pd.to_datetime(df['DATE'] + ' ' + df['TIME'])
    df['HOUR'] = df['DATETIME'].dt.hour
    df['DAY_OF_WEEK'] = df['DATETIME'].dt.dayofweek
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1 = axes[0]
    hourly_counts = df['HOUR'].value_counts().sort_index()
    ax1.bar(hourly_counts.index, hourly_counts.values, color='teal', alpha=0.7)
    ax1.set_xlabel('Hour of Day', fontsize=11)
    ax1.set_ylabel('Number of GPS Points', fontsize=11)
    ax1.set_title('GPS Data by Hour', fontsize=11, fontweight='bold')
    ax1.set_xticks(range(0, 24))
    ax1.grid(True, alpha=0.3, axis='y')
    
    ax2 = axes[1]
    day_counts = df['DAY_OF_WEEK'].value_counts().sort_index()
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    ax2.bar(range(7), [day_counts.get(i, 0) for i in range(7)], color='purple', alpha=0.7)
    ax2.set_xlabel('Day of Week', fontsize=11)
    ax2.set_ylabel('Number of GPS Points', fontsize=11)
    ax2.set_title('GPS Data by Day', fontsize=11, fontweight='bold')
    ax2.set_xticks(range(7))
    ax2.set_xticklabels(days)
    ax2.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    fig_file = output_folder / 'temporal_analysis.png'
    plt.savefig(fig_file, dpi=300, bbox_inches='tight')
    print(f"   ✓ Saved: {fig_file}")
    plt.close()
    
    # 6. SUMMARY STATISTICS
    print("6. Generating summary statistics...")
    summary_stats = {
        'Total GPS Points': len(df),
        'Total Trips': df['TRIP_ID'].nunique(),
        'Total Users': df['USER_ID'].nunique(),
        'Total Distance (km)': df['DISTANCE_KM'].sum(),
        'Average Speed (km/h)': df['SPEED'].mean(),
        'Max Speed (km/h)': df['SPEED'].max(),
        'Min Speed (km/h)': df['SPEED'].min(),
        'Average Distance (km)': df['DISTANCE_KM'].mean(),
        'Date Range': f"{df['DATE'].min()} to {df['DATE'].max()}"
    }
    
    summary_file = Path(csv_file).parent / 'summary_statistics.txt'
    with open(summary_file, 'w') as f:
        f.write("="*60 + "\n")
        f.write("GPS DATA SUMMARY STATISTICS\n")
        f.write("="*60 + "\n\n")
        for key, value in summary_stats.items():
            if isinstance(value, float):
                f.write(f"{key:.<45} {value:.2f}\n")
            else:
                f.write(f"{key:.<45} {value}\n")
    print(f"   ✓ Saved: {summary_file}")
    
    print()
    print("="*60)
    print("SUMMARY STATISTICS")
    print("="*60)
    for key, value in summary_stats.items():
        if isinstance(value, float):
            print(f"{key:.<45} {value:.2f}")
        else:
            print(f"{key:.<45} {value}")
    print("="*60)
    
    return output_folder


def main():
    print("="*80)
    print("GPS DATA VISUALIZATION - TASK 2")
    print("Course: AMI23K - Lab 2")
    print("="*80)
    print()
    print("Configured paths:")
    print(f"  INPUT CSV:  {CSV_FILE}")
    print(f"  OUTPUT:     {OUTPUT_FOLDER}")
    print()
    
    if not Path(CSV_FILE).exists():
        print(f"ERROR: File not found: {CSV_FILE}")
        print("Please run Task 1 first!")
        print()
        input("Press Enter to exit...")
        return
    
    fig_folder = visualize_gps_data(CSV_FILE, OUTPUT_FOLDER)
    
    if fig_folder:
        print()
        print("="*80)
        print("VISUALIZATION COMPLETE! ✓")
        print("="*80)
        print()
        print("Files created:")
        print("  1. longitude_vs_latitude.png  (REQUIRED)")
        print("  2. trips_trajectories.png")
        print("  3. gps_density_heatmap.png    (REQUIRED)")
        print("  4. speed_analysis.png")
        print("  5. temporal_analysis.png")
        print()
        print("✓ Ready for submission!")
    else:
        print()
        print("="*80)
        print("VISUALIZATION FAILED ✗")
        print("="*80)
    
    print()
    input("Press Enter to close...")


if __name__ == "__main__":
    main()