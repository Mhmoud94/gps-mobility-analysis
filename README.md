# GPS Mobility Data Analysis

Data Collection and Data Quality Course Project - Master's in Data Science and Analytics, Dalarna University

## Project Overview

Analysis of GPS mobility data from 20 users collected over three months (June-August 2011). The project processes 16,094 GPS points covering 97,030 kilometers across 47 trips to analyze mobility patterns and assess data quality.

## Objectives

- Develop a robust data processing pipeline for GPS logger files
- Implement quality validation methods for sensor data
- Analyze mobility patterns and temporal trends
- Visualize geographic distributions and movement trajectories

## Technical Stack

- Python 3.8+
- pandas - Data manipulation
- numpy - Numerical computations
- matplotlib - Visualization
- seaborn - Statistical graphics

## Methodology

### Data Processing
1. Parse raw GPS logger files (.gsd format)
2. Convert coordinates from degree-minute to decimal format
3. Calculate distances using the Haversine formula
4. Compute speed and acceleration metrics
5. Validate data quality across multiple dimensions

### Quality Assessment
- Spatial validation of coordinate ranges
- Speed reasonableness checks
- Temporal consistency analysis
- Distance-based validation
- Visual inspection of trajectories

## Key Results

| Metric | Value |
|--------|-------|
| Total GPS Points | 16,094 |
| Total Distance | 97,029.84 km |
| Average Speed | 51.56 km/h |
| Maximum Speed | 142.00 km/h |
| Study Period | June 1 - August 30, 2011 |
| Peak Travel Time | 14:00-15:00 |

## Findings

- Geographic analysis revealed concentrated activity areas around latitude 60.3°N
- Temporal patterns showed peak travel during afternoon hours
- Data quality validation identified signal gaps and accuracy variations
- Multiple validation methods proved necessary for reliable analysis

## Repository Structure

```
├── task1_FINAL.py              # Data processing pipeline
├── task2_FINAL.py              # Visualization generation
├── results/
│   ├── gps_processed_data.csv  # Processed dataset
│   ├── trip_summary.csv        # Trip-level statistics
│   └── figures/                # Visualizations
```

## Usage

Process GPS data:
```bash
python task1_FINAL.py
```

Generate visualizations:
```bash
python task2_FINAL.py
```

## Installation

```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

##

Master's in Data Science and Analytics

Dalarna University, 2025

## Course

Data Collection and Data Quality

AMI23K

## License

MIT License

