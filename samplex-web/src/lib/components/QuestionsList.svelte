<script lang="ts">
    import { filteredQuestions } from '../stores';
    import QuestionCard from './QuestionCard.svelte';
</script>

<div class="space-y-6">
    {#if $filteredQuestions.length > 0}
        {#each $filteredQuestions as questionGroup (questionGroup.number)}
            <QuestionCard {questionGroup} />
        {/each}
    {:else}
        <div class="text-center py-10 text-gray-500">
            {#if $filteredQuestions.length === 0}
                No questions found matching your criteria
            {:else}
                Loading questions...
            {/if}
        </div>
    {/if}
</div> 