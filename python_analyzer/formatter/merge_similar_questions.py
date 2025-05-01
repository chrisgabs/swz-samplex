#!/usr/bin/env python3
import os
import json
import argparse
from datetime import datetime
import sys


def find_similar_questions_files(root_dir):
    """
    Find all files named 'similar_questions.json' in the given directory and its subdirectories.
    
    Args:
        root_dir (str): Root directory to start the search from.
        
    Returns:
        list: List of tuples containing (directory_name, file_path)
    """
    result = []
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'similar_questions.json' in filenames:
            # Get the directory name (batch name)
            batch_name = os.path.basename(dirpath)
            file_path = os.path.join(dirpath, 'similar_questions.json')
            result.append((batch_name, file_path))
    
    return result


def merge_files(file_list):
    """
    Merge the content of all files into a single JSON structure.
    
    Args:
        file_list (list): List of tuples containing (batch_name, file_path)
        
    Returns:
        list: List of dictionaries with batch_name and similar_questions fields
    """
    merged_data = []
    
    for batch_name, file_path in file_list:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                similar_questions_data = json.load(f)
                
            merged_data.append({
                "batch_name": batch_name,
                "similar_questions": similar_questions_data
            })
            
        except json.JSONDecodeError:
            print(f"Warning: Skipping {file_path} due to invalid JSON format")
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    return merged_data


def main():
    parser = argparse.ArgumentParser(description="Merge similar_questions.json files from multiple directories")
    parser.add_argument("--root_dir", type=str, default=".", 
                        help="Root directory to search for similar_questions.json files (default: current directory)")
    
    args = parser.parse_args()
    
    # Generate the output filename with timestamp
    timestamp = datetime.now().strftime("%m:%d:%H:%M")
    output_filename = f"merged_similar_questions_{timestamp}.json"
    
    # Find all similar_questions.json files
    file_list = find_similar_questions_files(args.root_dir)
    
    if not file_list:
        print(f"No 'similar_questions.json' files found in {args.root_dir}")
        sys.exit(1)
        
    print(f"Found {len(file_list)} 'similar_questions.json' files")
    
    # Merge the files
    merged_data = merge_files(file_list)
    
    out_dir = "out"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Write the merged data to output file
    with open(os.path.join(out_dir, output_filename), 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully merged data into {output_filename}")


if __name__ == "__main__":
    main() 

# python merge_similar_questions.py --root_dir ../out
