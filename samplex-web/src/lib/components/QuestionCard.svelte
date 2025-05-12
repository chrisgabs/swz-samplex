<script lang="ts">
    import type { Question } from '../types';
    import { formatExamName, getCommonAnswer, getLatestExamination } from '../utils';
    
    export let questionGroup: Question;
    
    let expanded = false;
    let showAnswer = false;
    
    function toggleExpand() {
        expanded = !expanded;
    }
    
    function toggleAnswer() {
        showAnswer = !showAnswer;
    }
    
    $: exams = Object.keys(questionGroup.question);
    $: latestExam = getLatestExamination(questionGroup);
</script>

<div class="bg-white rounded-lg shadow-md p-6 fade-in mb-6 {expanded ? 'expanded' : ''}" data-number={questionGroup.number}>
    <div class="flex justify-between items-center mb-6">
        <h2 class="text-2xl font-bold text-gray-800">Question {questionGroup.number}</h2>
        
        <div class="flex items-center gap-2">
            {#each exams.slice(0, 3) as exam, index}
                <span class="exam-pill exam-pill-{(index % 3) + 1}">
                    {formatExamName(exam)}
                </span>
            {/each}
            {#if exams.length > 3}
                <span class="text-gray-500 text-sm">+{exams.length - 3} more</span>
            {/if}
            
            <button 
                class="toggle-question p-2 text-gray-500 hover:text-gray-700 focus:outline-none ml-2" 
                on:click={toggleExpand}
                aria-label={expanded ? "Collapse question" : "Expand question"}
            >
                <svg class="w-5 h-5" class:rotate-180={expanded} fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7"></path>
                </svg>
            </button>
        </div>
    </div>
    
    <div class="flex justify-between items-center mb-4">
        <p class="text-lg text-gray-600">Preview from {formatExamName(latestExam)}</p>
        
        <button 
            class="{showAnswer ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700'} hover:opacity-90 flex items-center gap-2 px-4 py-2 rounded-full whitespace-nowrap"
            on:click={toggleAnswer}
        >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path>
            </svg>
            {showAnswer ? 'Hide Answer' : 'Show Answer'}
        </button>
    </div>
    
    <div class="mb-6">
        <h3 class="text-xl font-semibold text-gray-700 mb-4">Question:</h3>
        <p class="text-gray-800 text-lg mb-6">{questionGroup.question[latestExam]}</p>
        
        <h3 class="text-xl font-semibold text-gray-700 mb-4">Choices:</h3>
        {#if questionGroup.choices[latestExam]}
            <div class="grid grid-cols-1 gap-3 mb-4">
                {#each Object.entries(questionGroup.choices[latestExam]) as [choice, text]}
                    <div class="p-3 {showAnswer && choice === questionGroup.answer[latestExam] ? 'bg-green-50 border-l-4 border-green-500' : ''} transition-all duration-200">
                        <span class="font-medium">{choice.toUpperCase()}.</span> {text}
                    </div>
                {/each}
            </div>
        {/if}
    </div>
    
    {#if expanded}
        <hr class="my-6 border-gray-200" />
        
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
                            <div class="grid grid-cols-1 gap-2 mb-4">
                                {#each Object.entries(questionGroup.choices[exam]) as [choice, text]}
                                    <div class="p-2 {choice === questionGroup.answer[exam] ? 'bg-green-50 border-l-4 border-green-500' : ''} transition-all duration-200">
                                        <span class="font-medium">{choice.toUpperCase()}.</span> {text}
                                    </div>
                                {/each}
                            </div>
                        {/if}
                        
                        {#if questionGroup.reference[exam]}
                            <div class="text-sm mt-2">
                                <span class="font-medium text-blue-700">Reference:</span> 
                                <span class="text-blue-800">{questionGroup.reference[exam]}</span>
                            </div>
                        {/if}
                    </div>
                {/if}
            {/each}
        </div>
    {/if}
</div> 