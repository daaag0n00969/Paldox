package com.paldexpro.data.local

import androidx.room.Database
import androidx.room.RoomDatabase
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

@Database(
    entities = [
        PalEntity::class,
        PassiveSkillEntity::class,
        ActiveSkillEntity::class,
        ItemEntity::class,
        BossEntity::class,
        GuideEntity::class,
        SpecialComboEntity::class,
        MetaEntity::class,
    ],
    version = 4,
    exportSchema = false,
)
abstract class PalDatabase : RoomDatabase() {
    abstract fun palDao(): PalDao
    abstract fun skillDao(): SkillDao
    abstract fun itemDao(): ItemDao
    abstract fun bossDao(): BossDao
    abstract fun guideDao(): GuideDao
    abstract fun breedingDao(): BreedingDao
    abstract fun metaDao(): MetaDao
}
