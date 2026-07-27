package com.paldexpro.domain.stats

import com.paldexpro.domain.model.Pal
import com.paldexpro.domain.model.PassiveSkill
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.floor

/**
 * Pal combat stats using community-verified formulas
 * (palworld.wiki.gg / ThePalProfessor-compatible).
 *
 * Species scaling values are stored on [Pal] as hp/attack/defense.
 * Base at level 0: HP 500, Attack 100, Defense 50.
 */
@Singleton
class StatCalculator @Inject constructor() {

    data class ComputedStats(
        val hp: Int,
        val attack: Int,
        val defense: Int,
        val level: Int,
        val potentialPercent: Float,
        val talent: Int,
        val attackBonusPercent: Float,
        val defenseBonusPercent: Float,
        val hpBonusPercent: Float,
        val workSpeedBonusPercent: Float,
        val condenserStars: Int,
        val soulBonusPercent: Float,
    )

    fun potentialFromTalent(talent: Int): Float =
        (talent.coerceIn(0, 100) * 0.3f) / 100f

    fun compute(
        pal: Pal,
        level: Int,
        talent: Int = 50,
        condenserStars: Int = 0,
        soulBonusPercent: Float = 0f,
        passives: List<PassiveSkill> = emptyList(),
        passiveRanks: Map<String, Int> = emptyMap(),
    ): ComputedStats {
        val lv = level.coerceIn(1, 65)
        val pot = potentialFromTalent(talent)
        val bonuses = aggregatePassiveBonuses(passives, passiveRanks)
        val condenser = condenserStars.coerceIn(0, 4) * 0.05f
        val soul = soulBonusPercent.coerceIn(0f, 1.2f)

        val hp = floor(
            floor(500.0 + 5 * lv + pal.hp * 0.5 * lv * (1 + pot)) *
                (1 + bonuses.hp) * (1 + soul) * (1 + condenser)
        ).toInt()

        val attack = floor(
            floor(100.0 + pal.attack * 0.075 * lv * (1 + pot)) *
                (1 + bonuses.attack) * (1 + soul) * (1 + condenser)
        ).toInt()

        // Base defense is 50 (not 100) per wiki formulas with rounding
        val defense = floor(
            floor(50.0 + pal.defense * 0.075 * lv * (1 + pot)) *
                (1 + bonuses.defense) * (1 + soul) * (1 + condenser)
        ).toInt()

        return ComputedStats(
            hp = hp,
            attack = attack,
            defense = defense,
            level = lv,
            potentialPercent = pot * 100f,
            talent = talent.coerceIn(0, 100),
            attackBonusPercent = bonuses.attack * 100f,
            defenseBonusPercent = bonuses.defense * 100f,
            hpBonusPercent = bonuses.hp * 100f,
            workSpeedBonusPercent = bonuses.workSpeed * 100f,
            condenserStars = condenserStars.coerceIn(0, 4),
            soulBonusPercent = soul * 100f,
        )
    }

    private data class Bonuses(
        val hp: Float = 0f,
        val attack: Float = 0f,
        val defense: Float = 0f,
        val workSpeed: Float = 0f,
    )

    private fun aggregatePassiveBonuses(
        passives: List<PassiveSkill>,
        ranks: Map<String, Int>,
    ): Bonuses {
        var hp = 0f
        var atk = 0f
        var def = 0f
        var work = 0f
        for (p in passives) {
            val rank = (ranks[p.id] ?: 1).coerceAtLeast(1)
            val scale = if (p.maxRank > 1) rank.toFloat() else 1f
            val e = p.effects
            hp += (e["hp"] ?: 0f) * scale
            atk += (e["attack"] ?: 0f) * scale
            def += (e["defense"] ?: 0f) * scale
            work += (e["workSpeed"] ?: 0f) * scale
        }
        return Bonuses(hp, atk, def, work)
    }
}
