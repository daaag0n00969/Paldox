package com.paldexpro.data.local.entity

import androidx.room.Entity
import androidx.room.PrimaryKey

@Entity(tableName = "pals")
data class PalEntity(
    @PrimaryKey val id: String,
    val dexNumber: String,
    val nameEn: String,
    val nameRu: String,
    val element1: String,
    val element2: String?,
    val breedingPower: Int,
    val eligibleChild: Boolean,
    val indexNo: Int,
    val rarity: String,
    val hp: Int,
    val attack: Int,
    val defense: Int,
    val foodAmount: Int,
    val eggSize: String,
    val workJson: String,
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
    val strongElementsCsv: String = "",
    val weakToElementsCsv: String = "",
    val strongVsPalIdsCsv: String = "",
    val weakToPalIdsCsv: String = "",
    val dropItemIdsCsv: String = "",
    val nightOnly: Boolean,
    val owned: Boolean = false,
    val iconAsset: String = "",
)

@Entity(tableName = "passive_skills")
data class PassiveSkillEntity(
    @PrimaryKey val id: String,
    val nameEn: String,
    val nameRu: String,
    val polarity: String,
    val tier: String,
    val descEn: String,
    val descRu: String,
    val effectsJson: String = "{}",
    val maxRank: Int = 1,
)

@Entity(tableName = "active_skills")
data class ActiveSkillEntity(
    @PrimaryKey val id: String,
    val nameEn: String,
    val nameRu: String,
    val element: String,
    val power: Int,
    val cooldown: Int,
    val descEn: String,
    val descRu: String,
)

@Entity(tableName = "items")
data class ItemEntity(
    @PrimaryKey val id: String,
    val nameEn: String,
    val nameRu: String,
    val category: String,
    val rarity: String = "common",
    val descEn: String,
    val descRu: String,
    val effectsEn: String = "",
    val effectsRu: String = "",
    val recipeJson: String = "[]",
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
)

@Entity(tableName = "bosses")
data class BossEntity(
    @PrimaryKey val id: String,
    val sortOrder: Int,
    val nameEn: String,
    val nameRu: String,
    val locationEn: String,
    val locationRu: String,
    val level: Int,
    val element1: String,
    val element2: String?,
    val strategyEn: String,
    val strategyRu: String,
    val counterPalIds: String,
    val descEn: String = "",
    val descRu: String = "",
    val gearEn: String = "",
    val gearRu: String = "",
    val imagePalId: String = "",
)

@Entity(tableName = "guides")
data class GuideEntity(
    @PrimaryKey val id: String,
    val titleEn: String,
    val titleRu: String,
    val category: String,
    val bodyEn: String,
    val bodyRu: String,
    val userNotes: String = "",
)

@Entity(tableName = "special_combos")
data class SpecialComboEntity(
    @PrimaryKey(autoGenerate = true) val id: Long = 0,
    val parentA: String,
    val parentB: String,
    val child: String,
)

@Entity(tableName = "meta")
data class MetaEntity(
    @PrimaryKey val key: String,
    val value: String,
)
