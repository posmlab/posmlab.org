---
layout: paper
title: "A Tunable, Simplified Model for Biological Latch Mediated Spring Actuated Systems"
year: "2022"
shortref: "Cook <i>et al.</i> 2022"
nickname: "tunable-model-lamsa"
journal: "Integrative Organismal Biology"
volume: 4
issue: 1
pages: "obac032"
authors: "Cook A, Pandhigunta K, Acevedo MA, Walker A, Didcock RL, Castro JT, O'Neill D, Acharya R, Bhamla MS, Anderson PSL, Ilton M"
image: /assets/images/papers/tunable-model-lamsa.png
redirect_from: /blog/2022/9/01/template-model
fulltext: https://academic.oup.com/iob/article/4/1/obac032/6652213
pdflink:
pdf: "/assets/pdfs/tunable-model-lamsa.pdf"
github:
pmid: 36060863
pmcid: PMC9434652
doi: "10.1093/iob/obac032"
category: paper
published: true
preprint: false
embargo: false
tags: [biomechanics, computational methods, modeling, LaMSA]
---
{% include JB/setup %}

# Abstract

We develop a model of latch-mediated spring actuated (LaMSA) systems relevant to comparative biomechanics and bioinspired design. The model contains five components: two motors (muscles), a spring, a latch, and a load mass. One motor loads the spring to store elastic energy and the second motor subsequently removes the latch, which releases the spring and causes movement of the load mass. We develop freely available software to accompany the model, which provides an extensible framework for simulating LaMSA systems. Output from the simulation includes information from the loading and release phases of motion, which can be used to calculate kinematic performance metrics that are important for biomechanical function. In parallel, we simulate a comparable, directly actuated system that uses the same motor and mass combinations as the LaMSA simulations. By rapidly iterating through biologically relevant input parameters to the model, simulated kinematic performance differences between LaMSA and directly actuated systems can be used to explore the evolutionary dynamics of biological LaMSA systems and uncover design principles for bioinspired LaMSA systems. As proof of principle of this concept, we compare a LaMSA simulation to a directly actuated simulation that includes either a Hill-type force-velocity trade-off or muscle activation dynamics, or both. For the biologically-relevant range of parameters explored, we find that the muscle force-velocity trade-off and muscle activation have similar effects on directly actuated performance. Including both of these dynamic muscle properties increases the accelerated mass range where a LaMSA system outperforms a directly actuated one.
