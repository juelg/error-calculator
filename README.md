# Physics Error Calculation Library

This library was made for every depressed physics student who gets confused with the amount of stupid error-prone work that one has to perform for error calcuation. My you have already thought if there isn't a way to do this autmoatically: Yes, there is. This library does the error calcuation fully automatically and even gives you the latex code back.
You shouldn't be busy by writing down some latex formulars, but instead focusing on the important stuff at your report
So, that you can focus on the important part of your report instead of writing down derivatives of formulars in latex taking you hours.
## Dependencies
* `sympy`
* `numpy`

## Installation
The most easiest way to install the package is via the python package manager pip since it is shipped with python upon version 3.4+:
`sudo pip3 install ...`
or the following if pip is not in the system enviorment variables:
`sudo python3 -m pip install ...`



Alternatively, you can also download the repository via the link above or clone it via
`git clone https://github.com/JobiProGrammer/error-calculator.git`
After cloing navigate into the directory and install it via
`sudo python3 setup.py install`


On Windows you have to use administrator rights instead of the `sudo` keyword. 

## Examples

### Basic Example
Let's assume we want to calculate the speed of sound of specific material. Therefore, we meassure the vibriation with a pieco cristall at one end of a rod. Because the sound will oscillate in the rod we can get the speed of sound via the following formular:

$$v=\frac{2l}{\Delta t}$$

where $l$ is the length of the rod and $\Delta t$ is the time for one oscillation.

Let's say our meassure examples look like this:
* $l = 1{\rm m}$ with a systematic error of $\Delta l_{\rm sys} = 0.2{\rm cm}$ and a statistical error of $\Delta l_{\rm stat} = 0.1{\rm cm}$
* $\Delta t = 0.38{\rm ms}$ with only a statistical error of $\Delta (\Delta t)_{\rm stat} = 0.001{\rm ms}$

First, we need to import the library:

```python
from error_calculator import Variable, LatexEngin
```
We can then define the varibales:

```python
l = Variable("l", value=100*10**-2, stat=0.2*10**-2, sys=0.1*10**-2)
dt = Variable("dt", latex="\\Delta t", value=0.38*10**-3, stat=0.001*10**-3)
```
A variable is defined with the `Variable` class. The firs argment the we needs to pass is the name that we will later use in the formular. Then, a optional latex string, that will be used for the rendering function later on. If no string is given, the formular name (first argument) will be used. After that, you can give a value, statistical and systematical error.

The error calculation would then be as follows:

```python
v = Variable("v")
la = v.calc("2*l/dt", [l, dt])
```
To caculate the value we simply create another Variable that will be our result and then we call the `.calc` function on it. The first argument needs to be the formular with the variable names defined in the Variables and the second a python list of the Variable objects that are needed for the calculation.

The formular string needs to be in [sympy sympify syntax](https://docs.sympy.org/latest/modules/core.html#module-sympy.core.sympify). But normally, you can just use normal python syntax. Be careful with a power function, the syntax for that would be `**`

Now, you can access the calculated value by using `v.value`. A correct roundend version according to the error can be accessed by `v.value()`.
Systematic and statistic error can be used by `v.sys` and `v.stat`. Also, the variable `v` can now used to do further calculation just like `l`. Since both systematic and statistic error are stored seperately you do not have to remember which was which for the next calculation.

But the best part of the library comes now: The returned object that we called `la` in our example can print the whole calculaton process in latex syntax:

```python
print(la)
```
will give the following output

```bash
v = \frac{2 l}{\Delta t} = (5260.0\pm 20.0)

\Delta v_{\rm sys} = \abs{ \frac{\partial v}{\partial l} \Delta l_{\rm sys} }=\abs{ \frac{2}{\Delta t}\cdot \Delta l_{\rm sys} }= 5.3

\Delta v_{\rm stat} = \sqrt{\begin{multlined}[b]{\left( \frac{\partial v}{\partial l}\Delta l_{\rm stat} \right) }^2+{\left( \frac{\partial v}{\partial \Delta t}\Delta \Delta t_{\rm stat} \right) }^2\end{multlined}  }=\sqrt{ \begin{multlined}[b]{ \left( \frac{2}{\Delta t} \cdot \Delta l_{\rm stat} \right) }^2+{ \left( - \frac{2 l}{\Delta t^{2}} \cdot \Delta \Delta t_{\rm stat} \right) }^2\end{multlined} } = 17.0

\Delta v = \Delta v_{\rm sys} + \Delta v_{\rm stat} = 23.0
```

which in latex will render to
$$v = \frac{2 l}{\Delta t} = (5260.0\pm 20.0)$$

$$\Delta v_{\rm sys} = \left| \frac{\partial v}{\partial l} \Delta l_{\rm sys} \right|=\left| \frac{2}{\Delta t}\cdot \Delta l_{\rm sys} \right|= 5.3$$

$$\Delta v_{\rm stat} = \sqrt{{\left( \frac{\partial v}{\partial l}\Delta l_{\rm stat} \right) }^2+{\left( \frac{\partial v}{\partial \Delta t}\Delta \Delta t_{\rm stat} \right) }^2 }\\=\sqrt{ { \left( \frac{2}{\Delta t} \cdot \Delta l_{\rm stat} \right) }^2+{ \left( - \frac{2 l}{\Delta t^{2}} \cdot \Delta \Delta t_{\rm stat} \right) }^2 } = 17.0$$

$$\Delta v = \Delta v_{\rm sys} + \Delta v_{\rm stat} = 23.0$$


You can also access every calculation step individually by using `la.sys`, `la.stat`, `la.overall` and `la.value`. The last one will be the calculated value with the error and the formular. These attributes will all be strings except `la.stat` which will be a list of strings

### Advanced Examples

### Pitfalls

## Contribution