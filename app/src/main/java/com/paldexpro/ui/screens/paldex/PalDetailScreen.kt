package com.paldexpro.ui.screens.paldex

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.filled.Egg
import androidx.compose.material.icons.filled.Star
import androidx.compose.material.icons.outlined.StarBorder
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Slider
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.paldexpro.R
import com.paldexpro.domain.model.WorkType
import com.paldexpro.ui.components.ElementChip
import com.paldexpro.ui.components.PalAvatar
import com.paldexpro.ui.components.RarityBadge
import com.paldexpro.ui.components.SectionTitle
import com.paldexpro.ui.components.StatBar
import com.paldexpro.ui.components.WorkChip
import com.paldexpro.ui.theme.ElementFire
import com.paldexpro.ui.theme.ElementGrass
import com.paldexpro.ui.theme.ElementWater

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun PalDetailScreen(
    palId: String,
    useRu: Boolean,
    onBack: () -> Unit,
    onBreed: () -> Unit,
    vm: PalDetailViewModel = hiltViewModel(),
) {
    val state by vm.state.collectAsStateWithLifecycle()
    val p = state.pal
    val stats = state.stats

    Column(Modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text(p?.displayName(useRu) ?: "…") },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = null)
                }
            },
            actions = {
                IconButton(onClick = { p?.let { vm.toggleOwned(it.id, !it.owned) } }) {
                    Icon(
                        if (p?.owned == true) Icons.Default.Star else Icons.Outlined.StarBorder,
                        contentDescription = stringResource(R.string.mark_owned),
                        tint = if (p?.owned == true) MaterialTheme.colorScheme.secondary
                        else MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            },
        )

        if (p == null) return@Column

        Column(
            Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                PalAvatar(p, size = 96)
                Spacer(Modifier.padding(12.dp))
                Column {
                    Text("#${p.dexNumber}", style = MaterialTheme.typography.labelMedium)
                    Text(p.displayName(useRu), style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
                    if (useRu) Text(p.nameEn, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    else Text(p.nameRu, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    Row(horizontalArrangement = Arrangement.spacedBy(6.dp), modifier = Modifier.padding(top = 6.dp)) {
                        p.elements().forEach { ElementChip(it) }
                        RarityBadge(p.rarity)
                    }
                }
            }

            // Species scaling
            SectionTitle(stringResource(R.string.species_scaling))
            Text(
                stringResource(R.string.species_scaling_hint, p.hp, p.attack, p.defense),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )

            SectionTitle(stringResource(R.string.stats_at_level))
            Text("${stringResource(R.string.level)}: ${state.level}", fontWeight = FontWeight.SemiBold)
            Slider(
                value = state.level.toFloat(),
                onValueChange = { vm.setLevel(it.toInt()) },
                valueRange = 1f..65f,
                steps = 63,
            )
            Text(
                "${stringResource(R.string.talent_iv)}: ${state.talent} (${"%.0f".format(state.stats?.potentialPercent ?: 0f)}%)",
                fontWeight = FontWeight.SemiBold,
            )
            Slider(
                value = state.talent.toFloat(),
                onValueChange = { vm.setTalent(it.toInt()) },
                valueRange = 0f..100f,
                steps = 99,
            )
            Text("${stringResource(R.string.condenser)}: ${state.condenserStars}★", fontWeight = FontWeight.SemiBold)
            Slider(
                value = state.condenserStars.toFloat(),
                onValueChange = { vm.setCondenser(it.toInt()) },
                valueRange = 0f..4f,
                steps = 3,
            )
            Text(
                "${stringResource(R.string.soul_bonus)}: ${"%.0f".format(state.soulBonus * 100)}%",
                fontWeight = FontWeight.SemiBold,
            )
            Slider(
                value = state.soulBonus,
                onValueChange = vm::setSoul,
                valueRange = 0f..0.6f,
            )

            if (stats != null) {
                StatBar(stringResource(R.string.stat_hp), stats.hp, max = 5000, color = ElementGrass)
                StatBar(stringResource(R.string.stat_attack), stats.attack, max = 1200, color = ElementFire)
                StatBar(stringResource(R.string.stat_defense), stats.defense, max = 1000, color = ElementWater)
                Text(
                    buildString {
                        if (stats.attackBonusPercent != 0f) append("ATK ${"%.0f".format(stats.attackBonusPercent)}%  ")
                        if (stats.defenseBonusPercent != 0f) append("DEF ${"%.0f".format(stats.defenseBonusPercent)}%  ")
                        if (stats.workSpeedBonusPercent != 0f) append("Work ${"%.0f".format(stats.workSpeedBonusPercent)}%")
                    },
                    style = MaterialTheme.typography.labelMedium,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier.padding(top = 4.dp),
                )
            }

            SectionTitle(stringResource(R.string.passives_for_stats))
            Text(
                stringResource(R.string.passives_for_stats_hint),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
            FlowRow(
                horizontalArrangement = Arrangement.spacedBy(6.dp),
                verticalArrangement = Arrangement.spacedBy(6.dp),
                modifier = Modifier.padding(top = 8.dp),
            ) {
                state.allPassives
                    .filter { it.effects.keys.any { k -> k in setOf("attack", "defense", "hp", "workSpeed") } }
                    .take(24)
                    .forEach { skill ->
                        val selected = state.selectedPassives.any { it.id == skill.id }
                        FilterChip(
                            selected = selected,
                            onClick = { vm.togglePassive(skill.id) },
                            label = { Text(skill.displayName(useRu), style = MaterialTheme.typography.labelSmall) },
                        )
                    }
            }

            Text(
                "${stringResource(R.string.food)}: ${p.foodAmount} · BP: ${p.breedingPower} · ${stringResource(R.string.egg)}: ${p.eggSize.name}",
                style = MaterialTheme.typography.bodyMedium,
                modifier = Modifier.padding(top = 12.dp),
            )

            SectionTitle(stringResource(R.string.partner_skill))
            Text(p.partnerSkillName(useRu), fontWeight = FontWeight.SemiBold)
            Text(p.partnerSkillDesc(useRu), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)

            SectionTitle(stringResource(R.string.work_suitability))
            FlowRow(horizontalArrangement = Arrangement.spacedBy(6.dp), verticalArrangement = Arrangement.spacedBy(6.dp)) {
                WorkType.entries.forEach { type ->
                    val lv = p.work.level(type)
                    if (lv > 0) WorkChip(type, lv)
                }
            }

            SectionTitle(stringResource(R.string.location_drops))
            Text(p.location(useRu), fontWeight = FontWeight.Medium)
            if (p.nightOnly) {
                Text(stringResource(R.string.night_spawn), color = MaterialTheme.colorScheme.tertiary, style = MaterialTheme.typography.labelMedium)
            }
            Text(p.drops(useRu), style = MaterialTheme.typography.bodyMedium, color = MaterialTheme.colorScheme.onSurfaceVariant)

            Spacer(Modifier.height(16.dp))
            Button(onClick = onBreed, modifier = Modifier.fillMaxWidth()) {
                Icon(Icons.Default.Egg, null)
                Spacer(Modifier.padding(6.dp))
                Text(stringResource(R.string.open_breeding))
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}
