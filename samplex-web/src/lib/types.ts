export interface Question {
    number: number;
    question: Record<string, string>;
    choices: Record<string, Record<string, string>>;
    answer: Record<string, string>;
    reference: Record<string, string>;
}

export interface Batch {
    batch_name: string;
    similar_questions: Question[];
}

export interface ExamDistributionItem {
    exam: string;
    count: number;
    percentage: number;
    color: string;
}

export interface NotificationOptions {
    message: string;
    type?: 'success' | 'info' | 'error';
    duration?: number;
} 