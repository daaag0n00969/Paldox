package com.paldexpro.data.seed

import android.content.Context
import com.google.gson.Gson
import com.paldexpro.data.local.dao.BreedingDao
import com.paldexpro.data.local.dao.BossDao
import com.paldexpro.data.local.dao.GuideDao
import com.paldexpro.data.local.dao.ItemDao
import com.paldexpro.data.local.dao.MetaDao
import com.paldexpro.data.local.dao.PalDao
import com.paldexpro.data.local.dao.SkillDao
import com.paldexpro.data.local.entity.ActiveSkillEntity
import com.paldexpro.data.local.entity.BossEntity
import com.paldexpro.data.local.entity.GuideEntity
import com.paldexpro.data.local.entity.ItemEntity
import com.paldexpro.data.local.entity.MetaEntity
import com.paldexpro.data.local.entity.PalEntity
import com.paldexpro.data.local.entity.PassiveSkillEntity
import com.paldexpro.data.local.entity.SpecialComboEntity
import dagger.hilt.android.qualifiers.ApplicationContext
import javax.inject.Inject
import javax.inject.Singleton

@Singleton
class SeedLoader @Inject constructor(
    @ApplicationContext private val context: Context,
    private val palDao: PalDao,
    private val skillDao: SkillDao,
    private val itemDao: ItemDao,
    private val bossDao: BossDao,
    private val guideDao: GuideDao,
    private val breedingDao: BreedingDao,
    private val metaDao: MetaDao,
    private val gson: Gson,
) {
    companion object {
        const val SEED_ASSET = "seed_data.json"
        const val META_SEED_VERSION = "seed_version"
        const val META_SAME_SPECIES = "same_species_only"
        const val META_GAME_VERSION = "game_version"
    }

    suspend fun ensureSeeded() {
        val assetVersion = peekAssetVersion()
        val dbVersion = metaDao.get(META_SEED_VERSION)?.toIntOrNull() ?: 0
        val count = palDao.count()
        if (count > 0 && dbVersion >= assetVersion) return
        loadFromAssets()
    }

    private fun peekAssetVersion(): Int {
        return try {
            context.assets.open(SEED_ASSET).bufferedReader().use { reader ->
                val text = reader.readText()
                val seed = gson.fromJson(text, SeedFile::class.java)
                seed.version
            }
        } catch (_: Exception) {
            1
        }
    }

    private suspend fun loadFromAssets() {
        val json = context.assets.open(SEED_ASSET).bufferedReader().use { it.readText() }
        val seed = gson.fromJson(json, SeedFile::class.java)

        // Preserve owned flags across re-seed
        val owned = if (palDao.count() > 0) palDao.getOwnedIds().toSet() else emptySet()
        val guideNotes = emptyMap<String, String>() // notes preserved if we re-query; first install empty

        palDao.insertAll(
            seed.pals.map { p ->
                PalEntity(
                    id = p.id,
                    dexNumber = p.dexNumber,
                    nameEn = p.nameEn,
                    nameRu = p.nameRu,
                    element1 = p.element1,
                    element2 = p.element2,
                    breedingPower = p.breedingPower,
                    eligibleChild = p.eligibleChild,
                    indexNo = p.indexNo,
                    rarity = p.rarity,
                    hp = p.hp,
                    attack = p.attack,
                    defense = p.defense,
                    foodAmount = p.foodAmount,
                    eggSize = p.eggSize,
                    workJson = gson.toJson(p.workSuitability),
                    partnerSkillNameEn = p.partnerSkillNameEn,
                    partnerSkillNameRu = p.partnerSkillNameRu,
                    partnerSkillDescEn = p.partnerSkillDescEn,
                    partnerSkillDescRu = p.partnerSkillDescRu,
                    locationEn = p.locationEn,
                    locationRu = p.locationRu,
                    dropsEn = p.dropsEn,
                    dropsRu = p.dropsRu,
                    nightOnly = p.nightOnly,
                    owned = p.id in owned,
                    iconAsset = p.icon ?: "pals/${p.id}.webp",
                )
            }
        )

        skillDao.insertPassives(
            seed.passives.map {
                PassiveSkillEntity(
                    id = it.id,
                    nameEn = it.nameEn,
                    nameRu = it.nameRu,
                    polarity = it.polarity,
                    tier = it.tier,
                    descEn = it.descEn,
                    descRu = it.descRu,
                    effectsJson = gson.toJson(it.effects),
                    maxRank = it.maxRank.coerceAtLeast(1),
                )
            }
        )
        skillDao.insertActives(
            seed.actives.map {
                ActiveSkillEntity(it.id, it.nameEn, it.nameRu, it.element, it.power, it.cooldown, it.descEn, it.descRu)
            }
        )
        itemDao.insertAll(
            seed.items.map {
                ItemEntity(
                    id = it.id,
                    nameEn = it.nameEn,
                    nameRu = it.nameRu,
                    category = it.category,
                    rarity = it.rarity,
                    descEn = it.descEn,
                    descRu = it.descRu,
                    effectsEn = it.effectsEn,
                    effectsRu = it.effectsRu,
                    recipeJson = gson.toJson(it.recipe),
                    craftStationEn = it.craftStationEn,
                    craftStationRu = it.craftStationRu,
                    techLevel = it.techLevel,
                    dropsEn = it.dropsEn,
                    dropsRu = it.dropsRu,
                    buyEn = it.buyEn,
                    buyRu = it.buyRu,
                    usesEn = it.usesEn,
                    usesRu = it.usesRu,
                    iconAsset = it.icon ?: "items/${it.id}.webp",
                )
            }
        )
        bossDao.insertAll(
            seed.bosses.map {
                BossEntity(
                    id = it.id,
                    sortOrder = it.order,
                    nameEn = it.nameEn,
                    nameRu = it.nameRu,
                    locationEn = it.locationEn,
                    locationRu = it.locationRu,
                    level = it.level,
                    element1 = it.element1,
                    element2 = it.element2,
                    strategyEn = it.strategyEn,
                    strategyRu = it.strategyRu,
                    counterPalIds = it.counterPalIds,
                    descEn = it.descEn,
                    descRu = it.descRu,
                    gearEn = it.gearEn,
                    gearRu = it.gearRu,
                    imagePalId = it.imagePalId,
                )
            }
        )
        guideDao.insertAll(
            seed.guides.map {
                GuideEntity(
                    id = it.id,
                    titleEn = it.titleEn,
                    titleRu = it.titleRu,
                    category = it.category,
                    bodyEn = it.bodyEn,
                    bodyRu = it.bodyRu,
                    userNotes = guideNotes[it.id].orEmpty(),
                )
            }
        )
        breedingDao.insertCombos(
            seed.specialCombos.map {
                SpecialComboEntity(parentA = it.parentA, parentB = it.parentB, child = it.child)
            }
        )

        metaDao.put(MetaEntity(META_SEED_VERSION, seed.version.toString()))
        metaDao.put(MetaEntity(META_GAME_VERSION, seed.gameVersion))
        metaDao.put(MetaEntity(META_SAME_SPECIES, gson.toJson(seed.sameSpeciesOnly)))
    }
}
