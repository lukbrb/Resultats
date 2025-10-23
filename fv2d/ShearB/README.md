# Cisaillement Magnetique

## Description
Ce test a pour but principal de vérifier comment nous maintenons les condtions aux bords pour un champ magnétique normal. 

Le problème est le suivant ; au temps initial on un fluide maintenu entre deux surfaces solides, avec une densité et ne pression constante (initialisées à $10$ pour chacune des grandeurs.) La vitesse est purement horizontal (selon $x$) et périodique pour commencer. Il y a de plus un champ magnétique vertical $B_0$.
Nous avons pour initialiser l'expérience deux paramètres libres $u_0$ et $B_0$, souvent initialisé à $u_0=1$ et $B_0=10^{-3}$. 

## Les tests

Depuis les premiers tests beaucoup de progrès ont été faits, néanmoins nous voyons toujours quelques oscillations émanants des bords. L'enjeu des expériences suivantes est de vérifier si nous arrivons à annihiler ces ondulations. À noter que la valeur du champ initial $B_0=0.1$ pour mettre en évidence les déviations.

### 1. Schémas

Nous refaison ce test avec `fv2d` car on peut observer les ghosts cells. Notre but est de vérifier si les oscillations que l'on voit au bord en $v_y$ avec Dyablo sont dûes à la reconstruction. 

|  Date     | Test           | Files|  Commit Hash|
|-----------|----------------|------|-------------|
| 2025-10-22| FiveWaves+PCM+RK2|[inifile](PCM_RK2/pcm_rk2.ini) / [output](PCM_RK2/) | [07ebad6ac88f2e576ed4eff62f52c2bbcf541a43](https://github.com/mdelorme/fv2d/commit/07ebad6ac88f2e576ed4eff62f52c2bbcf541a43)|
| 2025-10-22| FiveWaves+PLM+RK2|[inifile](PLM_RK2/plm_rk2.ini) / [output](PLM_RK2/)   |  [07ebad6ac88f2e576ed4eff62f52c2bbcf541a43](https://github.com/mdelorme/fv2d/commit/07ebad6ac88f2e576ed4eff62f52c2bbcf541a43)|
| 2025-10-22| FiveWaves+PCM+Euler| [inifile](PCM_Euler/pcm_euler.ini) / [output](PCM_Euler/)| [07ebad6ac88f2e576ed4eff62f52c2bbcf541a43](https://github.com/mdelorme/fv2d/commit/07ebad6ac88f2e576ed4eff62f52c2bbcf541a43)|

On constate sur la [figure 1](imgs/001_scheme_comparison_Bx.png) que la composante $B_x$ est mal reconstruite à l'interface, notamment pour que $B_x$ s'annule il faudrait que sa valeur dans les cells soient symmétriquement opposées. On observe la même chose pour les vitesses. 
Ce qui semble poser problème dans ce cas est la valeur mise dans les ghosts cells.

### 2. Valeurs des *ghosts cells*


|  Date     | Test           | Files|  Commit Hash|
|-----------|----------------|------|-------------|
| 2025-10-22| FiveWaves+PLM+RK2|[inifile](PLM_RK2_NOFLUX/pcm_rk2.ini) / [output](PLM_RK2_NOFLUX/) | [Difference from reference commit](PLM_RK2_NOFLUX/diff.md)|

Expériences :
1. Résultat sans utiliser la réécriture des flux au bord &rarr; permet de vérifier l'effet de la reconstruction, et le bon remplissage des ghosts cells
