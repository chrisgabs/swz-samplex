<script lang="ts">
    import { searchTerm, filteredQuestions, currentBatch } from '../stores';
    
    let inputValue = '';
    
    // Update the search term when input changes
    function handleInput(event: Event) {
        const input = event.target as HTMLInputElement;
        inputValue = input.value;
        searchTerm.set(inputValue);
    }
    
    // Clear the search term
    function clearSearch() {
        inputValue = '';
        searchTerm.set('');
    }
</script>

<div class="flex justify-between items-center mb-4">
    <div class="text-lg font-medium text-gray-700">
        {#if $currentBatch}
            Showing {$filteredQuestions.length} of {$currentBatch.similar_questions.length} 
            {$currentBatch.similar_questions.length === 1 ? 'question' : 'questions'}
            {$currentBatch.batch_name ? `(${$currentBatch.batch_name})` : ''}
        {:else}
            Loading questions...
        {/if}
    </div>
    
    <div class="relative">
        <input 
            type="text" 
            placeholder="Search questions..." 
            class="px-4 py-2 pr-10 border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 w-64"
            bind:value={inputValue}
            on:input={handleInput}
        >
        {#if inputValue}
            <button 
                class="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-gray-600"
                on:click={clearSearch}
                aria-label="Clear search"
            >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                </svg>
            </button>
        {/if}
    </div>
</div> 