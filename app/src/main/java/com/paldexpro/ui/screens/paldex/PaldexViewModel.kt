package com.paldexpro.ui.screens.paldex

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.Pal
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

data class PaldexUiState(
    val element: String? = null,
    val rarity: String? = null,
    val pals: List<Pal> = emptyList(),
)

@OptIn(ExperimentalCoroutinesApi::class)
@HiltViewModel
class PaldexViewModel @Inject constructor(
    private val repo: PalRepository,
) : ViewModel() {
    private val query = MutableStateFlow("")
    private val element = MutableStateFlow<String?>(null)
    private val rarity = MutableStateFlow<String?>(null)

    /** Independent of list results — keeps cursor stable while typing. */
    val queryText: StateFlow<String> = query.asStateFlow()

    val state: StateFlow<PaldexUiState> = combine(query, element, rarity) { q, e, r ->
        Triple(q, e, r)
    }.flatMapLatest { (q, e, r) ->
        repo.observePals(q, e.orEmpty(), r.orEmpty()).combine(element) { pals, el ->
            PaldexUiState(element = el, rarity = rarity.value, pals = pals)
        }
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), PaldexUiState())

    init {
        viewModelScope.launch { repo.init() }
    }

    fun setQuery(v: String) {
        query.value = v
    }

    fun setElement(v: String?) {
        element.value = v
    }

    fun setRarity(v: String?) {
        rarity.value = v
    }
}
