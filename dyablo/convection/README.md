# Convection

## Description


## Les tests

### 1. Test de base

Le premier test de base de convection *informations à compléter* &rarr; images disponibles [ici](imgs/001_convection_base/). Cette simulation a été lancée sasn prendre compte de l'échelonnage du domaine physique par rapport à la taille du domaine numérique.

### 2. Equilibre hydrostatique au bord

Auparavant l'équilibre hydrostatique était maintenu au bord en utilisant la pression du gaz sortant du solveur de Riemann de l'interface de la celulle opposée à la bordure. Cela fonctionnait très bien mais nécéssitait des informations non-locales à notre bord, et impliquait un remaniement important du code. Pour contourner ça nous avons décidé de reconstruire les pentes et ainsi les valeurs se trouvant sur cette interface oppossée

|  Date     | Test           | Files|  Commit Hash|
|-----------|----------------|------|-------------|
| 2025-10-27|GLMMHD+RK2|[inifile](20251027_WB_hydro_global/restart_WB_HydroGlobal_1006685.ini) / [output](20251027_WB_hydro_global/)| [fe4a93a1199a55393bd30a6b1a12ce3d95e11591](https://drf-gitlab.cea.fr/dyablo/dyablo/-/commit/fe4a93a1199a55393bd30a6b1a12ce3d95e11591)|
|2025-10-27|GLMMHD+RK2|[inifile](20251027_WB_from_GLMMHDPolicy/last.ini) / [output](20251027_WB_from_GLMMHDPolicy/)| [fe4a93a1199a55393bd30a6b1a12ce3d95e11591](https://drf-gitlab.cea.fr/dyablo/dyablo/-/commit/fe4a93a1199a55393bd30a6b1a12ce3d95e11591)|

1. Objectif : Avoir une base de référence pour la convection avec géométrie longiligne, en utilisant le WB classique et aucun eperturbation.
2. Objectif : Tester la nouvelle implémentation du WB. À noter que la nouvelle implémentation n'est disponible que pour la Policy MHD. Une nouvelle condition initiale a été crée, permettant d'utiliser cett nouvelle implémentation dans le cas hydro mais avec $B_0=0$.

Les résultats montrent que la nouvelle méthode ne garde hélas pas bien l'équilibre hydrostatique (voir [Fig. 1](imgs/002_well_balancing_comparison/01_new_old_WB.png)). On voit que la densité ne maintient pas son profil, notamment sur le haut du domaine. Par ailleurs, le deuxième essai, avec la nouvelle méthode de WB et un champ magnétique initial, montre un résultat similaire (voir [Fig. 2](imgs/002_well_balancing_comparison/02_new_old_and_mhd.png)).

[!WARNING]
> Il est important de garder à l'esprit que les runs 2 et 3 sont fait avec le solveur HLLD, tandis que le premier est avec le HLLC.
> Bien que lorsque $B_0=0$ on s'attende à retrouver le même résultat, on ne peut ici assurer que l'erreur vient uniquement du nouveau WB
> Il faut faire un run avec le HLLD et l'ancien WB, à $B_0=0$ pour être en mesure de comparer les résultats
