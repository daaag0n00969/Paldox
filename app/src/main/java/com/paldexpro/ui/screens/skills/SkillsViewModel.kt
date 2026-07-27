package com.paldexpro.ui.screens.skills

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.ActiveSkill
import com.paldexpro.domain.model.PassiveSkill
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.launch
import javax.inject.Inject

data class SkillsUiState(
    val passives: List<PassiveSkill> = emptyList(),
    val actives: List<ActiveSkill> = emptyList(),
    val sortByRarity: Boolean = true,
    val previewRank: Int = 1,
    val previewRankMax: Int = 1,
)

@HiltViewModel
class SkillsViewModel @Inject constructor(
    repo: PalRepository,
) : ViewModel() {
    private val query = MutableStateFlow("")
    private val sortByRarity = MutableStateFlow(true)
    private val previewRank = MutableStateFlow(1)

    val queryText: StateFlow<String> = query.asStateFlow()

    val state: StateFlow<SkillsUiState> = combine(
        query,
        repo.observePassives(),
        repo.observeActives(),
        sortByRarity,
        previewRank,
    ) { q, passives, actives, sortRarity, rank ->
        var pq = passives.filter {
            q.isBlank() || it.nameEn.contains(q, true) || it.nameRu.contains(q, true) || it.descEn.contains(q, true)
        }
        pq = if (sortRarity) {
            pq.sortedWith(compareByDescending<PassiveSkill> { it.rarityOrder }.thenBy { it.nameEn })
        } else {
            pq.sortedBy { it.nameEn }
        }
        val aq = actives.filter {
            q.isBlank() || it.nameEn.contains(q, true) || it.nameRu.contains(q, true)
        }.sortedByDescending { it.power }
        val maxRank = passives.maxOfOrNull { it.maxRank }?.coerceAtLeast(1) ?: 1
        SkillsUiState(pq, aq, sortRarity, rank.coerceIn(1, maxRank), maxRank)
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), SkillsUiState())

    init {
        viewModelScope.launch { repo.init() }
    }

    fun setQuery(v: String) {
        query.value = v
    }

    fun setSortByRarity(v: Boolean) {
        sortByRarity.value = v
    }

    fun setPreviewRank(v: Int) {
        previewRank.value = v
    }
}
