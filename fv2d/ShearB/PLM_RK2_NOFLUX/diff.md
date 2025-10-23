# Git Diff Expérience 1 sur les Ghosts Cells

Commmit de référence : [07ebad6ac88f2e576ed4eff62f52c2bbcf541a43](https://github.com/mdelorme/fv2d/commit/07ebad6ac88f2e576ed4eff62f52c2bbcf541a43)

<details>
  <summary> BoundaryConditions.h </summary>
    <br>
    ```diff
      diff --git a/BoundaryConditions.h b/BoundaryConditions.h
      index b0a07c1..d67262e 100644
      --- a/BoundaryConditions.h
      +++ b/BoundaryConditions.h
      @@ -12,7 +12,7 @@ namespace fv2d {
        void applyMagneticBoundaries(State &q, IDir dir, const DeviceParams &params){
          if (dir == IX){
            switch (params.magnetic_boundary_x){
      -          case BCMAG_NORMAL_FIELD:{
      +          case BCMAG_NORMAL_FIELD:{ // Bx=Bz=0 à l'interface
                  q[IBY] *= -1.0;
                  q[IBZ] *= -1.0;
                  break;
      @@ -135,15 +135,9 @@ namespace fv2d {
        
          if (dir == IX){
            q[IU] *= -1.0;
      -      #ifdef MHD
      -        q[IBX] *= -1.0;
      -      #endif
            }
            else {
              q[IV] *= -1.0;
      -        #ifdef MHD
      -          q[IBY] *= -1.0;
      -        #endif
            }
          #ifdef MHD
            applyMagneticBoundaries(q, dir, params);
    ```
</details>

<details>
<summary> Update.h </summary>
  <br>
    
    ```diff
        diff --git a/Update.h b/Update.h
        index ceba06d..4e56ac3 100644
        --- a/Update.h
        +++ b/Update.h
        @@ -160,15 +160,15 @@ public:
    
              fluxL = swap_component(fluxL, dir);
              fluxR = swap_component(fluxR, dir);
    -          const bool is_left_boundary   = i == params.ibeg;
    -          const bool is_right_boundary  = i == params.iend;
    -          const bool is_bottom_boundary = j == params.jbeg;
    -          const bool is_upper_boundary  = j == params.jend-1;
    -
    -          if (is_bottom_boundary && dir == IY)
    -            fluxL = getBoundaryFlux(qR, i, j, dir, params);
    -          if (is_upper_boundary && dir == IY)
    -            fluxR = getBoundaryFlux(qL, i, j, dir, params);
    +          // const bool is_left_boundary   = i == params.ibeg;
    +          // const bool is_right_boundary  = i == params.iend;
    +          // const bool is_bottom_boundary = j == params.jbeg;
    +          // const bool is_upper_boundary  = j == params.jend-1;
    +
    +          // if (is_bottom_boundary && dir == IY)
    +          //   fluxL = getBoundaryFlux(qR, i, j, dir, params);
    +          // if (is_upper_boundary && dir == IY)
    +          //   fluxR = getBoundaryFlux(qL, i, j, dir, params);
              
              auto un_loc = getStateFromArray(Unew, i, j);
              un_loc += dt*(fluxL - fluxR)/(dir == IX ? params.dx : params.dy);
    ```
</details>
