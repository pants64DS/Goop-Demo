# Weekly report \#1

**Time used:** around 20 hours

During the first week, I mostly worked on finding the intersection points of two quadratic Bézier curves. This may not be the main focus of the project, but most other aspects of the project rely on it. By searching the Internet, I learned that this is commonly done using iterative numerical algorithms. However, in the case of quadratic Bézier curves, I believe that an algebraic solution can be more efficient when implemented well.

Since quadratic Bézier curves are really just a parts of parabolas limited by their control points, all intersections of two curves are also intersections of the parabolas they're part of. This allows us to obtain the intersections of the curves by first finding the intersections of the parabolas, and then discarding any intersections that lie outside of either curve. The latter can be done easily if the parametric values for each point of intersection is known. Therefore, instead of just finding the points of intersection as 2D coordinates, I'm planning to find the parameters (often denoted by letter $t$) of each point of intersection relative to both curves.

If the axes of the parabolas are parallel, finding the intersections is rather trivial; one can choose a coordinate system aligned with both parabolas, so that their equations can be written as $y = a_1x^2 + b_1x + c_1$ and $y = a_2x^2 + b_2x + c_2$. Then their intersections can be found easily by equating the polynomials on the right-hand side in both equations and solving for $x$ in the resulting quadratic equation.

If the axes of the parabolas are not parallel, they can be made perpendicular by applying a linear map to the control points of the corresponding curves. After this, their equations can be written as $y = a_1x^2 + b_1x + c_1$ and $x = a_2y^2 + b_2y + c_2$. Now one can substitute $y$ (or $x$) with the polynomial it's equated to, which yields the quartic equation:
```math
x = a_2(a_1x^2 + b_1x + c_1)^2 + b_2(a_1x^2 + b_1x + c_1) + c_2$$
```
```math
\iff$$
```
```math
$$a_1^2a_2x^4 + 2a_1a_2b_1x^3 + (2a_1a_2c_1 + a_2b_1^2 + a_1b_2)x^2 + (2a_2b_1c_1 + b_1b_2 - 1)x + a_2c_1^2 + b_2c_1 + c_2 = 0$$
```

Solving quartic polynomials algebraically is generally quite tedious and computationally expensive, but I discovered that translating and scaling the parabolas so that $b_1 = 1$ and $c_2 = \frac{1}{a_1}(a_2c_1 + \frac{b_2-1}{2}) + \frac{b_2^2 - 1}{4a_2}$ ensures that the resulting quartic can be factored into two quadratic polynomials:
```math
(a_1x^2 + c_1+\frac{b_2 - 1}{2a_2})(a_1a_2x^2 + 2a_2x + a_2(c_1 + \frac{1}{a_1}) + \frac{b_2 + 1}{2})
```
```math
= a_1^2a_2x^4 + 2a_1a_2x^3 + (2a_1a_2c_1 + a_2 + a_1b_2)x^2 + (2a_2b_1c_1 + b_2 - 1)x + a_2c_1^2 + b_2c_1 + \frac{1}{a_1}(a_2c_1 + \frac{b_2-1}{2}) + \frac{b_2^2 - 1}{4a_2}
```

Next week I'm planning to start implementing this technique in code.
