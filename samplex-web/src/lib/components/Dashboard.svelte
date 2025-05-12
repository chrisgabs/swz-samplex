<!-- Dashboard component for displaying statistics and filters -->
<script lang="ts">
    import { currentBatch, activeFilters } from '../stores';
    import { calculateExamDistribution, formatExamName } from '../utils';
    import type { ExamDistributionItem } from '../types';
    
    let examDistribution: ExamDistributionItem[] = [];
    let uniqueExams: string[] = [];
    
    // Update when current batch changes
    $: if ($currentBatch) {
        examDistribution = calculateExamDistribution($currentBatch.similar_questions);
        
        // Get all unique exams
        const examsSet = new Set<string>();
        $currentBatch.similar_questions.forEach(q => {
            Object.keys(q.question).forEach(exam => examsSet.add(exam));
        });
        uniqueExams = Array.from(examsSet);
    }
    
    // Toggle exam filter
    function toggleFilter(exam: string) {
        if ($activeFilters.includes(exam)) {
            // Remove from filters
            activeFilters.update(filters => filters.filter(f => f !== exam));
        } else {
            // Add to filters
            activeFilters.update(filters => [...filters, exam]);
        }
    }
</script>

<div class="bg-white rounded-lg shadow-md p-6 mb-8">
    <div class="flex justify-between items-center mb-4">
        <div class="flex gap-4 items-center">
            <h2 class="text-xl font-semibold text-gray-800">Dashboard</h2>
            <div class="flex gap-1.5 items-center">
                <img src="/res/boi.jpeg" alt="boi" class="w-7 h-7 rounded-full">
                <img src="/res/gorl.jpeg" alt="gorl" class="w-7 h-7 rounded-full">
            </div>
        </div>
        <slot name="import-button"></slot>
    </div>
    
    <!-- Batch Selector -->
    <div class="mb-6">
        <slot name="batch-selector"></slot>
    </div>
    
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div class="bg-blue-50 rounded-lg p-4 border border-blue-100">
            <div class="text-blue-800 text-2xl font-bold">
                {$currentBatch?.similar_questions.length || 0}
            </div>
            <div class="text-blue-600 text-sm">Total Similar Questions</div>
        </div>
        <div class="bg-purple-50 rounded-lg p-4 border border-purple-100">
            <div class="text-purple-800 text-2xl font-bold">
                {uniqueExams.length}
            </div>
            <div class="text-purple-600 text-sm">Reference Exams</div>
        </div>
        <div class="bg-green-50 rounded-lg p-4 border border-green-100">
            <div class="text-green-800 font-medium">Exam Distribution</div>
            <div class="mt-2 h-6 rounded-md overflow-hidden flex" id="examDistributionBar">
                {#if examDistribution.length > 0}
                    {#each examDistribution as item}
                        <div 
                            class={item.color + " h-full"} 
                            style="width: {item.percentage}%"
                            title="{formatExamName(item.exam)}: {item.percentage}%"
                        ></div>
                    {/each}
                {:else}
                    <div class="bg-gray-200 h-full w-full flex items-center justify-center">
                        <span class="text-xs text-gray-500">Loading...</span>
                    </div>
                {/if}
            </div>
            <div class="mt-2 text-xs text-gray-600">
                {#each examDistribution as item}
                    <div class="flex items-center mt-1">
                        <div class="w-3 h-3 {item.color} rounded-sm mr-1"></div>
                        <span>{formatExamName(item.exam)}: {item.percentage}% ({item.count})</span>
                    </div>
                {/each}
            </div>
        </div>
    </div>
    
    <div class="border-t border-gray-200 pt-4">
        <h3 class="font-medium text-gray-700 mb-3">Quick Filters:</h3>
        <div class="flex flex-wrap gap-2">
            {#each uniqueExams as exam}
                <button 
                    class="exam-pill {$activeFilters.includes(exam) ? 'active-filter' : 'bg-gray-100 text-gray-700'}"
                    on:click={() => toggleFilter(exam)}
                >
                    {formatExamName(exam)}
                </button>
            {/each}
            
            {#if uniqueExams.length === 0}
                <span class="text-gray-400 italic">Loading exam filters...</span>
            {/if}
        </div>
    </div>
</div> 