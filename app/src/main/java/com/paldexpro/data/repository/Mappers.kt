package com.paldexpro.data.repository

import com.google.gson.Gson
import com.google.gson.reflect.TypeToken
import com.paldexpro.data.local.entity.ActiveSkillEntity
import com.paldexpro.data.local.entity.BossEntity
import com.paldexpro.data.local.entity.GuideEntity
import com.paldexpro.data.local.entity.ItemEntity
import com.paldexpro.data.local.entity.PalEntity
import com.paldexpro.data.local.entity.PassiveSkillEntity
import com.paldexpro.data.local.entity.SpecialComboEntity
import com.paldexpro.domain.model.ActiveSkill
import com.paldexpro.domain.model.Boss
import com.paldexpro.domain.model.CraftIngredient
import com.paldexpro.domain.model.EggSize
import com.paldexpro.domain.model.Element
import com.paldexpro.domain.model.GameItem
import com.paldexpro.domain.model.Guide
import com.paldexpro.domain.model.Pal
import com.paldexpro.domain.model.PassiveSkill
import com.paldexpro.domain.model.Rarity
import com.paldexpro.domain.model.SpecialCombo
import com.paldexpro.domain.model.WorkSuitability
import com.paldexpro.domain.model.WorkType

private val gson = Gson()
private val mapType = object : TypeToken<Map<String, Int>>() {}.type

fun PalEntity.toDomain(): Pal {
    val workMap: Map<String, Int> = try {
        gson.fromJson(workJson, mapType) ?: emptyMap()
    } catch (_: Exception) {
        emptyMap()
    }
    val levels = workMap.mapNotNull { (k, v) ->
        runCatching { WorkType.valueOf(k) to v }.getOrNull()
    }.toMap()
    return Pal(
        id = id,
        dexNumber = dexNumber,
        nameEn = nameEn,
        nameRu = nameRu,
        element1 = Element.from(element1) ?: Element.Neutral,
        element2 = Element.from(element2),
        breedingPower = breedingPower,
        eligibleChild = eligibleChild,
        indexNo = indexNo,
        rarity = runCatching { Rarity.valueOf(rarity) }.getOrDefault(Rarity.common),
        hp = hp,
        attack = attack,
        defense = defense,
        foodAmount = foodAmount,
        eggSize = runCatching { EggSize.valueOf(eggSize) }.getOrDefault(EggSize.common),
        work = WorkSuitability(levels),
        partnerSkillNameEn = partnerSkillNameEn,
        partnerSkillNameRu = partnerSkillNameRu,
        partnerSkillDescEn = partnerSkillDescEn,
        partnerSkillDescRu = partnerSkillDescRu,
        locationEn = locationEn,
        locationRu = locationRu,
        dropsEn = dropsEn,
        dropsRu = dropsRu,
        matchupEn = matchupEn,
        matchupRu = matchupRu,
        nightOnly = nightOnly,
        owned = owned,
        iconAsset = iconAsset.ifBlank { "pals/$id.webp" },
    )
}

fun PassiveSkillEntity.toDomain(): PassiveSkill {
    val effects: Map<String, Float> = try {
        val raw: Map<String, Double> = gson.fromJson(effectsJson, object : TypeToken<Map<String, Double>>() {}.type)
            ?: emptyMap()
        raw.mapValues { it.value.toFloat() }
    } catch (_: Exception) {
        emptyMap()
    }
    return PassiveSkill(id, nameEn, nameRu, polarity, tier, descEn, descRu, effects, maxRank.coerceAtLeast(1))
}

fun ActiveSkillEntity.toDomain() = ActiveSkill(
    id, nameEn, nameRu,
    Element.from(element) ?: Element.Neutral,
    power, cooldown, descEn, descRu,
)

fun ItemEntity.toDomain(): GameItem {
    val recipe: List<CraftIngredient> = try {
        val raw: List<Map<String, Any>> = gson.fromJson(
            recipeJson,
            object : TypeToken<List<Map<String, Any>>>() {}.type,
        ) ?: emptyList()
        raw.mapNotNull { m ->
            val id = m["itemId"]?.toString() ?: return@mapNotNull null
            val qty = (m["qty"] as? Number)?.toInt() ?: 1
            CraftIngredient(id, qty)
        }
    } catch (_: Exception) {
        emptyList()
    }
    return GameItem(
        id = id,
        nameEn = nameEn,
        nameRu = nameRu,
        category = category,
        rarity = runCatching { Rarity.valueOf(rarity) }.getOrDefault(Rarity.common),
        descEn = descEn,
        descRu = descRu,
        effectsEn = effectsEn,
        effectsRu = effectsRu,
        recipe = recipe,
        craftStationEn = craftStationEn,
        craftStationRu = craftStationRu,
        techLevel = techLevel,
        dropsEn = dropsEn,
        dropsRu = dropsRu,
        buyEn = buyEn,
        buyRu = buyRu,
        usesEn = usesEn,
        usesRu = usesRu,
        iconAsset = iconAsset.ifBlank { "items/$id.webp" },
    )
}

fun BossEntity.toDomain() = Boss(
    order = sortOrder,
    id = id,
    nameEn = nameEn,
    nameRu = nameRu,
    locationEn = locationEn,
    locationRu = locationRu,
    level = level,
    element1 = Element.from(element1) ?: Element.Neutral,
    element2 = Element.from(element2),
    strategyEn = strategyEn,
    strategyRu = strategyRu,
    counterPalIds = counterPalIds.split(",").map { it.trim() }.filter { it.isNotEmpty() },
    descEn = descEn,
    descRu = descRu,
    gearEn = gearEn,
    gearRu = gearRu,
    imagePalId = imagePalId,
)

fun GuideEntity.toDomain() = Guide(id, titleEn, titleRu, category, bodyEn, bodyRu, userNotes)

fun SpecialComboEntity.toDomain() = SpecialCombo(parentA, parentB, child)
