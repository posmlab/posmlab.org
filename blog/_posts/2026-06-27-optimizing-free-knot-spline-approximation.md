---
layout: post
title: "Optimizing Free-Knot Spline Approximation"
description: ""
author: "Helios Hong"
author_handle: hhong
category: blog
published: true
image: /assets/images/experiment-375-lambda-sweep.png
theme: lab
redirect_from: /blog/2026/6/27/optimizing-free-knot-spline-approximation
tags: []
---
{% include JB/setup %}

## The Main Problem: Inverse Dynamics Overshoot

This week, my work focused on understanding and improving one of the central analysis challenges in our recoil project: the mismatch between the inverse dynamics force curve and the force measured directly by the force sensor.

In our recoil experiments, we track dots on a stretched soft material as it recoils after release. From the high-speed camera data, we obtain position versus time for each dot. Then, after fitting those raw position data, we take numerical derivatives to calculate velocity and acceleration. Since force is related to mass times acceleration, we can use the acceleration of each tracked section of the material to construct a force-like quantity from inverse dynamics. Ideally, this inverse dynamics force should agree reasonably well with the force sensor beyond an initial unlatching force.

However, we had been seeing a persistent "overshoot" phenomenon, where the inverse dynamics force curve rose much higher than expected compared to the force sensor curve. At first, this looked like it might be caused by the spline-fitting method itself, or by the choice of fitting parameters. Eventually, we found that a large part of the overshoot came from a bug in the code: we had been using the relaxed length of the material as the initial length, instead of the 100% strained length. After correcting this, most of the overshoot was reduced.

## Why Fitting Still Matters

Even after fixing that bug, the inverse dynamics curve still depended noticeably on the fitting parameters used in the free-knot spline approximation. This matters because our analysis does not stop at position. We take derivatives of the fitted position curve, and derivatives tend to amplify small differences or noise. A fit that looks only slightly different in position can produce much larger differences in velocity, acceleration, and therefore inverse dynamics force.

This meant that the remaining variation was not just a small technical detail. Since quantities like acceleration, force, kinetic energy, and resilience all depend on processed position data, the way we fit the original tracking data directly affects the physics we calculate from the experiment.

## The Key Free-Knot Spline Parameters

To investigate the remaining variation in the inverse dynamics curve, I experimented with several parameters in the BSFK free-knot spline fitting method: lambda, d, k, maxknots, and the knot removal factor. These parameters control how flexible the fitted curve is, how smooth it is, and how many spline pieces the algorithm is allowed to use.

The parameter k controls the order of the spline. More specifically, each spline segment is a polynomial of order k - 1. For example, k = 4 corresponds to a cubic spline, while k = 2 corresponds to a linear spline. The value of k also determines how smooth the spline is at the knots where neighboring spline pieces meet. A spline with order k has continuous derivatives up to order k - 2. In our analysis, changing k changes how flexible the position fit can be, which then affects velocity, acceleration, and inverse dynamics after we take derivatives.

The parameter d is different from k. Instead of setting the polynomial order of the spline itself, d controls the derivative order used in the regularization penalty. In other words, d determines what kind of roughness the fitting algorithm penalizes. If d = 1, the algorithm penalizes large first derivatives; if d = 2, it penalizes curvature; if d = 3, it penalizes changes in curvature. Since our inverse dynamics calculation depends strongly on acceleration, this regularization choice matters a lot. It changes what the algorithm considers to be a "smooth" or "reasonable" fit.

The parameter lambda controls the strength of that regularization. The spline fit is not only trying to minimize the difference between the fitted curve and the raw data. It is also minimizing a smoothness penalty, and lambda determines how much that penalty matters. When lambda = 0, there is no regularization, so the fit focuses only on matching the data. A small lambda allows the curve to follow the raw tracking data closely, which can preserve fast recoil motion but also overfit noise. A larger lambda forces the curve to be smoother, which can reduce noise but may also remove real physical features. Since derivatives amplify noise, the choice of lambda can strongly affect the acceleration and inverse dynamics force curves.

The parameter maxknots, or more generally the number of knots allowed in the fit, controls how many subintervals the spline can use. Knots are the points where spline pieces connect. Allowing more knots gives the fit more flexibility, because the spline can adjust its shape over smaller regions of the data. However, too many knots can make the fit sensitive to tracking noise. Allowing too few knots can make the fit too rigid and unable to capture real changes in the recoil motion.

The knot removal factor controls how aggressively the algorithm removes redundant knots after fitting. A smaller knot removal factor removes fewer knots, so the final spline keeps more flexibility. A larger knot removal factor removes more knots, producing a simpler fit. This parameter matters because two fits may start with the same maximum number of knots but end with different effective complexity depending on how many knots are removed.

