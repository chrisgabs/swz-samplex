// Global variables
let subjects = [];
let currentSubjectIndex = 0;
let currentBatchIndex = 0;

document.addEventListener('DOMContentLoaded', () => {
    // Initialize the app with default data or from localStorage
    initializeApp();
    
    // Setup the import functionality
    setupImportModal();
    
    // Setup subject selection functionality
    setupSubjectSelector();
    
    // Setup batch selection functionality
    setupBatchSelector();
});

function initializeApp() {
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
    
    // Setup dashboard stats toggle
    setupDashboardStatsToggle();
}

function loadDefaultData() {
    // Fetch the similar questions data
    fetch('similar_questions.json')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to load data');
            }
            return response.json();
        })
        .then(data => {
            // Convert to new format with subjects and batches if needed
            let formattedData;
            
            // Check if the data is already in the new subject-batch format
            if (Array.isArray(data) && data.length > 0 && data[0].subject_name && data[0].batches) {
                // Already in the new format
                formattedData = data;
            } 
            // Check if it's in the batch format
            else if (Array.isArray(data) && data.length > 0 && data[0].batch_name) {
                // Convert batch format to subject-batch format
                formattedData = [{
                    subject_name: "Default Subject",
                    batches: data
                }];
            }
            // Check if it's a single batch object
            else if (data.batch_name) {
                // Convert single batch to subject-batch format
                formattedData = [{
                    subject_name: "Default Subject",
                    batches: [data]
                }];
            }
            // Check if it's the old format (just an array of questions)
            else if (Array.isArray(data)) {
                // Convert old format to subject-batch format
                formattedData = [{
                    subject_name: "Default Subject",
                    batches: [{
                        batch_name: "Default Batch",
                        similar_questions: data
                    }]
                }];
            }
            // Single question object
            else {
                // Convert to subject-batch format
                formattedData = [{
                    subject_name: "Default Subject",
                    batches: [{
                        batch_name: "Default Batch",
                        similar_questions: [data]
                    }]
                }];
            }
            
            processQuestionData(formattedData);
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('questionsList').innerHTML = `
                <div class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
                    <strong class="font-bold">Error!</strong>
                    <span class="block sm:inline"> Failed to load question data. Please check that similar_questions.json exists, or use the Import button to paste your data.</span>
                </div>
            `;
        });
}

function setupSubjectSelector() {
    const subjectSelector = document.getElementById('subjectSelector');
    
    subjectSelector.addEventListener('change', () => {
        const selectedSubjectIndex = parseInt(subjectSelector.value);
        currentSubjectIndex = selectedSubjectIndex;
        
        // Update batch selector with batches from the selected subject
        populateBatchSelector(subjects[selectedSubjectIndex].batches);
        
        // Reset to first batch in the new subject
        currentBatchIndex = 0;
        const batchSelector = document.getElementById('batchSelector');
        if (batchSelector.options.length > 0) {
            batchSelector.selectedIndex = 0;
            
            // Process the first batch of the selected subject
            processActiveBatch(subjects[selectedSubjectIndex].batches[0]);
        }
    });
}

function setupBatchSelector() {
    const batchSelector = document.getElementById('batchSelector');
    
    batchSelector.addEventListener('change', () => {
        const selectedBatchIndex = parseInt(batchSelector.value);
        currentBatchIndex = selectedBatchIndex;
        
        if (subjects && subjects.length > 0) {
            const currentSubject = subjects[currentSubjectIndex];
            if (currentSubject && currentSubject.batches && 
                selectedBatchIndex >= 0 && selectedBatchIndex < currentSubject.batches.length) {
                processActiveBatch(currentSubject.batches[selectedBatchIndex]);
            }
        }
    });
}

function processQuestionData(data) {
    // Store the subjects data
    subjects = data;
    
    // Populate the subject selector
    populateSubjectSelector(subjects);
    
    // If there are subjects, process the first one
    if (subjects && subjects.length > 0) {
        // Set the first subject as active
        currentSubjectIndex = 0;
        
        // Populate batch selector with batches from the first subject
        populateBatchSelector(subjects[0].batches);
        
        // Process the first batch of the first subject
        if (subjects[0].batches && subjects[0].batches.length > 0) {
            currentBatchIndex = 0;
            processActiveBatch(subjects[0].batches[0]);
        }
    }
}

