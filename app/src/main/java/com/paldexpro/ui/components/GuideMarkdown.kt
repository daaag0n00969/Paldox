package com.paldexpro.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.ExperimentalLayoutApi
import androidx.compose.foundation.layout.FlowRow
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Surface
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.paldexpro.domain.model.GameItem
import com.paldexpro.domain.model.Pal

/**
 * Guide body renderer with interactive pal/item links:
 * - explicit [[pal:id]] / [[item:id]]
 * - auto-detect EN/RU display names of known pals and items
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun GuideFormattedBody(
    body: String,
    pals: List<Pal> = emptyList(),
    items: List<GameItem> = emptyList(),
    useRu: Boolean = true,
    onOpenPal: (String) -> Unit = {},
    onOpenItem: (String) -> Unit = {},
) {
    val catalog = remember(pals, items) { buildLinkCatalog(pals, items) }
    val blocks = parseGuideBlocks(body)
    Column(Modifier.fillMaxWidth()) {
        blocks.forEach { block ->
            when (block) {
                is GuideBlock.Heading -> {
                    Spacer(Modifier.height(12.dp))
                    Text(
                        block.text.stripBold(),
                        style = MaterialTheme.typography.titleLarge,
                        fontWeight = FontWeight.Bold,
                        color = MaterialTheme.colorScheme.primary,
                    )
                    HorizontalDivider(
                        Modifier.padding(vertical = 6.dp),
                        color = MaterialTheme.colorScheme.primary.copy(0.3f),
                    )
                }
                is GuideBlock.SubHeading -> {
                    Spacer(Modifier.height(10.dp))
                    Text(
                        block.text.stripBold(),
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                    )
                }
                is GuideBlock.Bullet -> {
                    Row(Modifier.padding(vertical = 3.dp)) {
                        Text("•", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.width(8.dp))
                        InlineGuideText(block.text, catalog, useRu, onOpenPal, onOpenItem)
                    }
                }
                is GuideBlock.Numbered -> {
                    Row(Modifier.padding(vertical = 3.dp)) {
                        Text(
                            "${block.n}.",
                            color = MaterialTheme.colorScheme.primary,
                            fontWeight = FontWeight.Bold,
                            modifier = Modifier.width(24.dp),
                        )
                        InlineGuideText(block.text, catalog, useRu, onOpenPal, onOpenItem)
                    }
                }
                is GuideBlock.Check -> {
                    Row(Modifier.padding(vertical = 3.dp)) {
                        Text(if (block.done) "☑" else "☐", color = MaterialTheme.colorScheme.secondary)
                        Spacer(Modifier.width(8.dp))
                        InlineGuideText(block.text, catalog, useRu, onOpenPal, onOpenItem)
                    }
                }
                is GuideBlock.Table -> {
                    Spacer(Modifier.height(8.dp))
                    Card(
                        colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant.copy(0.4f)),
                        shape = RoundedCornerShape(12.dp),
                        modifier = Modifier.fillMaxWidth(),
                    ) {
                        Column(Modifier.padding(10.dp)) {
                            block.rows.forEachIndexed { index, row ->
                                Row(Modifier.fillMaxWidth().padding(vertical = 4.dp)) {
                                    row.forEach { cell ->
                                        InlineGuideText(
                                            text = cell,
                                            catalog = catalog,
                                            useRu = useRu,
                                            onOpenPal = onOpenPal,
                                            onOpenItem = onOpenItem,
                                            modifier = Modifier.weight(1f),
                                            compact = true,
                                        )
                                    }
                                }
                                if (index == 0) {
                                    HorizontalDivider(color = MaterialTheme.colorScheme.outline.copy(0.4f))
                                }
                            }
                        }
                    }
                }
                is GuideBlock.Quote -> {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 6.dp)
                            .background(
                                MaterialTheme.colorScheme.secondaryContainer.copy(0.35f),
                                RoundedCornerShape(8.dp),
                            )
                            .padding(12.dp),
                    ) {
                        InlineGuideText(block.text, catalog, useRu, onOpenPal, onOpenItem)
                    }
                }
                is GuideBlock.Paragraph -> {
                    InlineGuideText(
                        block.text,
                        catalog,
                        useRu,
                        onOpenPal,
                        onOpenItem,
                        modifier = Modifier.padding(vertical = 4.dp),
                    )
                }
                GuideBlock.SpacerLine -> Spacer(Modifier.height(6.dp))
            }
        }
    }
}

@OptIn(ExperimentalLayoutApi::class)
@Composable
private fun InlineGuideText(
    text: String,
    catalog: LinkCatalog,
    useRu: Boolean,
    onOpenPal: (String) -> Unit,
    onOpenItem: (String) -> Unit,
    modifier: Modifier = Modifier,
    compact: Boolean = false,
) {
    val parts = remember(text, catalog) { splitInteractive(text, catalog) }
    if (parts.none { it is TextPart.Link }) {
        Text(
            text.stripBold(),
            style = if (compact) MaterialTheme.typography.bodyMedium else MaterialTheme.typography.bodyLarge,
            modifier = modifier,
        )
        return
    }
    FlowRow(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(4.dp),
        verticalArrangement = Arrangement.spacedBy(4.dp),
    ) {
        parts.forEach { part ->
            when (part) {
                is TextPart.Plain -> {
                    if (part.text.isNotBlank()) {
                        Text(
                            part.text.stripBold(),
                            style = if (compact) {
                                MaterialTheme.typography.bodyMedium
                            } else {
                                MaterialTheme.typography.bodyLarge
                            },
                        )
                    }
                }
                is TextPart.Link -> {
                    val isPal = part.kind == "pal"
                    val label = when {
                        isPal -> {
                            val pal = catalog.palById[part.id]
                            if (pal != null) "🐾 ${pal.displayName(useRu)}" else "🐾 ${part.label.ifBlank { part.id }}"
                        }
                        else -> {
                            val item = catalog.itemById[part.id]
                            if (item != null) "📦 ${item.displayName(useRu)}" else "📦 ${part.label.ifBlank { part.id }}"
                        }
                    }
                    Surface(
                        color = if (isPal) {
                            MaterialTheme.colorScheme.primaryContainer.copy(0.55f)
                        } else {
                            MaterialTheme.colorScheme.secondaryContainer.copy(0.55f)
                        },
                        shape = RoundedCornerShape(50),
                        modifier = Modifier.clickable {
                            if (isPal) onOpenPal(part.id) else onOpenItem(part.id)
                        },
                    ) {
                        Text(
                            text = label,
                            modifier = Modifier.padding(horizontal = 10.dp, vertical = 4.dp),
                            style = MaterialTheme.typography.labelLarge,
                            fontWeight = FontWeight.SemiBold,
                            color = MaterialTheme.colorScheme.onSurface,
                        )
                    }
                }
            }
        }
    }
}

private data class LinkCatalog(
    val palById: Map<String, Pal>,
    val itemById: Map<String, GameItem>,
    /** Lowercase token → (kind, id), longer tokens first for matching */
    val tokens: List<Pair<String, Pair<String, String>>>,
)

