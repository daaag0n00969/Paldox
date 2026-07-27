package com.paldexpro.ui.screens.skills

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.PrimaryTabRow
import androidx.compose.material3.Slider
import androidx.compose.material3.Tab
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableIntStateOf
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.paldexpro.R
import com.paldexpro.ui.components.ElementChip
import com.paldexpro.ui.components.SearchField
import com.paldexpro.ui.theme.BlueTier
import com.paldexpro.ui.theme.GoldTier
import com.paldexpro.ui.theme.GreenTier
import com.paldexpro.ui.theme.LegendTier

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SkillsScreen(
    useRu: Boolean,
    onBack: (() -> Unit)? = null,
    vm: SkillsViewModel = hiltViewModel(),
) {
    val state by vm.state.collectAsStateWithLifecycle()
    val query by vm.queryText.collectAsStateWithLifecycle()
    var tab by rememberSaveable { mutableIntStateOf(0) }

    Column(Modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text(stringResource(R.string.nav_skills)) },
            navigationIcon = {
                if (onBack != null) {
                    IconButton(onClick = onBack) {
                        Icon(Icons.AutoMirrored.Filled.ArrowBack, null)
                    }
                }
            },
        )
        PrimaryTabRow(selectedTabIndex = tab) {
            Tab(selected = tab == 0, onClick = { tab = 0 }, text = { Text(stringResource(R.string.passive_skills)) })
            Tab(selected = tab == 1, onClick = { tab = 1 }, text = { Text(stringResource(R.string.active_skills)) })
        }
        SearchField(
            value = query,
            onValueChange = vm::setQuery,
            placeholder = stringResource(R.string.search_skills),
            modifier = Modifier.padding(horizontal = 16.dp, vertical = 8.dp),
        )

        if (tab == 0) {
            Row(
                Modifier.padding(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(6.dp),
            ) {
                FilterChip(
                    selected = state.sortByRarity,
                    onClick = { vm.setSortByRarity(true) },
                    label = { Text(stringResource(R.string.sort_rarity)) },
                )
                FilterChip(
                    selected = !state.sortByRarity,
                    onClick = { vm.setSortByRarity(false) },
                    label = { Text(stringResource(R.string.sort_name)) },
                )
            }
            if (state.previewRankMax > 1) {
                Text(
                    "${stringResource(R.string.passive_rank)}: ${state.previewRank}",
                    modifier = Modifier.padding(horizontal = 16.dp, vertical = 4.dp),
                    style = MaterialTheme.typography.labelLarge,
                )
                Slider(
                    value = state.previewRank.toFloat(),
                    onValueChange = { vm.setPreviewRank(it.toInt()) },
                    valueRange = 1f..state.previewRankMax.toFloat(),
                    steps = (state.previewRankMax - 2).coerceAtLeast(0),
                    modifier = Modifier.padding(horizontal = 16.dp),
                )
            }
            LazyColumn(
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                items(state.passives, key = { it.id }) { skill ->
                    val tierColor = when (skill.tier) {
                        "legendary" -> LegendTier
                        "gold" -> GoldTier
                        "blue" -> BlueTier
                        else -> GreenTier
                    }
                    val effects = skill.effectAtRank(state.previewRank.coerceAtMost(skill.maxRank))
                    Card(
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(0.35f)),
                        shape = RoundedCornerShape(14.dp),
                    ) {
                        Column(Modifier.padding(12.dp).fillMaxWidth()) {
                            Row {
                                Text(skill.displayName(useRu), fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f))
                                Text(
                                    skill.tier.uppercase(),
                                    color = tierColor,
                                    style = MaterialTheme.typography.labelSmall,
                                    fontWeight = FontWeight.Bold,
                                )
                            }
                            Text(
                                if (skill.isPositive) stringResource(R.string.positive) else stringResource(R.string.negative),
                                style = MaterialTheme.typography.labelSmall,
                                color = if (skill.isPositive) GreenTier else MaterialTheme.colorScheme.error,
                            )
                            Text(skill.desc(useRu), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                            if (effects.isNotEmpty()) {
                                Text(
                                    effects.entries.joinToString(" · ") { (k, v) ->
                                        val pct = (v * 100).toInt()
                                        val sign = if (pct >= 0) "+" else ""
                                        "$k $sign$pct%"
                                    },
                                    style = MaterialTheme.typography.labelMedium,
                                    color = MaterialTheme.colorScheme.primary,
                                    modifier = Modifier.padding(top = 4.dp),
                                )
                            }
                        }
                    }
                }
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(horizontal = 16.dp, vertical = 8.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                items(state.actives, key = { it.id }) { skill ->
                    Card(
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(0.35f)),
                        shape = RoundedCornerShape(14.dp),
                    ) {
                        Column(Modifier.padding(12.dp).fillMaxWidth()) {
                            Row {
                                Text(skill.displayName(useRu), fontWeight = FontWeight.SemiBold, modifier = Modifier.weight(1f))
                                ElementChip(skill.element, compact = true)
                            }
                            Row(Modifier.padding(top = 4.dp)) {
                                Text("${stringResource(R.string.power)}: ${skill.power}", style = MaterialTheme.typography.labelMedium)
                                Spacer(Modifier.width(12.dp))
                                Text("${stringResource(R.string.cooldown)}: ${skill.cooldown}s", style = MaterialTheme.typography.labelMedium)
                            }
                            Text(skill.desc(useRu), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)
                        }
                    }
                }
            }
        }
    }
}