function populateSubjectSelector(subjects) {
    const subjectSelector = document.getElementById('subjectSelector');
    subjectSelector.innerHTML = '';
    
    if (Array.isArray(subjects) && subjects.length > 0) {
        subjects.forEach((subject, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = subject.subject_name || `Subject ${index + 1}`;
            subjectSelector.appendChild(option);
        });
    } else {
        // No subjects available
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'No subjects available';
        option.disabled = true;
        subjectSelector.appendChild(option);
    }
}

function populateBatchSelector(batches) {
    const batchSelector = document.getElementById('batchSelector');
    batchSelector.innerHTML = '';
    
    if (Array.isArray(batches) && batches.length > 0) {
        batches.forEach((batch, index) => {
            const option = document.createElement('option');
            option.value = index;
            option.textContent = batch.batch_name || `Batch ${index + 1}`;
            batchSelector.appendChild(option);
        });
    } else {
        // No batches available
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'No batches available';
        option.disabled = true;
        batchSelector.appendChild(option);
    }
}

function processActiveBatch(batch) {
    // Extract the similar_questions array
    const questions = batch.similar_questions || batch;
    
    // Update dashboard with batch name and statistics
    updateDashboard(questions, batch.batch_name);
    
    // Setup exam filters for this batch
    setupExamFilters(questions);
    
    // Display the questions (will be filtered by the active exam filters)
    displayQuestions(questions);
    
    // Setup search functionality for this batch
    setupSearch(questions);
}

