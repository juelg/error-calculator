import sympy
import numpy as np
from math import sqrt
from typing import Dict, Tuple, Sequence, List
from math import floor, log10


class LatexEngin(object):
    # todo add option possibility like breaks, num,
    # todo add combinded calculation str
    # todo solution for simga calculation

    def __init__(self, var_object: 'Variable', dict: Dict[str, sympy.Symbol], formel,
                 var_list, dict_symbols: Dict[sympy.Symbol, str]):
        self.sys, self.stat, self.overall, self.value = LatexEngin.partial_str(var_object, dict, formel, dict_symbols)


    @staticmethod
    def partial_str(self, dict: Dict[str, sympy.Symbol], formel, var_list, dict_symbols: Dict[sympy.Symbol, str]):
        my_str_sys = ""
        my_str_stat = ""

        # create strings with partial derivatives
        for i in var_list:
            if i.sys != 0:
                # renter latex code for the systematic error formular
                my_str_sys += "+\\abs{{ \\frac{{\\partial {}}}{{\\partial {}}} \\Delta {}_{{\\rm sys}} }}".format(
                    self.latex, i.latex, i.latex)
            if i.stat != 0:
                # renter latex code for the statistic error formular
                my_str_stat += "+{{\\left( \\frac{{\\partial {}}}{{\\partial {}}}\\Delta {}_{{\\rm stat}}" \
                               " \\right) }}^2".format(self.latex, i.latex, i.latex)

        # add square root and absolut signs
        my_str_sys = "\\Delta {}_{{\\rm sys}} = ".format(self.latex) + my_str_sys[1:] + "="
        my_str_stat = "\\Delta {}_{{\\rm stat}} = \\sqrt{{\\begin{{multlined}}[b]".format(self.latex) \
                      + my_str_stat[1:] + "\\end{multlined}  }=\\sqrt{ \\begin{multlined}[b]"

        my_str_stat_temp = ""
        my_str_sys_temp = ""
        for i in var_list:
            formel_diff = formel.diff(dict[i.varname])
            formel_latex = sympy.latex(formel_diff, symbol_names=dict_symbols)
            if i.sys != 0:
                my_str_sys_temp += "+\\abs{{ {}\\cdot \\Delta {}_{{\\rm sys}} }}".format(formel_latex, i.latex)
            if i.stat != 0:
                my_str_stat_temp += "+{{ \\left( {} \\cdot \\Delta {}_{{\\rm stat}} \\right) }}^2".format(formel_latex,
                                                                                                          i.latex)

        my_str_sys = my_str_sys + my_str_sys_temp[1:] + "= {}".format(Variable.round_to_n(self.sys, 2))
        my_str_stat = my_str_stat + my_str_stat_temp[1:] + "\\end{{multlined}} }} = {}".format(
            Variable.round_to_n(self.stat, 2))

        my_str_overall = "\\Delta {} = \\Delta {}_{{\\rm sys}} + \\Delta {}_{{\\rm stat}} = {}".format(self.latex,
                                                                                                       self.latex,
                                                                                                       self.latex,
                                                                                                       Variable.round_to_n(
                                                                                                           self.overall_err(),
                                                                                                           2))

        my_str_sys = my_str_sys.replace("\\\\", "\\")
        my_str_stat = my_str_stat.replace("\\\\", "\\")
        my_str_overall = my_str_overall.replace("\\\\", "\\")
        my_str_value_formular = LatexEngin.value_formular(self, formel, dict_symbols).replace("\\\\", "\\")

        return my_str_sys, my_str_stat, my_str_overall, my_str_value_formular

    @staticmethod
    def value_formular(self, formular, dict: Dict[sympy.Symbol, str]):  # var_list,
        err = self.overall_err()
        n = Variable.round_return(err, 1)
        la = sympy.latex(formular, symbol_names=dict)
        return "{} = {} = ({}\\pm {})".format(self.latex, la, round(self.value, n), round(err, n))



