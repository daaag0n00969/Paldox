package com.paldexpro

import com.paldexpro.domain.breeding.BreedingCalculator
import com.paldexpro.domain.model.EggSize
import com.paldexpro.domain.model.Element
import com.paldexpro.domain.model.Pal
import com.paldexpro.domain.model.Rarity
import com.paldexpro.domain.model.SpecialCombo
import com.paldexpro.domain.model.WorkSuitability
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Test

class BreedingCalculatorTest {

    private val calc = BreedingCalculator()

    private fun pal(
        id: String,
        power: Int,
        index: Int,
        eligible: Boolean = true,
    ) = Pal(
        id = id,
        dexNumber = id,
        nameEn = id,
        nameRu = id,
        element1 = Element.Neutral,
        element2 = null,
        breedingPower = power,
        eligibleChild = eligible,
        indexNo = index,
        rarity = Rarity.common,
        hp = 100,
        attack = 100,
        defense = 100,
        foodAmount = 100,
        eggSize = EggSize.common,
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
    fun childPowerFormula() {
        assertEquals(1000, calc.childPower(1000, 1000))
        assertEquals(750, calc.childPower(500, 999))
        // floor((1470+1460+1)/2) = 1465
        assertEquals(1465, calc.childPower(1470, 1460))
    }

    @Test
    fun sameSpeciesProducesSelf() {
        val a = pal("lamball", 1470, 252)
        val result = calc.predictChild(a, a, listOf(a), emptyList(), emptySet())
        assertNotNull(result)
        assertEquals("lamball", result!!.child.id)
    }

    @Test
    fun specialComboOverridesRank() {
        val mossanda = pal("mossanda", 430, 325)
        val rayhound = pal("rayhound", 740, 328)
        val grizzbolt = pal("grizzbolt", 200, 237, eligible = false)
        val other = pal("filler", 585, 1)
        val combos = listOf(SpecialCombo("mossanda", "rayhound", "grizzbolt"))
        val result = calc.predictChild(
            mossanda, rayhound,
            listOf(mossanda, rayhound, grizzbolt, other),
            combos,
            emptySet(),
        )
        assertNotNull(result)
        assertTrue(result!!.isSpecial)
        assertEquals("grizzbolt", result.child.id)
    }

    @Test
    fun nearestEligibleOnTieUsesLowestIndex() {
        // Parents not eligible as children so they cannot win the tie
        val a = pal("a", 200, 10, eligible = false)
        val b = pal("b", 0, 20, eligible = false)
        // avg power = floor((200+0+1)/2) = 100
        val c1 = pal("c1", 100, 50)
        val c2 = pal("c2", 100, 30)
        val result = calc.predictChild(a, b, listOf(a, b, c1, c2), emptyList(), emptySet())
        assertEquals("c2", result!!.child.id)
    }

    /**
     * Palworld 1.0 ranks: Azurobe(1830) + Bushi(1560) => floor((1830+1560+1)/2)=1695
     * nearest eligible is Carnibora(1700), NOT Anubis(480).
     */
    @Test
    fun azurobeTimesBushiIsCarnibora_1_0() {
        val azurobe = pal("azurobe", 1830, 82)
        val bushi = pal("bushi", 1560, 72)
        val carnibora = pal("carnibora", 1700, 150)
        val anubis = pal("anubis", 480, 100)
        val all = listOf(azurobe, bushi, carnibora, anubis)
        val result = calc.predictChild(azurobe, bushi, all, emptyList(), emptySet())
        assertNotNull(result)
        assertEquals("carnibora", result!!.child.id)
        assertEquals(1695, result.childPower)
    }
}
