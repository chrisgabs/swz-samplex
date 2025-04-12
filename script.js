document.addEventListener('DOMContentLoaded', () => {
    // Fetch the similar questions data
    fetch('similar_questions.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load data');
            }
            return response.json();
        })
        .then(data => {
            // Update dashboard statistics
            updateDashboard(data);
            
            // Display the questions
            displayQuestions(data);
            
            // Setup search functionality
            setupSearch(data);
            
            // Setup exam filters
            setupExamFilters(data);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('questionsList').innerHTML = `
                <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                    <strong class="font-bold">Error!</strong>
                    <span class="block sm:inline"> Failed to load question data. Please check that similar_questions.json exists.</span>
                </div>
            `;
        });
});

function updateDashboard(questions) {
    // Get all unique exams across all questions
    const allExams = new Set();
    questions.forEach(q => {
        Object.keys(q.question).forEach(exam => allExams.add(exam));
    });
    
    // Calculate avg questions per exam group
    const totalExamInstances = questions.reduce((sum, q) => sum + Object.keys(q.question).length, 0);
    const avgPerGroup = (totalExamInstances / questions.length).toFixed(2);
    
    // Update the dashboard elements
    document.getElementById('totalQuestions').textContent = questions.length;
    document.getElementById('totalExams').textContent = allExams.size;
    document.getElementById('avgQuestionsPerExam').textContent = avgPerGroup;
    
    // Update results count
    document.getElementById('resultsCount').textContent = `Showing all ${questions.length} similar question groups`;
}

