# Implementation

## 1. Finding the intersections of quadratic Bézier curves

Because coordinates are stored with limited precision, clipping quadratic Bézier curves can create linear Bézier curves. This implies that it's not enough to be able to calculate intersections between two quadratic Bézier curves, but also between quadratic and linear curves.

When both Bézier curves are quadratic, i.e. segments of parabolas, their intersections are calculated differently depending on whether the axes of the parabolas are parallel or not. When they are not parallel, it's possible to transform them with a linear map so that the axes become perpendicular and aligned with the coordinate axes. Consequently, the x-function of one curve and the y-function of the other curve become first degree polynomials. This makes things a bit simpler, but solving for the intersections still requires solving a quartic equation.

When the curves are segments of parabolas with parallel axes, a linear map can be applied to them so that their axes are parallel with the y-axis, which implies that both of their x-functions are first-degree polynomials. After this, solving for the curve parameters yields either a quadratic or a linear equation.

When one curve is a segment of a parabola and the other one is a line segment, a linear map can be applied to them so that the line segment is vertical. After this, the intersections can be found by solving for $t$ in $x(t) = x_{0}$ where $x$ is the x-function of the quadratic curve and $x_{0}$ is the x-coordinate of every point on the linear curve. The equation is quadratic.

New loops generally don't contain any linear curves, but calculating intersections between two linear curves is implemented as well for the sake of completeness. This corresponds to solving a linear equation.

## 2. Managing areas delimited by curves

Although there are some existing algorithms for merging polygons with each other, I couldn't find any that would fit to the task at hand without significant modifications. Hence, an original algorithm is used instead. We'll start with a few definitions regarding what I'll call *loops*.

**Definition 2.1.** A continuous bijection $l: [0, a) \to \mathbb{R}^2$ is a *loop* of length $a$ if
$\lim\limits_{t \to a} l(t) = l(0)$
and $a\in\mathbb{R}_{\gt0}$.

**Definition 2.2.** If $l$ is a loop of length $a$, then $l^x: [0, a) \to \mathbb{R}$ and $l^y: [0, a) \to \mathbb{R}$ are functions so that $(l^x(t), l^y(t)) = l(t)$ for each $t \in [0, a)$.

**Definition 2.3.** If $l$ is a loop of length $a$, $x_1 \in \mathbb{R}$ an $l^x(t) < x_1$ for each $t \in [0, a)$, point $p \in \mathbb{R}^2$ *is outside of* loop $l$ if there exists a continuous function $f: [0, 1] \to \mathbb{R}^2$ so that $f(0) = p$, $f(1) = (x_1, 0)$ and $f(t_1) \neq l(t_2)$ with each $t_1 \in [0, 1]$ and $t_2 \in [0, a)$.

**Definition 2.4.** If $l$ is a loop of length $a$, $p \in \mathbb{R}^2$ and $l(t) = p$ with some $t \in [0, a)$, point $p$ *is on loop* $l$.

**Definition 2.5.** If $l$ is a loop, point $p \in \mathbb{R}^2$ is not outside of loop $l$ and point $p$ is not on loop $l$, then point $p$ *is inside of loop* $l$.

**Definition 2.6.** If $l_1$ and $l_2$ are loops and every point on $l_1$ is outside of $l_2$, $l_1$ *is outside of* $l_2$.

**Definition 2.7.** If $l_1$ and $l_2$ are loops and every point on $l_1$ is inside of $l_2$, $l_1$ *is inside of* $l_2$.

**Definition 2.8.** If $l_1$ and $l_2$ are loops, $l_1$ is outside of $l_2$ and $l_2$ is outside of $l_1$, loops $l_1$ and $l_2$ are *separate.*

A single loop can be define either a painted area, or a hole in a painted area. Since a painted area may contain holes, which may contain smaller painted areas, which may contain even smaller holes, etc., a recursive tree-like structure is needed.

**Definition 2.9.** The (possibly empty) set $\set{ (l_1, S_1), (l_2, S_2), \dots, (l_n, S_n) }$ where $n \in \mathbb{N}$ is a *loop system* if
1. $l_1, \dots, l_n$ are loops.
2. $l_i$ is outside of $l_j$ with any $i \neq j$ where $i, j \in \set{1, \dots, n}$.
3. $S_i$ is a loop system $\set{(m_1, T_1), (m_2, T_2), \dots, (m_k, T_k)}$ where $k \in \mathbb{N}$ so that $m_j$ is inside of $l_i$ with any $j \in \set{1, \dots, k}$ and $i \in \set{1, \dots, n}$.

The goal of the project requires an algorithm that adds a new loop to a loop system and merges it with any loops it intersects with, and any loop systems inside them. Creating such an algorithm becomes significantly easier when it can use a subalgorithm that simply merges the new loop with a set of separate older loops it intersects with, without dealing with the loop systems inside each older loop. The implementation of the subalgorithm depends on the type of curve used and will be specified later, but certain requirements for it apply regardless of the curves.

**Requirement 2.10.** The algorithm $\text{merge}\textunderscore\text{loops}(l, \set{l_1, \dots, l_n})$ may assume that
1. $l_i$ is outside of $l_j$ with any $i \neq j$ where $i, j \in \set{1, \dots, n}$.
2. $l_i$ is neither outside nor inside of $l$ with any $i \in \set{1, \dots, n}$.

