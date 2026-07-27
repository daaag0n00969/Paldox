package com.paldexpro.ui

import android.content.Context
import android.content.res.Configuration
import android.os.LocaleList
import com.paldexpro.data.prefs.AppLanguage
import java.util.Locale

/**
 * Applies app language to a base context (used from Activity.attachBaseContext).
 * Must wrap the Activity base context so the result remains a proper hierarchy.
 */
fun Context.withAppLanguage(language: AppLanguage): Context {
    val locale = Locale.forLanguageTag(language.tag)
    Locale.setDefault(locale)
    val config = Configuration(resources.configuration)
    config.setLocales(LocaleList(locale))
    return createConfigurationContext(config)
}
