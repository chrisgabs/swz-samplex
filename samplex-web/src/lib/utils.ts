import type { Question, ExamDistributionItem, NotificationOptions } from './types';

/**
 * Format exam name for display
 */
export function formatExamName(examName: string): string {
    return examName.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());
}

/**
 * Get the common answer across all exams in a question group
 */
export function getCommonAnswer(questionGroup: Question): string {
    const answers = Object.values(questionGroup.answer);
    if (answers.length === 0) return '';
    
    // Return the most common answer
    const answerCounts = answers.reduce((acc, answer) => {
        acc[answer] = (acc[answer] || 0) + 1;
        return acc;
    }, {} as Record<string, number>);
    
    return Object.entries(answerCounts)
        .sort((a, b) => b[1] - a[1])[0][0];
}

/**
 * Extract topic from question text
 */
export function extractTopic(questionGroup: Question): string {
    // Get the first question text
    const firstQuestion = Object.values(questionGroup.question)[0] || '';
    
    // Extract first 50 characters or up to the first period
    const periodIndex = firstQuestion.indexOf('.');
    if (periodIndex > 0 && periodIndex < 100) {
        return firstQuestion.substring(0, periodIndex + 1);
    }
    
    // If no period found or it's too far, return first 50 chars
    return firstQuestion.substring(0, Math.min(50, firstQuestion.length)) + 
        (firstQuestion.length > 50 ? '...' : '');
}

/**
 * Calculate exam distribution
 */
export function calculateExamDistribution(questions: Question[]): ExamDistributionItem[] {
    // Get all unique exams across all questions
    const examCounts: Record<string, number> = {};
    let totalExamInstances = 0;
    
    // Count occurrences of each exam
    questions.forEach(q => {
        Object.keys(q.question).forEach(exam => {
            examCounts[exam] = (examCounts[exam] || 0) + 1;
            totalExamInstances++;
        });
    });
    
    // Calculate percentages and prepare for visualization
    const availableColors = [
        'bg-blue-500', 'bg-purple-500', 'bg-green-500', 'bg-yellow-500', 
        'bg-red-500', 'bg-indigo-500', 'bg-pink-500', 'bg-orange-500',
        'bg-teal-500', 'bg-cyan-500'
    ];
    
    // Sort exams by count (descending)
    const sortedExams = Object.keys(examCounts).sort((a, b) => examCounts[b] - examCounts[a]);
    
    return sortedExams.map((exam, index) => {
        const count = examCounts[exam];
        const percentage = parseFloat(((count / totalExamInstances) * 100).toFixed(1));
        const color = availableColors[index % availableColors.length];
        
        return {
            exam,
            count,
            percentage,
            color
        };
    });
}

/**
 * Show a notification toast
 */
export function showNotification({ 
    message, 
    type = 'info',
    duration = 3000 
}: NotificationOptions): void {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500 text-white' : 
        type === 'error' ? 'bg-red-500 text-white' :
        'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    
    // Add to document
    document.body.appendChild(notification);
    
    // Remove after specified duration
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 500);
    }, duration);
}

/**
 * Validate question structure
 */
export function validateQuestionStructure(question: any): boolean {
    if (!question) {
        throw new Error('Invalid question object.');
    }
    
    if (!question.question || !question.choices || !question.answer || !question.reference) {
        throw new Error('Each question must have question, choices, answer, and reference properties.');
    }
    
    return true;
} 