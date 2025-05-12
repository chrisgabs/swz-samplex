import { writable, derived } from 'svelte/store';
import type { Batch, Question } from './types';

// Store for all batches of questions
export const batches = writable<Batch[]>([]);

// Store for the currently selected batch index
export const currentBatchIndex = writable<number>(0);

// Store for search term
export const searchTerm = writable<string>('');

// Store for active exam filters
export const activeFilters = writable<string[]>([]);

// Derived store for the current batch
export const currentBatch = derived(
    [batches, currentBatchIndex],
    ([$batches, $currentBatchIndex]) => {
        if ($batches.length === 0) return null;
        return $batches[$currentBatchIndex];
    }
);

// Derived store for filtered questions
export const filteredQuestions = derived(
    [currentBatch, searchTerm, activeFilters],
    ([$currentBatch, $searchTerm, $activeFilters]) => {
        if (!$currentBatch) return [];
        
        let questions = $currentBatch.similar_questions;
        
        // Apply search filter if search term exists
        if ($searchTerm) {
            const term = $searchTerm.toLowerCase();
            questions = questions.filter(q => {
                // Search in question text
                const questionMatches = Object.values(q.question).some(text => 
                    text.toLowerCase().includes(term)
                );
                
                // Search in choices
                const choicesMatch = Object.values(q.choices).some(choiceSet => 
                    Object.values(choiceSet).some(choice => 
                        choice.toLowerCase().includes(term)
                    )
                );
                
                return questionMatches || choicesMatch;
            });
        }
        
        // Apply exam filters if any are active
        if ($activeFilters.length > 0) {
            questions = questions.filter(q => 
                Object.keys(q.question).some(exam => 
                    $activeFilters.includes(exam)
                )
            );
        }
        
        return questions;
    }
); 