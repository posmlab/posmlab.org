---
layout: research
title: "Research"
description: "Research in posmlab"
group: navigation
navorder: 1

sections:
  - id: materials
    title: "Materials Team"
    image: "/assets/images/projects/ema-rsa-g2-composite.png"
    description: |
      Understanding how materials perform when slowly loaded and rapidly unloaded is key to assessing their potential as a spring in LaMSA systems. We're extending this approach beyond synthetic elastomers to biological tissues like tendon, working to connect bulk material performance back to the underlying molecular and structural architecture that produces it.

      Our custom-built Elastodynamic Mechanical Analyzer (EMA) measures how elastic materials behave as they're rapidly unloaded, the same kind of high strain-rate release that drives motion in LaMSA systems. A material is slowly stretched while a latch holds it in place; when the latch releases, EMA directly measures force and displacement as the material recoils, down to millisecond timescales and millimeter size-scales. This lets us separate internal energy loss within the material itself from external losses (like those introduced by unlatching), and connect high strain-rate recoil behavior back to a material's underlying viscoelastic properties.

      We also use a TA Instruments RSA-G2 Dynamic Mechanical Analyzer (DMA) to characterize how materials respond to cyclic loading across a wide range of frequencies. Beyond standard sinusoidal oscillation, the RSA-G2's arbitrary waveform capability lets us apply non-sinusoidal, asymmetric cyclic inputs, for example loading a material slowly but unloading it quickly, or vice versa. This is especially useful for characterizing real-world performance, since many biological and engineered systems don't load and unload symmetrically, and for probing nonlinear viscoelastic behavior that standard small-strain sinusoidal DMA tests can miss.

      We're always happy to collaborate with other groups on material characterization. If you have a material you think would be interesting to test at high strain rates, [reach out](/about.html#contact) and let's talk.
    papers:
      - authors: "Ilton _et al._"
        journal: "Soft Matter"
        year: 2019
        url: "/papers/paper/size-scale-elastic-energy-release"
        title: "The effect of size-scale on the kinematics of elastic energy release"
      - authors: "Tsai _et al._"
        journal: "J. R. Soc. Interface"
        year: 2024
        url: "/papers/paper/viscoelastic-materials"
        title: "Viscoelastic materials are most energy efficient when loaded and unloaded at equal rates"
      - authors: "Zheng _et al._"
        journal: "Soft Matter"
        year: 2026
        url: "/papers/paper/elastodynamic-mechanical-analyzer"
        title: "Elastodynamic mechanical analyzer for high strain-rate mechanical characterization"
      - authors: "Acker"
        journal: "HMC Senior Thesis"
        year: 2026
        url: "/papers/paper/tendon-viscoelastic-behavior"
        title: "Characterizing the Viscoelastic Behavior of the Bullfrog Plantaris Tendon"

  - id: biomechanical-modeling
    title: "Biomechanical Modeling Team"
    image: "/assets/images/papers/cascading-power-limits.jpg"
    description: |
      Some organisms have a loading motor, spring, and latch built into their anatomy, and use this combination to perform ultra-fast movement. Mantis shrimp use elastic energy to drive their hammer-like appendages at speeds greater than 60 mph, fast enough to break open snail and crab shells. What's perhaps even more impressive is that the performance of some of these biological LaMSA systems exceeds that of current engineering capabilities for repeatable kinematic performance at small sizes. By understanding the physical principles that govern these systems, our aim is to contribute to a better understanding of the evolutionary dynamics of these organisms and to inform future engineering design.

      To study these systems, we develop and maintain a general, tunable mathematical model for LaMSA systems, the [LaMSA Template Model](https://posmlab.github.io/lamsa-template-model/). The model represents a LaMSA mechanism as a small set of coupled components (a loading motor, spring, latch, and load mass) whose properties can be set from morphological or material measurements of a specific biological or engineered system, so the same framework can be applied broadly rather than rebuilt from scratch for each new system. We maintain it as an open-source tool so other researchers can apply it to their own systems, and we use it to understand how LaMSA systems perform across size-scale and morphological differences.

      We're extending this framework to explore how multiple LaMSA systems shape each other's mechanical performance when they interact directly, such as in predator-prey encounters.
    papers:
      - authors: "Ilton _et al._"
        journal: "Science"
        year: 2018
        url: "/papers/paper/cascading-power-limits"
        title: "The principles of cascading power limits in small, fast biological and engineered systems"
      - authors: "Sutton _et al._"
        journal: "Integr. Comp. Biol."
        year: 2019
        url: "/papers/paper/large-animals-latch-springs"
        title: "Why do large animals never actuate their jumps with latch-mediated springs? Because they can jump higher without them"
      - authors: "Acharya _et al._"
        journal: "J. R. Soc. Interface"
        year: 2021
        url: "/papers/paper/finger-snap"
        title: "The ultrafast snap of a finger is mediated by skin friction"
      - authors: "Cook _et al._"
        journal: "Integr. Organismal Biol."
        year: 2022
        url: "/papers/paper/tunable-model-lamsa"
        title: "A Tunable, Simplified Model for Biological Latch Mediated Spring Actuated Systems"
      - authors: "Anderson _et al._"
        journal: "bioRxiv (preprint)"
        year: 2024
        url: "/papers/paper/strumigenys-lamsa"
        title: "Tuning a mechanical model to biological reality: A case study in the LaMSA system of the trap-jaw ant Strumigenys"
---
**The Physics of Soft Matter Lab (PoSM Lab) at Harvey Mudd College studies latch-mediated spring actuated (LaMSA) systems,** mechanisms that use a motor to slowly load a spring, which is held in place by a latch, then rapidly release that stored elastic energy into motion. An archer's bow and arrow is a simple example: the archer's muscles (motor) slowly load elastic energy into the bow (spring) while it's held by the archer's fingers (latch); releasing the latch converts that stored energy into the arrow's motion almost instantly. The same basic mechanism drives some of the fastest movements in biology, from mantis shrimp strikes to trap-jaw ant mandibles, and is increasingly used in engineered systems designed for fast, repeatable actuation.

Our lab is organized into two subteams that approach LaMSA systems from complementary directions: a **Materials Team** that characterizes how elastic materials store and release energy at the high strain rates relevant to LaMSA systems, and a **Biomechanical Modeling Team** that builds and applies mathematical models to understand how LaMSA systems perform across different organisms, size-scales, and morphologies.
