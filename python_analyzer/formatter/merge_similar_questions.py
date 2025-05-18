#!/usr/bin/env python3
import os
import json
import argparse
from datetime import datetime
import sys
from collections import defaultdict


def find_similar_questions_files(root_dir):
    """
    Find all files named 'similar_questions.json' in the given directory and its subdirectories.
    
    Args:
        root_dir (str): Root directory to start the search from.
        
    Returns:
        dict: Dictionary with subject names as keys and lists of (batch_name, file_path) as values
    """
    result = defaultdict(list)
    
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if 'similar_questions.json' in filenames:
            # Get the directory structure
            rel_path = os.path.relpath(dirpath, root_dir)
            path_parts = rel_path.split(os.sep)
            
            if len(path_parts) >= 2:
                # Structure is: root_dir/subject_dir/batch_dir/similar_questions.json
                subject_name = path_parts[0]
                batch_name = path_parts[1]
                file_path = os.path.join(dirpath, 'similar_questions.json')
                result[subject_name].append((batch_name, file_path))
            elif len(path_parts) == 1:
                # Structure is: root_dir/batch_dir/similar_questions.json
                # Use "Default Subject" as subject name
                subject_name = "Default Subject"
                batch_name = path_parts[0]
                file_path = os.path.join(dirpath, 'similar_questions.json')
                result[subject_name].append((batch_name, file_path))
    
    return result


def merge_files(subject_files_dict):
    """
    Merge the content of all files into a single JSON structure with subjects and batches.
    
    Args:
        subject_files_dict (dict): Dictionary with subject names as keys and lists of (batch_name, file_path) as values
        
    Returns:
        list: List of dictionaries with subject_name and batches fields
    """
    merged_data = []
    
    for subject_name, file_list in subject_files_dict.items():
        subject_data = {
            "subject_name": subject_name,
            "batches": []
        }
        
        for batch_name, file_path in file_list:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    similar_questions_data = json.load(f)
                
                subject_data["batches"].append({
                    "batch_name": batch_name,
                    "similar_questions": similar_questions_data
                })
                
            except json.JSONDecodeError:
                print(f"Warning: Skipping {file_path} due to invalid JSON format")
            except Exception as e:
                print(f"Error processing {file_path}: {str(e)}")
        
        if subject_data["batches"]:  # Only add subjects that have at least one valid batch
            merged_data.append(subject_data)
    
    return merged_data


# python merge_similar_questions.py --root_dir ../out/test_root
def main():
    parser = argparse.ArgumentParser(description="Merge similar_questions.json files from multiple directories into a subject-batch structure")
    parser.add_argument("--root_dir", type=str, default=".", 
                        help="Root directory to search for similar_questions.json files (default: current directory)")
    args = parser.parse_args()
    
    # Generate the output filename with timestamp - using a Windows-compatible format
    timestamp = datetime.now().strftime("%m-%d-%H-%M")
    output_filename = f"merged_similar_questions_{timestamp}.json"
    
    # Find all similar_questions.json files organized by subject
    subject_files_dict = find_similar_questions_files(args.root_dir)
    
    if not subject_files_dict:
        print(f"No 'similar_questions.json' files found in {args.root_dir}")
        sys.exit(1)
        
    total_files = sum(len(files) for files in subject_files_dict.values())
    print(f"Found {total_files} 'similar_questions.json' files across {len(subject_files_dict)} subjects")
    
    # Merge the files into the subject-batch structure
    merged_data = merge_files(subject_files_dict)
    
    out_dir = "out"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Write the merged data to output file
    with open(os.path.join(out_dir, output_filename), 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, indent=2, ensure_ascii=False)
    
    print(f"Successfully merged data into {output_filename}")
    print(f"Output structure: {len(merged_data)} subjects with a total of {total_files} batches")


if __name__ == "__main__":
    main() 

# python merge_similar_questions.py --root_dir ../out
