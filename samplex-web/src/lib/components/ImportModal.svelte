<script lang="ts">
    import { importJSON, resetToDefaultData } from '../services/dataService';
    
    let showModal = false;
    let jsonInput = '';
    let importError = '';
    
    function openModal() {
        showModal = true;
        importError = '';
        
        // Pre-fill with stored data if available
        const storedData = localStorage.getItem('importedQuestionData');
        if (storedData) {
            try {
                const formatted = JSON.stringify(JSON.parse(storedData), null, 2);
                jsonInput = formatted;
            } catch (e) {
                jsonInput = '';
            }
        }
        
        // Focus the textarea after the modal is visible
        setTimeout(() => {
            const textarea = document.getElementById('jsonInput');
            if (textarea) textarea.focus();
        }, 100);
    }
    
    function closeModal() {
        showModal = false;
    }
    
    function handleImport() {
        importError = '';
        
        if (importJSON(jsonInput)) {
            closeModal();
        } else {
            // Error message is shown by the importJSON function
        }
    }
    
    function handleReset() {
        if (confirm('Are you sure you want to clear your imported data and reload the default data?')) {
            resetToDefaultData();
            closeModal();
        }
    }
</script>

<!-- Import Button -->
<button 
    on:click={openModal}
    class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center"
>
    <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M9 19l3 3m0 0l3-3m-3 3V10"></path>
    </svg>
    Import JSON Data
</button>

<!-- Import Modal -->
{#if showModal}
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-lg shadow-lg max-w-4xl w-full p-6 max-h-screen overflow-y-auto">
            <div class="flex justify-between items-center mb-4">
                <h3 class="text-xl font-semibold text-gray-800">Import Similar Questions JSON Data</h3>
                <button on:click={closeModal} class="text-gray-500 hover:text-gray-700">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
            
            <div class="mb-4">
                <p class="text-gray-600 mb-2">Paste your JSON data below. The format should match the new batch structure.</p>
                <textarea 
                    id="jsonInput"
                    bind:value={jsonInput}
                    class="w-full h-64 px-3 py-2 text-gray-700 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-mono text-sm"
                    placeholder="Paste your JSON data here..."
                ></textarea>
            </div>
            
            <div class="flex items-center justify-between">
                <div class="text-red-600 text-sm" class:hidden={!importError}>
                    {importError}
                </div>
                <div class="flex space-x-2">
                    <button 
                        on:click={handleReset}
                        class="ml-2 text-sm text-red-600 hover:text-red-800 hover:underline"
                    >
                        Reset to Default Data
                    </button>
                    <button 
                        on:click={closeModal}
                        class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-100"
                    >
                        Cancel
                    </button>
                    <button 
                        on:click={handleImport}
                        class="px-4 py-2 bg-blue-600 rounded-lg text-white hover:bg-blue-700"
                    >
                        Import Data
                    </button>
                </div>
            </div>
        </div>
    </div>
{/if} 