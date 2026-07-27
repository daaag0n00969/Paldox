package com.paldexpro.ui.screens.breeding

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.BreedingPair
import com.paldexpro.domain.model.Pal
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.Job
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

/** Three breeding calculator modes. */
enum class BreedingMode {
    /** P+P — two parents → one child */
    Pair,
    /** P+ — one parent → all partners & children */
    Plus,
    /** =P — target child → parent combinations */
    Target,
}

data class BreedingUiState(
    val mode: BreedingMode = BreedingMode.Pair,
    val allPals: List<Pal> = emptyList(),
    val filteredPals: List<Pal> = emptyList(),
    val parentA: Pal? = null,
    val parentB: Pal? = null,
    val target: Pal? = null,
    val ownedOnly: Boolean = false,
    val pairResult: BreedingPair? = null,
    val plusResults: List<BreedingPair> = emptyList(),
    val targetResults: List<BreedingPair> = emptyList(),
    val loading: Boolean = false,
)

@HiltViewModel
class BreedingViewModel @Inject constructor(
    private val repo: PalRepository,
) : ViewModel() {
    private val _state = MutableStateFlow(BreedingUiState())
    val state: StateFlow<BreedingUiState> = _state.asStateFlow()
    private val _search = MutableStateFlow("")
    val searchText: StateFlow<String> = _search.asStateFlow()
    private var computeJob: Job? = null

    init {
        viewModelScope.launch {
            repo.init()
            val pals = repo.getAllPals().sortedBy { it.dexNumber }
            _state.update { it.copy(allPals = pals, filteredPals = pals) }
        }
    }

    fun setMode(mode: BreedingMode) {
        _state.update {
            it.copy(
                mode = mode,
                pairResult = null,
                plusResults = emptyList(),
                targetResults = emptyList(),
            )
        }
        recompute()
    }

    fun setSearch(q: String) {
        _search.value = q
        _state.update { s ->
            val filtered = s.allPals.filter {
                q.isBlank() ||
                    it.nameEn.contains(q, true) ||
                    it.nameRu.contains(q, true) ||
                    it.dexNumber.contains(q, true)
            }
            s.copy(filteredPals = filtered)
        }
    }

    fun setOwnedOnly(v: Boolean) {
        _state.update { it.copy(ownedOnly = v) }
        recompute()
    }

    fun setParentA(pal: Pal) {
        _state.update { it.copy(parentA = pal) }
        recompute()
    }

    fun setParentB(pal: Pal) {
        _state.update { it.copy(parentB = pal) }
        recompute()
    }

    fun setTarget(pal: Pal) {
        _state.update { it.copy(target = pal) }
        recompute()
    }

    fun clearSelection() {
        _state.update {
            it.copy(
                parentA = null,
                parentB = null,
                target = null,
                pairResult = null,
                plusResults = emptyList(),
                targetResults = emptyList(),
            )
        }
    }

    private fun recompute() {
        computeJob?.cancel()
        computeJob = viewModelScope.launch {
            val s = _state.value
            _state.update { it.copy(loading = true) }
            when (s.mode) {
                BreedingMode.Pair -> {
                    val result = if (s.parentA != null && s.parentB != null) {
                        repo.predictBreed(s.parentA.id, s.parentB.id)
                    } else null
                    _state.update { it.copy(pairResult = result, loading = false) }
                }
                BreedingMode.Plus -> {
                    val results = if (s.parentA != null) {
                        repo.offspringFor(s.parentA.id, s.ownedOnly)
                    } else emptyList()
                    _state.update { it.copy(plusResults = results, loading = false) }
                }
                BreedingMode.Target -> {
                    val results = if (s.target != null) {
                        repo.parentsFor(s.target.id, s.ownedOnly)
                    } else emptyList()
                    _state.update { it.copy(targetResults = results, loading = false) }
                }
            }
        }
    }
}
