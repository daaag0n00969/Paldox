package com.paldexpro.ui.screens.home

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
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.MenuBook
import androidx.compose.material.icons.filled.Castle
import androidx.compose.material.icons.filled.Egg
import androidx.compose.material.icons.filled.Extension
import androidx.compose.material.icons.filled.Inventory2
import androidx.compose.material.icons.filled.Map
import androidx.compose.material.icons.filled.NewReleases
import androidx.compose.material.icons.filled.Pets
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material.icons.filled.SportsMartialArts
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.paldexpro.R
import com.paldexpro.ui.components.PalAvatar
import com.paldexpro.ui.components.SectionTitle

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    useRu: Boolean,
    onOpenPaldex: () -> Unit,
    onOpenBreeding: () -> Unit,
    onOpenSkills: () -> Unit,
    onOpenItems: () -> Unit,
    onOpenBosses: () -> Unit,
    onOpenGuides: () -> Unit,
    onOpenUpdates: () -> Unit,
    onOpenMap: () -> Unit,
    onOpenMods: () -> Unit,
    onOpenSettings: () -> Unit,
    onOpenPal: (String) -> Unit,
    vm: HomeViewModel = hiltViewModel(),
) {
    val state by vm.state.collectAsStateWithLifecycle()

    Column(Modifier.fillMaxSize()) {
        TopAppBar(
            title = {
                Column {
                    Text(stringResource(R.string.app_name), fontWeight = FontWeight.Bold)
                    Text(
                        stringResource(R.string.home_subtitle, state.gameVersion, state.palCount),
                        style = MaterialTheme.typography.labelSmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
            },
            actions = {
                IconButton(onClick = onOpenSettings) {
                    Icon(Icons.Default.Settings, contentDescription = stringResource(R.string.settings))
                }
            },
        )

        Column(
            Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(horizontal = 16.dp),
        ) {
            SectionTitle(stringResource(R.string.quick_access))
            val tiles = listOf(
                Triple(stringResource(R.string.nav_paldex), Icons.Default.Pets, onOpenPaldex),
                Triple(stringResource(R.string.nav_breeding), Icons.Default.Egg, onOpenBreeding),
                Triple(stringResource(R.string.nav_skills), Icons.Default.SportsMartialArts, onOpenSkills),
                Triple(stringResource(R.string.nav_items), Icons.Default.Inventory2, onOpenItems),
                Triple(stringResource(R.string.nav_bosses), Icons.Default.Castle, onOpenBosses),
                Triple(stringResource(R.string.nav_guides), Icons.AutoMirrored.Filled.MenuBook, onOpenGuides),
                Triple(stringResource(R.string.nav_updates), Icons.Default.NewReleases, onOpenUpdates),
                Triple(stringResource(R.string.nav_map), Icons.Default.Map, onOpenMap),
                Triple(stringResource(R.string.nav_mods), Icons.Default.Extension, onOpenMods),
            )
            tiles.chunked(2).forEach { row ->
                Row(
                    Modifier.fillMaxWidth().padding(bottom = 10.dp),
                    horizontalArrangement = Arrangement.spacedBy(10.dp),
                ) {
                    row.forEach { (title, icon, action) ->
                        HomeTile(title, icon, Modifier.weight(1f), action)
                    }
                    if (row.size == 1) Spacer(Modifier.weight(1f))
                }
            }

            SectionTitle(stringResource(R.string.featured_pals))
            LazyRow(
                contentPadding = PaddingValues(bottom = 20.dp),
                horizontalArrangement = Arrangement.spacedBy(10.dp),
            ) {
                items(state.featured, key = { it.id }) { pal ->
                    Card(
                        modifier = Modifier
                            .size(width = 118.dp, height = 138.dp)
                            .clickable { onOpenPal(pal.id) },
                        shape = RoundedCornerShape(18.dp),
                        colors = CardDefaults.cardColors(
                            containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(0.4f),
                        ),
                    ) {
                        Column(
                            Modifier.padding(12.dp).fillMaxSize(),
                            horizontalAlignment = Alignment.CenterHorizontally,
                            verticalArrangement = Arrangement.Center,
                        ) {
                            PalAvatar(pal, size = 56)
                            Spacer(Modifier.height(8.dp))
                            Text(
                                pal.displayName(useRu),
                                style = MaterialTheme.typography.labelLarge,
                                fontWeight = FontWeight.SemiBold,
                                maxLines = 1,
                                overflow = TextOverflow.Ellipsis,
                            )
                            Text(
                                "#${pal.dexNumber}",
                                style = MaterialTheme.typography.labelSmall,
                                color = MaterialTheme.colorScheme.onSurfaceVariant,
                            )
                        }
                    }
                }
            }

            SectionTitle(stringResource(R.string.offline_badge))
            Text(
                stringResource(R.string.offline_hint),
                style = MaterialTheme.typography.bodyMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(bottom = 28.dp),
            )
        }
    }
}

@Composable
private fun HomeTile(
    title: String,
    icon: ImageVector,
    modifier: Modifier,
    onClick: () -> Unit,
) {
    Card(
        modifier = modifier
            .height(84.dp)
            .clickable(onClick = onClick),
        shape = RoundedCornerShape(18.dp),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.primaryContainer.copy(0.4f),
        ),
    ) {
        Row(
            Modifier.padding(horizontal = 14.dp, vertical = 12.dp).fillMaxSize(),
            verticalAlignment = Alignment.CenterVertically,
            horizontalArrangement = Arrangement.spacedBy(12.dp),
        ) {
            Icon(icon, null, tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(26.dp))
            Text(
                title,
                style = MaterialTheme.typography.titleSmall,
                fontWeight = FontWeight.SemiBold,
                maxLines = 2,
                overflow = TextOverflow.Ellipsis,
                textAlign = TextAlign.Start,
            )
        }
    }
}
