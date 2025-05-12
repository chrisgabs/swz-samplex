<script lang="ts">
    import type { Question } from '../types';
    import { formatExamName, getCommonAnswer, extractTopic, getLatestExamination } from '../utils';
    
    export let questionGroup: Question;
    
    let expanded = false;
    
    function toggleExpand() {
        expanded = !expanded;
    }
    
    $: exams = Object.keys(questionGroup.question);
    $: latestExam = getLatestExamination(questionGroup);
    $: commonAnswer = getCommonAnswer(questionGroup);
</script>

<div class="bg-white rounded-lg shadow-md p-6 fade-in mb-6 {expanded ? 'expanded' : ''}" data-number={questionGroup.number}>
    <div class="flex justify-between items-start mb-4">
        <div>
            <div class="flex items-center gap-2">
                <span class="bg-blue-100 text-blue-800 text-sm font-semibold px-2.5 py-0.5 rounded">
                    Question {questionGroup.number}
                </span>
                {#each exams.slice(0, 3) as exam, index}
                    <span class="exam-pill exam-pill-{(index % 3) + 1}">
                        {formatExamName(exam)}
                    </span>
                {/each}
                {#if exams.length > 3}
                    <span class="text-gray-500 text-sm">+{exams.length - 3} more</span>
                {/if}
            </div>
            
            <!-- Show full question from latest exam in summary -->
            <div class="mt-2">
                <p class="text-gray-800">{questionGroup.question[latestExam]}</p>
                
                {#if questionGroup.choices[latestExam]}
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mt-3">
                        {#each Object.entries(questionGroup.choices[latestExam]) as [choice, text]}
                            <div class="p-2 rounded-md border border-gray-200 {choice === questionGroup.answer[latestExam] ? 'choice-correct' : ''}">
                                <span class="font-medium">{choice}.</span> {text}
                            </div>
                        {/each}
                    </div>
                {/if}
                
                {#if questionGroup.answer[latestExam]}
                    <div class="mt-2 text-sm">
                        <span class="font-medium text-green-700">Answer:</span> 
                        <span class="text-green-800">{questionGroup.answer[latestExam]}</span>
                    </div>
                {/if}
            </div>
        </div>
        
        <button 
            class="toggle-question p-2 text-gray-500 hover:text-gray-700 focus:outline-none" 
            on:click={toggleExpand}
            aria-label={expanded ? "Collapse question" : "Expand question"}
        >
            <svg class="w-5 h-5" class:rotate-180={expanded} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
            </svg>
        </button>
    </div>
    
    <div class="collapsible-content">
        {#each exams as exam}
            {#if exam !== latestExam}
                <div class="exam-container mb-8">
                    <div class="mb-2">
                        <span class="font-semibold text-gray-700">{formatExamName(exam)}</span>
                    </div>
                    
                    <div class="mb-4">
                        <p class="text-gray-800">{questionGroup.question[exam]}</p>
                    </div>
                    
                    {#if questionGroup.choices[exam]}
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-2 mb-4">
                            {#each Object.entries(questionGroup.choices[exam]) as [choice, text]}
                                <div class="p-2 rounded-md border border-gray-200 {choice === questionGroup.answer[exam] ? 'choice-correct' : ''}">
                                    <span class="font-medium">{choice}.</span> {text}
                                </div>
                            {/each}
                        </div>
                    {/if}
                    
                    <div class="flex flex-wrap gap-4 text-sm">
                        {#if questionGroup.answer[exam]}
                            <div>
                                <span class="font-medium text-green-700">Answer:</span> 
                                <span class="text-green-800">{questionGroup.answer[exam]}</span>
                            </div>
                        {/if}
                        
                        {#if questionGroup.reference[exam]}
                            <div>
                                <span class="font-medium text-blue-700">Reference:</span> 
                                <span class="text-blue-800">{questionGroup.reference[exam]}</span>
                            </div>
                        {/if}
                    </div>
                </div>
            {/if}
        {/each}
    </div>
    
    <div class="mt-2 text-sm text-gray-500 flex justify-between items-center">
        <div>
            <span class="font-medium">From:</span> {formatExamName(latestExam)}
        </div>
        <div>
            <button 
                class="text-blue-600 hover:text-blue-800 hover:underline focus:outline-none"
                on:click={toggleExpand}
            >
                {expanded ? 'Show Less' : 'Show More Exams'}
            </button>
        </div>
    </div>
</div> 