package com.paldexpro.ui.screens.items

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.CraftIngredient
import com.paldexpro.domain.model.GameItem
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ItemDetailUiState(
    val item: GameItem? = null,
    val recipeItems: List<Pair<CraftIngredient, GameItem?>> = emptyList(),
    val related: List<GameItem> = emptyList(),
)

@HiltViewModel
class ItemDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val repo: PalRepository,
) : ViewModel() {
    private val itemId: String = checkNotNull(savedStateHandle["itemId"])

    val state: StateFlow<ItemDetailUiState> = combine(
        repo.observeItem(itemId),
        repo.observeItems(),
    ) { item, all ->
        val recipe = item?.recipe.orEmpty().map { ing ->
            ing to all.firstOrNull { it.id == ing.itemId }
        }
        val related = all.filter {
            it.id != itemId && (
                it.category == item?.category ||
                    item?.recipe?.any { r -> r.itemId == it.id } == true ||
                    it.recipe.any { r -> r.itemId == itemId }
                )
        }.take(8)
        ItemDetailUiState(item, recipe, related)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ItemDetailUiState())

    init {
        viewModelScope.launch { repo.init() }
    }
}
