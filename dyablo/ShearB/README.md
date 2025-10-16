# Cisaillement Magnetique

## Description
Ce test a pour but principal de vérifier comment nous maintenons les condtions aux bords pour un champ magnétiue normal.

Le problème est le suivant ; au temps initial on un fluide maintenu entre deux surfaces solides, avec une densité et ne pression constante (initialisées à $10$ pour chacune des grandeurs.) La vitesse est purement horizontal (selon $x$) et périodique pour commencer. Il y a de plus un champ magnétique vertical $B_0$.
Nous avons pour initialiser l'expérience deux paramètres libres $u_0$ et $B_0$, souvent initialisé à $u_0=1$ et $B_0=10^{-3}$. 

## Les tests

Depuis les premiers tests beaucoup de progrès ont été faits, néanmoins nous voyons toujours quelques oscillations émanants des bords. L'enjeu des expériences suivantes est de vérifier si nous arrivons à annihiler ces ondulations. À noter que la valeur du champ initial $B_0=0.1$ pour mettre en évidence les déviations.

### 1. Solveur de Riemann


|  Date     | Test           | Files|  Commit Hash|
|-----------|----------------|------|-------------|
| 2025-10-16| FiveWaves+RK2|[inifile](inifiles/fw_RK2_20251016.ini) / [output](FiveWaves_RK2/)   | b0267fd8b152086020756799d2a0ee20f61c9896[^1]|
| 2025-10-16| FiveWaves+MUSCL-Hancock| [inifile](inifiles/fw_MH_20251016.ini) / [output](FiveWaves_hancock/)   |  b0267fd8b152086020756799d2a0ee20f61c9896 |
| 2025-10-16| FiveWaves+Euler| [inifile](inifiles/fw_Euler_20251016.ini) / [output](FiveWaves_Euler/)| b0267fd8b152086020756799d2a0ee20f61c9896|
|2025-10-16| HLLD&divCleaning+RK2|[inifile](inifiles/GLMMHD_RK2_20251016.ini) / [output](HLLD_RK2/)|b0267fd8b152086020756799d2a0ee20f61c9896|

[^1]: Pour les solveurs 5 ondes, il est encore nécessaire de désactiver la correction GLM puis de recompiler. Améliroation à venir...

On souhaite vérifier s'il y a une différence entre les solveurs de Riemann
Les configuration sont accessible sur chaque lien (test effectués le 16/10/2025):
- [Cinq Ondes avec RK2](inifiles/fw_RK2_20251016.ini) &rarr; aucune différence notable.
- [Cinq Ondes avec MUSCL-Hancock](inifiles/fw_MH_20251016.ini) &rarr; légères différences avec le schéma RK2.
- [Cinq ondes avec Euler](inifiles/fw_Euler_20251016.ini) &rarr; Davantage similaire au RK2, tout reste très similaire.
- [HLLD + div-cleaning](inifiles/GLMMHD_RK2_20251016.ini) &rarr; utilisé comme référence.

Les différents schémas et solveurs semblent converger vers le même résultat (voir figures [1.1-1.3](imgs/001_riemann_solvers_comparison/)) :

### 2. Pression du gaz au bord


|  Date     | Test           | Files|  Commit Hash|
|-----------|----------------|------|-------------|
|2025-10-16| HLLD&divCleaning+RK2|[inifile](inifiles/GLMMHD_RK2_20251016.ini) / [output](HLLD_RK2/)|b0267fd8b152086020756799d2a0ee20f61c9896|
| 2025-10-16| HLLD&divCleaning+R2|[inifile](inifiles/GLMMHD_RK2_20251016.ini) / [output](EqualPressure/)   | 579227f8dd6bcd55b62e69b9879e914d1ee9ace2|
|2025-10-16| HLLD&divCleaning+RK2|[inifile](inifiles/GLMMHD_RK2_20251016.ini) / [output](RecomputedPfinal/)|628bb549520dd62c6b4fbae0aa67242ea12c6a29|

Nous voulons maintenant déterminer quelle pression doit-être prise au bord. Pour cette expérience nous continuons à utiliser pour référence le HLLD avec le GLM, pour contrôler la dovergence, et un intégrateur RK2.

1. Par défaut, la pression est re-calculée comme $$e^{int}_f = e^{int}_i + \frac{1}{2}v^2 + \frac{1}{2}(B_x^2 + B_z^2)$$ où $e^{int}$ est l'énergie interne, et les indices $i$ et $f$ désignent respectivement les états initiaux et finaux. Ensuite, $p_f = \frac{e^{int}_f}{\gamma - 1}$.

2. Le premier essai va être d'utiliser $p_f = p_i$. 
Étonnement, cela ne fait aucune différence, peut-être que la manière de calculer $p_f$ présentée ci-dessus est mal implémentée dans le code, et revient juste à faire $p_f=p_i$.

3. Finalement, on a réessayé en utilisant directement  $$p_f = p_i + \frac{1}{\gamma - 1} \left[(E_c^i - E_c^f) + (E_m^i - E_m^f)\right]$$
Là encore aucune différence notable. À noter que dans notre cas cette égalité se réduit à $$ p_f = p_i + \frac{1}{\gamma-1}\left[\frac{1}{2}v_i^2 + \frac{1}{2}(B_x^2 + B_z^2)_i\right]$$ où au bord $v_i\sim 10^{-3}$, $B_z=0$ et $B_x \sim 0$. Donc en effet ça donne $p_f \sim p_i$. Peut-être augmenter $B_0$ ou $u_0$ pour augmenter les valeurs des grandeurs considérées au-dessus.

4. La pression du gaz $p_{in}$ comme étant la pression en sortie d'un solveur de Riemann, et non la valeur reconstruite.

Les résultats sont visibles sur les figures ([2.1-2.2](imgs/002_pressure_comparison/)).