function displayQuestions(questions) {
    const questionsContainer = document.getElementById('questionsList');
    questionsContainer.innerHTML = '';
    
    if (questions.length === 0) {
        questionsContainer.innerHTML = '<div class="text-center py-10 text-gray-500">No questions found</div>';
        document.getElementById('resultsCount').textContent = 'No questions found';
        return;
    }
    
    // Update results count
    document.getElementById('resultsCount').textContent = `Showing ${questions.length} similar question groups`;
    
    questions.forEach((questionGroup, index) => {
        const exams = Object.keys(questionGroup.question);
        const questionCard = document.createElement('div');
        questionCard.className = 'bg-white rounded-lg shadow-md p-6 fade-in mb-6';
        questionCard.dataset.number = questionGroup.number;
        
        // Question header (clickable to expand/collapse)
        let header = `
            <div class="flex justify-between items-start mb-4 cursor-pointer toggle-question" data-target="question-${questionGroup.number}">
                <h2 class="text-xl font-semibold text-gray-800">Question ${questionGroup.number}</h2>
                <div class="flex items-center">
                    <div class="mr-4">
                        ${exams.map((exam, i) => 
                            `<span class="exam-pill exam-pill-${i+1}">${formatExamName(exam)}</span>`
                        ).join('')}
                    </div>
                    <svg class="h-6 w-6 text-gray-500 transform transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                    </svg>
                </div>
            </div>
        `;
        
        // Question overview (short summary visible when collapsed)
        let overview = `
            <div class="mb-4 border-b pb-4">
                <p class="text-gray-700">
                    <strong>Topic:</strong> ${extractTopic(questionGroup)}
                </p>
                <p class="text-gray-700 mt-1">
                    <strong>Appears in:</strong> ${exams.length} exams (${exams.map(e => formatExamName(e)).join(', ')})
                </p>
            </div>
        `;
        
        // Collapsible content
        let collapsibleContent = `<div id="question-${questionGroup.number}" class="collapsible-content">`;
        
        // Question body with comparison
        let questionBody = `<div class="mb-6">`;
        
        // Add each exam's question
        exams.forEach((exam, i) => {
            const examClass = `exam-pill-${i+1}`;
            questionBody += `
                <div class="exam-container mb-6 pb-4">
                    <div class="flex items-center mb-2">
                        <span class="exam-pill ${examClass}">${formatExamName(exam)}</span>
                        <span class="text-sm text-gray-500 ml-2">Q${questionGroup.reference[exam].number} - ${questionGroup.reference[exam].section}</span>
                    </div>
                    <div class="text-gray-700 mb-4 pl-4 border-l-4 border-gray-200">
                        ${highlightDifferences(questionGroup.question[exam], questionGroup.question)}
                    </div>
                    
                    <div class="mt-4">
                        <h3 class="font-medium text-gray-700 mb-2">Choices:</h3>
                        <div class="pl-4 space-y-2">
                            ${Object.entries(questionGroup.choices[exam]).map(([key, value]) => {
                                const isCorrect = questionGroup.answer[exam].toLowerCase() === key.toLowerCase();
                                return `
                                    <div class="p-2 ${isCorrect ? 'choice-correct' : ''}">
                                        <span class="font-medium">${key.toUpperCase()}:</span> ${value}
                                        ${isCorrect ? '<span class="ml-2 text-green-600 text-sm font-medium">(Correct Answer)</span>' : ''}
                                    </div>
                                `;
                            }).join('')}
                        </div>
                    </div>
                    
                    <div class="mt-4 text-sm text-gray-600">
                        <span class="font-medium">Reference:</span> ${questionGroup.reference[exam].reference}
                    </div>
                </div>
            `;
        });
        
        questionBody += `</div>`;
        
        // Add a similarity analysis section
        let similarityAnalysis = analyzeQuestionSimilarity(questionGroup);
        let similaritySection = `
            <div class="mt-6 pt-4 border-t border-gray-200">
                <h3 class="font-medium text-gray-700 mb-2">Similarity Analysis:</h3>
                <div class="text-sm text-gray-600">
                    <p>These ${exams.length} questions test the same medical knowledge across different exams.</p>
                    <p class="mt-2"><span class="font-medium">Common correct answer:</span> ${getCommonAnswer(questionGroup)}</p>
                    <div class="mt-3 p-3 bg-blue-50 rounded-md">
                        <p class="font-medium text-blue-800">Analysis:</p>
                        <ul class="list-disc pl-5 mt-1 space-y-1 text-blue-800">
                            ${similarityAnalysis.map(point => `<li>${point}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            </div>
        `;
        
        collapsibleContent += questionBody + similaritySection + '</div>';
        
        questionCard.innerHTML = header + overview + collapsibleContent;
        questionsContainer.appendChild(questionCard);
    });
    
    // Add event listeners for toggling questions
    document.querySelectorAll('.toggle-question').forEach(element => {
        element.addEventListener('click', function() {
            const targetId = this.dataset.target;
            const targetElement = document.getElementById(targetId);
            const parentCard = this.closest('.bg-white');
            const arrow = this.querySelector('svg');
            
            if (parentCard.classList.contains('expanded')) {
                parentCard.classList.remove('expanded');
                arrow.classList.remove('rotate-180');
            } else {
                parentCard.classList.add('expanded');
                arrow.classList.add('rotate-180');
            }
        });
    });
}

function formatExamName(examName) {
    return examName.replace('sample_', 'Exam ').replace(/(\d+)$/, ' $1');
}

function getCommonAnswer(questionGroup) {
    const answers = Object.values(questionGroup.answer);
    // Check if all answers are the same
    if (answers.every(a => a.toLowerCase() === answers[0].toLowerCase())) {
        return answers[0].toUpperCase();
    } else {
        return 'Varies across exams';
    }
}

function extractTopic(questionGroup) {
    // Get the first question's text
    const firstQuestion = Object.values(questionGroup.question)[0];
    
    // Extract potential medical topics from the question
    const topics = firstQuestion.match(/\b(?:cancer|disease|syndrome|disorder|infection|carcinoma|tumor|lesion|cyst|fracture|injury|condition)\b/gi);
    
    if (topics && topics.length > 0) {
        // Return the first identified topic
        return topics[0];
    }
    
    // If no specific topic found, return the first 50 characters of the question
    return firstQuestion.substring(0, 50) + '...';
}

function highlightDifferences(currentQuestion, allQuestions) {
    // For simplicity, we'll just return the text without highlighting
    // A more sophisticated implementation could compare text across questions and highlight differences
    return currentQuestion;
}

function analyzeQuestionSimilarity(questionGroup) {
    const analysis = [];
    const exams = Object.keys(questionGroup.question);
    
    // Check if the questions are identical
    const questions = Object.values(questionGroup.question);
    const areQuestionsIdentical = questions.every(q => q === questions[0]);
    
    if (areQuestionsIdentical) {
        analysis.push("The questions are identical across exams.");
    } else {
        analysis.push("The questions vary slightly in wording but test the same concept.");
    }
    
    // Check if the answers are the same
    const answers = Object.values(questionGroup.answer);
    const areAnswersIdentical = answers.every(a => a.toLowerCase() === answers[0].toLowerCase());
    
    if (areAnswersIdentical) {
        analysis.push("All exams have the same correct answer option.");
    } else {
        analysis.push("The correct answer varies across exams.");
    }
    
    // Check if the options are the same
    const numberOfChoices = Object.values(questionGroup.choices).map(choices => Object.keys(choices).length);
    const sameNumberOfChoices = numberOfChoices.every(num => num === numberOfChoices[0]);
    
    if (sameNumberOfChoices) {
        analysis.push(`All questions present ${numberOfChoices[0]} answer options.`);
    } else {
        analysis.push("The number of answer options varies between exams.");
    }
    
    // Check if from same section
    const sections = Object.values(questionGroup.reference).map(ref => ref.section);
    const uniqueSections = [...new Set(sections)];
    
    if (uniqueSections.length === 1) {
        analysis.push(`All questions come from the same section: "${uniqueSections[0]}".`);
    } else {
        analysis.push(`Questions appear in different sections across exams.`);
    }
    
    return analysis;
}

function setupExamFilters(questions) {
    // Get all unique exams
    const allExams = new Set();
    questions.forEach(q => {
        Object.keys(q.question).forEach(exam => allExams.add(exam));
    });
    
    // Create filter buttons
    const filtersContainer = document.getElementById('examFilters');
    filtersContainer.innerHTML = '';
    
    // Add "All" filter
    const allFilter = document.createElement('button');
    allFilter.className = 'px-3 py-1 rounded-full bg-gray-200 text-gray-800 text-sm font-medium hover:bg-gray-300 active-filter';
    allFilter.textContent = 'All Exams';
    allFilter.dataset.filter = 'all';
    filtersContainer.appendChild(allFilter);
    
    // Add individual exam filters
    Array.from(allExams).sort().forEach((exam, index) => {
        const filterButton = document.createElement('button');
        filterButton.className = `px-3 py-1 rounded-full bg-gray-200 text-gray-800 text-sm font-medium hover:bg-gray-300`;
        filterButton.textContent = formatExamName(exam);
        filterButton.dataset.filter = exam;
        filtersContainer.appendChild(filterButton);
    });
    
    // Add event listeners
    document.querySelectorAll('#examFilters button').forEach(button => {
        button.addEventListener('click', function() {
            // Update active class
            document.querySelectorAll('#examFilters button').forEach(btn => {
                btn.classList.remove('active-filter');
            });
            this.classList.add('active-filter');
            
            // Filter questions
            const filter = this.dataset.filter;
            if (filter === 'all') {
                displayQuestions(questions);
            } else {
                const filtered = questions.filter(q => Object.keys(q.question).includes(filter));
                displayQuestions(filtered);
            }
        });
    });
}

function setupSearch(questions) {
    const searchInput = document.getElementById('searchInput');
    
    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        if (searchTerm === '') {
            displayQuestions(questions);
            return;
        }
        
        const filteredQuestions = questions.filter(q => {
            // Search in all exam questions
            return Object.values(q.question).some(text => 
                text.toLowerCase().includes(searchTerm)
            ) || 
            // Search in choices
            Object.values(q.choices).some(choiceSet => 
                Object.values(choiceSet).some(choice => 
                    choice.toLowerCase().includes(searchTerm)
                )
            );
        });
        
        displayQuestions(filteredQuestions);
    });
} 