# Magnetoconvection

Premiers tests effectués avec Dyablo


## Description


## Les tests

Le plan de test est le suivant : 

1. On teste dans un premier temps un équilibre hydrostatique avec une reconstruction ad-hoc de la pression opposée, simpliste : `p_opp = p_ref + dx/2 * slope`. Tester avec une frite de magnétoconvection, en mettant dans les deux cas les perturbations à 0.  
    - [X] Avant le changement
    - [X] Après le changement

    Ces runs ont été enregistrés dans la [section convection](../convection#2-equilibre-hydrostatique-au-bord)

2. Modifier la condition au bord
    - [ ] Passer à la policy la valeur de p_opp et l’utiliser à la place du calcul ad-hoc
    - [ ] Refaire les tests 1.1 et 1.2

3. Passer aussi B_opp comme un vecteur et imposer un équilibre magnetohydrostatique au bord
    - [ ] Refaire le test 1.b
    - [ ] Refaire le test 1.c

### 1. Test initial de référence


|  Date     | Test           | Files|  Commit Hash|
|-----------|----------------|------|-------------|
| 2025-10-16| HLLDGLM+RK2[^1]| [inifile](inifiles/restart_mhd_magnetoconvection.ini) / [output](magnetoconvection_base/) |  [2a3bb26b01a9d33f792eca2100a245eddc8832be](https://drf-gitlab.cea.fr/dyablo/dyablo/-/commit/2a3bb26b01a9d33f792eca2100a245eddc8832be) |
| 2025-10-24| HLLDGLM+RK2+WBH|[inifile](inifiles/restart_mhd_magnetoconvection.ini)| [43cac11b4ea51608faa46cf5045ca1844e85cdd7](https://drf-gitlab.cea.fr/dyablo/dyablo/-/commit/43cac11b4ea51608faa46cf5045ca1844e85cdd7)|
|2025-11-04|HLLDGLM+RK2+WBH|[inifile](20251104_WB_hydro_with_mag/restart_WB_Hydro_and_Magneto_1006685.ini) / [output](20251104_WB_hydro_with_mag/)|[4cf43368f90d221836976987b39a9d4a8564be59](https://drf-gitlab.cea.fr/dyablo/dyablo/-/commit/4cf43368f90d221836976987b39a9d4a8564be59)|

[^1]: Ici on utilise également le *Well Balanced au bord*, qui permet de s'assurer que l'équilibre hydrostatique est respecté au bord du domaine.

L'idée pour le deuxième test du 2025-10-24 est de relancer un test de référence, mais avec une faible résolution horizontale afin d'avoir des runs plus rapides.

Images and animation can be found [here](imgs/).