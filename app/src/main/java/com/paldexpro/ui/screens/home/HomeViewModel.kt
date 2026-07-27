package com.paldexpro.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.Pal
import com.paldexpro.domain.model.Rarity
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class HomeUiState(
    val palCount: Int = 0,
    val gameVersion: String = "1.0",
    val featured: List<Pal> = emptyList(),
)

@HiltViewModel
class HomeViewModel @Inject constructor(
    private val repo: PalRepository,
) : ViewModel() {
    private val _state = MutableStateFlow(HomeUiState())
    val state: StateFlow<HomeUiState> = _state.asStateFlow()

    init {
        viewModelScope.launch {
            repo.init()
            val pals = repo.getAllPals()
            val featured = pals
                .filter { it.rarity == Rarity.legendary || it.rarity == Rarity.epic }
                .sortedBy { it.breedingPower }
                .take(12)
            _state.update {
                it.copy(
                    palCount = pals.size,
                    gameVersion = repo.gameVersion(),
                    featured = featured,
                )
            }
        }
    }
}
