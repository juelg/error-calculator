import sympy
import numpy as np
from math import sqrt
from typing import Dict, Tuple, Sequence, List
from math import floor, log10


# add consistant type annotations
class LatexEngin(object):
    # todo add option possibility like breaks, num,
    # todo add rounding decimals
    # todo add möglichkeit für \num
    # todo everthing in english


    # def __init__(self, var_object: 'Variable', dict: Dict[str, sympy.Symbol], formel,
    #             var_list, dict_symbols: Dict[sympy.Symbol, str]):
    #    self.sys, self.stat, self.overall, self.value = LatexEngin.partial_str(var_object, dict, formel, dict_symbols)

    def __init__(self, var_object: 'Variable'):
        self.var_object = var_object
        self.overall = self.get_overall()
        self.sys = self.get_err_str("sys")
        self.stat = [self.get_err_str("stat")]
        self.value = self.get_value()

    def set_from_values(self, mean, sigma, deviation, stud_t):
        self.stat = []
        self.stat.append(
            "\\overline{{ {} }} = \\dfrac{{1}}{{n}}\\sum\\limits_{{i=1}}^{{n}}{}_i = {}".format(self.var_object.latex,
                                                                                                self.var_object.latex,
                                                                                                mean))

        self.stat.append("\\sigma_{{ {} }} = \\sqrt{{\\dfrac{{1}}{{n-1}}\\sum\\limits_{{i=1}}^{{n}}({}_i-" \
                         "\\overline{{ {} }})^2}} = {}".format(self.var_object.latex, self.var_object.latex,
                                                               self.var_object.latex, sigma))

        self.stat.append("\\Delta {}_{{\\rm stat}} = \\dfrac{{t}}{{\\sqrt{{n}}}}\\sigma_{{ {} }} = {} " \
                         "\cdot \\sigma_{{ {} }} = {}".format(self.var_object.latex, self.var_object.latex, stud_t,
                                                              self.var_object.latex, deviation))

        # update latex code of the var_object and update strings
        self.var_object._latex = "\\overline{{ {} }}".format(self.var_object.latex)
        self.overall = self.get_overall()
        self.sys = self.get_err_str("sys")
        self.value = self.get_value()

    def set_from_calculation(self, formular, var_list: List['Variable']):
        dict, dict_symbols = Variable.get_symbols_dicts(var_list)
        my_str_sys = ""
        my_str_stat = ""

        # create strings with partial derivatives
        for i in var_list:
            if i.sys != 0:
                # renter latex code for the systematic error formular
                my_str_sys += "+\\abs{{ \\frac{{\\partial {}}}{{\\partial {}}} \\Delta {}_{{\\rm sys}} }}".format(
                    self.var_object.latex, i.latex, i.latex)
            if i.stat != 0:
                # renter latex code for the statistic error formular
                my_str_stat += "+{{\\left( \\frac{{\\partial {}}}{{\\partial {}}}\\Delta {}_{{\\rm stat}}" \
                               " \\right) }}^2".format(self.var_object.latex, i.latex, i.latex)

        # add square root and absolut signs
        my_str_sys = "\\Delta {}_{{\\rm sys}} = ".format(self.var_object.latex) + my_str_sys[1:] + "="
        my_str_stat = "\\Delta {}_{{\\rm stat}} = \\sqrt{{\\begin{{multlined}}[b]".format(self.var_object.latex) \
                      + my_str_stat[1:] + "\\end{multlined}  }=\\sqrt{ \\begin{multlined}[b]"

        my_str_stat_temp = ""
        my_str_sys_temp = ""
        for i in var_list:
            formel_diff = formular.diff(dict[i.varname])
            formel_latex = sympy.latex(formel_diff, symbol_names=dict_symbols)
            if i.sys != 0:
                my_str_sys_temp += "+\\abs{{ {}\\cdot \\Delta {}_{{\\rm sys}} }}".format(formel_latex, i.latex)
            if i.stat != 0:
                my_str_stat_temp += "+{{ \\left( {} \\cdot \\Delta {}_{{\\rm stat}} \\right) }}^2".format(formel_latex,
                                                                                                          i.latex)

        my_str_sys = my_str_sys + my_str_sys_temp[1:] + "= {}".format(Variable.round_to_n(self.sys, 2))
        my_str_stat = my_str_stat + my_str_stat_temp[1:] + "\\end{{multlined}} }} = {}".format(
            Variable.round_to_n(self.stat, 2))

        self.overall = self.get_overall()
        self.value = self.value_formular(formular, var_list)
        self.sys = my_str_sys.replace("\\\\", "\\")
        self.stat = my_str_stat.replace("\\\\", "\\")

    def get_overall(self):
        my_str_overall = "\\Delta {} = \\Delta {}_{{\\rm sys}} + " \
                         "\\Delta {}_{{\\rm stat}} = {}".format(self.var_object.latex,
                                                                self.var_object.latex,
                                                                self.var_object.latex,
                                                                Variable.round_to_n(self.var_object.overall_err(), 2))
        return my_str_overall.replace("\\\\", "\\")

    def get_value(self):
        err = self.var_object.overall_err()
        n = Variable.round_return(err, 1)
        return "{} = ({}\\pm {})".format(self.var_object.latex, round(self.var_object.value, n), round(err, n))

    def get_err_str(self, kind: str):
        return "\\Delta {}_{{\\rm {}}} = {}".format(self.var_object.latex, kind, Variable.round_to_n(self.sys, 2))

    def value_formular(self, formular, var_list: List['Variable']):
        _, dict = Variable.get_symbols_dicts(var_list)
        err = self.var_object.overall_err()
        n = Variable.round_return(err, 1)
        la = sympy.latex(formular, symbol_names=dict)
        return "{} = {} = ({}\\pm {})".format(self.var_object.latex, la, round(self.var_object.value, n),
                                              round(err, n)).replace("\\\\", "\\")


