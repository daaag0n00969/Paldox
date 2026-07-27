package com.paldexpro.data.seed

data class SeedFile(
    val version: Int = 1,
    val gameVersion: String = "1.0",
    val pals: List<SeedPal> = emptyList(),
    val passives: List<SeedPassive> = emptyList(),
    val actives: List<SeedActive> = emptyList(),
    val items: List<SeedItem> = emptyList(),
    val bosses: List<SeedBoss> = emptyList(),
    val guides: List<SeedGuide> = emptyList(),
    val specialCombos: List<SeedCombo> = emptyList(),
    val sameSpeciesOnly: List<String> = emptyList(),
)

data class SeedPal(
    val id: String,
    val dexNumber: String,
    val nameEn: String,
    val nameRu: String,
    val element1: String,
    val element2: String? = null,
    val breedingPower: Int,
    val eligibleChild: Boolean,
    val indexNo: Int,
    val rarity: String,
    val hp: Int,
    val attack: Int,
    val defense: Int,
    val foodAmount: Int,
    val eggSize: String,
    val workSuitability: Map<String, Int> = emptyMap(),
    val partnerSkillId: String? = null,
    val partnerSkillNameEn: String = "",
    val partnerSkillNameRu: String = "",
    val partnerSkillDescEn: String = "",
    val partnerSkillDescRu: String = "",
    val locationEn: String = "",
    val locationRu: String = "",
    val dropsEn: String = "",
    val dropsRu: String = "",
    val nightOnly: Boolean = false,
    val icon: String? = null,
)

data class SeedPassive(
    val id: String,
    val nameEn: String,
    val nameRu: String,
    val polarity: String,
    val tier: String,
    val descEn: String,
    val descRu: String,
    val effects: Map<String, Double> = emptyMap(),
    val maxRank: Int = 1,
)

data class SeedActive(
    val id: String,
    val nameEn: String,
    val nameRu: String,
    val element: String,
    val power: Int,
    val cooldown: Int,
    val descEn: String,
    val descRu: String,
)

data class SeedRecipePart(
    val itemId: String = "",
    val qty: Int = 1,
)

data class SeedItem(
    val id: String,
    val nameEn: String,
    val nameRu: String,
    val category: String,
    val rarity: String = "common",
    val descEn: String,
    val descRu: String,
    val effectsEn: String = "",
    val effectsRu: String = "",
    val recipe: List<SeedRecipePart> = emptyList(),
    val craftStationEn: String = "",
    val craftStationRu: String = "",
    val techLevel: Int = 0,
    val dropsEn: String = "",
    val dropsRu: String = "",
    val buyEn: String = "",
    val buyRu: String = "",
    val usesEn: String = "",
    val usesRu: String = "",
    val icon: String? = null,
)

data class SeedBoss(
    val order: Int,
    val id: String,
    val nameEn: String,
    val nameRu: String,
    val locationEn: String,
    val locationRu: String,
    val level: Int,
    val element1: String,
    val element2: String? = null,
    val strategyEn: String,
    val strategyRu: String,
    val counterPalIds: String,
    val descEn: String = "",
    val descRu: String = "",
    val gearEn: String = "",
    val gearRu: String = "",
    val imagePalId: String = "",
)

data class SeedGuide(
    val id: String,
    val titleEn: String,
    val titleRu: String,
    val category: String,
    val bodyEn: String,
    val bodyRu: String,
)

data class SeedCombo(
    val parentA: String,
    val parentB: String,
    val child: String,
)
