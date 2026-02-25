## 1D Gaussian
Interactive visualization of the univariate Gaussian density

$$
f(x) = \frac{1}{\sqrt{2\pi}\sigma}
\cdot \exp\!\left\{ -\frac{1}{2} \cdot \left(\frac{x-\mu}{\sigma}\right)^2 \right\}\enspace, \quad x\in \mathbb{R} \enspace,
$$

with mean $\mu \in \mathbb{R}$ and standard deviation $\sigma \in \mathbb{R}_+$ .

It was discovered by Karl Friedrich Gauß (1777-1855) in Göttingen, Germany.

### Formulas
- quantile function  
$Q(p) = \mu + \sigma\, \sqrt{2}\, \mathrm{erf}^{-1}(2p-1)$
- uniform to Gaussian  
$x_i^{\text{Gauss}} = Q(x_i^{\text{uni}})$
- golden Kronecker sequence   
$x_i^{\text{uni}}=\mod( \Phi \cdot (i+z), 1) \enspace, \quad i \in \{1,2,\ldots,L\}\enspace, \quad z \in \mathbb{Z}$
- equidistant samples  
$x_i^{\text{uni}} = \frac{2 i - 1 + \gamma}{2 L} \enspace, \quad i \in \{1,2,\ldots,L\}\enspace,\quad \gamma\in[-1,1]$
- unscented (𝐿=2)  
$x_1=\mu-\sigma\enspace, \quad x_2=\mu+\sigma$
- unscented (𝐿=3)  
TODO

### Interactivity
- GUI
- add/remove lines: click in legend
- sampling methods (radiobutton)
- independent identically distributed (iid), the usual random samples
- golden sequence, a low-discrepancy Kronecker sequence based on the golden ratio
- equidistant, with identical amount of probability mass for all samples
- unscented transform sampling (𝐿=2)
- sampling parameter (slider)
- iid: dice again
- golden: integer offset 𝑧
- equidistant: offset 𝛾
- unscented: TODO
- number of Samples 𝐿 (slider)
- density parameters (slider)
- mean 𝜇
- standard deviation 𝜎
