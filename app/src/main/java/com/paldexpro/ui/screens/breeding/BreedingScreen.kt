package com.paldexpro.ui.screens.breeding

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ChildCare
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.SwapHoriz
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.FilterChip
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.SegmentedButton
import androidx.compose.material3.SegmentedButtonDefaults
import androidx.compose.material3.SingleChoiceSegmentedButtonRow
import androidx.compose.material3.Switch
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
import com.paldexpro.domain.model.BreedingPair
import com.paldexpro.domain.model.Pal
import com.paldexpro.ui.components.EmptyState
import com.paldexpro.ui.components.PalAvatar
import com.paldexpro.ui.components.PalNameWithDex
import com.paldexpro.ui.components.SearchField
import com.paldexpro.ui.components.SectionTitle

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun BreedingScreen(
    useRu: Boolean,
    onOpenPal: (String) -> Unit,
    vm: BreedingViewModel = hiltViewModel(),
) {
    val state by vm.state.collectAsStateWithLifecycle()
    val search by vm.searchText.collectAsStateWithLifecycle()

    Column(Modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text(stringResource(R.string.nav_breeding)) },
            actions = {
                IconButton(onClick = vm::clearSelection) {
                    Icon(Icons.Default.Close, contentDescription = stringResource(R.string.clear))
                }
            },
        )

        Column(Modifier.padding(horizontal = 16.dp)) {
            // Three modes: P+P | P+ | =P
            SingleChoiceSegmentedButtonRow(Modifier.fillMaxWidth()) {
                SegmentedButton(
                    selected = state.mode == BreedingMode.Pair,
                    onClick = { vm.setMode(BreedingMode.Pair) },
                    shape = SegmentedButtonDefaults.itemShape(0, 3),
                    label = { Text(stringResource(R.string.breed_mode_pair), maxLines = 1) },
                )
                SegmentedButton(
                    selected = state.mode == BreedingMode.Plus,
                    onClick = { vm.setMode(BreedingMode.Plus) },
                    shape = SegmentedButtonDefaults.itemShape(1, 3),
                    label = { Text(stringResource(R.string.breed_mode_plus), maxLines = 1) },
                )
                SegmentedButton(
                    selected = state.mode == BreedingMode.Target,
                    onClick = { vm.setMode(BreedingMode.Target) },
                    shape = SegmentedButtonDefaults.itemShape(2, 3),
                    label = { Text(stringResource(R.string.breed_mode_target), maxLines = 1) },
                )
            }

            Text(
                text = when (state.mode) {
                    BreedingMode.Pair -> stringResource(R.string.breed_mode_pair_hint)
                    BreedingMode.Plus -> stringResource(R.string.breed_mode_plus_hint)
                    BreedingMode.Target -> stringResource(R.string.breed_mode_target_hint)
                },
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(top = 8.dp, bottom = 4.dp),
            )

            SearchField(
                value = search,
                onValueChange = vm::setSearch,
                placeholder = stringResource(R.string.search_pals),
            )

            if (state.mode != BreedingMode.Pair) {
                Row(
                    Modifier.fillMaxWidth().padding(vertical = 6.dp),
                    verticalAlignment = Alignment.CenterVertically,
                    horizontalArrangement = Arrangement.SpaceBetween,
                ) {
                    Text(stringResource(R.string.owned_only), style = MaterialTheme.typography.bodyMedium)
                    Switch(checked = state.ownedOnly, onCheckedChange = vm::setOwnedOnly)
                }
            } else {
                Spacer(Modifier.height(8.dp))
            }

            when (state.mode) {
                BreedingMode.Pair -> {
                    SectionTitle(stringResource(R.string.select_parent_a))
                    SelectedOrPicker(state.parentA, state.filteredPals, useRu, vm::setParentA, onOpenPal)
                    SectionTitle(stringResource(R.string.select_parent_b))
                    SelectedOrPicker(state.parentB, state.filteredPals, useRu, vm::setParentB, onOpenPal)
                    state.pairResult?.let {
                        Spacer(Modifier.height(8.dp))
                        ResultCard(it, useRu, onOpenPal)
                    }
                }
                BreedingMode.Plus -> {
                    SectionTitle(stringResource(R.string.select_parent_a))
                    SelectedOrPicker(state.parentA, state.filteredPals, useRu, vm::setParentA, onOpenPal)
                }
                BreedingMode.Target -> {
                    SectionTitle(stringResource(R.string.select_target_child))
                    SelectedOrPicker(state.target, state.filteredPals, useRu, vm::setTarget, onOpenPal)
                }
            }
        }

        if (state.loading) {
            Column(Modifier.fillMaxWidth().padding(24.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                CircularProgressIndicator()
            }
            return@Column
        }

        when (state.mode) {
            BreedingMode.Pair -> Unit
            BreedingMode.Plus -> {
                if (state.parentA == null) {
                    EmptyState(stringResource(R.string.pick_one_pal))
                } else if (state.plusResults.isEmpty()) {
                    EmptyState(stringResource(R.string.no_results))
                } else {
                    LazyColumn(
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        item {
                            Text(
                                stringResource(R.string.all_offspring_with, state.parentA!!.displayName(useRu)) +
                                    " · ${state.plusResults.size}",
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                        items(state.plusResults, key = { "${it.parentB.id}_${it.child.id}" }) { pair ->
                            ParentPairCard(pair, useRu, onOpenPal, highlightPartner = true)
                        }
                    }
                }
            }
            BreedingMode.Target -> {
                if (state.target == null) {
                    EmptyState(stringResource(R.string.pick_target_pal))
                } else if (state.targetResults.isEmpty()) {
                    EmptyState(stringResource(R.string.no_parent_pairs))
                } else {
                    LazyColumn(
                        contentPadding = PaddingValues(16.dp),
                        verticalArrangement = Arrangement.spacedBy(8.dp),
                    ) {
                        item {
                            Text(
                                stringResource(R.string.parent_pairs_count, state.targetResults.size),
                                style = MaterialTheme.typography.labelLarge,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                        items(
                            state.targetResults,
                            key = { "${it.parentA.id}_${it.parentB.id}_${it.child.id}" },
                        ) { pair ->
                            ParentPairCard(pair, useRu, onOpenPal)
                        }
                    }
                }
            }
        }
    }
}

@Composable
private fun SelectedOrPicker(
    selected: Pal?,
    pals: List<Pal>,
    useRu: Boolean,
    onPick: (Pal) -> Unit,
    onOpen: (String) -> Unit,
) {
    if (selected != null) {
        Card(
            Modifier.fillMaxWidth().clickable { onOpen(selected.id) },
            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.primaryContainer.copy(0.35f)),
            shape = RoundedCornerShape(14.dp),
        ) {
            Row(Modifier.padding(10.dp), verticalAlignment = Alignment.CenterVertically) {
                PalAvatar(selected, 48)
                Spacer(Modifier.width(10.dp))
                Column(Modifier.weight(1f)) {
                    Text(selected.displayName(useRu), fontWeight = FontWeight.SemiBold)
                    Text("#${selected.dexNumber} · BP ${selected.breedingPower}", style = MaterialTheme.typography.labelSmall)
                }
                FilterChip(selected = true, onClick = {}, label = { Text(stringResource(R.string.selected)) })
            }
        }
        Spacer(Modifier.height(6.dp))
    }
    LazyRow(horizontalArrangement = Arrangement.spacedBy(8.dp)) {
        items(pals.take(48), key = { it.id }) { pal ->
            Card(
                modifier = Modifier.width(96.dp).clickable { onPick(pal) },
                colors = CardDefaults.cardColors(
                    containerColor = if (selected?.id == pal.id)
                        MaterialTheme.colorScheme.primaryContainer
                    else MaterialTheme.colorScheme.surfaceVariant.copy(0.4f),
                ),
                shape = RoundedCornerShape(12.dp),
            ) {
                Column(Modifier.padding(8.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    PalAvatar(pal, 44)
                    PalNameWithDex(pal, useRu)
                }
            }
        }
    }
}

@Composable
private fun ResultCard(pair: BreedingPair, useRu: Boolean, onOpen: (String) -> Unit) {
    Card(
        Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.secondaryContainer.copy(0.45f)),
        shape = RoundedCornerShape(18.dp),
    ) {
        Column(Modifier.padding(16.dp), horizontalAlignment = Alignment.CenterHorizontally) {
            Text(stringResource(R.string.breed_result), fontWeight = FontWeight.Bold)
            if (pair.isSpecial) {
                Text(
                    stringResource(R.string.special_combo),
                    color = MaterialTheme.colorScheme.secondary,
                    style = MaterialTheme.typography.labelMedium,
                )
            }
            Spacer(Modifier.height(12.dp))
            Row(
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clickable { onOpen(pair.parentA.id) }) {
                    PalAvatar(pair.parentA, 56)
                    PalNameWithDex(pair.parentA, useRu)
                }
                Icon(Icons.Default.SwapHoriz, null)
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clickable { onOpen(pair.parentB.id) }) {
                    PalAvatar(pair.parentB, 56)
                    PalNameWithDex(pair.parentB, useRu)
                }
                Icon(Icons.Default.ChildCare, null, tint = MaterialTheme.colorScheme.primary)
                Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clickable { onOpen(pair.child.id) }) {
                    PalAvatar(pair.child, 64)
                    PalNameWithDex(pair.child, useRu, bold = true)
                }
            }
            Text(
                "BP → ${pair.childPower}",
                style = MaterialTheme.typography.labelSmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(top = 8.dp),
            )
        }
    }
}

