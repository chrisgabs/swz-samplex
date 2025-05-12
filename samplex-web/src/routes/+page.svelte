<script lang="ts">
    import { onMount } from 'svelte';
    import { initializeApp } from '$lib/services/dataService';
    import Dashboard from '$lib/components/Dashboard.svelte';
    import BatchSelector from '$lib/components/BatchSelector.svelte';
    import ImportModal from '$lib/components/ImportModal.svelte';
    import SearchBar from '$lib/components/SearchBar.svelte';
    import QuestionsList from '$lib/components/QuestionsList.svelte';
    
    onMount(() => {
        // Initialize the app with data
        initializeApp();
    });
</script>

<svelte:head>
    <title>Exam Question Cross-Referencer</title>
</svelte:head>

<div class="bg-gray-100 min-h-screen">
    <div class="container mx-auto max-w-3xl px-4 py-8">
        <header class="mb-8">
            <h1 class="text-3xl font-bold text-center text-blue-800">Exam Question Cross-Referencer</h1>
            <p class="text-center text-gray-600 mt-2">Displaying similar questions found across different examinations</p>
        </header>

        <!-- Dashboard Section -->
        <Dashboard>
            <svelte:fragment slot="batch-selector">
                <BatchSelector />
            </svelte:fragment>
            
            <svelte:fragment slot="import-button">
                <ImportModal />
            </svelte:fragment>
        </Dashboard>

        <!-- Search Section -->
        <SearchBar />

        <!-- Questions List -->
        <QuestionsList />
    </div>
</div>
