import { batches, currentBatchIndex } from '../stores';
import type { Batch } from '../types';
import { validateQuestionStructure, showNotification } from '../utils';

/**
 * Initialize the application with data from localStorage or default data
 */
export function initializeApp(): void {
    // Check if we have imported data in localStorage
    const storedData = localStorage.getItem('importedQuestionData');
    
    if (storedData) {
        try {
            const parsedData = JSON.parse(storedData);
            processQuestionData(parsedData);
        } catch (error) {
            console.error('Error parsing stored data:', error);
            // If stored data is corrupt, try to load the default file
            loadDefaultData();
        }
    } else {
        // Load the default similar_questions.json file
        loadDefaultData();
    }
}

/**
 * Load the default question data
 */
export function loadDefaultData(): void {
    // Fetch the similar questions data
    fetch('/similar_questions.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load data');
            }
            return response.json();
        })
        .then(data => {
            // Check if the loaded data is already in the new format (with batch_name and similar_questions)
            // If not, convert it to the new format
            if (!data.batch_name) {
                data = {
                    batch_name: "Default Batch",
                    similar_questions: data
                };
            }
            processQuestionData(data);
        })
        .catch(error => {
            console.error('Error:', error);
            showNotification({ 
                message: 'Failed to load question data. Please use the Import button to paste your data.',
                type: 'error'
            });
        });
}

/**
 * Process question data and update stores
 */
export function processQuestionData(data: Batch | Batch[]): void {
    // Check if data is an array of batches or a single batch
    if (Array.isArray(data) && data.length > 0 && data[0].batch_name) {
        // It's an array of batches
        batches.set(data);
        currentBatchIndex.set(0);
    } else {
        // It's a single batch (or old format)
        batches.set([data as Batch]);
        currentBatchIndex.set(0);
    }
}

/**
 * Import JSON data
 */
export function importJSON(jsonText: string): boolean {
    if (!jsonText) {
        showNotification({ message: 'Please enter JSON data.', type: 'error' });
        return false;
    }
    
    try {
        let data = JSON.parse(jsonText);
        
        // Validate the structure
        if (Array.isArray(data)) {
            // Array of batch objects
            if (data.length === 0) {
                throw new Error('JSON data must contain at least one batch.');
            }
            
            // Check if each item has batch_name and similar_questions array
            for (const batch of data) {
                if (!batch.batch_name || !Array.isArray(batch.similar_questions) || batch.similar_questions.length === 0) {
                    throw new Error('Each batch must have a batch_name and similar_questions array.');
                }
                validateQuestionStructure(batch.similar_questions[0]);
            }
        } else {
            // Single batch object
            if (!data.batch_name || !Array.isArray(data.similar_questions) || data.similar_questions.length === 0) {
                // Try to check if it's the old format (just an array of questions)
                if (Array.isArray(data) && data.length > 0) {
                    validateQuestionStructure(data[0]);
                    // Convert to new format
                    data = {
                        batch_name: "Imported Batch",
                        similar_questions: data
                    };
                } else {
                    validateQuestionStructure(data);
                }
            } else {
                // It's a single batch in the new format
                validateQuestionStructure(data.similar_questions[0]);
            }
        }
        
        // Store in localStorage
        localStorage.setItem('importedQuestionData', jsonText);
        
        // Process the data
        processQuestionData(data);
        
        // Show success notification
        showNotification({ message: 'Data imported successfully!', type: 'success' });
        
        return true;
    } catch (error) {
        console.error('Import error:', error);
        showNotification({ 
            message: `Invalid JSON format: ${(error as Error).message}`,
            type: 'error'
        });
        return false;
    }
}

/**
 * Clear imported data and reset to default
 */
export function resetToDefaultData(): void {
    localStorage.removeItem('importedQuestionData');
    loadDefaultData();
    showNotification({ message: 'Reset to default data.', type: 'info' });
} 