function setupImportModal() {
    const importButton = document.getElementById('importButton');
    const importModal = document.getElementById('importModal');
    const closeModal = document.getElementById('closeModal');
    const cancelImport = document.getElementById('cancelImport');
    const confirmImport = document.getElementById('confirmImport');
    const jsonInput = document.getElementById('jsonInput');
    const importError = document.getElementById('importError');
    
    // Open the modal
    importButton.addEventListener('click', () => {
        importModal.classList.remove('hidden');
        jsonInput.focus();
        
        // Pre-fill with stored data if available
        const storedData = localStorage.getItem('importedQuestionData');
        if (storedData) {
            try {
                const formatted = JSON.stringify(JSON.parse(storedData), null, 2);
                jsonInput.value = formatted;
            } catch (e) {
                jsonInput.value = '';
            }
        }
    });
    
    // Close the modal
    function closeImportModal() {
        importModal.classList.add('hidden');
        importError.classList.add('hidden');
    }
    
    closeModal.addEventListener('click', closeImportModal);
    cancelImport.addEventListener('click', closeImportModal);
    
    // Handle import
    confirmImport.addEventListener('click', () => {
        const jsonText = jsonInput.value.trim();
        
        if (!jsonText) {
            importError.textContent = 'Please enter JSON data.';
            importError.classList.remove('hidden');
            return;
        }
        
        try {
            const data = JSON.parse(jsonText);
            
            // Validate the new structure with subjects and batches
            if (Array.isArray(data)) {
                // Check if it's the new subject-batch format
                if (data.length > 0 && data[0].subject_name && data[0].batches) {
                    // Validate each subject
                    for (const subject of data) {
                        if (!subject.subject_name || !Array.isArray(subject.batches) || subject.batches.length === 0) {
                            throw new Error('Each subject must have a subject_name and non-empty batches array.');
                        }
                        
                        // Validate each batch in the subject
                        for (const batch of subject.batches) {
                            if (!batch.batch_name || !Array.isArray(batch.similar_questions) || batch.similar_questions.length === 0) {
                                throw new Error('Each batch must have a batch_name and non-empty similar_questions array.');
                            }
                            validateQuestionStructure(batch.similar_questions[0]);
                        }
                    }
                }
                // Check if it's the old batch format
                else if (data.length > 0 && data[0].batch_name) {
                    // Convert to new subject-batch format
                    data = [{
                        subject_name: "Imported Subject",
                        batches: data
                    }];
                    
                    // Validate each batch
                    for (const batch of data[0].batches) {
                        if (!Array.isArray(batch.similar_questions) || batch.similar_questions.length === 0) {
                            throw new Error('Each batch must have a non-empty similar_questions array.');
                        }
                        validateQuestionStructure(batch.similar_questions[0]);
                    }
                }
                // Check if it's the oldest format (just an array of questions)
                else {
                    // Convert to new subject-batch format
                    data = [{
                        subject_name: "Imported Subject",
                        batches: [{
                            batch_name: "Imported Batch",
                            similar_questions: data
                        }]
                    }];
                    validateQuestionStructure(data[0].batches[0].similar_questions[0]);
                }
            } 
            // Check if it's a single batch object
            else if (data.batch_name) {
                // Convert to new subject-batch format
                data = [{
                    subject_name: "Imported Subject",
                    batches: [data]
                }];
                validateQuestionStructure(data[0].batches[0].similar_questions[0]);
            }
            // Invalid format
            else {
                throw new Error('Invalid data format. Expected an array of subjects or batches.');
            }
            
            // Store in localStorage
            localStorage.setItem('importedQuestionData', JSON.stringify(data));
            
            // Process the data
            processQuestionData(data);
            
            // Close the modal
            closeImportModal();
            
            // Show success notification
            showNotification('Data imported successfully!', 'success');
            
        } catch (error) {
            console.error('Import error:', error);
            importError.textContent = `Invalid JSON format: ${error.message}`;
            importError.classList.remove('hidden');
        }
    });
    
    // Allow clearing imported data
    const clearImportedData = document.createElement('button');
    clearImportedData.textContent = 'Reset to Default Data';
    clearImportedData.className = 'ml-2 text-sm text-red-600 hover:text-red-800 hover:underline';
    clearImportedData.addEventListener('click', () => {
        if (confirm('Are you sure you want to clear your imported data and reload the default data?')) {
            localStorage.removeItem('importedQuestionData');
            closeImportModal();
            loadDefaultData();
            showNotification('Reset to default data.', 'info');
        }
    });
    
    // Add the clear button to the modal
    document.querySelector('#importModal .flex.items-center.justify-between div:last-child').prepend(clearImportedData);
}

