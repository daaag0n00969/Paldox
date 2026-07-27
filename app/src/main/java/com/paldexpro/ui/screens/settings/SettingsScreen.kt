package com.paldexpro.ui.screens.settings

import android.content.Intent
import android.net.Uri
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.automirrored.filled.OpenInNew
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import com.paldexpro.R
import com.paldexpro.ui.components.SectionTitle

const val FEEDBACK_TELEGRAM = "https://t.me/paldox_official"
const val FEEDBACK_EMAIL = "dag0n00969@gmail.com"
const val FEEDBACK_X = "https://x.com/nikolas_borman"

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    useRu: Boolean,
    darkTheme: Boolean,
    onBack: () -> Unit,
    onToggleLanguage: () -> Unit,
    onToggleTheme: () -> Unit,
    onOpenAbout: () -> Unit,
    onOpenAds: () -> Unit,
) {
    val context = LocalContext.current

    fun openUrl(url: String) {
        runCatching {
            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
        }
    }

    fun openEmail() {
        runCatching {
            val intent = Intent(Intent.ACTION_SENDTO).apply {
                data = Uri.parse("mailto:$FEEDBACK_EMAIL")
                putExtra(Intent.EXTRA_EMAIL, arrayOf(FEEDBACK_EMAIL))
                putExtra(Intent.EXTRA_SUBJECT, "Paldox feedback")
            }
            context.startActivity(Intent.createChooser(intent, null))
        }
    }

    Column(Modifier.fillMaxSize()) {
        TopAppBar(
            title = { Text(stringResource(R.string.settings)) },
            navigationIcon = {
                IconButton(onClick = onBack) {
                    Icon(Icons.AutoMirrored.Filled.ArrowBack, null)
                }
            },
        )
        Column(
            Modifier
                .verticalScroll(rememberScrollState())
                .padding(16.dp),
        ) {
            SectionTitle(stringResource(R.string.appearance))
            Row(
                Modifier.fillMaxWidth().padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Text(stringResource(R.string.dark_theme), modifier = Modifier.weight(1f))
                Switch(checked = darkTheme, onCheckedChange = { onToggleTheme() })
            }
            Row(
                Modifier.fillMaxWidth().padding(vertical = 8.dp),
                verticalAlignment = Alignment.CenterVertically,
            ) {
                Column(Modifier.weight(1f)) {
                    Text(stringResource(R.string.language))
                    Text(
                        if (useRu) stringResource(R.string.lang_russian) else stringResource(R.string.lang_english),
                        style = MaterialTheme.typography.bodySmall,
                        color = MaterialTheme.colorScheme.onSurfaceVariant,
                    )
                }
                Switch(checked = useRu, onCheckedChange = { onToggleLanguage() })
            }

            // Single "About" entry (no duplicate section title with the same text)
            SectionTitle(stringResource(R.string.settings_app_section))
            SettingsNavRow(
                title = stringResource(R.string.about_button),
                subtitle = stringResource(R.string.about_button_hint),
                external = false,
                onClick = onOpenAbout,
            )
            SettingsNavRow(
                title = stringResource(R.string.ads_title),
                subtitle = stringResource(R.string.ads_button_hint),
                external = false,
                onClick = onOpenAds,
            )

            SectionTitle(stringResource(R.string.feedback_section))
            Text(
                stringResource(R.string.feedback_intro),
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
                modifier = Modifier.padding(bottom = 4.dp),
            )
            SettingsNavRow(
                title = stringResource(R.string.feedback_telegram),
                subtitle = "@paldox_official",
                external = true,
                onClick = { openUrl(FEEDBACK_TELEGRAM) },
            )
            SettingsNavRow(
                title = stringResource(R.string.feedback_email),
                subtitle = FEEDBACK_EMAIL,
                external = true,
                onClick = { openEmail() },
            )
            SettingsNavRow(
                title = stringResource(R.string.feedback_x),
                subtitle = "@nikolas_borman",
                external = true,
                onClick = { openUrl(FEEDBACK_X) },
            )
        }
    }
}

@Composable
private fun SettingsNavRow(
    title: String,
    subtitle: String,
    external: Boolean,
    onClick: () -> Unit,
) {
    Row(
        Modifier
            .fillMaxWidth()
            .clickable(onClick = onClick)
            .padding(vertical = 12.dp),
        verticalAlignment = Alignment.CenterVertically,
    ) {
        Column(Modifier.weight(1f)) {
            Text(title, style = MaterialTheme.typography.titleMedium)
            Text(
                subtitle,
                style = MaterialTheme.typography.bodySmall,
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        Icon(
            if (external) Icons.AutoMirrored.Filled.OpenInNew
            else Icons.AutoMirrored.Filled.KeyboardArrowRight,
            contentDescription = null,
            tint = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}