# todo einheiten
# todo add plotting
# todo add excel file öffnungs möglichkeit
class Variable(object):

    def __init__(self, varname, value=0.0, latex=None, sys=0.0, stat=0.0):
        self.varname = varname
        self._latex = latex
        self.sys = sys
        self.stat = stat
        self.value = value
        self.latex_resp = LatexEngin(self)

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

        # stat_mean = "\\overline{{ {} }} = \\dfrac{{1}}{{n}}\\sum\\limits_{{i=1}}^{{n}}{}_i = {}".format(self.latex,
        #                                                                                                 self.latex,
        #                                                                                                 mean)
        # stat_sigma = "\\sigma_{{ {} }} = \\sqrt{{\\dfrac{{1}}{{n-1}}\\sum\\limits_{{i=1}}^{{n}}({}_i-" \
        #              "\\overline{{ {} }})^2}} = {}".format(self.latex, self.latex, self.latex, var)
        #
        # stat_deviation = "\\Delta {}_{{\\rm stat}} = \\dfrac{{t}}{{\\sqrt{{n}}}}\\sigma_{{ {} }} = {} " \
        #                  "\cdot \\sigma_{{ {} }} = {}".format(self.latex, self.latex, stud_t, self.latex, self.stat)

        # create new object to avoid side effects
        self.latex_resp = LatexEngin(self)
        # call has side effects on self object: will change latex code with an overline on it
        self.latex_resp.set_from_values(mean, var, self.stat, stud_t)

        # self._latex = "\\overline{{ {} }}".format(self.latex)
        return self.latex_resp

    def overall_err(self):
        return self.sys + self.stat

    @staticmethod
    def get_symbols_dicts(var_list: List['Variable']):
        dict = {}
        dict_symbols = {}
        for i in var_list:
            dict[i.varname] = sympy.Symbol(i.varname)
            dict_symbols[sympy.Symbol(i.varname)] = i.latex
        return dict, dict_symbols

    def calc_err(self, formular: str, var_list: List['Variable']):

        dict, dict_symbols = Variable.get_symbols_dicts(var_list)
        sym_formular = sympy.sympify(formular)

        # calculate errors
        sys = 0
        stat = 0
        for i in var_list:
            sym_formular_diff = sym_formular.diff(dict[i.varname])
            for j in var_list:
                sym_formular_diff = sym_formular_diff.subs(dict[j.varname], j.value)

            stat_formular = sym_formular_diff * i.stat
            sys_formular = i.sys * sym_formular_diff
            sys += abs(sys_formular.evalf())
            stat += stat_formular.evalf() ** 2

        self.sys = sys
        self.stat = sqrt(stat)

        # calculate the actual value
        sym_formular_calc = sym_formular
        for i in var_list:
            sym_formular_calc = sym_formular_calc.subs(dict[i.varname], i.value)
        self.value = sym_formular_calc.evalf()

        # create new object to avoid side effects
        self.latex_resp = LatexEngin(self)
        self.latex_resp.set_from_calculation(sym_formular, var_list)

        return self.latex_resp

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
