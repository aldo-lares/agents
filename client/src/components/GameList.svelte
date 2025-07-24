<script lang="ts">
    import { onMount } from "svelte";
    import GameFilters from './GameFilters.svelte';

    interface Game {
        id: number;
        title: string;
        description: string;
        publisher_name?: string;
        category_name?: string;
        starRating?: number;
        publisher?: { name: string };
        category?: { name: string };
    }

    export let games: Game[] = [];
    let loading = true;
    let error: string | null = null;
    let selectedCategoryId: number | null = null;
    let selectedPublisherId: number | null = null;

    /**
     * Get URL parameters for filtering
     */
    const getUrlParams = () => {
        if (typeof window !== 'undefined') {
            const urlParams = new URLSearchParams(window.location.search);
            const categoryId = urlParams.get('category_id');
            const publisherId = urlParams.get('publisher_id');
            
            return {
                categoryId: categoryId ? parseInt(categoryId) : null,
                publisherId: publisherId ? parseInt(publisherId) : null
            };
        }
        return { categoryId: null, publisherId: null };
    };

    /**
     * Update URL with current filter parameters
     */
    const updateUrlParams = (categoryId: number | null, publisherId: number | null) => {
        if (typeof window !== 'undefined') {
            const url = new URL(window.location.href);
            
            if (categoryId) {
                url.searchParams.set('category_id', categoryId.toString());
            } else {
                url.searchParams.delete('category_id');
            }
            
            if (publisherId) {
                url.searchParams.set('publisher_id', publisherId.toString());
            } else {
                url.searchParams.delete('publisher_id');
            }
            
            // Update URL without reloading the page
            window.history.replaceState({}, '', url.toString());
        }
    };

    /**
     * Fetch games from the API with optional filtering
     * @param categoryId - Optional category ID to filter by
     * @param publisherId - Optional publisher ID to filter by
     */
    const fetchGames = async (categoryId: number | null = null, publisherId: number | null = null) => {
        loading = true;
        error = null;
        
        try {
            // Build query parameters
            const params = new URLSearchParams();
            if (categoryId) {
                params.append('category_id', categoryId.toString());
            }
            if (publisherId) {
                params.append('publisher_id', publisherId.toString());
            }
            
            const queryString = params.toString();
            const url = queryString ? `/api/games?${queryString}` : '/api/games';
            
            const response = await fetch(url);
            if(response.ok) {
                games = await response.json();
            } else {
                error = `Failed to fetch data: ${response.status} ${response.statusText}`;
            }
        } catch (err) {
            error = `Error: ${err instanceof Error ? err.message : String(err)}`;
        } finally {
            loading = false;
        }
    };

    const handleFilterChange = (event: CustomEvent<{ categoryId: number | null; publisherId: number | null }>) => {
        selectedCategoryId = event.detail.categoryId;
        selectedPublisherId = event.detail.publisherId;
        
        // Update URL with new filter parameters
        updateUrlParams(selectedCategoryId, selectedPublisherId);
        
        // Fetch filtered games
        fetchGames(selectedCategoryId, selectedPublisherId);
    };

    /**
     * Render star rating as visual stars
     * @param rating - The star rating (0-5)
     * @returns HTML string for star display
     */
    const renderStarRating = (rating: number): string => {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);
        
        return '★'.repeat(fullStars) + 
               (hasHalfStar ? '☆' : '') + 
               '☆'.repeat(emptyStars);
    };

    onMount(() => {
        // Read initial filter state from URL
        const urlParams = getUrlParams();
        selectedCategoryId = urlParams.categoryId;
        selectedPublisherId = urlParams.publisherId;
        
        // Fetch games with initial filters
        fetchGames(selectedCategoryId, selectedPublisherId);
    });
</script>

<div>
    <GameFilters 
        bind:selectedCategoryId 
        bind:selectedPublisherId 
        on:filterChange={handleFilterChange}
    />
    
    {#if loading}
        <!-- loading animation -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {#each Array(6) as _, i}
                <div class="bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50">
                    <div class="p-6">
                        <div class="animate-pulse">
                            <div class="h-6 bg-slate-700 rounded w-3/4 mb-3"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/2 mb-4"></div>
                            <div class="h-3 bg-slate-700 rounded w-full mb-3"></div>
                            <div class="h-3 bg-slate-700 rounded w-5/6 mb-4"></div>
                            <div class="h-2 bg-slate-700 rounded-full w-full mb-2"></div>
                            <div class="h-4 bg-slate-700 rounded w-1/4 mt-4"></div>
                        </div>
                    </div>
                </div>
            {/each}
        </div>
    {:else if error}
        <!-- error display -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-red-400">{error}</p>
        </div>
    {:else if games.length === 0}
        <!-- no games found -->
        <div class="text-center py-12 bg-slate-800/50 backdrop-blur-sm rounded-xl border border-slate-700">
            <p class="text-slate-300">No games available at the moment.</p>
        </div>
    {:else}
        <!-- game list -->
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6" data-testid="games-grid">
            {#each games as game (game.id)}
                <a 
                    href={`/game/${game.id}`} 
                    class="group block bg-slate-800/60 backdrop-blur-sm rounded-xl overflow-hidden shadow-lg border border-slate-700/50 hover:border-blue-500/50 hover:shadow-blue-500/10 hover:shadow-xl transition-all duration-300 hover:translate-y-[-6px]"
                    data-testid="game-card"
                    data-game-id={game.id}
                    data-game-title={game.title}
                >
                    <div class="p-6 relative">
                        <div class="absolute inset-0 bg-gradient-to-r from-blue-600/10 to-purple-600/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300"></div>
                        <div class="relative z-10">
                            <h3 class="text-xl font-semibold text-slate-100 mb-2 group-hover:text-blue-400 transition-colors" data-testid="game-title">{game.title}</h3>
                            
                            {#if (game.category?.name || game.category_name) || (game.publisher?.name || game.publisher_name)}
                                <div class="flex gap-2 mb-3">
                                    {#if game.category?.name || game.category_name}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-blue-900/60 text-blue-300" data-testid="game-category">
                                            {game.category?.name || game.category_name}
                                        </span>
                                    {/if}
                                    {#if game.publisher?.name || game.publisher_name}
                                        <span class="text-xs font-medium px-2.5 py-0.5 rounded bg-purple-900/60 text-purple-300" data-testid="game-publisher">
                                            {game.publisher?.name || game.publisher_name}
                                        </span>
                                    {/if}
                                </div>
                            {/if}
                            
                            <p class="text-slate-400 mb-4 text-sm line-clamp-2" data-testid="game-description">{game.description}</p>
                            
                            {#if game.starRating}
                                <div class="flex items-center gap-2 mb-4">
                                    <span class="text-yellow-400 text-sm" data-testid="game-rating">
                                        {@html renderStarRating(game.starRating)}
                                    </span>
                                    <span class="text-slate-400 text-xs">({game.starRating})</span>
                                </div>
                            {/if}
                            
                            <div class="mt-4 text-sm text-blue-400 font-medium flex items-center">
                                <span>View details</span>
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 ml-1 transform transition-transform duration-300 group-hover:translate-x-2" viewBox="0 0 20 20" fill="currentColor">
                                    <path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd" />
                                </svg>
                            </div>
                        </div>
                    </div>
                </a>
            {/each}
        </div>
    {/if}
</div>