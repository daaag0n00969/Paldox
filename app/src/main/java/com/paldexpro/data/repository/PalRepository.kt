package com.paldexpro.data.repository

import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.paldexpro.data.local.dao.BreedingDao
import com.paldexpro.data.local.dao.BossDao
import com.paldexpro.data.local.dao.GuideDao
import com.paldexpro.data.local.dao.ItemDao
import com.paldexpro.data.local.dao.MetaDao
import com.paldexpro.data.local.dao.PalDao
import com.paldexpro.data.local.dao.SkillDao
import com.paldexpro.data.seed.SeedLoader
import com.paldexpro.domain.breeding.BreedingCalculator
import com.paldexpro.domain.model.ActiveSkill
import com.paldexpro.domain.model.Boss
import com.paldexpro.domain.model.BreedingChain
import com.paldexpro.domain.model.BreedingPair
import com.paldexpro.domain.model.GameItem
import com.paldexpro.domain.model.Guide
import com.paldexpro.domain.model.Pal
import com.paldexpro.domain.model.PassiveSkill
import com.paldexpro.domain.model.SpecialCombo
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.map
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class PalRepository @Inject constructor(
    private val palDao: PalDao,
    private val skillDao: SkillDao,
    private val itemDao: ItemDao,
    private val bossDao: BossDao,
    private val guideDao: GuideDao,
    private val breedingDao: BreedingDao,
    private val metaDao: MetaDao,
    private val seedLoader: SeedLoader,
    private val breedingCalculator: BreedingCalculator,
    private val gson: Gson,
) {
    suspend fun init() = seedLoader.ensureSeeded()

    fun observePals(
        query: String = "",
        element: String = "",
        rarity: String = "",
    ): Flow<List<Pal>> = palDao.search(query, element, rarity).map { list -> list.map { it.toDomain() } }

    fun observePal(id: String): Flow<Pal?> = palDao.observeById(id).map { it?.toDomain() }

    suspend fun getAllPals(): List<Pal> = palDao.getAll().map { it.toDomain() }

    suspend fun getPal(id: String): Pal? = palDao.getById(id)?.toDomain()

    suspend fun setOwned(id: String, owned: Boolean) = palDao.setOwned(id, owned)

    suspend fun getOwnedIds(): Set<String> = palDao.getOwnedIds().toSet()

    fun observePassives(): Flow<List<PassiveSkill>> =
        skillDao.observePassives().map { it.map { e -> e.toDomain() } }

    fun observeActives(): Flow<List<ActiveSkill>> =
        skillDao.observeActives().map { it.map { e -> e.toDomain() } }

    fun observeItems(query: String = "", category: String = ""): Flow<List<GameItem>> =
        itemDao.search(query, category).map { it.map { e -> e.toDomain() } }

    fun observeItem(id: String): Flow<GameItem?> =
        itemDao.observeById(id).map { it?.toDomain() }

    suspend fun getItem(id: String): GameItem? = itemDao.getById(id)?.toDomain()

    fun observeBosses(): Flow<List<Boss>> =
        bossDao.observeAll().map { it.map { e -> e.toDomain() } }

    fun observeBoss(id: String): Flow<Boss?> =
        bossDao.observeById(id).map { it?.toDomain() }

    fun observeGuides(): Flow<List<Guide>> =
        guideDao.observeAll().map { it.map { e -> e.toDomain() } }

    fun observeGuide(id: String): Flow<Guide?> =
        guideDao.observeById(id).map { it?.toDomain() }

    suspend fun updateGuideNotes(id: String, notes: String) =
        guideDao.updateNotes(id, notes)

    suspend fun getSpecialCombos(): List<SpecialCombo> =
        breedingDao.getSpecialCombos().map { it.toDomain() }

    suspend fun getSameSpeciesOnly(): Set<String> {
        val raw = metaDao.get(SeedLoader.META_SAME_SPECIES) ?: return emptySet()
        val type = object : TypeToken<List<String>>() {}.type
        return (gson.fromJson<List<String>>(raw, type) ?: emptyList()).toSet()
    }

    suspend fun gameVersion(): String =
        metaDao.get(SeedLoader.META_GAME_VERSION) ?: "1.0"

    suspend fun predictBreed(parentAId: String, parentBId: String): BreedingPair? {
        val pals = getAllPals()
        val a = pals.firstOrNull { it.id == parentAId } ?: return null
        val b = pals.firstOrNull { it.id == parentBId } ?: return null
        return breedingCalculator.predictChild(a, b, pals, getSpecialCombos(), getSameSpeciesOnly())
    }

    suspend fun offspringFor(
        parentId: String,
        ownedOnly: Boolean,
    ): List<BreedingPair> {
        val pals = getAllPals()
        val parent = pals.firstOrNull { it.id == parentId } ?: return emptyList()
        return breedingCalculator.allOffspringFor(
            parent, pals, getSpecialCombos(), getSameSpeciesOnly(),
            ownedOnly, getOwnedIds(),
        )
    }

    suspend fun parentsFor(
        targetId: String,
        ownedOnly: Boolean,
        limit: Int = 300,
    ): List<BreedingPair> {
        val pals = getAllPals()
        val target = pals.firstOrNull { it.id == targetId } ?: return emptyList()
        return breedingCalculator.parentPairsFor(
            target, pals, getSpecialCombos(), getSameSpeciesOnly(),
            ownedOnly, getOwnedIds(), limit,
        )
    }

    suspend fun shortestChain(targetId: String): BreedingChain? {
        return breedingCalculator.shortestChain(
            targetId, getAllPals(), getSpecialCombos(), getSameSpeciesOnly(), getOwnedIds(),
        )
    }
}