private fun buildLinkCatalog(pals: List<Pal>, items: List<GameItem>): LinkCatalog {
    val palById = pals.associateBy { it.id }
    val itemById = items.associateBy { it.id }
    val map = linkedMapOf<String, Pair<String, String>>()

    fun putToken(raw: String, kind: String, id: String) {
        val t = raw.trim()
        if (t.length < 3) return // skip short tokens (Mau, Nox…) to reduce false positives
        val key = t.lowercase()
        // Prefer first registration; longer names registered later overwrite only if longer key conflict handled by sort
        if (key !in map) map[key] = kind to id
    }

    pals.forEach { p ->
        putToken(p.nameEn, "pal", p.id)
        putToken(p.nameRu, "pal", p.id)
        putToken(p.id.replace('_', ' '), "pal", p.id)
    }
    items.forEach { it ->
        putToken(it.nameEn, "item", it.id)
        putToken(it.nameRu, "item", it.id)
    }
    val tokens = map.entries
        .sortedByDescending { it.key.length }
        .map { it.key to it.value }
    return LinkCatalog(palById, itemById, tokens)
}

private sealed class TextPart {
    data class Plain(val text: String) : TextPart()
    data class Link(val kind: String, val id: String, val label: String = "") : TextPart()
}

private val MARKER_RE = Regex("""\[\[(pal|item):([a-zA-Z0-9_]+)\]\]""")

private fun splitInteractive(text: String, catalog: LinkCatalog): List<TextPart> {
    // Pass 1: explicit markers
    val withMarkers = mutableListOf<TextPart>()
    var last = 0
    MARKER_RE.findAll(text).forEach { m ->
        if (m.range.first > last) {
            withMarkers += TextPart.Plain(text.substring(last, m.range.first))
        }
        withMarkers += TextPart.Link(m.groupValues[1], m.groupValues[2])
        last = m.range.last + 1
    }
    if (last < text.length) withMarkers += TextPart.Plain(text.substring(last))
    if (withMarkers.isEmpty()) withMarkers += TextPart.Plain(text)

    // Pass 2: auto-link names inside plain segments
    if (catalog.tokens.isEmpty()) return withMarkers
    val out = mutableListOf<TextPart>()
    withMarkers.forEach { part ->
        if (part is TextPart.Link) {
            out += part
        } else if (part is TextPart.Plain) {
            out += autoLinkPlain(part.text, catalog)
        }
    }
    return out
}

