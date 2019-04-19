# Physics Error Calculation Library

This library was made for depressed physics student like me who get stressed with the amount of stupid error-prone work that one has to perform for error calcuation. If you are in that situation, maybe you have also already thought if there isn't a way to do this automatically.

And I can give you the answer: Yes there is. This library which will is also able to output the ![equation](https://latex.codecogs.com/gif.latex?%5CLaTeX) code of the calculaton so that you can directly copy and paste it into the error calcuation section of your lab report and focus on the important parts of it.

## Dependencies
* `sympy` for doing basically everthing when it comes to the calculation. But most important deriving
* `numpy` for numpy arrays

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

![equation](https://latex.codecogs.com/gif.latex?v%3D%5Cfrac%7B2l%7D%7B%5CDelta%20t%7D)

where ![equation](https://latex.codecogs.com/gif.latex?l) is the length of the rod and ![equation](https://latex.codecogs.com/gif.latex?%5CDelta%20t) is the time for one oscillation.

Let's say our meassure examples look like this:
* ![equation](https://latex.codecogs.com/gif.latex?l%20%3D%201%7B%5Crm%20m%7D) with a systematic error of ![equation](https://latex.codecogs.com/gif.latex?%5CDelta%20l_%7B%5Crm%20sys%7D%20%3D%200.2%7B%5Crm%20cm%7D) and a statistical error of ![equation](https://latex.codecogs.com/gif.latex?%5CDelta%20l_%7B%5Crm%20stat%7D%20%3D%200.1%7B%5Crm%20cm%7D)
* ![equation](https://latex.codecogs.com/gif.latex?%5CDelta%20t%20%3D%200.38%7B%5Crm%20ms%7D) with only a statistical error of ![equation](https://latex.codecogs.com/gif.latex?%5CDelta%20%28%5CDelta%20t%29_%7B%5Crm%20stat%7D%20%3D%200.001%7B%5Crm%20ms%7D)

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

![equation](https://latex.codecogs.com/gif.latex?v%20%3D%20%5Cfrac%7B2%20l%7D%7B%5CDelta%20t%7D%20%3D%20%285260.0%5Cpm%2020.0%29)

![equation](https://latex.codecogs.com/gif.latex?%5CDelta%20v_%7B%5Crm%20sys%7D%20%3D%20%5Cleft%7C%20%5Cfrac%7B%5Cpartial%20v%7D%7B%5Cpartial%20l%7D%20%5CDelta%20l_%7B%5Crm%20sys%7D%20%5Cright%7C%3D%5Cleft%7C%20%5Cfrac%7B2%7D%7B%5CDelta%20t%7D%5Ccdot%20%5CDelta%20l_%7B%5Crm%20sys%7D%20%5Cright%7C%3D%205.3)

![equation](https://latex.codecogs.com/gif.latex?%5CDelta%20v_%7B%5Crm%20stat%7D%20%3D%20%5Csqrt%7B%7B%5Cleft%28%20%5Cfrac%7B%5Cpartial%20v%7D%7B%5Cpartial%20l%7D%5CDelta%20l_%7B%5Crm%20stat%7D%20%5Cright%29%20%7D%5E2%2B%7B%5Cleft%28%20%5Cfrac%7B%5Cpartial%20v%7D%7B%5Cpartial%20%5CDelta%20t%7D%5CDelta%20%5CDelta%20t_%7B%5Crm%20stat%7D%20%5Cright%29%20%7D%5E2%20%7D%5C%5C%3D%5Csqrt%7B%20%7B%20%5Cleft%28%20%5Cfrac%7B2%7D%7B%5CDelta%20t%7D%20%5Ccdot%20%5CDelta%20l_%7B%5Crm%20stat%7D%20%5Cright%29%20%7D%5E2%2B%7B%20%5Cleft%28%20-%20%5Cfrac%7B2%20l%7D%7B%5CDelta%20t%5E%7B2%7D%7D%20%5Ccdot%20%5CDelta%20%5CDelta%20t_%7B%5Crm%20stat%7D%20%5Cright%29%20%7D%5E2%20%7D%20%3D%2017.0)

![equation](https://latex.codecogs.com/gif.latex?%5CDelta%20v%20%3D%20%5CDelta%20v_%7B%5Crm%20sys%7D%20%2B%20%5CDelta%20v_%7B%5Crm%20stat%7D%20%3D%2023.0)


You can also access every calculation step individually by using `la.sys`, `la.stat`, `la.overall` and `la.value`. The last one will be the calculated value with the error and the formular. These attributes will all be strings except `la.stat` which will be a list of strings

### Advanced Example

Let's say, for the example above you have messured the oscillation times several times to get a more meaningful value. We can also calculate the systematic error of the values:

```python
import numpy as np
# meassured for 11 oscilations
stat_t = np.array([4.24, 4.22, 4.22, 4.2, 4.24])*10**-3
dt2 = Variable("dt", latex="\\Delta t_2")
la = dt1.calc_stat(stat_t, 0.51)
[print(i) for i in la.stat]
```
The first argument of calc_stat is the list of values. This can also be a normal python list. We only used numpy here to multiply the vector with `10**-3`. The second value needs to be the ![equation](https://latex.codecogs.com/gif.latex?%5Cfrac%7Bt%7D%7B%5Csqrt%7Bn%7D%7D) factor for your ![equation](https://latex.codecogs.com/gif.latex?%5Ckappa) of the [student-t distribution](https://en.wikipedia.org/wiki/Student%27s_t-distribution).

This will output the following:
```
\overline{ \Delta t_2 } = \dfrac{1}{n}\sum\limits_{i=1}^{n}\Delta t_2_i = 0.004224
\sigma_{ \Delta t_2 } = \sqrt{\dfrac{1}{n-1}\sum\limits_{i=1}^{n}(\Delta t_2_i-\overline{ \Delta t_2 })^2} = 1.6733200530681657e-05
\Delta \Delta t_2_{\rm stat} = \dfrac{t}{\sqrt{n}}\sigma_{ \Delta t_2 } = 0.51 \cdot \sigma_{ \Delta t_2 } = 8.5e-06
```
With minor changes this will rendert to the following:

![equation](https://latex.codecogs.com/gif.latex?%5Coverline%7B%20%5CDelta%20t_2%20%7D%20%3D%20%5Cdfrac%7B1%7D%7Bn%7D%5Csum%5Climits_%7Bi%3D1%7D%5E%7Bn%7D%5CDelta%20t_%7B2%2Ci%7D%20%3D%200.004224%5C%5C%0A%5Csigma_%7B%20%5CDelta%20t_2%20%7D%20%3D%20%5Csqrt%7B%5Cdfrac%7B1%7D%7Bn-1%7D%5Csum%5Climits_%7Bi%3D1%7D%5E%7Bn%7D%28%5CDelta%20t_%7B2%2Ci%7D-%5Coverline%7B%20%5CDelta%20t_2%20%7D%29%5E2%7D%20%3D%201.7e-05%5C%5C%0A%5CDelta%20%5CDelta%20t_%7B2%5Crm%20stat%7D%20%3D%20%5Cdfrac%7Bt%7D%7B%5Csqrt%7Bn%7D%7D%5Csigma_%7B%20%5CDelta%20t_2%20%7D%20%3D%200.51%20%5Ccdot%20%5Csigma_%7B%20%5CDelta%20t_2%20%7D%20%3D%208.5e-06)

The syntax a![equation](https://latex.codecogs.com/gif.latex?e)b means ![equation](https://latex.codecogs.com/gif.latex?a%5Ccdot%2010%5Eb). Python will always output floting points like this. You should not use this syntax in scientific reports. One way to auto format this correctly in Latex would be to use the command `\num{3.14e3}` from the package `siunitx`. (Including the num command in the latex is already planned to add in a future version)

### Pitfalls

Let's say you want to calculate something like this:
![equation](https://latex.codecogs.com/gif.latex?c%20%3D%20%5Cfrac%7Ba%7D%7Bb%7D)
So you do something like this
```python
a = Variable("a", value=..., sys=..., stat=...)
b = Variable("b", value=..., sys=..., stat=...)
c = Variable("c")
c.calc("a/b", [a, b])
```
And then you would like to calculate
![equation](https://latex.codecogs.com/gif.latex?d%20%3D%20a%5Ccdot%20c)
So you would do
```python
d = Variable("d")
d.calc("a*c", [a, c])
```
In this case we would derive once for a and once for c, because in the current design only the error values will be remembered and not the formulars. But this would be wrong because c consists of a. For getting the correct value in cases like this where we multiply, devide etc. by a value that was already used in the calculation before we need to write out c as ![equation](https://latex.codecogs.com/gif.latex?%5Cfrac%7Ba%7D%7Bb%7D):
```python
d = Variable("d")
d.calc("a*a/b", [a, b])
```

## Contribution

Everyone is welcome to contribute to this package! Feel free to open a pull request.