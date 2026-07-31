package com.paldexpro.ui.screens.guides

import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.hilt.navigation.compose.hiltViewModel
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import com.paldexpro.R
import com.paldexpro.ui.components.GuideFormattedBody
import com.paldexpro.ui.components.SectionTitle

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GuideDetailScreen(
    guideId: String,
    useRu: Boolean,
    onBack: () -> Unit,
    onOpenPal: (String) -> Unit = {},
    onOpenItem: (String) -> Unit = {},
    vm: GuideDetailViewModel = hiltViewModel(),
) {
    val state by vm.state.collectAsStateWithLifecycle()
    val guide = state.guide
    var notes by remember { mutableStateOf("") }

    LaunchedEffect(guide?.userNotes) {
        notes = guide?.userNotes.orEmpty()
    }

    Column(Modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text(guide?.title(useRu) ?: "…") },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, null)
                }
            },
        )
        val g = guide ?: return@Column
        Column(
            Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
        ) {
            Text(
                guideCategoryLabel(g.category, useRu),
                style = MaterialTheme.typography.labelMedium,
                color = MaterialTheme.colorScheme.primary,
            )
            Text(g.title(useRu), style = MaterialTheme.typography.headlineMedium, fontWeight = FontWeight.Bold)
            Spacer(Modifier.height(12.dp))
            GuideFormattedBody(
                body = g.body(useRu),
                pals = state.pals,
                items = state.items,
                useRu = useRu,
                onOpenPal = onOpenPal,
                onOpenItem = onOpenItem,
            )
            SectionTitle(stringResource(R.string.my_notes))
            OutlinedTextField(
                value = notes,
                onValueChange = { notes = it },
                modifier = Modifier.fillMaxWidth().height(140.dp),
                placeholder = { Text(stringResource(R.string.notes_hint)) },
            )
            Spacer(Modifier.height(8.dp))
            Button(onClick = { vm.saveNotes(notes) }, modifier = Modifier.fillMaxWidth()) {
                Text(stringResource(R.string.save_notes))
            }
        }
    }
}
