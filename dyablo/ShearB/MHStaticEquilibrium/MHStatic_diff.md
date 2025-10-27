# Git Diff MHStatic Run

## Informations

- **Date :** 27/10/2025 
- **Reference Commit** : [747aabe5cf862ebf9aaefcfdd7ca12d8bcd254e1](https://drf-gitlab.cea.fr/dyablo/dyablo/-/tree/747aabe5cf862ebf9aaefcfdd7ca12d8bcd254e1)

## Modifications

Les modification sont été faites dans le but de créer un équilibre magnéto-hydrostatique. Des améliorations doivent être faites pour mieux combiner ça aux conditions magnétiques.

**Fichier** `/core/src/hyperbolic/policy/HyperbolicPolicy_GLMMHD.h`
```diff
diff --git a/core/src/hyperbolic/policy/HyperbolicPolicy_GLMMHD.h b/core/src/hyperbolic/policy/HyperbolicPolicy_GLMMHD.h
index c7149c38..c19dda60 100644
--- a/core/src/hyperbolic/policy/HyperbolicPolicy_GLMMHD.h
+++ b/core/src/hyperbolic/policy/HyperbolicPolicy_GLMMHD.h
@@ -990,6 +990,15 @@ public:
       const real_t dP = q_ref.p - q_in.p;
       const real_t p_opp = q_ref.p + dP;
 
+      const real_t dBx = q_ref.Bx - q_in.Bx;
+      const real_t dBy = q_ref.By - q_in.By;
+      const real_t dBz = q_ref.Bz - q_in.Bz;
+
+      const real_t Bx_opp = q_ref.Bx + dBx;
+      const real_t By_opp = q_ref.By + dBy;
+      const real_t Bz_opp = q_ref.Bz + dBz;
+      const real_t pmag_opp = 0.5 * (Bx_opp*Bx_opp + By_opp*By_opp + Bz_opp*Bz_opp);
+
       // Getting cell-size
       const real_t dh = metadata.getCellSize(iCell_ref)[dir];
 
@@ -997,7 +1006,7 @@ public:
       q_out.u = (dir == IX ? 0.0 : q_in.u);
       q_out.v = (dir == IY ? 0.0 : q_in.v);
       q_out.w = (dir == IZ ? 0.0 : q_in.w);
-      q_out.p = p_opp + sgn * dh * q_ref.rho * rparams.g[dir];
+      q_out.p = (p_opp + pmag_opp) + sgn * dh * q_ref.rho * rparams.g[dir]; // Soustraire plus tard pmag_i+1/2
     }
 
     /**
@@ -1046,14 +1055,15 @@ public:
     
     const real_t v_out [3] {q_out.u, q_out.v, q_out.w};
     const real_t v_normal = v_out[dir];
-    const real_t Ek = 0.5 * q_out.rho * (v_out[IX]*v_out[IX] + v_out[IY]*v_out[IY] + v_out[IZ]*v_out[IZ]);
+    // const real_t Ek = 0.5 * q_out.rho * (v_out[IX]*v_out[IX] + v_out[IY]*v_out[IY] + v_out[IZ]*v_out[IZ]);
 
     const real_t Bx = u_out.Bx, By = u_out.By, Bz = u_out.Bz;
     const real_t B_out [3] {Bx, By, Bz};
     const real_t B_normal = B_out[dir];
     const real_t B2 = Bx*Bx + By*By + Bz*Bz;
 
-    const real_t p_gas = (u_out.e_tot - Ek - 0.5*B2) * (rparams.gamma0 - 1.0);
+    const real_t p_gas = q_out.p;
+    // const real_t p_gas = (u_out.e_tot - Ek - 0.5*B2) * (rparams.gamma0 - 1.0);
     
     // We first compute the hydro flux
     flux_hydro.rho = u_out.rho*v_normal;
diff --git a/settings/wholesun/B_shearing.ini b/settings/wholesun/B_shearing.ini
index a9734b00..3745b21c 100644
```
