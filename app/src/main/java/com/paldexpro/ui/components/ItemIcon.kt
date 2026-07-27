package com.paldexpro.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.paldexpro.domain.model.GameItem
import com.paldexpro.domain.model.Rarity

@Composable
fun ItemIcon(
    item: GameItem,
    size: Int = 48,
    modifier: Modifier = Modifier,
) {
    val context = LocalContext.current
    val shape = RoundedCornerShape((size / 5).coerceAtLeast(8).dp)
    val border = rarityColor(item.rarity).copy(0.55f)
    Box(
        modifier = modifier
            .size(size.dp)
            .clip(shape)
            .background(MaterialTheme.colorScheme.surfaceVariant.copy(0.55f))
            .border(1.dp, border, shape),
        contentAlignment = Alignment.Center,
    ) {
        AsyncImage(
            model = ImageRequest.Builder(context)
                .data("file:///android_asset/${item.iconPath()}")
                .crossfade(true)
                .build(),
            contentDescription = item.nameEn,
            contentScale = ContentScale.Fit,
            modifier = Modifier.size((size * 0.82f).dp),
        )
        Text(
            text = item.nameEn.take(1),
            color = Color.White.copy(0.12f),
            fontWeight = FontWeight.Bold,
            fontSize = (size / 2.8f).sp,
        )
    }
}

fun rarityColor(rarity: Rarity): Color = when (rarity) {
    Rarity.common -> Color(0xFF90A4AE)
    Rarity.uncommon -> Color(0xFF66BB6A)
    Rarity.rare -> Color(0xFF42A5F5)
    Rarity.epic -> Color(0xFFAB47BC)
    Rarity.legendary -> Color(0xFFFFA726)
}