function validateQuestionStructure(question) {
    // Basic validation to ensure it has the right structure
    if (!question) {
        throw new Error('Invalid question object.');
    }
    
    if (!question.question || !question.choices || !question.answer || !question.reference) {
        throw new Error('Each question must have question, choices, answer, and reference properties.');
    }
    
    return true;
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg z-50 ${
        type === 'success' ? 'bg-green-500 text-white' : 'bg-blue-500 text-white'
    }`;
    notification.textContent = message;
    
    // Add to document
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        notification.classList.add('fade-out');
        setTimeout(() => notification.remove(), 500);
    }, 3000);
}

function updateDashboard(questions, batchName = '') {
    // Get all unique exams across all questions
    const allExams = new Set();
    questions.forEach(q => {
        Object.keys(q.question).forEach(exam => allExams.add(exam));
    });
    
    // Calculate exam distribution
    const examCounts = {};
    let totalExamInstances = 0;
    
    // Count occurrences of each exam
    questions.forEach(q => {
        Object.keys(q.question).forEach(exam => {
            examCounts[exam] = (examCounts[exam] || 0) + 1;
            totalExamInstances++;
        });
    });
    
    // Calculate percentages and prepare for visualization
    const examDistribution = [];
    const availableColors = [
        'bg-blue-500', 'bg-purple-500', 'bg-green-500', 'bg-yellow-500', 
        'bg-red-500', 'bg-indigo-500', 'bg-pink-500', 'bg-orange-500',
        'bg-teal-500', 'bg-cyan-500'
    ];
    
    let colorIndex = 0;
    
    // Sort exams by count (descending)
    const sortedExams = Object.keys(examCounts).sort((a, b) => examCounts[b] - examCounts[a]);
    
    sortedExams.forEach(exam => {
        const count = examCounts[exam];
        const percentage = (count / totalExamInstances * 100).toFixed(1);
        const color = availableColors[colorIndex % availableColors.length];
        
        examDistribution.push({
            exam: exam,
            count: count,
            percentage: percentage,
            color: color
        });
        
        colorIndex++;
    });
    
    // Update the dashboard elements
    document.getElementById('totalQuestions').textContent = questions.length;
    document.getElementById('totalExams').textContent = allExams.size;
    
    // Update exam distribution visualization
    updateExamDistributionVisualization(examDistribution);
    
    // Update batch info in the results count
    const subjectName = subjects[currentSubjectIndex]?.subject_name || '';
    const batchInfo = batchName ? `${batchName}` : '';
    const subjectInfo = subjectName ? `${subjectName} - ` : '';
    document.getElementById('resultsCount').textContent = `Showing all ${questions.length} similar question groups (${subjectInfo}${batchInfo})`;
}

function updateExamDistributionVisualization(examDistribution) {
    const distributionBar = document.getElementById('examDistributionBar');
    const distributionLegend = document.getElementById('examDistributionLegend');
    
    // Clear previous content
    distributionBar.innerHTML = '';
    distributionLegend.innerHTML = '';
    
    // Create the distribution bar segments
    examDistribution.forEach(item => {
        const segment = document.createElement('div');
        segment.className = `${item.color} h-full`;
        segment.style.width = `${item.percentage}%`;
        segment.title = `${formatExamName(item.exam)}: ${item.percentage}%`;
        distributionBar.appendChild(segment);
    });
    
    // Create the distribution legend
    const legendHTML = examDistribution.map(item => `
        <div class="flex items-center mt-1">
            <div class="w-3 h-3 ${item.color} rounded-sm mr-1"></div>
            <span>${formatExamName(item.exam)}: ${item.percentage}% (${item.count})</span>
        </div>
    `).join('');
    
    distributionLegend.innerHTML = legendHTML;
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
        
        // Sort exam keys to find the one to preview
        const sortedExams = [...exams].sort((a, b) => {
            // Try numeric sorting first
            const numA = parseInt(a.replace(/[^\d]/g, ''));
            const numB = parseInt(b.replace(/[^\d]/g, ''));
            
            if (!isNaN(numA) && !isNaN(numB)) {
                return numB - numA; // Descending order for largest first
            }
            
            // Fall back to alphabetical sorting
            return b.localeCompare(a); // Descending order for largest first
        });
        
        // Get the exam with the largest key
        const previewExam = sortedExams[0];
        
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
        
        // Create a unique ID for this question's answer toggle
        const toggleId = `answer-toggle-${questionGroup.number}`;
        
        // Question overview (showing full question and choices from the preview exam)
        let overview = `
            <div class="mb-4 border-b pb-4">
                <div class="mb-2 flex justify-between items-center">
                    <div>
                        <span class="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs font-medium">Preview from ${formatExamName(previewExam)}</span>
                    </div>
                    <button class="answer-toggle text-xs bg-blue-50 hover:bg-blue-100 text-blue-600 px-3 py-1 rounded-full flex items-center" data-toggle-id="${toggleId}">
                        <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                        </svg>
                        Show Answer
                    </button>
                </div>
                <div class="text-gray-700 mb-4">
                    <p class="font-medium mb-2">Question:</p>
                    <p class="pl-4">${questionGroup.question[previewExam]}</p>
                </div>
                <div class="text-gray-700">
                    <p class="font-medium mb-2">Choices:</p>
                    <div class="pl-4 space-y-1" id="${toggleId}">
                        ${Object.entries(questionGroup.choices[previewExam]).map(([key, value]) => {
                            const isCorrect = questionGroup.answer[previewExam].toLowerCase() === key.toLowerCase();
                            return `
                                <div class="py-1 ${isCorrect ? 'correct-answer' : ''}">
                                    <span class="${isCorrect ? 'answer-key' : ''}">${key.toUpperCase()}. </span>${value}
                                    ${isCorrect ? `<span class="answer-indicator ml-1 hidden text-green-700">✓</span>` : ''}
                                </div>
                            `;
                        }).join('')}
                        ${questionGroup.rationale && questionGroup.rationale[previewExam] ? `
                        <div class="rationale-preview mt-3 border-l-4 border-blue-200 py-2 px-4 bg-blue-50 rounded-r-md text-gray-700 hidden">
                            <span class="font-medium mb-1">Rationale:</span>
                            <span>${questionGroup.rationale[previewExam]}</span>
                        </div>
                        ` : ''}
                    </div>
                </div>
            </div>
        `;
        
        // Collapsible content
        let collapsibleContent = `<div id="question-${questionGroup.number}" class="collapsible-content">`;
        
        // Question body with comparison
        let questionBody = `<div class="mb-6">`;

        
        // Add each exam's question
        exams.forEach((exam, i) => {
            let rationale = ""
            console.log(questionGroup["rationale"]);
            if (questionGroup.rationale) {
                rationale = questionGroup.rationale[exam]
            }
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

                    ${rationale ? `
                    <div class="mt-4">
                        <div class="pl-4 border-l-4 border-blue-200 py-2 px-4 bg-blue-50 rounded-r-md text-gray-700">
                            <span class="font-medium mb-1">Rationale:</span>
                            <span>${rationale}</span>
                        </div>
                    </div>
                    ` : ''}
                    
                    <div class="mt-4 text-sm text-gray-600">
                        <span class="font-medium">Page:</span> ${questionGroup.reference[exam].reference}
                    </div>
                </div>
            `;
        });
        
        questionBody += `</div>`;
        
        collapsibleContent += questionBody + '</div>';
        
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
    
    // Add event listeners for answer toggle buttons
    document.querySelectorAll('.answer-toggle').forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent triggering the question toggle
            
            const toggleId = this.getAttribute('data-toggle-id');
            const choicesContainer = document.getElementById(toggleId);
            
            if (!choicesContainer) return; // Guard clause if container not found
            
            const correctAnswer = choicesContainer.querySelector('.correct-answer');
            const answerKey = correctAnswer?.querySelector('.answer-key');
            const answerIndicator = correctAnswer?.querySelector('.answer-indicator');
            
            if (!correctAnswer || !answerKey || !answerIndicator) return; // Guard clause if elements not found
            
            const isHidden = answerIndicator.classList.contains('hidden');
            
            if (isHidden) {
                // Show the answer
                answerIndicator.classList.remove('hidden');
                answerKey.classList.add('font-medium', 'text-green-700');
                correctAnswer.classList.add('bg-green-50', 'border-l-2', 'border-green-500', 'pl-2');
                
                // Show rationale if it exists
                const rationalePreview = choicesContainer.querySelector('.rationale-preview');
                if (rationalePreview) {
                    rationalePreview.classList.remove('hidden');
                }
                
                // Update button text and icon
                this.innerHTML = `
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"></path>
                    </svg>Hide Answer`;
            } else {
                // Hide the answer
                answerIndicator.classList.add('hidden');
                answerKey.classList.remove('font-medium', 'text-green-700');
                correctAnswer.classList.remove('bg-green-50', 'border-l-2', 'border-green-500', 'pl-2');
                
                // Hide rationale
                const rationalePreview = choicesContainer.querySelector('.rationale-preview');
                if (rationalePreview) {
                    rationalePreview.classList.add('hidden');
                }
                
                // Update button text and icon
                this.innerHTML = `
                    <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
                    </svg>Show Answer`;
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
    filtersContainer.className = 'flex flex-wrap gap-2 mb-4';
    
    // Add a "Select All / Deselect All" toggle button
    const toggleAllButton = document.createElement('button');
    toggleAllButton.id = 'toggleAllExams';
    toggleAllButton.className = 'px-4 py-2 rounded-lg bg-blue-100 text-blue-700 text-sm font-medium hover:bg-blue-200 mb-2 mr-2 transition-colors duration-200 shadow-sm';
    toggleAllButton.textContent = 'Deselect All';
    toggleAllButton.dataset.state = 'all-selected';
    filtersContainer.appendChild(toggleAllButton);
    
    // Create a warning message div that will be shown when no exams are selected
    const warningDiv = document.createElement('div');
    warningDiv.className = 'hidden bg-yellow-100 border border-yellow-400 text-yellow-700 px-4 py-2 rounded-lg relative mt-2 w-full shadow-sm';
    warningDiv.id = 'noExamsWarning';
    warningDiv.innerHTML = 'Please select at least one examination to display questions.';
    
    // Track selected exams (all selected by default)
    const selectedExams = new Set(allExams);
    
    // Add individual exam filters as toggleable pills
    Array.from(allExams).sort().forEach((exam, index) => {
        const pillButton = document.createElement('button');
        pillButton.id = `exam-filter-${exam}`;
        // Use different styling for selected/unselected state
        pillButton.className = 'px-4 py-2 rounded-lg bg-blue-500 text-white text-sm font-medium hover:bg-blue-600 hover:text-white mb-2 transition-colors duration-200 shadow-sm flex items-center';
        pillButton.dataset.exam = exam;
        pillButton.dataset.selected = 'true'; // All exams selected by default
        
        // Add a checkmark icon to indicate selected state
        pillButton.innerHTML = `
            <svg class="w-4 h-4 mr-1.5 check-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
            </svg>
            <span>${formatExamName(exam)}</span>
        `;
        
        filtersContainer.appendChild(pillButton);
    });
    
    // Add the warning after all pills
    filtersContainer.appendChild(warningDiv);
    
    // Function to apply filters based on selected exams
    function applyExamFilters() {
        // Show warning if no exams are selected
        const noExamsWarning = document.getElementById('noExamsWarning');
        if (selectedExams.size === 0) {
            noExamsWarning.classList.remove('hidden');
            // Don't filter questions when no exams are selected
            return;
        } else {
            noExamsWarning.classList.add('hidden');
        }
        
        // Get the current batch data
        const currentSubject = subjects[currentSubjectIndex];
        const currentBatch = currentSubject?.batches[currentBatchIndex];
        const currentQuestions = currentBatch?.similar_questions || questions;
        
        // Filter questions - show questions that have at least one exam from the selected exams
        const filtered = currentQuestions.filter(q => {
            const questionExams = Object.keys(q.question);
            // Check if all question exams are in the selected exams
            return questionExams.every(exam => selectedExams.has(exam));
        });
        
        displayQuestions(filtered);
        
        // Update results count with filtering info
        const resultsCount = document.getElementById('resultsCount');
        const subjectName = currentSubject?.subject_name || '';
        const batchName = currentBatch?.batch_name || '';
        const subjectInfo = subjectName ? `${subjectName} - ` : '';
        resultsCount.textContent = `Showing ${filtered.length} of ${currentQuestions.length} similar question groups (${subjectInfo}${batchName})`;
    }
    
    // Add event listener for the toggle all button
    toggleAllButton.addEventListener('click', function() {
        const pillButtons = document.querySelectorAll('#examFilters button[data-exam]');
        const currentState = this.dataset.state;
        
        if (currentState === 'all-selected') {
            // Deselect all
            pillButtons.forEach(pill => {
                pill.dataset.selected = 'false';
                pill.classList.remove('bg-blue-500', 'text-white');
                pill.classList.add('bg-gray-200', 'text-gray-700');
                // Hide checkmark
                const checkIcon = pill.querySelector('.check-icon');
                if (checkIcon) checkIcon.classList.add('hidden');
                selectedExams.delete(pill.dataset.exam);
            });
            this.textContent = 'Select All';
            this.dataset.state = 'none-selected';
        } else {
            // Select all
            pillButtons.forEach(pill => {
                pill.dataset.selected = 'true';
                pill.classList.remove('bg-gray-200', 'text-gray-700');
                pill.classList.add('bg-blue-500', 'text-white');
                // Show checkmark
                const checkIcon = pill.querySelector('.check-icon');
                if (checkIcon) checkIcon.classList.remove('hidden');
                selectedExams.add(pill.dataset.exam);
            });
            this.textContent = 'Deselect All';
            this.dataset.state = 'all-selected';
        }
        
        // Apply the filters
        applyExamFilters();
    });
    
    // Add event listeners to pill buttons
    document.querySelectorAll('#examFilters button[data-exam]').forEach(pill => {
        pill.addEventListener('click', function() {
            const exam = this.dataset.exam;
            const isSelected = this.dataset.selected === 'true';
            
            if (isSelected) {
                // Deselect this exam
                this.dataset.selected = 'false';
                this.classList.remove('bg-blue-500', 'text-white');
                this.classList.add('bg-gray-200', 'text-gray-700');
                // Hide checkmark
                const checkIcon = this.querySelector('.check-icon');
                if (checkIcon) checkIcon.classList.add('hidden');
                selectedExams.delete(exam);
            } else {
                // Select this exam
                this.dataset.selected = 'true';
                this.classList.remove('bg-gray-200', 'text-gray-700');
                this.classList.add('bg-blue-500', 'text-white');
                // Show checkmark
                const checkIcon = this.querySelector('.check-icon');
                if (checkIcon) checkIcon.classList.remove('hidden');
                selectedExams.add(exam);
            }
            
            // Update toggle all button state
            const toggleAllButton = document.getElementById('toggleAllExams');
            if (selectedExams.size === allExams.size) {
                toggleAllButton.textContent = 'Deselect All';
                toggleAllButton.dataset.state = 'all-selected';
            } else if (selectedExams.size === 0) {
                toggleAllButton.textContent = 'Select All';
                toggleAllButton.dataset.state = 'none-selected';
            }
            
            // Apply the filters
            applyExamFilters();
        });
    });
    
    // Apply initial filtering (all exams selected by default)
    applyExamFilters();
}

