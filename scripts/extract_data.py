#!/usr/bin/env python3
"""
Extract data from the Drawthings Community Models repository and create
parquet and CSV files.
"""

import json
import os
import pandas as pd
from pathlib import Path
from datetime import datetime, timezone

def extract_models_data():
    """Extract model information from the external repository."""
    external_repo_path = Path("external-repo")
    
    if not external_repo_path.exists():
        print("External repository not found!")
        return
    
    # Create data directory if it doesn't exist
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Look for JSON files in the external repo
    models = []
    
    # Search for model metadata files
    for json_file in external_repo_path.rglob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Add file path information
                data['source_file'] = str(json_file.relative_to(external_repo_path))
                models.append(data)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading {json_file}: {e}")
            continue
    
    # If we found model data, create the exports
    if models:
        df = pd.DataFrame(models)
        
        # Add extraction timestamp
        df['extracted_at'] = datetime.now(timezone.utc).isoformat()
        
        # Export to parquet
        parquet_file = data_dir / "community_models.parquet"
        df.to_parquet(parquet_file, index=False)
        print(f"Created parquet file: {parquet_file} with {len(df)} records")
        
        # Export to CSV
        csv_file = data_dir / "community_models.csv"
        df.to_csv(csv_file, index=False)
        print(f"Created CSV file: {csv_file} with {len(df)} records")
    else:
        print("No model data found in external repository")
    
    # Create a metadata file with extraction info
    metadata = {
        "extracted_at": datetime.now(timezone.utc).isoformat(),
        "record_count": len(models),
        "source_repository": "https://github.com/drawthings/community-models"
    }
    
    metadata_file = data_dir / "extraction_metadata.json"
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Created metadata file: {metadata_file}")

if __name__ == "__main__":
    extract_models_data()
