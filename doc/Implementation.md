# Implementation

## Finding the intersections of quadratic Bézier curves

[todo]

## Managing areas delimited by curves

Although there are some existing algorithms for merging polygons with each other, I couldn't find any that would fit to the task at hand without significant modifications. Hence, an original algorithm is used instead. We'll start with a few definitions regarding what I'll call *loops*.

**Definition 2.1.** A continous bijection $l: [0, a) \to \mathbb{R}^2$ is a *loop* of length $a$ if
$\lim\limits_{t \to a} l(t) = l(0)$
and $a\in\mathbb{R}_{\gt0}$.

**Definition 2.2.** If $l$ is a loop of length $a$, then $l^x: [0, a) \to \mathbb{R}$ and $l^y: [0, a) \to \mathbb{R}$ are functions so that $(l^x(t), l^y(t)) = l(t)$ for each $t \in [0, a)$.

**Definition 2.3.** If $l$ is a loop of length $a$, $x_1 \in \mathbb{R}$ an $l^x(t) < x_1$ for each $t \in [0, a)$, point $p \in \mathbb{R}^2$ *is outside of* loop $l$ if there exists a continuous function $f: [0, 1] \to \mathbb{R}^2$ so that $f(0) = p$, $f(1) = (x_1, 0)$ and $f(t_1) \neq l(t_2)$ with each $t_1 \in [0, 1]$ and $t_2 \in [0, a)$.

**Definition 2.4.** If $l$ is a loop of length $a$, $p \in \mathbb{R}^2$ and $l(t) = p$ with some $t_2 \in [0, a)$, point $p$ *is on loop* $l$.

**Definition 2.5.** If $l$ is a loop, point $p \in \mathbb{R}^2$ is not outside of loop $l$ and point $p$ is not on loop $l$, then point $p$ *is inside of loop* $l$.

**Definition 2.6.** If $l_1$ and $l_2$ are loops and every point on $l_1$ is outside of $l_2$, $l_1$ *is outside of* $l_2$.

**Definition 2.7.** If $l_1$ and $l_2$ are loops and every point on $l_1$ is inside of $l_2$, $l_1$ *is inside of* $l_2$.

**Definition 2.8.** If $l_1$ and $l_2$ are loops, $l_1$ is outside of $l_2$ and $l_2$ is outside of $l_1$, loops $l_1$ and $l_2$ are *separate.*

A single loop can be define either a painted area, or a hole in a painted area. Since a painted area may contain holes, which may contain smaller painted areas, which may contain even smaller holes, etc., a recursive tree-like structure is needed.

**Definition 2.9.** The (possibly empty) set $\set{ (l_1, S_1), (l_2, S_2), \dots, (l_n, S_n) }$ where $n \in \mathbb{N}$ is a *loop system* if
* $l_1, \dots, l_n$ are loops.
* $l_i$ is outside of $l_j$ with any $i \neq j$ where $i, j \in \set{1, \dots, n}$.
* $S_i$ is a loop system $\set{(m_1, T_1), (m_2, T_2), \dots, (m_k, T_k)}$ where $k \in \mathbb{N}$ so that $m_j$ is inside of $l_i$ with any $j \in \set{1, \dots, k}$ and $i \in \set{1, \dots, n}$.