function setupSearch(questions) {
    const searchInput = document.getElementById('searchInput');
    
    searchInput.addEventListener('input', () => {
        const searchTerm = searchInput.value.toLowerCase().trim();
        
        // Get the current subject and batch
        const currentSubject = subjects[currentSubjectIndex];
        const currentBatch = currentSubject?.batches[currentBatchIndex];
        
        // Get the questions from the current batch
        let currentQuestions = currentBatch?.similar_questions || questions;
        
        // Get currently selected exams
        const selectedExams = new Set();
        document.querySelectorAll('#examFilters button[data-exam]').forEach(pill => {
            if (pill.dataset.selected === 'true') {
                selectedExams.add(pill.dataset.exam);
            }
        });
        
        // First filter by selected exams
        let filteredByExams = currentQuestions;
        
        // Only apply exam filtering if at least one exam is selected
        if (selectedExams.size > 0) {
            filteredByExams = currentQuestions.filter(q => {
                const questionExams = Object.keys(q.question);
                return questionExams.some(exam => selectedExams.has(exam));
            });
        }
        
        // Then filter by search term
        if (searchTerm === '') {
            displayQuestions(filteredByExams);
            return;
        }
        
        const filteredQuestions = filteredByExams.filter(q => {
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
        
        // Update results count with filtering info
        const resultsCount = document.getElementById('resultsCount');
        const subjectName = currentSubject?.subject_name || '';
        const batchName = currentBatch?.batch_name || '';
        const subjectInfo = subjectName ? `${subjectName} - ` : '';
        resultsCount.textContent = `Showing ${filteredQuestions.length} of ${currentQuestions.length} similar question groups (${subjectInfo}${batchName})`;
    });
}

function importJSON() {
    const jsonInput = document.getElementById('jsonInput').value.trim();
    const importError = document.getElementById('importError');
    
    if (!jsonInput) {
        importError.textContent = 'Please enter JSON data.';
        return;
    }
    
    try {
        let jsonData = JSON.parse(jsonInput);
        
        // Handle case where JSON is an array of batches
        if (Array.isArray(jsonData)) {
            batches = jsonData;
        } else {
            // Handle case where JSON is a single batch object
            batches = [jsonData];
        }
        
        // Validate each batch
        for (let i = 0; i < batches.length; i++) {
            const batch = batches[i];
            if (!batch.similar_questions || !Array.isArray(batch.similar_questions) || batch.similar_questions.length === 0) {
                importError.textContent = `Batch ${i+1} is missing valid questions data.`;
                return;
            }
        }
        
        currentBatchIndex = 0;
        updateBatchSelector();
        updateDashboard();
        displayQuestions(filterQuestions());
        
        importError.textContent = '';
        document.getElementById('jsonInput').value = '';
        document.getElementById('importModal').style.display = 'none';
    } catch (e) {
        importError.textContent = `Invalid JSON format: ${e.message}`;
    }
}

function filterQuestions() {
    if (!batches || batches.length === 0 || currentBatchIndex === undefined) {
        return [];
    }
    
    // Return the current batch's questions
    return batches[currentBatchIndex].similar_questions || [];
}

function updateBatchSelector() {
    const batchSelector = document.getElementById('batchSelector');
    batchSelector.innerHTML = '';
    
    if (!batches || batches.length === 0) {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'No batches available';
        option.disabled = true;
        option.selected = true;
        batchSelector.appendChild(option);
        return;
    }
    
    batches.forEach((batch, index) => {
        const option = document.createElement('option');
        option.value = index;
        option.textContent = batch.batch_name || `Batch ${index + 1}`;
        batchSelector.appendChild(option);
    });
    
    batchSelector.value = currentBatchIndex;
    
    // Trigger the change event to update the display
    const event = new Event('change');
    batchSelector.dispatchEvent(event);
}

function setupDashboardStatsToggle() {
    // Get the dashboard stats container
    const dashboardStats = document.getElementById('dashboardStats');
    
    // Create toggle button
    const toggleButton = document.createElement('button');
    toggleButton.id = 'toggleDashboardStats';
    toggleButton.className = 'text-gray-600 hover:text-blue-600 text-sm flex items-center mb-3 transition-colors duration-200 bg-gray-50 hover:bg-gray-100 px-3 py-1.5 rounded-lg shadow-sm';
    toggleButton.innerHTML = `
        <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
        </svg>
        <span>Hide Statistics</span>
    `;
    
    // Create a container for the toggle button
    const toggleContainer = document.createElement('div');
    toggleContainer.className = 'flex justify-end mb-1';
    toggleContainer.appendChild(toggleButton);
    
    // Check if stats should be hidden based on localStorage
    const statsHidden = localStorage.getItem('dashboardStatsHidden') === 'true';
    if (statsHidden) {
        dashboardStats.classList.add('hidden');
        toggleButton.innerHTML = `
            <svg class="w-4 h-4 mr-1.5 transform -rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
            <span>Show Statistics</span>
        `;
    }
    
    // Add click event to toggle stats visibility
    toggleButton.addEventListener('click', () => {
        const isHidden = dashboardStats.classList.contains('hidden');
        
        if (isHidden) {
            // Show stats
            dashboardStats.classList.remove('hidden');
            toggleButton.innerHTML = `
                <svg class="w-4 h-4 mr-1.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
                <span>Hide Statistics</span>
            `;
            localStorage.setItem('dashboardStatsHidden', 'false');
        } else {
            // Hide stats
            dashboardStats.classList.add('hidden');
            toggleButton.innerHTML = `
                <svg class="w-4 h-4 mr-1.5 transform -rotate-90" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
                <span>Show Statistics</span>
            `;
            localStorage.setItem('dashboardStatsHidden', 'true');
        }
    });
    
    // Insert toggle container before the dashboard stats
    dashboardStats.parentNode.insertBefore(toggleContainer, dashboardStats);
}