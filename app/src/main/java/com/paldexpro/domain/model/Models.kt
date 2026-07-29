package com.paldexpro.domain.model

enum class Element {
    Neutral, Fire, Water, Grass, Electric, Ice, Ground, Dark, Dragon;

    companion object {
        fun from(value: String?): Element? =
            entries.firstOrNull { it.name.equals(value, ignoreCase = true) }
    }
}

enum class Rarity { common, uncommon, rare, epic, legendary }

enum class EggSize { common, large, huge }

enum class WorkType {
    kindling, watering, planting, generating_electricity, handiwork,
    gathering, lumbering, mining, medicine, cooling, transporting, farming
}

data class WorkSuitability(
    val levels: Map<WorkType, Int> = emptyMap()
) {
    fun level(type: WorkType): Int = levels[type] ?: 0
    fun hasAny(): Boolean = levels.values.any { it > 0 }
}

data class Pal(
    val id: String,
    val dexNumber: String,
    val nameEn: String,
    val nameRu: String,
    val element1: Element,
    val element2: Element?,
    val breedingPower: Int,
    val eligibleChild: Boolean,
    val indexNo: Int,
    val rarity: Rarity,
    val hp: Int,
    val attack: Int,
    val defense: Int,
    val foodAmount: Int,
    val eggSize: EggSize,
    val work: WorkSuitability,
    val partnerSkillNameEn: String,
    val partnerSkillNameRu: String,
    val partnerSkillDescEn: String,
    val partnerSkillDescRu: String,
    val locationEn: String,
    val locationRu: String,
    val dropsEn: String,
    val dropsRu: String,
    val matchupEn: String = "",
    val matchupRu: String = "",
    val nightOnly: Boolean,
    val owned: Boolean = false,
    val iconAsset: String = "",
) {
    fun displayName(ru: Boolean): String = if (ru) nameRu else nameEn
    fun location(ru: Boolean): String = if (ru) locationRu else locationEn
    fun partnerSkillName(ru: Boolean): String = if (ru) partnerSkillNameRu else partnerSkillNameEn
    fun partnerSkillDesc(ru: Boolean): String = if (ru) partnerSkillDescRu else partnerSkillDescEn
    fun drops(ru: Boolean): String = if (ru) dropsRu else dropsEn
    fun matchup(ru: Boolean): String = if (ru) matchupRu else matchupEn
    fun elements(): List<Element> = listOfNotNull(element1, element2)
    fun iconPath(): String = iconAsset.ifBlank { "pals/$id.webp" }
}

data class PassiveSkill(
    val id: String,
    val nameEn: String,
    val nameRu: String,
    val polarity: String,
    val tier: String,
    val descEn: String,
    val descRu: String,
    val effects: Map<String, Float> = emptyMap(),
    val maxRank: Int = 1,
) {
    fun displayName(ru: Boolean) = if (ru) nameRu else nameEn
    fun desc(ru: Boolean) = if (ru) descRu else descEn
    val isPositive: Boolean get() = polarity == "positive"
    val rarityOrder: Int
        get() = when (tier.lowercase()) {
            "legendary" -> 4
            "gold" -> 3
            "blue" -> 2
            "green" -> 1
            else -> 0
        }

    fun effectAtRank(rank: Int): Map<String, Float> {
        val r = rank.coerceIn(1, maxRank.coerceAtLeast(1))
        val scale = if (maxRank > 1) r.toFloat() else 1f
        return effects.mapValues { it.value * scale }
    }
}

data class ActiveSkill(
    val id: String,
    val nameEn: String,
    val nameRu: String,
    val element: Element,
    val power: Int,
    val cooldown: Int,
    val descEn: String,
    val descRu: String,
) {
    fun displayName(ru: Boolean) = if (ru) nameRu else nameEn
    fun desc(ru: Boolean) = if (ru) descRu else descEn
}

data class CraftIngredient(
    val itemId: String,
    val qty: Int,
)

