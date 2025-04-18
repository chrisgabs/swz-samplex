import json
import os
import sys
from pathlib import Path
import glob
import re
from collections import defaultdict, Counter
import difflib

def preprocess_text(text):
    """Preprocess text for similarity comparison."""
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters
    text = re.sub(r'[^\w\s]', ' ', text)
    
    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_domain_specific_terms(text):
    """Extract potential domain-specific terms from text."""
    if not text:
        return []
    
    # Find words with at least 4 characters (likely to be specialized terms)
    words = re.findall(r'\b[A-Za-z][A-Za-z-]{3,}\b', text.lower())
    
    # Common English words to exclude
    common_words = {
        'with', 'that', 'this', 'what', 'from', 'have', 'they', 'will', 'would', 'should', 'could',
        'than', 'then', 'them', 'there', 'these', 'those', 'been', 'were', 'when', 'where', 'which',
        'while', 'your', 'following', 'most', 'common', 'typically', 'often', 'presents', 'patient',
        'patients', 'following', 'symptoms', 'clinical', 'diagnosis', 'treatment', 'management',
        'appropriate', 'therapy', 'disease', 'best', 'characteristic', 'likely', 'cause', 'causes',
        'each', 'both', 'case', 'cases', 'include', 'includes', 'including', 'additional', 'other',
        'further', 'important', 'significant', 'normal', 'abnormal', 'given', 'above', 'below',
        'next', 'previous', 'first', 'second', 'third', 'fourth', 'fifth', 'correct', 'incorrect',
        'true', 'false', 'different', 'various', 'several', 'many', 'much', 'more', 'less', 'some',
        'same', 'based', 'only', 'after', 'before', 'during', 'initial', 'final', 'early', 'late'
    }
    
    # Extract more likely domain-specific terms
    specific_terms = [word for word in words if word not in common_words]
    
    return specific_terms

def extract_key_concepts(all_questions):
    """Extract key concepts from all questions to help identify important terms."""
    # Extract all terms from all questions
    all_terms = []
    for q in all_questions:
        q_text = q["question"] + " " + " ".join(q["choices"].values())
        all_terms.extend(extract_domain_specific_terms(q_text))
    
    # Count term frequencies
    term_counts = Counter(all_terms)
    
    # Terms appearing multiple times are likely key domain concepts
    key_concepts = {term for term, count in term_counts.items() if count >= 2}
    
    return key_concepts

def identify_key_terms(text, key_concepts):
    """Identify key domain-specific terms in the text using the extracted key concepts."""
    terms = extract_domain_specific_terms(text)
    return {term for term in terms if term in key_concepts}

def calculate_similarity(q1, q2, key_concepts):
    """Calculate similarity between two questions."""
    # Combine question text with choices for better comparison
    q1_text = q1["question"] + " " + " ".join(q1["choices"].values())
    q2_text = q2["question"] + " " + " ".join(q2["choices"].values())
    
    # Extract key domain terms
    q1_key_terms = identify_key_terms(q1_text, key_concepts)
    q2_key_terms = identify_key_terms(q2_text, key_concepts)
    
    # If the questions share key terms, they're more likely to be similar
    key_term_overlap = len(q1_key_terms.intersection(q2_key_terms))
    
    # Calculate term overlap ratio if there are key terms
    total_key_terms = len(q1_key_terms.union(q2_key_terms))
    if total_key_terms > 0:
        key_term_overlap_ratio = key_term_overlap / total_key_terms
    else:
        key_term_overlap_ratio = 0
    
    # Apply similarity discount if no key terms overlap
    if key_term_overlap == 0 and (q1_key_terms and q2_key_terms):
        initial_similarity_discount = 0.3  # More aggressive discount
    else:
        initial_similarity_discount = 1.0
    
    # Preprocess texts
    q1_processed = preprocess_text(q1_text)
    q2_processed = preprocess_text(q2_text)
    
    # Use difflib for sequence comparison
    sequence_matcher = difflib.SequenceMatcher(None, q1_processed, q2_processed)
    sequence_similarity = sequence_matcher.ratio()
    
    # Extract all domain-specific terms
    q1_terms = set(extract_domain_specific_terms(q1_text))
    q2_terms = set(extract_domain_specific_terms(q2_text))
    
    # Calculate term overlap (Jaccard similarity)
    union_size = len(q1_terms.union(q2_terms))
    if union_size > 0:
        term_overlap = len(q1_terms.intersection(q2_terms)) / union_size
    else:
        term_overlap = 0
    
    # Check if answers match
    answer_match = 1 if q1["answer"] == q2["answer"] else 0
    
    # Check if sections are related
    section_relation = 0.2
    if q1.get("section", "").lower() in q2.get("section", "").lower() or \
       q2.get("section", "").lower() in q1.get("section", "").lower():
        section_relation = 0.8
    
    # Weighted combination of similarity scores
    weights = [0.35, 0.3, 0.2, 0.15]  # Sequence, terms, answer, section
    similarity_score = initial_similarity_discount * (
        weights[0] * sequence_similarity + 
        weights[1] * term_overlap + 
        weights[2] * answer_match +
        weights[3] * section_relation
    )
    
    # Boost similarity if key terms overlap significantly
    if key_term_overlap_ratio > 0.3:
        similarity_score *= (1 + 0.5 * key_term_overlap_ratio)
    
    return similarity_score

