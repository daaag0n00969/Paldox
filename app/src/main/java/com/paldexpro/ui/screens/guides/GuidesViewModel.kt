package com.paldexpro.ui.screens.guides

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.Guide
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

@HiltViewModel
class GuidesViewModel @Inject constructor(
    repo: PalRepository,
) : ViewModel() {
    val guides: StateFlow<List<Guide>> = repo.observeGuides()
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())

    init {
        viewModelScope.launch { repo.init() }
    }
}

@HiltViewModel
class GuideDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val repo: PalRepository,
) : ViewModel() {
    private val guideId: String = checkNotNull(savedStateHandle["guideId"])

    val guide: StateFlow<Guide?> = repo.observeGuide(guideId)
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), null)

    fun saveNotes(notes: String) {
        viewModelScope.launch { repo.updateGuideNotes(guideId, notes) }
    }
}
