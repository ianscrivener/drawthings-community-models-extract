#!/usr/bin/env python3
"""
Test script for the data extraction functionality.
This validates that the extraction script works correctly.
"""

import json
import os
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path to import the extraction script
sys.path.insert(0, str(Path(__file__).parent))
from extract_data import extract_models_data

def test_extraction():
    """Test the extraction script with mock data."""
    # Save current directory
    original_dir = os.getcwd()
    
    # Create a temporary directory for testing
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            os.chdir(tmpdir)
            
            # Create mock external repository structure
            ext_repo = Path("external-repo")
            ext_repo.mkdir()
            
            # Create test models directory
            models_dir = ext_repo / "models"
            models_dir.mkdir()
            
            # Create test JSON files
            test_model1 = {
                "name": "test-model-1",
                "version": "1.0.0",
                "author": "Test Author",
                "description": "A test model"
            }
            
            test_model2 = {
                "name": "test-model-2",
                "version": "2.0.0",
                "category": "diffusion"
            }
            
            with open(models_dir / "model1.json", 'w') as f:
                json.dump(test_model1, f)
            
            with open(models_dir / "model2.json", 'w') as f:
                json.dump(test_model2, f)
            
            # Run the extraction
            extract_models_data()
            
            # Verify outputs
            data_dir = Path("data")
            assert data_dir.exists(), "Data directory was not created"
            
            # Check parquet file
            parquet_file = data_dir / "community_models.parquet"
            assert parquet_file.exists(), "Parquet file was not created"
            
            # Check CSV file
            csv_file = data_dir / "community_models.csv"
            assert csv_file.exists(), "CSV file was not created"
            
            # Check metadata file
            metadata_file = data_dir / "extraction_metadata.json"
            assert metadata_file.exists(), "Metadata file was not created"
            
            # Verify metadata content
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
                assert metadata['record_count'] == 2, \
                    f"Expected 2 records, got {metadata['record_count']}"
                assert 'extracted_at' in metadata, "Missing extraction timestamp"
                assert metadata['source_repository'] == \
                    "https://github.com/drawthings/community-models"
            
            print("✓ All tests passed!")
            return True
        finally:
            # Always restore original directory
            os.chdir(original_dir)

if __name__ == "__main__":
    try:
        test_extraction()
        sys.exit(0)
    except AssertionError as e:
        print(f"✗ Test failed: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
