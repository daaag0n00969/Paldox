package com.paldexpro.ui.screens.items

import androidx.compose.foundation.clickable
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
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.SuggestionChip
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
import com.paldexpro.ui.components.ItemIcon
import com.paldexpro.ui.components.RarityBadge
import com.paldexpro.ui.components.SectionTitle

@OptIn(ExperimentalMaterial3Api::class, ExperimentalLayoutApi::class)
@Composable
fun ItemDetailScreen(
    itemId: String,
    useRu: Boolean,
    onBack: () -> Unit,
    onOpenItem: (String) -> Unit,
    vm: ItemDetailViewModel = hiltViewModel(),
) {
    val state by vm.state.collectAsStateWithLifecycle()
    val item = state.item

    Column(Modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text(item?.displayName(useRu) ?: "…") },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, null)
                }
            },
        )
        if (item == null) return@Column

        Column(
            Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                ItemIcon(item, size = 88)
                Spacer(Modifier.width(16.dp))
                Column {
                    Text(item.displayName(useRu), style = MaterialTheme.typography.headlineSmall, fontWeight = FontWeight.Bold)
                    if (useRu) {
                        Text(item.nameEn, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    } else {
                        Text(item.nameRu, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
                    }
                    Spacer(Modifier.height(6.dp))
                    Row(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalAlignment = Alignment.CenterVertically) {
                        Text(
                            item.category.replaceFirstChar { it.uppercase() },
                            style = MaterialTheme.typography.labelLarge,
                            color = MaterialTheme.colorScheme.primary,
                        )
                        RarityBadge(item.rarity)
                    }
                }
            }

            SectionTitle(stringResource(R.string.description))
            Text(item.desc(useRu), style = MaterialTheme.typography.bodyLarge)

            if (item.effects(useRu).isNotBlank()) {
                SectionTitle(stringResource(R.string.effects_stats))
                InfoCard(item.effects(useRu))
            }

            SectionTitle(stringResource(R.string.crafting))
            if (item.recipe.isEmpty()) {
                InfoCard(stringResource(R.string.no_recipe))
            } else {
                Card(
                    colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(0.4f)),
                    shape = RoundedCornerShape(14.dp),
                    modifier = Modifier.fillMaxWidth(),
                ) {
                    Column(Modifier.padding(14.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                        Text(
                            "${stringResource(R.string.station)}: ${item.craftStation(useRu)}",
                            fontWeight = FontWeight.SemiBold,
                        )
                        if (item.techLevel > 0) {
                            Text("${stringResource(R.string.tech_level)}: ${item.techLevel}")
                        }
                        state.recipeItems.forEach { (ing, linked) ->
                            Row(
                                verticalAlignment = Alignment.CenterVertically,
                                modifier = Modifier
                                    .fillMaxWidth()
                                    .then(
                                        if (linked != null) Modifier.clickable { onOpenItem(linked.id) }
                                        else Modifier
                                    ),
                            ) {
                                if (linked != null) {
                                    ItemIcon(linked, size = 36)
                                    Spacer(Modifier.width(10.dp))
                                    Text("${linked.displayName(useRu)} × ${ing.qty}", modifier = Modifier.weight(1f))
                                } else {
                                    Text("${ing.itemId.replace('_', ' ')} × ${ing.qty}")
                                }
                            }
                        }
                    }
                }
            }

            SectionTitle(stringResource(R.string.where_to_get))
            InfoCard(item.drops(useRu).ifBlank { "—" })

            SectionTitle(stringResource(R.string.where_to_buy))
            InfoCard(item.buy(useRu).ifBlank { "—" })

            SectionTitle(stringResource(R.string.uses))
            InfoCard(item.uses(useRu).ifBlank { "—" })

            if (state.related.isNotEmpty()) {
                SectionTitle(stringResource(R.string.related_items))
                FlowRow(horizontalArrangement = Arrangement.spacedBy(8.dp), verticalArrangement = Arrangement.spacedBy(8.dp)) {
                    state.related.forEach { rel ->
                        SuggestionChip(
                            onClick = { onOpenItem(rel.id) },
                            label = { Text(rel.displayName(useRu)) },
                            icon = { ItemIcon(rel, size = 22) },
                        )
                    }
                }
            }
            Spacer(Modifier.height(24.dp))
        }
    }
}

@Composable
private fun InfoCard(text: String) {
    Card(
        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(0.35f)),
        shape = RoundedCornerShape(14.dp),
        modifier = Modifier.fillMaxWidth(),
    ) {
        Text(text, Modifier.padding(14.dp), style = MaterialTheme.typography.bodyMedium)
    }
}
