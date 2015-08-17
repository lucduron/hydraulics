Free Surface
============

The TELEMAC-2D code solves the following four hydrodynamic equations simultaneously:

* Continuity Equation:
$$ \frac{\partial h}{\partial t} + \overrightarrow{u}\cdot\overrightarrow{\nabla}h + h.div(\overrightarrow{u}) = S_{h} $$
* 1st Momentum Equation:
$$ \frac{\partial u}{\partial t} + \overrightarrow{u}\cdot\overrightarrow{\nabla}u = -g.\frac{\partial Z}{\partial x} + S_{x} + \frac{1}{h}div(h\nu_{t}\overrightarrow{\nabla}u}) $$
* 2nd Momentum Equation:
$$ \frac{\partial v}{\partial t} + \overrightarrow{u}\cdot\overrightarrow{\nabla}v = -g.\frac{\partial Z}{\partial y} + S_{y} + \frac{1}{h}div(h\nu_{t}\overrightarrow{\nabla}v}) $$
* Tracer Conservation Equation:
$$ \frac{\partial T}{\partial t} + \overrightarrow{u}\cdot\overrightarrow{\nabla}T = + S_{T} + \frac{1}{h}div(h\nu_{T}\overrightarrow{\nabla}T}) $$