private fun autoLinkPlain(text: String, catalog: LinkCatalog): List<TextPart> {
    if (text.isEmpty() || catalog.tokens.isEmpty()) return listOf(TextPart.Plain(text))
    val lower = text.lowercase()
    val hits = mutableListOf<Triple<Int, Int, Pair<String, String>>>() // start, end, kind/id
    var i = 0
    while (i < lower.length) {
        var matched: Triple<Int, Int, Pair<String, String>>? = null
        for ((token, ref) in catalog.tokens) {
            if (i + token.length > lower.length) continue
            if (!lower.regionMatches(i, token, 0, token.length)) continue
            // boundary check: avoid matching inside words
            val beforeOk = i == 0 || !lower[i - 1].isLetterOrDigit()
            val afterIdx = i + token.length
            val afterOk = afterIdx >= lower.length || !lower[afterIdx].isLetterOrDigit()
            if (beforeOk && afterOk) {
                matched = Triple(i, afterIdx, ref)
                break
            }
        }
        if (matched != null) {
            hits += matched
            i = matched.second
        } else {
            i++
        }
    }
    if (hits.isEmpty()) return listOf(TextPart.Plain(text))

    val parts = mutableListOf<TextPart>()
    var cursor = 0
    hits.forEach { (start, end, ref) ->
        if (start > cursor) parts += TextPart.Plain(text.substring(cursor, start))
        val label = text.substring(start, end)
        parts += TextPart.Link(ref.first, ref.second, label)
        cursor = end
    }
    if (cursor < text.length) parts += TextPart.Plain(text.substring(cursor))
    return parts
}

private sealed class GuideBlock {
    data class Heading(val text: String) : GuideBlock()
    data class SubHeading(val text: String) : GuideBlock()
    data class Bullet(val text: String) : GuideBlock()
    data class Numbered(val n: Int, val text: String) : GuideBlock()
    data class Check(val text: String, val done: Boolean) : GuideBlock()
    data class Table(val rows: List<List<String>>) : GuideBlock()
    data class Quote(val text: String) : GuideBlock()
    data class Paragraph(val text: String) : GuideBlock()
    data object SpacerLine : GuideBlock()
}

private fun parseGuideBlocks(body: String): List<GuideBlock> {
    val lines = body.replace("\r\n", "\n").split("\n")
    val out = mutableListOf<GuideBlock>()
    var i = 0
    while (i < lines.size) {
        val line = lines[i].trim()
        when {
            line.isEmpty() -> out += GuideBlock.SpacerLine
            line.startsWith("## ") -> out += GuideBlock.Heading(line.removePrefix("## ").trim())
            line.startsWith("### ") -> out += GuideBlock.SubHeading(line.removePrefix("### ").trim())
            line.startsWith("- [x] ") || line.startsWith("- [X] ") ->
                out += GuideBlock.Check(line.drop(6).trim(), true)
            line.startsWith("- [ ] ") ->
                out += GuideBlock.Check(line.drop(6).trim(), false)
            line.startsWith("- ") || line.startsWith("* ") ->
                out += GuideBlock.Bullet(line.drop(2).trim())
            line.matches(Regex("^\\d+\\.\\s+.*")) -> {
                val n = line.substringBefore('.').toIntOrNull() ?: 1
                out += GuideBlock.Numbered(n, line.substringAfter('.').trim())
            }
            line.startsWith("|") && line.endsWith("|") -> {
                val rows = mutableListOf<List<String>>()
                while (i < lines.size) {
                    val l = lines[i].trim()
                    if (!l.startsWith("|")) break
                    if (l.contains("---")) {
                        i++
                        continue
                    }
                    val cells = l.trim('|').split("|").map { it.trim() }
                    if (cells.isNotEmpty()) rows += cells
                    i++
                }
                i--
                if (rows.isNotEmpty()) out += GuideBlock.Table(rows)
            }
            line.startsWith("> ") -> out += GuideBlock.Quote(line.removePrefix("> ").trim())
            line == "---" -> out += GuideBlock.SpacerLine
            else -> out += GuideBlock.Paragraph(line)
        }
        i++
    }
    return out
}

private fun String.stripBold(): String = replace("**", "")
