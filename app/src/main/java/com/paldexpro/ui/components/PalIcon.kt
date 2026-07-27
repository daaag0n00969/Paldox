package com.paldexpro.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import coil.request.ImageRequest
import com.paldexpro.domain.model.Pal
import com.paldexpro.ui.theme.elementColor

@Composable
fun PalIcon(
    pal: Pal,
    size: Int = 52,
    modifier: Modifier = Modifier,
) {
    val context = LocalContext.current
    val shape = RoundedCornerShape((size / 4).coerceAtLeast(10).dp)
    val c1 = elementColor(pal.element1.name)
    val c2 = pal.element2?.let { elementColor(it.name) } ?: c1

    Box(
        modifier = modifier
            .size(size.dp)
            .clip(shape)
            .background(Brush.linearGradient(listOf(c1.copy(0.35f), c2.copy(0.2f))))
            .border(1.dp, c1.copy(0.35f), shape),
        contentAlignment = Alignment.Center,
    ) {
        AsyncImage(
            model = ImageRequest.Builder(context)
                .data("file:///android_asset/${pal.iconPath()}")
                .crossfade(true)
                .build(),
            contentDescription = pal.nameEn,
            contentScale = ContentScale.Fit,
            modifier = Modifier.size((size * 0.9f).dp),
        )
        Text(
            text = pal.nameEn.take(2).uppercase(),
            fontWeight = FontWeight.Bold,
            color = Color.White.copy(alpha = 0.15f),
            fontSize = (size / 3.5f).sp,
        )
    }
}

@Composable
fun PalAvatar(pal: Pal, size: Int = 52) {
    PalIcon(pal = pal, size = size)
}

/** Name with Palpedia number underneath (breeding / pickers). */
@Composable
fun PalNameWithDex(
    pal: Pal,
    useRu: Boolean,
    bold: Boolean = false,
    maxLines: Int = 1,
) {
    Column(horizontalAlignment = Alignment.CenterHorizontally) {
        Text(
            text = pal.displayName(useRu),
            style = if (bold) MaterialTheme.typography.labelLarge else MaterialTheme.typography.labelSmall,
            fontWeight = if (bold) FontWeight.Bold else FontWeight.Normal,
            maxLines = maxLines,
            overflow = TextOverflow.Ellipsis,
        )
        Text(
            text = "#${pal.dexNumber}",
            style = MaterialTheme.typography.labelSmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
    }
}
