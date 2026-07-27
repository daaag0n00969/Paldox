package com.paldexpro.ui.screens.bosses

import androidx.lifecycle.SavedStateHandle
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

data class BossDetailUiState(
    val boss: Boss? = null,
    val heroPal: Pal? = null,
    val counterPals: List<Pal> = emptyList(),
)

@HiltViewModel
class BossDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val repo: PalRepository,
) : ViewModel() {
    private val bossId: String = checkNotNull(savedStateHandle["bossId"])

    val state: StateFlow<BossDetailUiState> = combine(
        repo.observeBoss(bossId),
        flow { emit(repo.getAllPals().associateBy { it.id }) },
    ) { boss, pals ->
        val heroId = boss?.imagePalId?.ifBlank { boss.counterPalIds.firstOrNull().orEmpty() }.orEmpty()
        val counters = boss?.counterPalIds?.mapNotNull { pals[it] }.orEmpty()
        BossDetailUiState(
            boss = boss,
            heroPal = pals[heroId],
            counterPals = counters,
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), BossDetailUiState())

    init {
        viewModelScope.launch { repo.init() }
    }
}
