package com.paldexpro.ui.components

import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
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
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp

/**
 * Lightweight markdown-ish renderer for guide bodies:
 * headings, bullets, numbered lists, simple tables, bold markers, dividers,
 * and interactive [[pal:id]] / [[item:id]] chips.
 */
@OptIn(ExperimentalLayoutApi::class)
@Composable
fun GuideFormattedBody(
    body: String,
    onOpenPal: (String) -> Unit = {},
    onOpenItem: (String) -> Unit = {},
) {
    val blocks = parseGuideBlocks(body)
    Column(Modifier.fillMaxWidth()) {
        blocks.forEach { block ->
            when (block) {
                is GuideBlock.Heading -> {
                    Spacer(Modifier.height(12.dp))
                    Text(
                        block.text,
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
                        block.text,
                        style = MaterialTheme.typography.titleMedium,
                        fontWeight = FontWeight.SemiBold,
                    )
                }
                is GuideBlock.Bullet -> {
                    Row(Modifier.padding(vertical = 3.dp)) {
                        Text("•", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                        Spacer(Modifier.width(8.dp))
                        InlineGuideText(block.text, onOpenPal, onOpenItem)
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
                        InlineGuideText(block.text, onOpenPal, onOpenItem)
                    }
                }
                is GuideBlock.Check -> {
                    Row(Modifier.padding(vertical = 3.dp)) {
                        Text(if (block.done) "☑" else "☐", color = MaterialTheme.colorScheme.secondary)
                        Spacer(Modifier.width(8.dp))
                        InlineGuideText(block.text, onOpenPal, onOpenItem)
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
                                        Text(
                                            cell,
                                            modifier = Modifier.weight(1f),
                                            style = if (index == 0) {
                                                MaterialTheme.typography.labelLarge
                                            } else {
                                                MaterialTheme.typography.bodyMedium
                                            },
                                            fontWeight = if (index == 0) FontWeight.Bold else FontWeight.Normal,
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
                    Text(
                        block.text,
                        modifier = Modifier
                            .fillMaxWidth()
                            .padding(vertical = 6.dp)
                            .background(
                                MaterialTheme.colorScheme.secondaryContainer.copy(0.35f),
                                RoundedCornerShape(8.dp),
                            )
                            .padding(12.dp),
                        style = MaterialTheme.typography.bodyLarge,
                    )
                }
                is GuideBlock.Paragraph -> {
                    InlineGuideText(
                        block.text,
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
    onOpenPal: (String) -> Unit,
    onOpenItem: (String) -> Unit,
    modifier: Modifier = Modifier,
) {
    val parts = splitInteractive(text)
    if (parts.none { it is TextPart.Link }) {
        Text(text.stripBold(), style = MaterialTheme.typography.bodyLarge, modifier = modifier)
        return
    }
    FlowRow(
        modifier = modifier.fillMaxWidth(),
        horizontalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(6.dp),
        verticalArrangement = androidx.compose.foundation.layout.Arrangement.spacedBy(4.dp),
    ) {
        parts.forEach { part ->
            when (part) {
                is TextPart.Plain -> {
                    if (part.text.isNotBlank()) {
                        Text(part.text.stripBold(), style = MaterialTheme.typography.bodyLarge)
                    }
                }
                is TextPart.Link -> {
                    val isPal = part.kind == "pal"
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
                            text = if (isPal) "🐾 ${part.id}" else "📦 ${part.id}",
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

private sealed class TextPart {
    data class Plain(val text: String) : TextPart()
    data class Link(val kind: String, val id: String) : TextPart()
}

private val LINK_RE = Regex("""\[\[(pal|item):([a-zA-Z0-9_]+)\]\]""")

private fun splitInteractive(text: String): List<TextPart> {
    val out = mutableListOf<TextPart>()
    var last = 0
    LINK_RE.findAll(text).forEach { m ->
        if (m.range.first > last) {
            out += TextPart.Plain(text.substring(last, m.range.first))
        }
        out += TextPart.Link(m.groupValues[1], m.groupValues[2])
        last = m.range.last + 1
    }
    if (last < text.length) out += TextPart.Plain(text.substring(last))
    return out
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
        val raw = lines[i]
        val line = raw.trim()
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
                    val cells = l.trim('|').split("|").map { it.trim().stripBold() }
                    if (cells.isNotEmpty()) rows += cells
                    i++
                }
                i--
                if (rows.isNotEmpty()) out += GuideBlock.Table(rows)
            }
            line.startsWith("> ") -> out += GuideBlock.Quote(line.removePrefix("> ").stripBold())
            line == "---" -> out += GuideBlock.SpacerLine
            else -> out += GuideBlock.Paragraph(line)
        }
        i++
    }
    return out
}

private fun String.stripBold(): String = replace("**", "")
