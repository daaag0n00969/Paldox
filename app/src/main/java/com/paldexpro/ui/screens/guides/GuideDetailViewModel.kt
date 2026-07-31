package com.paldexpro.ui.screens.guides

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.GameItem
import com.paldexpro.domain.model.Guide
import com.paldexpro.domain.model.Pal
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class GuideDetailUiState(
    val guide: Guide? = null,
    val pals: List<Pal> = emptyList(),
    val items: List<GameItem> = emptyList(),
)

@HiltViewModel
class GuideDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val repo: PalRepository,
) : ViewModel() {
    private val guideId: String = checkNotNull(savedStateHandle["guideId"])

    val state: StateFlow<GuideDetailUiState> = combine(
        repo.observeGuide(guideId),
        repo.observePals(),
        repo.observeItems(),
    ) { guide, pals, items ->
        GuideDetailUiState(guide = guide, pals = pals, items = items)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), GuideDetailUiState())

    fun saveNotes(notes: String) {
        viewModelScope.launch { repo.updateGuideNotes(guideId, notes) }
    }
}
