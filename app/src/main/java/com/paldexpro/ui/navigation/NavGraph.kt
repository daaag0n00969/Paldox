package com.paldexpro.ui.navigation

import androidx.compose.animation.AnimatedContentTransitionScope
import androidx.compose.animation.core.tween
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Egg
import androidx.compose.material.icons.filled.Home
import androidx.compose.material.icons.filled.MoreHoriz
import androidx.compose.material.icons.filled.Pets
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.NavigationBar
import androidx.compose.material3.NavigationBarItem
import androidx.compose.material3.NavigationBarItemDefaults
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.vector.ImageVector
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.sp
import androidx.navigation.NavGraph.Companion.findStartDestination
import androidx.navigation.NavType
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.currentBackStackEntryAsState
import androidx.navigation.compose.rememberNavController
import androidx.navigation.navArgument
import com.paldexpro.R
import com.paldexpro.ui.screens.bosses.BossDetailScreen
import com.paldexpro.ui.screens.bosses.BossesScreen
import com.paldexpro.ui.screens.breeding.BreedingScreen
import com.paldexpro.ui.screens.guides.GuideDetailScreen
import com.paldexpro.ui.screens.guides.GuidesScreen
import com.paldexpro.ui.screens.home.HomeScreen
import com.paldexpro.ui.screens.items.ItemDetailScreen
import com.paldexpro.ui.screens.items.ItemsScreen
import com.paldexpro.ui.screens.map.MapPlaceholderScreen
import com.paldexpro.ui.screens.more.MoreScreen
import com.paldexpro.ui.screens.paldex.PalDetailScreen
import com.paldexpro.ui.screens.paldex.PaldexScreen
import com.paldexpro.ui.screens.settings.AboutScreen
import com.paldexpro.ui.screens.settings.SettingsScreen
import com.paldexpro.ui.screens.skills.SkillsScreen

sealed class Dest(val route: String) {
    data object Home : Dest("home")
    data object Paldex : Dest("paldex")
    data object PalDetail : Dest("pal/{palId}") {
        fun create(id: String) = "pal/$id"
    }
    data object Breeding : Dest("breeding")
    data object More : Dest("more")
    data object Skills : Dest("skills")
    data object Items : Dest("items")
    data object ItemDetail : Dest("item/{itemId}") {
        fun create(id: String) = "item/$id"
    }
    data object Bosses : Dest("bosses")
    data object BossDetail : Dest("boss/{bossId}") {
        fun create(id: String) = "boss/$id"
    }
    data object Guides : Dest("guides")
    data object GuideDetail : Dest("guide/{guideId}") {
        fun create(id: String) = "guide/$id"
    }
    data object Map : Dest("map")
    data object Settings : Dest("settings")
    data object About : Dest("about")
}

private data class Tab(val dest: Dest, val labelRes: Int, val icon: ImageVector)

