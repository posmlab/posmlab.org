---
layout: post
title: "Summer 2026 June 5th Update"
description: ""
author: "Helios Hong"
author_handle: hhong
category: blog
published: true
theme: lab
redirect_from: /blog/2026/6/27/posm-lab-summer-2026-june-5th-update
tags: []
---
{% include JB/setup %}

This summer in the POSM lab, we're studying how soft materials recoil after being stretched and released. The bigger goal is to connect experimental recoil videos, force sensor data, and simulations so we can better understand how material properties, load mass, and geometry affect the dynamics of elastic recoil.

This week, Cleo and I focused on cleaning up the recoil analysis workflow and processing more experiments. We reran resilience calculations, added energy input and load-mass resilience metrics, and looked through which recoil videos were usable. Some trials had syncing problems, friction, sticking, or shaking in the clamp and force sensor, so part of the work was figuring out which data could be trusted and which experiments may need to be redone.

On the coding side, we updated the MATLAB file calcKinematics so that the time of recoil now ends when the kinetic energy reaches its maximum. We added comments and summaries to the code, reorganized file paths, and uploaded updated experiment data to Google Drive. We also started troubleshooting MATLAB on the lab computer, with MATLAB Online as a backup, and began testing parallel computing for longer simulations.

In addition, the summer machine shop proctors helped us out by designing a new load mass clamp, updating our attachment component, and adding a valve switch to ensure the clamp stays secure while loading.

Sam has been working on developing an algorithm to perform time-temperature superposition to varying degrees of success. This week he worked on refining the cost function used by the algorithm to determine the optimal shift factor for each temperature; he tested various methods including a logarithmic and normalized version of the function.