# todo einheiten
# todo englisch
# todo add möglichkeit für \num
# todo add plotting
# todo add excel file öffnungs möglichkeit
class Variable(object):

    def __init__(self, varname, value=0.0, latex=None, sys=0.0, stat=0.0):
        self.varname = varname
        self._latex = latex
        self.sys = sys
        self.stat = stat
        self.value = value

    def value_exact(self):
        return "{}={}".format(self.latex, self.value)

    def __str__(self):
        err = self.overall_err()
        n = Variable.round_return(err, 1)
        return "({}\\pm {})".format(round(self.value, n), round(err, n))



    @property
    def latex(self):
        if not self._latex:
            return self.varname
        else:
            return self._latex

    def calc_stat(self, stat: List[float], stud_t=None):
        stat = np.array(stat)

        mean = Variable.mittel_wert(stat)
        self.value = mean
        var = Variable.stand_abweich(stat)
        student_t = [-1, -1, 1.3, 0.76, 0.6, 0.51, 0.45, -1, 0.38, -1, 0.34, 0.32, 0.19, 0.14, 0.10, 0.07]
        if not stud_t:
            stud_t = student_t[len(stat)]
        self.stat = stud_t * var

        stat_mean = "\\overline{{ {} }} = \\dfrac{{1}}{{n}}\\sum\\limits_{{i=1}}^{{n}}{}_i = {}".format(self.latex,
                                                                                                        self.latex,
                                                                                                        mean)
        stat_sigma = "\\sigma_{{ {} }} = \\sqrt{{\\dfrac{{1}}{{n-1}}\\sum\\limits_{{i=1}}^{{n}}({}_i-" \
                     "\\overline{{ {} }})^2}} = {}".format(self.latex, self.latex, self.latex, var)

        stat_deviation = "\\Delta {}_{{\\rm stat}} = \\dfrac{{t}}{{\\sqrt{{n}}}}\\sigma_{{ {} }} = {} " \
                         "\cdot \\sigma_{{ {} }} = {}".format(self.latex, self.latex, stud_t, self.latex, self.stat)

        self._latex = "\\overline{{ {} }}".format(self.latex)

        return stat_mean, stat_sigma, stat_deviation

    def overall_err(self):
        return self.sys + self.stat


    def calc_err(self, formel: str, var_list: List['Variable']):
        # todo change var names to english names and consitant with sys and stat
        dict = {}
        dict_symbols = {}
        for i in var_list:
            dict[i.varname] = sympy.Symbol(i.varname)
            dict_symbols[sympy.Symbol(i.varname)] = i.latex

        sym_formel = sympy.sympify(formel)

        # calculate errors
        sys = 0
        stat = 0
        for i in var_list:
            sysformel_ = sym_formel.diff(dict[i.varname])
            for j in var_list:
                sysformel_ = sysformel_.subs(dict[j.varname], j.value)

            statformel = sysformel_ * i.stat
            sysformel = i.sys * sysformel_
            sys += abs(sysformel.evalf())
            stat += statformel.evalf() ** 2

        self.sys = sys
        self.stat = sqrt(stat)

        # calculate the actual value
        sym_formel_ = sym_formel
        for i in var_list:
            sym_formel = sym_formel.subs(dict[i.varname], i.value)
        self.value = sym_formel.evalf()

        return LatexEngin(self, dict, sym_formel_, var_list, dict_symbols)

    # todo do with numpy function
    @staticmethod
    def mittel_wert(arr):
        return 1 / len(arr) * sum(arr)

    @staticmethod
    def round_to_n(x, n):
        if x == 0:
            return 0
        n = abs(n) - 1
        return round(x, -int(floor(log10(abs(x)) - n)))

    @staticmethod
    def round_return(x, n):
        if x == 0:
            return 0
        n = abs(n) - 1
        return -int(floor(log10(abs(x)) - n))

    @staticmethod
    def stand_abweich(arr):
        mittel_wert = Variable.mittel_wert(arr)
        summe = 0
        for i in arr:
            summe += (i - mittel_wert) ** 2
        return sqrt(1 / (len(arr) - 1) * summe)


if __name__ == "__main__":
    v1 = Variable("Rgw", value=6.34, latex="R_{gw}", sys=0.0526, stat=0.02)
    v2 = Variable("Rgsl", value=6.56, latex="R_{gsl}", sys=0.0526, stat=0.02)

    v3 = Variable("Rg", latex="R_G")
    re = v3.calc_err("Rgw - Rgsl", [v1, v2])

    print(re[0])
    print(re[1])
    print(re[2])
    print(re[3])
    print(re[4])