@Composable
private fun ParentPairCard(
    pair: BreedingPair,
    useRu: Boolean,
    onOpen: (String) -> Unit,
    highlightPartner: Boolean = false,
) {
    Card(
        Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(0.35f)),
        shape = RoundedCornerShape(14.dp),
    ) {
        Row(
            Modifier.padding(12.dp).fillMaxWidth(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.SpaceBetween,
        ) {
            Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.weight(1f)) {
                if (highlightPartner) {
                    Column(
                        horizontalAlignment = Alignment.CenterHorizontally,
                        modifier = Modifier.clickable { onOpen(pair.parentB.id) },
                    ) {
                        PalAvatar(pair.parentB, 44)
                        PalNameWithDex(pair.parentB, useRu)
                    }
                } else {
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clickable { onOpen(pair.parentA.id) }) {
                        PalAvatar(pair.parentA, 40)
                        PalNameWithDex(pair.parentA, useRu)
                    }
                    Text(" + ", fontWeight = FontWeight.Bold)
                    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clickable { onOpen(pair.parentB.id) }) {
                        PalAvatar(pair.parentB, 40)
                        PalNameWithDex(pair.parentB, useRu)
                    }
                }
            }
            Text("→", modifier = Modifier.padding(horizontal = 6.dp), fontWeight = FontWeight.Bold)
            Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.clickable { onOpen(pair.child.id) }) {
                PalAvatar(pair.child, 48)
                PalNameWithDex(pair.child, useRu, bold = true)
                if (pair.isSpecial) {
                    Text(
                        stringResource(R.string.special_combo),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.secondary,
                    )
                }
            }
        }
    }
}
