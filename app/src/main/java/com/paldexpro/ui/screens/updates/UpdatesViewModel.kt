package com.paldexpro.ui.screens.updates

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.Guide
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.map
import kotlinx.coroutines.flow.stateIn
import javax.inject.Inject

@HiltViewModel
class UpdatesViewModel @Inject constructor(
    repo: PalRepository,
) : ViewModel() {
    val updates: StateFlow<List<Guide>> = repo.observeGuides()
        .map { list ->
            list.filter { it.category.equals("updates", ignoreCase = true) }
                .sortedByDescending { it.id }
        }
        .stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), emptyList())
}
