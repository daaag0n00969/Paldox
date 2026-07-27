package com.paldexpro

import com.paldexpro.domain.model.EggSize
import com.paldexpro.domain.model.Element
import com.paldexpro.domain.model.Pal
import com.paldexpro.domain.model.PassiveSkill
import com.paldexpro.domain.model.Rarity
import com.paldexpro.domain.model.WorkSuitability
import com.paldexpro.domain.stats.StatCalculator
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test

class StatCalculatorTest {
    private val calc = StatCalculator()

    private fun jetragon() = Pal(
        id = "jetragon",
        dexNumber = "111",
        nameEn = "Jetragon",
        nameRu = "Jetragon",
        element1 = Element.Dragon,
        element2 = null,
        breedingPower = 90,
        eligibleChild = false,
        indexNo = 333,
        rarity = Rarity.legendary,
        hp = 110,
        attack = 140,
        defense = 110,
        foodAmount = 550,
        eggSize = EggSize.huge,
        work = WorkSuitability(),
        partnerSkillNameEn = "",
        partnerSkillNameRu = "",
        partnerSkillDescEn = "",
        partnerSkillDescRu = "",
        locationEn = "",
        locationRu = "",
        dropsEn = "",
        dropsRu = "",
        nightOnly = false,
    )

    @Test
    fun jetragonLevel50MinPotential() {
        // talent 0 → 0% potential
        val s = calc.compute(jetragon(), level = 50, talent = 0)
        // wiki table approx min HP 3500, ATK 625, DEF 462
        assertEquals(3500, s.hp)
        assertEquals(625, s.attack)
        assertEquals(462, s.defense)
    }

    @Test
    fun muscleheadBoostsAttack() {
        val base = calc.compute(jetragon(), level = 50, talent = 50)
        val boosted = calc.compute(
            jetragon(),
            level = 50,
            talent = 50,
            passives = listOf(
                PassiveSkill(
                    id = "musclehead",
                    nameEn = "Musclehead",
                    nameRu = "Musclehead",
                    polarity = "positive",
                    tier = "gold",
                    descEn = "",
                    descRu = "",
                    effects = mapOf("attack" to 0.30f, "workSpeed" to -0.50f),
                )
            ),
        )
        assertTrue(boosted.attack > base.attack)
        assertEquals(30f, boosted.attackBonusPercent, 0.01f)
    }
}
