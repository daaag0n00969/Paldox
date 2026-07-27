package com.paldexpro.ui.screens.items

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.GameItem
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.ExperimentalCoroutinesApi
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flatMapLatest
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class ItemsUiState(
    val category: String? = null,
    val items: List<GameItem> = emptyList(),
)

@OptIn(ExperimentalCoroutinesApi::class)
@HiltViewModel
class ItemsViewModel @Inject constructor(
    private val repo: PalRepository,
) : ViewModel() {
    private val query = MutableStateFlow("")
    private val category = MutableStateFlow<String?>(null)

    val queryText: StateFlow<String> = query.asStateFlow()

    val state: StateFlow<ItemsUiState> = combine(query, category) { q, c -> q to c }
        .flatMapLatest { (q, c) ->
            repo.observeItems(q, c.orEmpty()).combine(category) { items, cat ->
                ItemsUiState(category = cat, items = items)
            }
        }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), ItemsUiState())

    init {
        viewModelScope.launch { repo.init() }
    }

    fun setQuery(v: String) {
        query.value = v
    }

    fun setCategory(v: String?) {
        category.value = v
    }
}
