package com.paldexpro.data.local.dao

import androidx.room.Dao
import androidx.room.Insert
import androidx.room.OnConflictStrategy
import androidx.room.Query
import androidx.room.Update
import com.paldexpro.data.local.entity.ActiveSkillEntity
import com.paldexpro.data.local.entity.BossEntity
import com.paldexpro.data.local.entity.GuideEntity
import com.paldexpro.data.local.entity.ItemEntity
import com.paldexpro.data.local.entity.MetaEntity
import com.paldexpro.data.local.entity.PalEntity
import com.paldexpro.data.local.entity.PassiveSkillEntity
import com.paldexpro.data.local.entity.SpecialComboEntity
import kotlinx.coroutines.flow.Flow

@Dao
interface PalDao {
    @Query("SELECT * FROM pals ORDER BY dexNumber ASC")
    fun observeAll(): Flow<List<PalEntity>>

    @Query("SELECT * FROM pals ORDER BY dexNumber ASC")
    suspend fun getAll(): List<PalEntity>

    @Query("SELECT * FROM pals WHERE id = :id LIMIT 1")
    suspend fun getById(id: String): PalEntity?

    @Query("SELECT * FROM pals WHERE id = :id LIMIT 1")
    fun observeById(id: String): Flow<PalEntity?>

    @Query(
        """
        SELECT * FROM pals WHERE
        (:query = '' OR nameEn LIKE '%' || :query || '%' OR nameRu LIKE '%' || :query || '%' OR dexNumber LIKE '%' || :query || '%')
        AND (:element = '' OR element1 = :element OR element2 = :element)
        AND (:rarity = '' OR rarity = :rarity)
        ORDER BY dexNumber ASC
        """
    )
    fun search(query: String, element: String, rarity: String): Flow<List<PalEntity>>

    @Query("UPDATE pals SET owned = :owned WHERE id = :id")
    suspend fun setOwned(id: String, owned: Boolean)

    @Query("SELECT id FROM pals WHERE owned = 1")
    suspend fun getOwnedIds(): List<String>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<PalEntity>)

    @Query("SELECT COUNT(*) FROM pals")
    suspend fun count(): Int
}

@Dao
interface SkillDao {
    @Query("SELECT * FROM passive_skills ORDER BY tier DESC, nameEn ASC")
    fun observePassives(): Flow<List<PassiveSkillEntity>>

    @Query("SELECT * FROM active_skills ORDER BY power DESC")
    fun observeActives(): Flow<List<ActiveSkillEntity>>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertPassives(items: List<PassiveSkillEntity>)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertActives(items: List<ActiveSkillEntity>)
}

@Dao
interface ItemDao {
    @Query("SELECT * FROM items ORDER BY category, nameEn")
    fun observeAll(): Flow<List<ItemEntity>>

    @Query(
        """
        SELECT * FROM items WHERE
        (:query = '' OR nameEn LIKE '%' || :query || '%' OR nameRu LIKE '%' || :query || '%')
        AND (:category = '' OR category = :category)
        ORDER BY category, nameEn
        """
    )
    fun search(query: String, category: String): Flow<List<ItemEntity>>

    @Query("SELECT * FROM items WHERE id = :id LIMIT 1")
    fun observeById(id: String): Flow<ItemEntity?>

    @Query("SELECT * FROM items WHERE id = :id LIMIT 1")
    suspend fun getById(id: String): ItemEntity?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<ItemEntity>)
}

@Dao
interface BossDao {
    @Query("SELECT * FROM bosses ORDER BY sortOrder ASC")
    fun observeAll(): Flow<List<BossEntity>>

    @Query("SELECT * FROM bosses WHERE id = :id LIMIT 1")
    fun observeById(id: String): Flow<BossEntity?>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<BossEntity>)
}

@Dao
interface GuideDao {
    @Query("SELECT * FROM guides ORDER BY category, titleEn")
    fun observeAll(): Flow<List<GuideEntity>>

    @Query("SELECT * FROM guides WHERE id = :id LIMIT 1")
    fun observeById(id: String): Flow<GuideEntity?>

    @Update
    suspend fun update(guide: GuideEntity)

    @Query("UPDATE guides SET userNotes = :notes WHERE id = :id")
    suspend fun updateNotes(id: String, notes: String)

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertAll(items: List<GuideEntity>)
}

@Dao
interface BreedingDao {
    @Query("SELECT * FROM special_combos")
    suspend fun getSpecialCombos(): List<SpecialComboEntity>

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insertCombos(items: List<SpecialComboEntity>)
}

@Dao
interface MetaDao {
    @Query("SELECT value FROM meta WHERE `key` = :key LIMIT 1")
    suspend fun get(key: String): String?

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun put(meta: MetaEntity)
}
