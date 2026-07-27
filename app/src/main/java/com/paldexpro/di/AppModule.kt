package com.paldexpro.di

import android.content.Context
import androidx.room.Room
import com.google.gson.Gson
import com.paldexpro.data.local.PalDatabase
import com.paldexpro.data.local.dao.BreedingDao
import com.paldexpro.data.local.dao.BossDao
import com.paldexpro.data.local.dao.GuideDao
import com.paldexpro.data.local.dao.ItemDao
import com.paldexpro.data.local.dao.MetaDao
import com.paldexpro.data.local.dao.PalDao
import com.paldexpro.data.local.dao.SkillDao
import dagger.Module
import dagger.Provides
import dagger.hilt.InstallIn
import dagger.hilt.android.qualifiers.ApplicationContext
import dagger.hilt.components.SingletonComponent
import javax.inject.Singleton

@Module
@InstallIn(SingletonComponent::class)
object AppModule {

    @Provides
    @Singleton
    fun provideGson(): Gson = Gson()

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): PalDatabase =
        Room.databaseBuilder(context, PalDatabase::class.java, "paldex_pro.db")
            .fallbackToDestructiveMigration()
            .build()

    @Provides fun providePalDao(db: PalDatabase): PalDao = db.palDao()
    @Provides fun provideSkillDao(db: PalDatabase): SkillDao = db.skillDao()
    @Provides fun provideItemDao(db: PalDatabase): ItemDao = db.itemDao()
    @Provides fun provideBossDao(db: PalDatabase): BossDao = db.bossDao()
    @Provides fun provideGuideDao(db: PalDatabase): GuideDao = db.guideDao()
    @Provides fun provideBreedingDao(db: PalDatabase): BreedingDao = db.breedingDao()
    @Provides fun provideMetaDao(db: PalDatabase): MetaDao = db.metaDao()
}
