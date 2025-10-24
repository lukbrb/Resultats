# Magnetoconvection

Premiers tests effectués avec Dyablo


## Description


## Les tests

Le plan de test est le suivant : 

1. On teste dans un premier temps un équilibre hydrostatique avec une reconstruction ad-hoc de la pression opposée, simpliste : `p_opp = p_ref + dx/2 * slope`. Tester avec une frite de magnétoconvection, en mettant dans les deux cas les perturbations à 0.  
    - [ ] Avant le changement
    - [ ] Après le changement

2. Modifier la condition au bord
    - [ ] Passer à la policy la valeur de p_opp et l’utiliser à la place du calcul ad-hoc
    - [ ] Refaire les tests 1.1 et 1.2

3. Passer aussi B_opp comme un vecteur et imposer un équilibre magnetohydrostatique au bord
    - [ ] Refaire le test 1.b
    - [ ] Refaire le test 1.c

### 1. Test initial de référence


|  Date     | Test           | Files|  Commit Hash|
|-----------|----------------|------|-------------|
| 2025-10-16| HLLDGLM+RK2[^1]| [inifile](inifiles/restart_mhd_magnetoconvection.ini) / No output file yet   |  [2a3bb26b01a9d33f792eca2100a245eddc8832be](https://drf-gitlab.cea.fr/dyablo/dyablo/-/tree/2a3bb26b01a9d33f792eca2100a245eddc8832be) |
| 2025-10-24| HLLDGLM+RK2+WBH|[inifile]()
[^1]: Ici on utilise également le *Well Balanced au bord*, qui permet de s'assurer que l'équilibre hydrostatique est respecté au bord du domaine.

Images and animation can be found [here](imgs/).