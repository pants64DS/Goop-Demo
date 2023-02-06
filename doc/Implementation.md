# Implementation

## Finding the intersections of quadratic Bézier curves

[todo]

## Managing areas delimited by curves

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

This algorithm also relies on the $\text{remove}\textunderscore\text{loop}$ subalgorithm to remove or "cut out" a loop from a loop system. The latter algorithm will be defined later, but it will probably look quite similar. It will certainly have to call $\text{add}\textunderscore\text{loop}$ for inner loop systems, just like $\text{add}\textunderscore\text{loop}$ calls it. This effectively adds recursion to both algorithms, which is unavoidable unless iteration is used instead. However, an iterative algorithm would most likely be significantly more complicated.