def find_similar_questions(exam_files):
    """Find similar questions across multiple examination files."""
    exams = {}
    questions = []
    
    # Load all questions from all exams
    for file_path in exam_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                exam_name = Path(file_path).stem
                exams[exam_name] = data
                
                for q in data:
                    q['source_exam'] = exam_name
                    questions.append(q)
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            continue
    
    # Extract key concepts from all questions
    key_concepts = extract_key_concepts(questions)
    print(f"Extracted {len(key_concepts)} key domain concepts from {len(questions)} questions")
    
    # Dictionary to store groups of similar questions
    similar_groups = []
    processed_indices = set()
    
    # Threshold for similarity - adjusted based on testing
    similarity_threshold = 0.60
    
    print(f"Using similarity threshold: {similarity_threshold}")
    
    # Compare each question with every other question
    for i in range(len(questions)):
        if i in processed_indices:
            continue
            
        group = [questions[i]]
        processed_indices.add(i)
        
        for j in range(i+1, len(questions)):
            if j in processed_indices:
                continue
                
            # Skip if questions are from the same exam
            if questions[i]['source_exam'] == questions[j]['source_exam']:
                continue
                
            # Calculate similarity
            similarity = calculate_similarity(questions[i], questions[j], key_concepts)
            
            if similarity >= similarity_threshold:
                group.append(questions[j])
                processed_indices.add(j)
        
        # Only keep groups with questions from at least 2 different exams
        if len(group) >= 2 and len(set(q['source_exam'] for q in group)) >= 2:
            similar_groups.append(group)
    
    return similar_groups, exams

def format_output(similar_groups):
    """Format the output according to the specified structure."""
    results = []
    
    for group in similar_groups:
        result = {
            "number": len(results) + 1,
            "question": {},
            "choices": {},
            "answer": {},
            "reference": {}
        }
        
        for question in group:
            exam_name = question['source_exam']
            
            # Add question text
            result["question"][exam_name] = question["question"]
            
            # Add choices
            result["choices"][exam_name] = question["choices"]
            
            # Add answer
            result["answer"][exam_name] = question["answer"]
            
            # Add reference
            result["reference"][exam_name] = {
                "number": question["number"],
                "section": question["section"],
                "reference": question["reference"]
            }
        
        results.append(result)
    
    return results

def main():
    """Main function to process examination files."""
    # Check if files are provided as arguments
    if len(sys.argv) > 1:
        exam_files = sys.argv[1:]
    else:
        # Try to find JSON files in the current directory
        exam_files = glob.glob("*.json")
        # Filter out the output file if it exists
        exam_files = [f for f in exam_files if f != "similar_questions.json"]
    
    if not exam_files:
        print("Error: No JSON files found. Please provide the paths to the JSON files as arguments.")
        return
    
    print(f"Processing {len(exam_files)} examination files: {', '.join(exam_files)}")
    
    # Find similar questions
    similar_groups, exams = find_similar_questions(exam_files)
    
    # Format output
    results = format_output(similar_groups)
    
    # Write results to file
    output_file = "similar_questions.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"Found {len(results)} groups of similar questions across {len(exams)} examinations.")
    print(f"Results saved to {output_file}")
    
    # Display some statistics
    exams_per_group = [len(set(q['source_exam'] for q in group)) for group in similar_groups]
    if exams_per_group:
        avg_exams_per_group = sum(exams_per_group) / len(exams_per_group)
        print(f"Average number of examinations per similar question group: {avg_exams_per_group:.2f}")
    
    # Display the similar question groups (if any)
    if results:
        for i, example in enumerate(results):
            print(f"\nSimilar Question Group #{i+1}:")
            for exam_name in sorted(example["question"].keys()):
                print(f"\n--- {exam_name} ---")
                print(f"Question: {example['question'][exam_name]}")
                print("Choices:")
                for choice_key, choice_text in sorted(example["choices"][exam_name].items()):
                    print(f"  {choice_key}) {choice_text}")
                print(f"Answer: {example['answer'][exam_name]}")
                print(f"Original Question Number: {example['reference'][exam_name]['number']}")
                print(f"Section: {example['reference'][exam_name]['section']}")
                print(f"Reference: {example['reference'][exam_name]['reference']}")
            print("-" * 50)

if __name__ == "__main__":
    main() 