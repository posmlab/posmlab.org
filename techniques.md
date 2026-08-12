---
layout: research
title: "Techniques"
description: "Experimental and computational techniques used in PoSM Lab"
group: navigation
navorder: 5

sections:
  - id: ema
    title: "Elastodynamic Mechanical Analyzer (EMA)"
    image: "/assets/images/projects/ELLA_assembly.png"
    description: |
      The Elastodynamic Mechanical Analyzer (EMA) is a custom-built instrument we developed to measure how elastic materials behave as they're rapidly unloaded — the same kind of high strain-rate release that drives motion in LaMSA systems. A material is slowly stretched while a latch holds it in place; when the latch releases, EMA directly measures force and displacement as the material recoils, down to millisecond timescales and millimeter size-scales. This lets us separate internal energy loss within the material itself from external losses (like those introduced by unlatching), and connect high strain-rate recoil behavior back to a material's underlying viscoelastic properties.
    papers:
      - authors: "Zheng _et al._"
        journal: "Soft Matter"
        year: 2026
        url: "/papers/paper/elastodynamic-mechanical-analyzer"
        title: "Elastodynamic mechanical analyzer for high strain-rate mechanical characterization"
      - authors: "Ilton _et al._"
        journal: "Soft Matter"
        year: 2019
        url: "/papers/paper/size-scale-elastic-energy-release"
        title: "The effect of size-scale on the kinematics of elastic energy release"

  - id: rsa-g2
    title: "RSA-G2 Dynamic Mechanical Analyzer"
    description: |
      We also use a TA Instruments RSA-G2 Dynamic Mechanical Analyzer (DMA) to characterize how materials respond to cyclic loading across a wide range of frequencies. Beyond standard sinusoidal oscillation, the RSA-G2's arbitrary waveform capability lets us apply non-sinusoidal, asymmetric cyclic inputs — for example, loading a material quickly but unloading it slowly, or vice versa. This is especially useful for characterizing real-world performance, since many biological and engineered systems don't load and unload symmetrically, and for probing nonlinear viscoelastic behavior that standard small-strain sinusoidal DMA tests can miss.
    papers:
      - authors: "Tsai _et al._"
        journal: "J. R. Soc. Interface"
        year: 2024
        url: "/papers/paper/viscoelastic-materials"
        title: "Viscoelastic materials are most energy efficient when loaded and unloaded at equal rates"
      - authors: "Acker"
        journal: "HMC Senior Thesis"
        year: 2026
        url: "/papers/paper/tendon-viscoelastic-behavior"
        title: "Characterizing the Viscoelastic Behavior of the Bullfrog Plantaris Tendon"

  - id: modeling
    title: "LaMSA Template Model"
    image: "/assets/images/projects/modeling-kinematics.jpg"
    description: |
      Alongside our experimental techniques, we develop and maintain a general, tunable mathematical model for LaMSA systems. The model represents a LaMSA mechanism as a small set of coupled components — a loading motor, spring, latch, and load mass — whose properties can be set from morphological or material measurements of a specific biological or engineered system, so the same framework can be applied broadly rather than rebuilt from scratch for each new system. We maintain this model as an open-source tool, the [LaMSA Template Model](https://posmlab.github.io/lamsa-template-model/), so other researchers can apply it to their own systems.
    papers:
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
PoSM Lab combines custom-built and commercial instrumentation with computational modeling to study how latch-mediated spring actuated (LaMSA) systems store, release, and dissipate elastic energy. Below are the core techniques we use across our experimental and modeling work.
