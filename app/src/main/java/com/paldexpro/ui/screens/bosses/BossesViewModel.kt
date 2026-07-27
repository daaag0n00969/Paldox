package com.paldexpro.ui.screens.bosses

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.Boss
import com.paldexpro.domain.model.Pal
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class BossesUiState(
    val bosses: List<Boss> = emptyList(),
    val palById: Map<String, Pal> = emptyMap(),
)

@HiltViewModel
class BossesViewModel @Inject constructor(
    private val repo: PalRepository,
) : ViewModel() {
    val state: StateFlow<BossesUiState> = combine(
        repo.observeBosses(),
        flow {
            emit(repo.getAllPals().associateBy { it.id })
        },
    ) { bosses, pals ->
        BossesUiState(bosses, pals)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), BossesUiState())

    init {
        viewModelScope.launch { repo.init() }
    }
}
