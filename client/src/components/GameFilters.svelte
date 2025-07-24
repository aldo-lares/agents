<script lang="ts">
    import { onMount } from "svelte";
    import { createEventDispatcher } from "svelte";

    interface Category {
        id: number;
        name: string;
    }

    interface Publisher {
        id: number;
        name: string;
    }

    export let selectedCategoryId: number | null = null;
    export let selectedPublisherId: number | null = null;

    let categories: Category[] = [];
    let publishers: Publisher[] = [];
    let loadingCategories = true;
    let loadingPublishers = true;
    let categoriesError: string | null = null;
    let publishersError: string | null = null;

    const dispatch = createEventDispatcher<{
        filterChange: {
            categoryId: number | null;
            publisherId: number | null;
        };
    }>();

    /**
     * Fetch all categories from the API
     */
    const fetchCategories = async () => {
        loadingCategories = true;
        try {
            const response = await fetch('/api/categories');
            if (response.ok) {
                categories = await response.json();
            } else {
                categoriesError = `Failed to fetch categories: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            categoriesError = `Error fetching categories: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loadingCategories = false;
        }
    };

    /**
     * Fetch all publishers from the API
     */
    const fetchPublishers = async () => {
        loadingPublishers = true;
        try {
            const response = await fetch('/api/publishers');
            if (response.ok) {
                publishers = await response.json();
            } else {
                publishersError = `Failed to fetch publishers: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            publishersError = `Error fetching publishers: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loadingPublishers = false;
        }
    };

    const handleCategoryChange = (event: Event) => {
        const target = event.target as HTMLSelectElement;
        selectedCategoryId = target.value ? parseInt(target.value) : null;
        dispatch('filterChange', {
            categoryId: selectedCategoryId,
            publisherId: selectedPublisherId
        });
    };

    const handlePublisherChange = (event: Event) => {
        const target = event.target as HTMLSelectElement;
        selectedPublisherId = target.value ? parseInt(target.value) : null;
        dispatch('filterChange', {
            categoryId: selectedCategoryId,
            publisherId: selectedPublisherId
        });
    };

    const clearFilters = () => {
        selectedCategoryId = null;
        selectedPublisherId = null;
        dispatch('filterChange', {
            categoryId: null,
            publisherId: null
        });
    };

    onMount(() => {
        fetchCategories();
        fetchPublishers();
    });
</script>

<div class="mb-6">
    <div class="flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <h2 class="text-2xl font-medium text-slate-100">Featured Games</h2>
        
        <div class="flex flex-col sm:flex-row gap-3 items-start sm:items-center">
            <!-- Category Filter -->
            <div class="flex flex-col">
                <label for="category-filter" class="text-sm text-slate-300 mb-1">Category</label>
                {#if loadingCategories}
                    <div class="animate-pulse bg-slate-700 rounded h-10 w-40"></div>
                {:else if categoriesError}
                    <div class="text-red-400 text-sm">Error loading categories</div>
                {:else}
                    <select
                        id="category-filter"
                        class="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-w-[160px]"
                        value={selectedCategoryId || ''}
                        on:change={handleCategoryChange}
                        data-testid="category-filter"
                    >
                        <option value="">All Categories</option>
                        {#each categories as category (category.id)}
                            <option value={category.id}>{category.name}</option>
                        {/each}
                    </select>
                {/if}
            </div>

            <!-- Publisher Filter -->
            <div class="flex flex-col">
                <label for="publisher-filter" class="text-sm text-slate-300 mb-1">Publisher</label>
                {#if loadingPublishers}
                    <div class="animate-pulse bg-slate-700 rounded h-10 w-40"></div>
                {:else if publishersError}
                    <div class="text-red-400 text-sm">Error loading publishers</div>
                {:else}
                    <select
                        id="publisher-filter"
                        class="bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-slate-100 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent min-w-[160px]"
                        value={selectedPublisherId || ''}
                        on:change={handlePublisherChange}
                        data-testid="publisher-filter"
                    >
                        <option value="">All Publishers</option>
                        {#each publishers as publisher (publisher.id)}
                            <option value={publisher.id}>{publisher.name}</option>
                        {/each}
                    </select>
                {/if}
            </div>

            <!-- Clear Filters Button -->
            {#if selectedCategoryId || selectedPublisherId}
                <button
                    class="mt-6 sm:mt-0 px-4 py-2 bg-slate-700 hover:bg-slate-600 text-slate-300 rounded-lg transition-colors duration-200 text-sm"
                    on:click={clearFilters}
                    data-testid="clear-filters"
                >
                    Clear Filters
                </button>
            {/if}
        </div>
    </div>
</div>
