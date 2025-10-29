# Architecture actuelle : Hyperbolic Policy et Schéma RK2

```mermaid
classDiagram
    %% -- Classes de base et interfaces --
    class HyperbolicPolicy_base {
        <<Template>>
        +method1()
        +method2()
    }

    class HyperbolicUpdate {
        <<Interface>>
        +update(UserData, ScalarSimulationData)
    }

    %% -- Composants de la Policy --
    class HyperbolicPolicy_State_GLMMHD {
        +getConsState()
        +getPrimState()
        +consToPrim()
        +primToCons()
    }

    class HyperbolicPolicy_RiemannSolver_GLMMHD_hlld {
        +riemann_solver()
    }

    class HyperbolicPolicy_Slope_dynamic {
        +compute_slope()
    }

    class HyperbolicPolicy_BoundaryConditions_GLMMHD {
        +getBoundaryValue()
        +getBoundaryFlux()
    }

    %% -- Policy concrète --
    class HyperbolicPolicy_GLMMHD_impl {
        +postProcess()
        +printWarnings()
    }

    %% -- Spécialisation de la Policy --
    class HyperbolicPolicy_GLMMHD {
        <<Alias>>
    }

    %% -- Schéma RK2 --
    class Hyperbolic_WholeSun_RK2 {
        <<Template>>
        +update(UserData, ScalarSimulationData)
        +update_once()
    }

    %% -- Implémentation finale --
    class GLMMHDUpdate_WholeSun_RK2 {
        +update(UserData, ScalarSimulationData)
    }

    %% -- Relations --
    HyperbolicPolicy_GLMMHD_impl --|> HyperbolicPolicy_State_GLMMHD
    HyperbolicPolicy_GLMMHD_impl --|> HyperbolicPolicy_RiemannSolver_GLMMHD_hlld
    HyperbolicPolicy_GLMMHD_impl --|> HyperbolicPolicy_Slope_dynamic
    HyperbolicPolicy_GLMMHD_impl --|> HyperbolicPolicy_BoundaryConditions_GLMMHD

    HyperbolicPolicy_base <|-- HyperbolicPolicy_GLMMHD_impl : CRTP
    HyperbolicPolicy_GLMMHD : HyperbolicPolicy_base<HyperbolicPolicy_GLMMHD_impl>

    Hyperbolic_WholeSun_RK2 <|-- GLMMHDUpdate_WholeSun_RK2 : Instanciation
    Hyperbolic_WholeSun_RK2 o-- HyperbolicPolicy_base : Utilise une Policy

    HyperbolicUpdate <|-- Hyperbolic_WholeSun_RK2
