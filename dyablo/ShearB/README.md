# Cisaillement Magnetique

## Description
Ce test a pour but principal de vérifier comment nous maintenons les condtions aux bords pour un champ magnétiue normal.

Le problème est le suivant ; au temps initial on un fluide maintenu entre deux surfaces solides, avec une densité et ne pression constante (initialisées à $10$ pour chacune des grandeurs.) La vitesse est purement horizontal (selon $x$) et périodique pour commencer. Il y a de plus un champ magnétique vertical $B_0$.
Nous avons pour initialiser l'expérience deux paramètres libres $u_0$ et $B_0$, souvent initialisé à $u_0=1$ et $B_0=10^{-3}$. 

## Les tests

Depuis les premiers tests beaucoup de progrès ont été faits, néanmoins nous voyons toujours quelques oscillations émanants des bords. L'enjeu des expériences suivantes est de vérifier si nous arrivons à annihiler ces ondulations. À noter que la valeur du champ initial $B_0=0.1$ pour mettre en évidence les déviations.

## Expériences
|  Date     | Test           | Files|  Commit Hash|
|-----------|----------------|------|-------------|
| 2025-10-16| FiveWaves+RK2|[inifile](inifiles/fw_RK2_20251016.ini) / [output](FiveWaves_RK2/)   | b0267fd8b152086020756799d2a0ee20f61c9896[^1]|
| 2025-10-16| FiveWaves+MUSCL-Hancock| [inifile](inifiles/fw_MH_20251016.ini) / [output](FiveWaves_hancock/)   |  b0267fd8b152086020756799d2a0ee20f61c9896 |
| 2025-10-16| FiveWaves+Euler| [inifile](inifiles/fw_Euler_20251016.ini) / [output](FiveWaves_Euler/)| b0267fd8b152086020756799d2a0ee20f61c9896|
|2025-10-16| HLLD&divCleaning+RK2|[inifile](inifiles/GLMMHD_RK2_20251016.ini) / [output](HLLD_RK2/)|b0267fd8b152086020756799d2a0ee20f61c9896|

[^1]: Pour les solveurs 5 ondes, il est encore nécessaire de désactiver la correction GLM puis de recompiler. Améliroation à venir...
### 1. Solveur de Riemann

On souhaite vérifier s'il y a une différence entre les solveurs de Riemann
Les configuration sont accessible sur chaque lien (test effectués le 16/10/2025):
- [Cinq Ondes avec RK2](inifiles/fw_RK2_20251016.ini) &rarr; aucune différence notable.
- [Cinq Ondes avec MUSCL-Hancock](inifiles/fw_MH_20251016.ini) &rarr; légères différences avec le schéma RK2.
- [Cinq ondes avec Euler](inifiles/fw_Euler_20251016.ini) &rarr; Davantage similaire au RK2, tout reste très similaire.
- [HLLD + div-cleaning](inifiles/GLMMHD_RK2_20251016.ini) &rarr; utilisé comme référence.

Les différents schémas et solveurs semblent converger vers le même résultat (voir figures [1-3](imgs/001_riemann_solvers_comparison/)) :

### 2. Pression du gaz au bord

Nous voulons maintenant déterminer quelle pression doit-être prise au bord. Nous allons pour cette expérience continuer à utiliser pour référence le HLLD avec le GLM et un intégrateur RK2.
1. Par défaut, la pression est re-calculée comme $$e_{int}^f = e_{int}^i + \frac{1}{2}v^2 + \frac{1}{2}(B_x^2 + B_z^2)$$ où $e_{int}$ est l'énergie interne, et les exposants $i$ et $f$ désignent respectivement les états initiaux et finaux. Ensuite, $p^f = \frac{e_{int}^f}{\gamma - 1}$.
2. Le premier essai va être d'utiliser $p^f = p^i$.
3. La pression du gaz $p_{in}$ comme étant la pression en sortie d'un solveur de Riemann, et non la valeur reconstruite.
