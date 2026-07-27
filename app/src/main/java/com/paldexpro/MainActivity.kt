package com.paldexpro

import android.content.Context
import android.os.Bundle
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.appcompat.app.AppCompatActivity
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.lifecycle.lifecycleScope
import com.paldexpro.data.prefs.AppLanguage
import com.paldexpro.data.prefs.AppPreferences
import com.paldexpro.data.prefs.SyncSettings
import com.paldexpro.ui.navigation.PalDexNavHost
import com.paldexpro.ui.theme.PalDexTheme
import com.paldexpro.ui.withAppLanguage
import dagger.hilt.android.AndroidEntryPoint
import kotlinx.coroutines.launch
import javax.inject.Inject

@AndroidEntryPoint
class MainActivity : AppCompatActivity() {

    @Inject lateinit var prefs: AppPreferences

    override fun attachBaseContext(newBase: Context) {
        // Apply language before any resource lookup. Keep Activity as base of hierarchy.
        val lang = SyncSettings.language(newBase)
        super.attachBaseContext(newBase.withAppLanguage(lang))
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()

        setContent {
            var useRu by remember {
                mutableStateOf(SyncSettings.language(applicationContext) == AppLanguage.Russian)
            }
            var darkTheme by remember {
                mutableStateOf(SyncSettings.darkTheme(applicationContext))
            }

            PalDexTheme(darkTheme = darkTheme) {
                PalDexNavHost(
                    useRu = useRu,
                    darkTheme = darkTheme,
                    onToggleLanguage = {
                        lifecycleScope.launch {
                            val next = if (useRu) AppLanguage.English else AppLanguage.Russian
                            prefs.setLanguage(next)
                            // Recreate Activity so attachBaseContext reloads all string resources
                            recreate()
                        }
                    },
                    onToggleTheme = {
                        lifecycleScope.launch {
                            val next = !darkTheme
                            prefs.setDarkTheme(next)
                            darkTheme = next
                        }
                    },
                )
            }
        }
    }
}
