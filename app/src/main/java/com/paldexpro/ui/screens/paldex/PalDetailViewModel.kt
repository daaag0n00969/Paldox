package com.paldexpro.ui.screens.paldex

import androidx.lifecycle.SavedStateHandle
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.paldexpro.data.repository.PalRepository
import com.paldexpro.domain.model.GameItem
import com.paldexpro.domain.model.Pal
import com.paldexpro.domain.model.PassiveSkill
import com.paldexpro.domain.stats.StatCalculator
import dagger.hilt.android.lifecycle.HiltViewModel
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.SharingStarted
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.stateIn
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch
import javax.inject.Inject

data class PalDetailUiState(
    val pal: Pal? = null,
    val level: Int = 1,
    val talent: Int = 50,
    val condenserStars: Int = 0,
    val soulBonus: Float = 0f,
    val selectedPassives: List<PassiveSkill> = emptyList(),
    val allPassives: List<PassiveSkill> = emptyList(),
    val stats: StatCalculator.ComputedStats? = null,
    val strongVsPals: List<Pal> = emptyList(),
    val weakToPals: List<Pal> = emptyList(),
    val dropItems: List<GameItem> = emptyList(),
)

@HiltViewModel
class PalDetailViewModel @Inject constructor(
    savedStateHandle: SavedStateHandle,
    private val repo: PalRepository,
    private val statCalculator: StatCalculator,
) : ViewModel() {
    private val palId: String = checkNotNull(savedStateHandle["palId"])

    private val level = MutableStateFlow(1)
    private val talent = MutableStateFlow(50)
    private val condenser = MutableStateFlow(0)
    private val soul = MutableStateFlow(0f)
    private val selectedIds = MutableStateFlow<List<String>>(emptyList())

    private data class Controls(
        val level: Int,
        val talent: Int,
        val condenser: Int,
        val soul: Float,
        val selectedIds: List<String>,
    )

    val state: StateFlow<PalDetailUiState> = combine(
        repo.observePal(palId),
        repo.observePals(),
        repo.observeItems(),
        repo.observePassives(),
        combine(level, talent, condenser, soul, selectedIds) { lv, tal, stars, soulB, sel ->
            Controls(lv, tal, stars, soulB, sel)
        },
    ) { pal, allPals, items, passives, controls ->
        val selected = passives.filter { it.id in controls.selectedIds }.take(4)
        val stats = pal?.let {
            statCalculator.compute(
                pal = it,
                level = controls.level,
                talent = controls.talent,
                condenserStars = controls.condenser,
                soulBonusPercent = controls.soul,
                passives = selected,
            )
        }
        val byId = allPals.associateBy { it.id }
        val itemById = items.associateBy { it.id }
        PalDetailUiState(
            pal = pal,
            level = controls.level,
            talent = controls.talent,
            condenserStars = controls.condenser,
            soulBonus = controls.soul,
            selectedPassives = selected,
            allPassives = passives.sortedByDescending { it.rarityOrder },
            stats = stats,
            strongVsPals = pal?.strongVsPalIds.orEmpty().mapNotNull { byId[it] },
            weakToPals = pal?.weakToPalIds.orEmpty().mapNotNull { byId[it] },
            dropItems = pal?.dropItemIds.orEmpty().mapNotNull { itemById[it] },
        )
    }.stateIn(viewModelScope, SharingStarted.WhileSubscribed(5_000), PalDetailUiState())

    fun setLevel(v: Int) {
        level.value = v
    }

    fun setTalent(v: Int) {
        talent.value = v
    }

    fun setCondenser(v: Int) {
        condenser.value = v
    }

    fun setSoul(v: Float) {
        soul.value = v
    }

    fun togglePassive(id: String) {
        selectedIds.update { cur ->
            if (id in cur) cur - id
            else if (cur.size >= 4) cur
            else cur + id
        }
    }

    fun toggleOwned(id: String, owned: Boolean) {
        viewModelScope.launch { repo.setOwned(id, owned) }
    }
}