@Composable
fun PalDexNavHost(
    useRu: Boolean,
    darkTheme: Boolean,
    onToggleLanguage: () -> Unit,
    onToggleTheme: () -> Unit,
) {
    val nav = rememberNavController()
    val backStack by nav.currentBackStackEntryAsState()
    val current = backStack?.destination?.route

    val tabs = listOf(
        Tab(Dest.Home, R.string.nav_home_short, Icons.Default.Home),
        Tab(Dest.Paldex, R.string.nav_paldex_short, Icons.Default.Pets),
        Tab(Dest.Breeding, R.string.nav_breed_short, Icons.Default.Egg),
        Tab(Dest.More, R.string.nav_more_short, Icons.Default.MoreHoriz),
    )

    val showBottomBar = tabs.any { current == it.dest.route }

    fun goTab(route: String) {
        nav.navigate(route) {
            popUpTo(nav.graph.findStartDestination().id) { saveState = true }
            launchSingleTop = true
            restoreState = true
        }
    }

    Scaffold(
        bottomBar = {
            if (showBottomBar) {
                NavigationBar(
                    containerColor = MaterialTheme.colorScheme.surface.copy(alpha = 0.98f),
                ) {
                    tabs.forEach { tab ->
                        val selected = current == tab.dest.route
                        NavigationBarItem(
                            selected = selected,
                            onClick = { goTab(tab.dest.route) },
                            icon = { Icon(tab.icon, contentDescription = stringResource(tab.labelRes)) },
                            label = {
                                Text(
                                    text = stringResource(tab.labelRes),
                                    maxLines = 1,
                                    overflow = TextOverflow.Clip,
                                    softWrap = false,
                                    fontSize = 11.sp,
                                )
                            },
                            alwaysShowLabel = true,
                            colors = NavigationBarItemDefaults.colors(
                                selectedIconColor = MaterialTheme.colorScheme.primary,
                                selectedTextColor = MaterialTheme.colorScheme.primary,
                                indicatorColor = MaterialTheme.colorScheme.primaryContainer.copy(0.55f),
                            ),
                        )
                    }
                }
            }
        }
    ) { padding ->
        val fade = tween<Float>(220)
        NavHost(
            navController = nav,
            startDestination = Dest.Home.route,
            modifier = Modifier.padding(padding),
            enterTransition = {
                fadeIn(fade) + slideIntoContainer(
                    AnimatedContentTransitionScope.SlideDirection.Start,
                    tween(240),
                )
            },
            exitTransition = {
                fadeOut(fade) + slideOutOfContainer(
                    AnimatedContentTransitionScope.SlideDirection.Start,
                    tween(200),
                )
            },
            popEnterTransition = {
                fadeIn(fade) + slideIntoContainer(
                    AnimatedContentTransitionScope.SlideDirection.End,
                    tween(240),
                )
            },
            popExitTransition = {
                fadeOut(fade) + slideOutOfContainer(
                    AnimatedContentTransitionScope.SlideDirection.End,
                    tween(200),
                )
            },
        ) {
            composable(Dest.Home.route) {
                HomeScreen(
                    useRu = useRu,
                    onOpenPaldex = { goTab(Dest.Paldex.route) },
                    onOpenBreeding = { goTab(Dest.Breeding.route) },
                    onOpenSkills = { nav.navigate(Dest.Skills.route) },
                    onOpenItems = { nav.navigate(Dest.Items.route) },
                    onOpenBosses = { nav.navigate(Dest.Bosses.route) },
                    onOpenGuides = { nav.navigate(Dest.Guides.route) },
                    onOpenMap = { nav.navigate(Dest.Map.route) },
                    onOpenSettings = { nav.navigate(Dest.Settings.route) },
                    onOpenPal = { nav.navigate(Dest.PalDetail.create(it)) },
                )
            }
            composable(Dest.Paldex.route) {
                PaldexScreen(
                    useRu = useRu,
                    onPalClick = { nav.navigate(Dest.PalDetail.create(it)) },
                )
            }
            composable(
                Dest.PalDetail.route,
                arguments = listOf(navArgument("palId") { type = NavType.StringType }),
            ) {
                PalDetailScreen(
                    palId = it.arguments?.getString("palId") ?: return@composable,
                    useRu = useRu,
                    onBack = { nav.popBackStack() },
                    onBreed = { goTab(Dest.Breeding.route) },
                )
            }
            composable(Dest.Breeding.route) {
                BreedingScreen(useRu = useRu, onOpenPal = { nav.navigate(Dest.PalDetail.create(it)) })
            }
            composable(Dest.More.route) {
                MoreScreen(
                    onOpenSkills = { nav.navigate(Dest.Skills.route) },
                    onOpenItems = { nav.navigate(Dest.Items.route) },
                    onOpenBosses = { nav.navigate(Dest.Bosses.route) },
                    onOpenGuides = { nav.navigate(Dest.Guides.route) },
                    onOpenMap = { nav.navigate(Dest.Map.route) },
                    onOpenSettings = { nav.navigate(Dest.Settings.route) },
                )
            }
            composable(Dest.Skills.route) {
                SkillsScreen(useRu = useRu, onBack = { nav.popBackStack() })
            }
            composable(Dest.Items.route) {
                ItemsScreen(
                    useRu = useRu,
                    onBack = { nav.popBackStack() },
                    onOpenItem = { nav.navigate(Dest.ItemDetail.create(it)) },
                )
            }
            composable(
                Dest.ItemDetail.route,
                arguments = listOf(navArgument("itemId") { type = NavType.StringType }),
            ) {
                ItemDetailScreen(
                    itemId = it.arguments?.getString("itemId") ?: return@composable,
                    useRu = useRu,
                    onBack = { nav.popBackStack() },
                    onOpenItem = { id -> nav.navigate(Dest.ItemDetail.create(id)) },
                )
            }
            composable(Dest.Bosses.route) {
                BossesScreen(
                    useRu = useRu,
                    onBack = { nav.popBackStack() },
                    onOpenBoss = { nav.navigate(Dest.BossDetail.create(it)) },
                )
            }
            composable(
                Dest.BossDetail.route,
                arguments = listOf(navArgument("bossId") { type = NavType.StringType }),
            ) {
                BossDetailScreen(
                    bossId = it.arguments?.getString("bossId") ?: return@composable,
                    useRu = useRu,
                    onBack = { nav.popBackStack() },
                    onOpenPal = { nav.navigate(Dest.PalDetail.create(it)) },
                )
            }
            composable(Dest.Guides.route) {
                GuidesScreen(
                    useRu = useRu,
                    onBack = { nav.popBackStack() },
                    onOpenGuide = { nav.navigate(Dest.GuideDetail.create(it)) },
                )
            }
            composable(
                Dest.GuideDetail.route,
                arguments = listOf(navArgument("guideId") { type = NavType.StringType }),
            ) {
                GuideDetailScreen(
                    guideId = it.arguments?.getString("guideId") ?: return@composable,
                    useRu = useRu,
                    onBack = { nav.popBackStack() },
                )
            }
            composable(Dest.Map.route) {
                MapPlaceholderScreen(onBack = { nav.popBackStack() })
            }
            composable(Dest.Settings.route) {
                SettingsScreen(
                    useRu = useRu,
                    darkTheme = darkTheme,
                    onBack = { nav.popBackStack() },
                    onToggleLanguage = onToggleLanguage,
                    onToggleTheme = onToggleTheme,
                    onOpenAbout = { nav.navigate(Dest.About.route) },
                )
            }
            composable(Dest.About.route) {
                AboutScreen(onBack = { nav.popBackStack() })
            }
        }
    }
}
