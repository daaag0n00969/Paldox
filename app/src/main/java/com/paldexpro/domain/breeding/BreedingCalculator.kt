package com.paldexpro.domain.breeding

import com.paldexpro.domain.model.BreedingChain
import com.paldexpro.domain.model.BreedingChainStep
import com.paldexpro.domain.model.BreedingPair
import com.paldexpro.domain.model.Pal
import com.paldexpro.domain.model.SpecialCombo
import javax.inject.Inject
import javax.inject.Singleton
import kotlin.math.abs

/**
 * Palworld breeding engine (1.0 CombiRank rules).
 *
 * Child rank = floor((parentA + parentB + 1) / 2)
 * Then pick eligible-child species with nearest breedingPower (CombiRank);
 * on tie pick lowest indexNo.
 * Special combos and same-species-only rules override rank result.
 *
 * Breeding ranks in seed_data.json must match Palworld 1.0 tables
 * (e.g. Azurobe 1830 + Bushi 1560 → Carnibora 1700, not legacy Anubis).
 */
@Singleton
class BreedingCalculator @Inject constructor() {

    fun childPower(a: Int, b: Int): Int = (a + b + 1) / 2

    fun predictChild(
        parentA: Pal,
        parentB: Pal,
        allPals: List<Pal>,
        specialCombos: List<SpecialCombo>,
        sameSpeciesOnly: Set<String>,
    ): BreedingPair? {
        // Same species always produces same species
        if (parentA.id == parentB.id) {
            return BreedingPair(parentA, parentB, parentA, isSpecial = false, childPower = parentA.breedingPower)
        }

        // Special combo override (order-independent)
        val special = findSpecial(parentA.id, parentB.id, specialCombos)
        if (special != null) {
            val child = allPals.firstOrNull { it.id == special.child } ?: return null
            return BreedingPair(parentA, parentB, child, isSpecial = true, childPower = child.breedingPower)
        }

        // If either is same-species-only and different species, no rank breed to that species;
        // rank system still runs among eligible children only.
        val power = childPower(parentA.breedingPower, parentB.breedingPower)
        val child = nearestEligible(power, allPals, sameSpeciesOnly) ?: return null
        return BreedingPair(parentA, parentB, child, isSpecial = false, childPower = power)
    }

    fun allOffspringFor(
        parent: Pal,
        allPals: List<Pal>,
        specialCombos: List<SpecialCombo>,
        sameSpeciesOnly: Set<String>,
        ownedOnly: Boolean = false,
        ownedIds: Set<String> = emptySet(),
    ): List<BreedingPair> {
        val partners = allPals.filter { p ->
            if (ownedOnly && p.id !in ownedIds && p.id != parent.id) return@filter false
            true
        }
        return partners.mapNotNull { other ->
            predictChild(parent, other, allPals, specialCombos, sameSpeciesOnly)
        }.distinctBy { "${it.parentB.id}->${it.child.id}" }
            .sortedWith(compareBy({ it.child.breedingPower }, { it.child.indexNo }))
    }

    fun parentPairsFor(
        target: Pal,
        allPals: List<Pal>,
        specialCombos: List<SpecialCombo>,
        sameSpeciesOnly: Set<String>,
        ownedOnly: Boolean = false,
        ownedIds: Set<String> = emptySet(),
        limit: Int = 500,
    ): List<BreedingPair> {
        val results = mutableListOf<BreedingPair>()

        // Same-species
        if (!ownedOnly || target.id in ownedIds) {
            results += BreedingPair(target, target, target, isSpecial = false, childPower = target.breedingPower)
        }

        // Special combos that produce target
        specialCombos.filter { it.child == target.id }.forEach { combo ->
            val a = allPals.firstOrNull { it.id == combo.parentA } ?: return@forEach
            val b = allPals.firstOrNull { it.id == combo.parentB } ?: return@forEach
            if (ownedOnly && (a.id !in ownedIds || b.id !in ownedIds)) return@forEach
            results += BreedingPair(a, b, target, isSpecial = true, childPower = target.breedingPower)
        }

        // Rank-based: if target is not eligible child (except via special), skip rank search
        // for pals that can only come from special/same-species.
        if (target.eligibleChild && target.id !in sameSpeciesOnly) {
            val candidates = allPals.filter { !ownedOnly || it.id in ownedIds }
            val n = candidates.size
            outer@ for (i in 0 until n) {
                for (j in i until n) {
                    val a = candidates[i]
                    val b = candidates[j]
                    val pair = predictChild(a, b, allPals, specialCombos, sameSpeciesOnly)
                    if (pair != null && pair.child.id == target.id && !pair.isSpecial) {
                        results += pair
                        if (results.size >= limit) break@outer
                    }
                }
            }
        }

        return results
            .distinctBy { sortedPairKey(it.parentA.id, it.parentB.id) }
            .sortedWith(
                compareBy(
                    { !it.isSpecial },
                    { abs(it.parentA.breedingPower - it.parentB.breedingPower) },
                    { it.parentA.breedingPower + it.parentB.breedingPower },
                )
            )
    }

