package com.paldexpro.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// Element colors (game-like palette)
val ElementNeutral = Color(0xFFB0BEC5)
val ElementFire = Color(0xFFFF6B3D)
val ElementWater = Color(0xFF3DB8FF)
val ElementGrass = Color(0xFF5CDB7A)
val ElementElectric = Color(0xFFFFD54F)
val ElementIce = Color(0xFF7ED4FF)
val ElementGround = Color(0xFFC4A484)
val ElementDark = Color(0xFFB39DDB)
val ElementDragon = Color(0xFFE48CFF)

val GoldTier = Color(0xFFFFD54F)
val BlueTier = Color(0xFF64B5F6)
val GreenTier = Color(0xFF81C784)
val LegendTier = Color(0xFFFF8A65)

// Palworld-inspired UI tokens (not official assets — fan palette)
val PalHudCyan = Color(0xFF4FD6D0)
val PalHudGold = Color(0xFFE8B84A)
val PalHudOrange = Color(0xFFFF8A4C)
val PalPanelDeep = Color(0xFF0B1520)
val PalPanelMid = Color(0xFF142433)
val PalPanelRaised = Color(0xFF1C3145)
val PalStroke = Color(0xFF3D5A70)

/**
 * Dark scheme tuned toward Palworld HUD: deep navy panels, cyan primary, warm gold accents.
 */
private val DarkColors = darkColorScheme(
    primary = PalHudCyan,
    onPrimary = Color(0xFF003735),
    primaryContainer = Color(0xFF0F4F4C),
    onPrimaryContainer = Color(0xFFA8F5F0),
    secondary = PalHudGold,
    onSecondary = Color(0xFF3D2A00),
    secondaryContainer = Color(0xFF5C4200),
    onSecondaryContainer = Color(0xFFFFE5A8),
    tertiary = PalHudOrange,
    onTertiary = Color(0xFF3B1400),
    tertiaryContainer = Color(0xFF5C2800),
    onTertiaryContainer = Color(0xFFFFDBC8),
    background = PalPanelDeep,
    onBackground = Color(0xFFE6EEF5),
    surface = PalPanelMid,
    onSurface = Color(0xFFE6EEF5),
    surfaceVariant = PalPanelRaised,
    onSurfaceVariant = Color(0xFFB7C9D6),
    outline = PalStroke,
    outlineVariant = Color(0xFF2A4054),
    error = Color(0xFFFFB4AB),
    inverseSurface = Color(0xFFE6EEF5),
    inverseOnSurface = Color(0xFF0F1A24),
    inversePrimary = Color(0xFF006A66),
)

private val LightColors = lightColorScheme(
    primary = Color(0xFF006A66),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFF8EF2EC),
    onPrimaryContainer = Color(0xFF00201F),
    secondary = Color(0xFF7A5900),
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xFFFFDEA3),
    onSecondaryContainer = Color(0xFF271900),
    tertiary = Color(0xFF9C4500),
    onTertiary = Color(0xFFFFFFFF),
    background = Color(0xFFF3F7FA),
    onBackground = Color(0xFF141C22),
    surface = Color(0xFFF3F7FA),
    onSurface = Color(0xFF141C22),
    surfaceVariant = Color(0xFFD5E3EC),
    onSurfaceVariant = Color(0xFF3C4C57),
    outline = Color(0xFF6C7C88),
)

@Composable
fun PalDexTheme(
    darkTheme: Boolean = true,
    content: @Composable () -> Unit,
) {
    // Dark by default — closer to in-game HUD.
    val colors = if (darkTheme) DarkColors else LightColors
    MaterialTheme(
        colorScheme = colors,
        typography = Typography,
        content = content,
    )
}

fun elementColor(name: String): Color = when (name.lowercase()) {
    "neutral" -> ElementNeutral
    "fire" -> ElementFire
    "water" -> ElementWater
    "grass" -> ElementGrass
    "electric" -> ElementElectric
    "ice" -> ElementIce
    "ground" -> ElementGround
    "dark" -> ElementDark
    "dragon" -> ElementDragon
    else -> ElementNeutral
}
