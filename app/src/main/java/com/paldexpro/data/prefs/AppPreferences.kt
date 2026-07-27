package com.paldexpro.data.prefs

import android.content.Context
import androidx.datastore.core.DataStore
import androidx.datastore.preferences.core.Preferences
import androidx.datastore.preferences.core.booleanPreferencesKey
import androidx.datastore.preferences.core.edit
import androidx.datastore.preferences.core.stringPreferencesKey
import androidx.datastore.preferences.preferencesDataStore
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

private val Context.dataStore: DataStore<Preferences> by preferencesDataStore(name = "paldox_settings")

enum class AppLanguage(val tag: String) {
    English("en"),
    Russian("ru");

    companion object {
        fun fromTag(tag: String?): AppLanguage =
            entries.firstOrNull { it.tag.equals(tag, ignoreCase = true) } ?: English
    }
}

data class UserSettings(
    val language: AppLanguage = AppLanguage.English,
    val darkTheme: Boolean = true,
)

/**
 * Synchronous prefs for [android.app.Activity.attachBaseContext] (DataStore is async-only).
 * Kept in sync with DataStore writes.
 */
object SyncSettings {
    private const val NAME = "paldox_sync"
    private const val KEY_LANG = "language"
    private const val KEY_DARK = "dark_theme"

    fun language(context: Context): AppLanguage {
        val tag = context.applicationContext
            .getSharedPreferences(NAME, Context.MODE_PRIVATE)
            .getString(KEY_LANG, AppLanguage.English.tag)
        return AppLanguage.fromTag(tag)
    }

    fun darkTheme(context: Context): Boolean {
        return context.applicationContext
            .getSharedPreferences(NAME, Context.MODE_PRIVATE)
            .getBoolean(KEY_DARK, true)
    }

    fun setLanguage(context: Context, language: AppLanguage) {
        context.applicationContext
            .getSharedPreferences(NAME, Context.MODE_PRIVATE)
            .edit()
            .putString(KEY_LANG, language.tag)
            .apply()
    }

    fun setDarkTheme(context: Context, enabled: Boolean) {
        context.applicationContext
            .getSharedPreferences(NAME, Context.MODE_PRIVATE)
            .edit()
            .putBoolean(KEY_DARK, enabled)
            .apply()
    }
}

@Singleton
class AppPreferences @Inject constructor(
    @ApplicationContext private val context: Context,
) {
    private val keyLang = stringPreferencesKey("language")
    private val keyDark = booleanPreferencesKey("dark_theme")

    val settings: Flow<UserSettings> = context.dataStore.data.map { prefs ->
        UserSettings(
            language = AppLanguage.fromTag(
                prefs[keyLang] ?: SyncSettings.language(context).tag,
            ),
            darkTheme = prefs[keyDark] ?: SyncSettings.darkTheme(context),
        )
    }

    suspend fun setLanguage(language: AppLanguage) {
        SyncSettings.setLanguage(context, language)
        context.dataStore.edit { it[keyLang] = language.tag }
    }

    suspend fun setDarkTheme(enabled: Boolean) {
        SyncSettings.setDarkTheme(context, enabled)
        context.dataStore.edit { it[keyDark] = enabled }
    }
}
