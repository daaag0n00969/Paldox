package com.paldexpro.ui.screens.paldex

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.PaddingValues
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.paldexpro.R
import com.paldexpro.ui.components.ElementFilterRow
import com.paldexpro.ui.components.EmptyState
import com.paldexpro.ui.components.PalListItem
import com.paldexpro.ui.components.SearchField

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PaldexScreen(
    useRu: Boolean,
    onPalClick: (String) -> Unit,
    vm: PaldexViewModel = hiltViewModel(),
) {
    val state by vm.state.collectAsStateWithLifecycle()
    val query by vm.queryText.collectAsStateWithLifecycle()

    Column(Modifier.fillMaxSize()) {
        TopAppBar(title = { Text(stringResource(R.string.nav_paldex)) })
        Column(Modifier.padding(horizontal = 16.dp)) {
            SearchField(
                value = query,
                onValueChange = vm::setQuery,
                placeholder = stringResource(R.string.search_pals),
            )
            Text(
                text = stringResource(R.string.results_count, state.pals.size),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(top = 8.dp, bottom = 4.dp),
            )
            ElementFilterRow(selected = state.element, onSelect = vm::setElement)
        }
        if (state.pals.isEmpty()) {
            EmptyState(stringResource(R.string.no_results))
        } else {
            LazyColumn(
                contentPadding = PaddingValues(16.dp),
                verticalArrangement = Arrangement.spacedBy(8.dp),
            ) {
                items(state.pals, key = { it.id }) { pal ->
                    PalListItem(pal = pal, useRu = useRu, onClick = { onPalClick(pal.id) })
                }
            }
        }
    }
}