But it must return $(l', H)$ so that
1. Each $p \in \mathbb{R}^2$ is inside of $l'$ if it's inside any of $l_1, \dots, l_n$ or $l$.
2. If any $p \in \mathbb{R}^2$ is outside all of $l_1, \dots, l_n$ and $l$ but it's inside of $l'$, it's inside of some loop $h \in H$.
3. All $h \in H$ are loops that are inside of $l'$.
4. $h_1$ is outside of $h_2$ with any $h_1, h_2 \in H$.

Since there can be any number of holes between the merged loops, it doesn't just return the new loop that contains them but also a set containing the holes. The following algorithm takes that into account as well.

**Algorithm 2.11.**
$\text{add}\textunderscore\text{loop}(\text{loop system } S, \text{loop } l)$
1. Let $\set{(m_1, T_1), \dots, (m_n, T_n)} = S$.
2. If $l$ is inside any of $m_i \in \set{m_1, \dots, m_n}$, return $(S \setminus \set{(m_i, T_i)}) \cup \set{(m_i, \text{remove}\textunderscore\text{loop}(T_i, l))}$.
3. Let $I = \set{(m, T) \in S \mid m \text{ is inside of } l}$.
4. Let $O = \set{(m, T) \in S \mid m \text{ is outside of } l}$.
5. Let $E = S \setminus \set{I \cup O}$.
6. Let $(l', H) = \text{merge}\textunderscore\text{loops}(l, \set{m_i \mid (m_i, T_i) \in E})$.
7. Let $T = \displaystyle\bigcup_{(m_i, T_i) \in E}T_i$.
8. Let $O_h = \set{m \in O \mid m\text{ is inside of }h}$ for each $h \in H$.
9. Let $T' = \text{remove}\textunderscore\text{loop}(T, l) \cup \set{(h, O_h) \mid h \in H}$.
10. Return $\set{m \in O \mid m\text{ is outside of }l'} \cup \set{(l', T')}$.

This algorithm also relies on the $\text{remove}\textunderscore\text{loop}$ subalgorithm to remove or "cut out" a loop from a loop system. The latter algorithm is partially defined in the code, with the limitation that it only allows cutting with loops that don't intersect with any top-level loops in the loop system.

## 3. Determining if a loop is inside another when no intersections are found

The above algorithm needs to be able to find out if a loop is inside another, even when they don't intersect. This is achieved by picking an arbitrary point on one loop, and checking if it's inside the other loop. This is in turn achieved by drawing a vertical ray starting from that point, and counting how many times it intersects the loop. If the number of intersections is even, the point is outside of the loop, and otherwise it's inside of the loop. Tangential points are not counted as intersection points.

The intersection points between the ray and each curve are actually calculated only when the starting point of the ray is inside the bounding box of the curve's control points. In other cases, it's basically sufficient to check whether the ray is between the starting and ending points of the curve, or if the curve is above the whole ray. However, since the ray can also pass through control points, which could normally lead to intersections getting counted twice, some tricks are used to get the right parity in all cases, making things somewhat more complicated.

## 4. Merging loops with each other
Loops are merged with each other with the `Loop.merge_to` function, which meets the requirements for $merge_to$ defined above. To put it simply, it finds all intersections between the new loop and the previous loops and forms a directed graph of them so that there's an edge from each intersection to the next intersection on the same loop ("next" meaning the one with the following parameter value).

It's also important to know which loop is "outer" and which one is "inner" after each intersection, so that the algorithm can trace the loop that bounds all input loops. This is determined by taking the determinant of a matrix made of the derivative vectors of both loops at the given intersection, which is equivalent to rotating one vector 90° and then calculating the dot product.

First, an arbitrary intersection is chosen, and a path is traced by following the "outer" loop at each intersection. If nothing weird happens because of numerical inaccuracies, the starting intersection is eventually reached. Once this happens, the parts of the traced loop are clipped out of the input loops and turned into a new loop that's added to a list of result loops. After this, a new intersection (that hasn't been marked as visited) is chosen and the process is repeated until no intersections are left.

At this point, all resulting loops are in a list with no particular order. However, we know that one of the loops contains all others, and the algorithm is required to return this loop separately from them. We could use the algorithm that checks whether a point is inside a loop, but to avoid dealing with edge cases I decided to use a different approach and determine which loops clockwise and which ones are not. The loop with the same turning number as the input loops is the outer one, and the other ones must be inside it. The turning number of a loop is determined by calculating the sum of exterior angles of a polygon consisting of its control points.

## 5. Clipping loops and curves

The process described above requires being able to clip a part of a loop between intersection points, which in turn requires being able to clip individual loops between parameter values. When clipping either a quadratic or a linear Bézier curve, the new start and end points can be found by simply evaluating the curve with the given parameters. If the curve is quadratic, it's also necessary to find the third control point. This can be done by drawing tangent lines to the curve at the points corresponding to the parameter values, and finding their intersection point. When clipping a part of a whole loop between two parameter values, the start is clipped from the first curve, the end is clipped of the last curve, and any curves between the two are copied.