Together, these parameters define the balance between data fidelity and smoothness. k controls the polynomial structure of the spline, d controls what derivative is penalized in the regularization, lambda controls how strongly that penalty is applied, maxknots controls the maximum flexibility of the fit, and the knot removal factor controls how much of that flexibility remains after redundant knots are removed.

This parameter sensitivity became important because our final analysis depends on derivatives of the fitted position curve. Even if two position fits look similar, their velocity and acceleration curves can differ significantly. Since inverse dynamics is calculated from acceleration, small fitting choices can produce large differences in the final force curve.

<p align="center">
<img src="{{ BASE_PATH }}/assets/images/experiment-375-lambda-sweep.png" width="90%">
</p>

<p align="center"><em>This plot shows the inverse dynamics force curve for Experiment 375 using several different values of the spline regularization parameter lambda, while keeping the other fitting parameters fixed. The colored curves are inverse dynamics results from camera-based position fitting, and the thick black curve is the force sensor fit. Smaller changes in lambda can noticeably change the timing, height, and smoothness of the inverse dynamics peak, showing why the choice of smoothing parameter strongly affects higher-derivative quantities like acceleration and force.</em></p>

## Why One "Best Fit" Was Not Enough

At first, the plan was to find one best set of parameters for each material and load mass. For example, we could imagine having one recommended parameter set for neoprene with no load mass, another for neoprene with 2 grams, another for 8 grams, and so on. But this strategy quickly became vague. Different parameter choices sometimes looked better for position, while other choices looked better for velocity or acceleration. Since the higher derivatives are where the largest variations appear, picking one "best" fit by eye did not feel reliable enough.

This was the key realization of the week: there may not be a single perfect fit. Instead, there may be a family of reasonable fits, and the spread between them tells us something important about the uncertainty in our analysis.

## A New Strategy: Fitting Across Many Parameter Sets

Because of this, we adopted a new strategy: instead of choosing one spline fit, we generate hundreds of acceptable fits using many different combinations of lambda, d, k, maxknots, and knot removal factors. Then, at each time point, we collect the values from all of those fits and sort them. From that distribution, we record a median curve, as well as upper and lower bounds after cutting off a chosen percentage from the top and bottom.

This gives us a way to treat the spread across reasonable fits as an estimate of uncertainty. The resulting median, upper, and lower curves may not come from one single smooth spline fit, but they capture the range of behavior produced by many acceptable smooth fits. This is especially useful because our final quantities depend on derivatives.

## Carrying Uncertainty Through Derivatives

For velocity, we do not simply take the derivative of the median position curve. Instead, we take the derivative of each individual spline fit, then sort the velocity values at each time point and again record the median, upper, and lower bounds. We do the same for acceleration and jerk.

This is important because different fitting parameters may perform better for different derivative orders. A parameter set that gives a clean position curve may not necessarily give the most reliable acceleration curve. By ranking the values separately for position, velocity, acceleration, and jerk, we avoid forcing one fitting choice to determine the entire analysis.

## Turning Fit Variation Into Error Bars

We then treat the upper and lower bounds as error bars. The cutoff percentage, which we are calling alpha, has not been finalized yet. Next week, we plan to run more fits and compare different cutoff choices to decide how much of the top and bottom of the distribution should be removed. The goal is to avoid letting extreme parameter choices dominate the uncertainty range while still capturing meaningful variation across the fitting process.

In other words, instead of reporting only one inverse dynamics curve, we can report a median curve with an uncertainty band around it. This should make our final results more honest and more useful, especially when comparing experiments with different materials, load masses, or tracking quality.

<p align="center">
<img src="{{ BASE_PATH }}/assets/images/experiment-375-uncertainty-band.png" width="90%">
</p>

<p align="center"><em>This figure shows the final uncertainty-aware inverse dynamics curve for Experiment 375 compared with the force sensor measurement. The blue curve represents the median inverse dynamics force across many BSFK spline fits, while the red dashed curves and shaded region show the top-bottom uncertainty band from acceptable parameter choices (alpha=10). Compared with choosing a single spline fit, this approach shows both the central trend and how much the inverse dynamics result can vary due to fitting choices.</em></p>

## Main Takeaway

Overall, this week shifted the analysis from trying to find one perfect spline fit toward building a more robust uncertainty-aware fitting pipeline. The overshoot problem started as a debugging issue, but it led us to a deeper question: how much of our final physics depends on the choices we make during data processing?

By sweeping many fitting parameters and carrying that variation through position, velocity, acceleration, jerk, and inverse dynamics, we are building a better way to report not just a single result, but also how confident we are in that result.
