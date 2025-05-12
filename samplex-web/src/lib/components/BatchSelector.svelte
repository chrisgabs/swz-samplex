<script lang="ts">
    import { batches, currentBatchIndex } from '../stores';
    
    function handleBatchChange(event: Event) {
        const select = event.target as HTMLSelectElement;
        const selectedIndex = parseInt(select.value);
        if (!isNaN(selectedIndex) && selectedIndex >= 0 && selectedIndex < $batches.length) {
            currentBatchIndex.set(selectedIndex);
        }
    }
</script>

<div>
    <label for="batchSelector" class="block text-sm font-medium text-gray-700 mb-2">Select Subject:</label>
    <select 
        id="batchSelector" 
        class="w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
        on:change={handleBatchChange}
        value={$currentBatchIndex}
    >
        {#if $batches.length === 0}
            <option value="" disabled selected>Loading batches...</option>
        {:else}
            {#each $batches as batch, index}
                <option value={index}>{batch.batch_name || `Batch ${index + 1}`}</option>
            {/each}
        {/if}
    </select>
</div> 