    /**
     * Shortest breeding chain from owned pals (or all if none owned) to [targetId].
     * BFS on species graph: edge A+B -> child.
     */
    fun shortestChain(
        targetId: String,
        allPals: List<Pal>,
        specialCombos: List<SpecialCombo>,
        sameSpeciesOnly: Set<String>,
        ownedIds: Set<String>,
        maxDepth: Int = 4,
    ): BreedingChain? {
        val start = if (ownedIds.isNotEmpty()) ownedIds else allPals.map { it.id }.toSet()
        if (targetId in start) {
            return BreedingChain(targetId, emptyList())
        }

        // Precompute: for each possible child, list of parent pairs from available species set growing
        val byId = allPals.associateBy { it.id }
        val obtained = start.toMutableSet()
        val steps = mutableListOf<BreedingChainStep>()
        val parentOf = mutableMapOf<String, BreedingChainStep>()

        repeat(maxDepth) {
            val newly = mutableListOf<BreedingChainStep>()
            val current = obtained.toList()
            for (i in current.indices) {
                for (j in i until current.size) {
                    val a = byId[current[i]] ?: continue
                    val b = byId[current[j]] ?: continue
                    val pair = predictChild(a, b, allPals, specialCombos, sameSpeciesOnly) ?: continue
                    if (pair.child.id in obtained) continue
                    val step = BreedingChainStep(a.id, b.id, pair.child.id, pair.isSpecial)
                    newly += step
                    parentOf.putIfAbsent(pair.child.id, step)
                    if (pair.child.id == targetId) {
                        return reconstruct(targetId, parentOf)
                    }
                }
            }
            if (newly.isEmpty()) return null
            newly.forEach {
                obtained += it.childId
                steps += it
            }
        }
        return parentOf[targetId]?.let { reconstruct(targetId, parentOf) }
    }

    private fun reconstruct(
        targetId: String,
        parentOf: Map<String, BreedingChainStep>,
    ): BreedingChain {
        val path = ArrayDeque<BreedingChainStep>()
        var cur: String? = targetId
        val guard = HashSet<String>()
        while (cur != null && cur !in guard) {
            guard += cur
            val step = parentOf[cur] ?: break
            path.addFirst(step)
            // Prefer reconstructing via parents that themselves needed breeding
            cur = listOf(step.parentAId, step.parentBId).firstOrNull { it in parentOf }
        }
        return BreedingChain(targetId, path.toList())
    }

    private fun nearestEligible(
        power: Int,
        allPals: List<Pal>,
        sameSpeciesOnly: Set<String>,
    ): Pal? {
        val eligible = allPals.filter { it.eligibleChild && it.id !in sameSpeciesOnly }
        if (eligible.isEmpty()) return null
        return eligible.minWith(
            compareBy<Pal> { abs(it.breedingPower - power) }
                .thenBy { it.indexNo }
        )
    }

    private fun findSpecial(a: String, b: String, combos: List<SpecialCombo>): SpecialCombo? {
        return combos.firstOrNull {
            (it.parentA == a && it.parentB == b) || (it.parentA == b && it.parentB == a)
        }
    }

    private fun sortedPairKey(a: String, b: String): String {
        return if (a <= b) "$a|$b" else "$b|$a"
    }
}
