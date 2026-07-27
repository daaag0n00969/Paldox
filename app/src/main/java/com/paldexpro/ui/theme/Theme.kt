package com.paldexpro.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

// Element colors
val ElementNeutral = Color(0xFFB0BEC5)
val ElementFire = Color(0xFFFF6E40)
val ElementWater = Color(0xFF40C4FF)
val ElementGrass = Color(0xFF69F0AE)
val ElementElectric = Color(0xFFFFD740)
val ElementIce = Color(0xFF80D8FF)
val ElementGround = Color(0xFFBCAAA4)
val ElementDark = Color(0xFFB39DDB)
val ElementDragon = Color(0xFFEA80FC)

val GoldTier = Color(0xFFFFD54F)
val BlueTier = Color(0xFF64B5F6)
val GreenTier = Color(0xFF81C784)
val LegendTier = Color(0xFFFF8A65)

private val DarkColors = darkColorScheme(
    primary = Color(0xFF7CDBB6),
    onPrimary = Color(0xFF00382A),
    primaryContainer = Color(0xFF00513E),
    onPrimaryContainer = Color(0xFF99F8D2),
    secondary = Color(0xFFFFB74D),
    onSecondary = Color(0xFF4A2800),
    secondaryContainer = Color(0xFF6A3C00),
    onSecondaryContainer = Color(0xFFFFDDB3),
    tertiary = Color(0xFF80CBC4),
    background = Color(0xFF0E1412),
    onBackground = Color(0xFFE1E3E0),
    surface = Color(0xFF0E1412),
    onSurface = Color(0xFFE1E3E0),
    surfaceVariant = Color(0xFF3F4945),
    onSurfaceVariant = Color(0xFFBFC9C3),
    outline = Color(0xFF89938E),
    error = Color(0xFFFFB4AB),
)

private val LightColors = lightColorScheme(
    primary = Color(0xFF006C53),
    onPrimary = Color(0xFFFFFFFF),
    primaryContainer = Color(0xFF89F8D1),
    onPrimaryContainer = Color(0xFF002117),
    secondary = Color(0xFF8B5000),
    onSecondary = Color(0xFFFFFFFF),
    secondaryContainer = Color(0xFFFFDDB3),
    onSecondaryContainer = Color(0xFF2C1600),
    tertiary = Color(0xFF006A64),
    background = Color(0xFFF5FBF6),
    onBackground = Color(0xFF171D1A),
    surface = Color(0xFFF5FBF6),
    onSurface = Color(0xFF171D1A),
    surfaceVariant = Color(0xFFDBE5DF),
    onSurfaceVariant = Color(0xFF3F4945),
    outline = Color(0xFF6F7974),
)

@Composable
fun PalDexTheme(
    darkTheme: Boolean = true,
    content: @Composable () -> Unit,
) {
    // Dark by default; user can switch in Settings.
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