data class GameItem(
    val id: String,
    val nameEn: String,
    val nameRu: String,
    val category: String,
    val rarity: Rarity,
    val descEn: String,
    val descRu: String,
    val effectsEn: String = "",
    val effectsRu: String = "",
    val recipe: List<CraftIngredient> = emptyList(),
    val craftStationEn: String = "",
    val craftStationRu: String = "",
    val techLevel: Int = 0,
    val dropsEn: String = "",
    val dropsRu: String = "",
    val buyEn: String = "",
    val buyRu: String = "",
    val usesEn: String = "",
    val usesRu: String = "",
    val iconAsset: String = "",
) {
    fun displayName(ru: Boolean) = if (ru) nameRu else nameEn
    fun desc(ru: Boolean) = if (ru) descRu else descEn
    fun effects(ru: Boolean) = if (ru) effectsRu else effectsEn
    fun craftStation(ru: Boolean) = if (ru) craftStationRu else craftStationEn
    fun drops(ru: Boolean) = if (ru) dropsRu else dropsEn
    fun buy(ru: Boolean) = if (ru) buyRu else buyEn
    fun uses(ru: Boolean) = if (ru) usesRu else usesEn
    fun iconPath(): String = iconAsset.ifBlank { "items/$id.webp" }
}

data class Boss(
    val order: Int,
    val id: String,
    val nameEn: String,
    val nameRu: String,
    val locationEn: String,
    val locationRu: String,
    val level: Int,
    val element1: Element,
    val element2: Element?,
    val strategyEn: String,
    val strategyRu: String,
    val counterPalIds: List<String>,
    val descEn: String = "",
    val descRu: String = "",
    val gearEn: String = "",
    val gearRu: String = "",
    val imagePalId: String = "",
) {
    fun displayName(ru: Boolean) = if (ru) nameRu else nameEn
    fun location(ru: Boolean) = if (ru) locationRu else locationEn
    fun strategy(ru: Boolean) = if (ru) strategyRu else strategyEn
    fun desc(ru: Boolean) = if (ru) descRu else descEn
    fun gear(ru: Boolean) = if (ru) gearRu else gearEn
    fun elements(): List<Element> = listOfNotNull(element1, element2)
    fun imageAsset(): String {
        val pid = imagePalId.ifBlank {
            counterPalIds.firstOrNull().orEmpty()
        }
        return if (pid.isNotBlank()) "pals/$pid.webp" else ""
    }
}

data class Guide(
    val id: String,
    val titleEn: String,
    val titleRu: String,
    val category: String,
    val bodyEn: String,
    val bodyRu: String,
    val userNotes: String = "",
) {
    fun title(ru: Boolean) = if (ru) titleRu else titleEn
    fun body(ru: Boolean) = if (ru) bodyRu else bodyEn

    /** Plain-text preview for list rows (no markdown symbols). */
    fun preview(ru: Boolean, maxLen: Int = 120): String {
        val plain = stripMarkdown(body(ru))
        return if (plain.length <= maxLen) plain else plain.take(maxLen).trimEnd() + "…"
    }

    companion object {
        fun stripMarkdown(text: String): String {
            return text
                .replace("\r\n", "\n")
                .lineSequence()
                .map { line ->
                    line.trim()
                        .removePrefix("## ").removePrefix("### ")
                        .removePrefix("- [ ] ").removePrefix("- [x] ").removePrefix("- [X] ")
                        .removePrefix("- ").removePrefix("* ").removePrefix("> ")
                        .replace(Regex("^\\d+\\.\\s+"), "")
                        .replace("**", "")
                        .replace("|", " ")
                        .replace("---", "")
                        .replace(Regex("\\s+"), " ")
                        .trim()
                }
                .filter { it.isNotBlank() }
                .joinToString(" ")
        }
    }
}

data class SpecialCombo(
    val parentA: String,
    val parentB: String,
    val child: String,
)

data class BreedingPair(
    val parentA: Pal,
    val parentB: Pal,
    val child: Pal,
    val isSpecial: Boolean,
    val childPower: Int,
)

data class BreedingChainStep(
    val parentAId: String,
    val parentBId: String,
    val childId: String,
    val isSpecial: Boolean,
)

data class BreedingChain(
    val targetId: String,
    val steps: List<BreedingChainStep>,
)
