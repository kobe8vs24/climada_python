"""
Define Entity Class.
"""

import os

from climada.entity.loader import Loader
from climada.entity.impact_funcs.base  import ImpactFuncs
from climada.entity.impact_funcs.source_excel  import ImpactFuncsExcel
from climada.entity.impact_funcs.source_mat  import ImpactFuncsMat
from climada.entity.discounts.base import Discounts
from climada.entity.discounts.source_excel import DiscountsExcel
from climada.entity.discounts.source_mat import DiscountsMat
from climada.entity.measures.base import Measures
from climada.entity.measures.source_excel import MeasuresExcel
from climada.entity.measures.source_mat import MeasuresMat
from climada.entity.exposures.base import Exposures
from climada.entity.exposures.source_excel import ExposuresExcel
from climada.entity.exposures.source_mat import ExposuresMat
from climada.util.config import ENT_DEF_XLS

class Entity(Loader):
    """Collects exposures, impact functions, measures and discount rates.

    Attributes
    ----------
        exposures (Exposures): exposures
        impact_funcs (ImpactFucs): vulnerability functions
        measures (Measures): measures
        discounts (Discounts): discount rates
        def_file (str): name of the xls file used as default source data
    """

    def_file = ENT_DEF_XLS

    def __init__(self, file_name=None, description=None):
        """Fill values from file. Default file used when no file provided.

        Parameters
        ----------
            file_name (str, optional): name of the source file with supported
                format (xls, xlsx and mat)
            description (str, optional): description of the source data

        Raises
        ------
            ValueError

        Examples
        ---------
            >>> Entity()
            Builds an Entity with the values obtained from ENT_DEF_XLS file.
            >>> Entity(filename)
            Builds an Entity with the values obtained from filename file.
            >>> Entity(impact_funcs=myimpact_funcs, measures=mymeasures)
            Builds an Entity with exposures and discount rates from
            ENT_DEF_XLS file, and the given impact functions and measures.
        """
        if file_name is None:
            self._exposures = ExposuresExcel(self.def_file)
            self._impact_funcs = ImpactFuncsExcel(self.def_file)
            self._measures = MeasuresExcel(self.def_file)
            self._discounts = DiscountsExcel(self.def_file)
        else:
            self.load(file_name, description)

    def read(self, file_name, description=None):
        """Override read Loader method."""
        # Call readers depending on file extension
        extension = os.path.splitext(file_name)[1]
        if extension == '.mat':
            self._exposures = ExposuresMat()
            self._exposures.read(file_name, description)

            self._impact_funcs = ImpactFuncsMat()
            self._impact_funcs.read(file_name, description)

            self._discounts = DiscountsMat()
            self._discounts.read(file_name, description)

            self._measures = MeasuresMat()
            self._measures.read(file_name, description)

        elif (extension == '.xlsx') or (extension == '.xls'):
            self._exposures = ExposuresExcel()
            self._exposures.read(file_name, description)

            self._impact_funcs = ImpactFuncsExcel()
            self._impact_funcs.read(file_name, description)

            self._discounts = DiscountsExcel()
            self._discounts.read(file_name, description)

            self._measures = MeasuresExcel()
            self._measures.read(file_name, description)

        else:
            raise TypeError('Input file extension not supported: %s.' % \
                            extension)

    def check(self):
        """ Override Loader check."""
        self._discounts.check()
        self._exposures.check()
        self._impact_funcs.check()
        self._measures.check()

    @property
    def tags(self):
        return [self._exposures.tag, self._impact_funcs.tag,
                self._measures.tag, self._discounts.tag]

    @property
    def exposures(self):
        return self._exposures

    @exposures.setter
    def exposures(self, value):
        if not isinstance(value, Exposures):
            raise ValueError("Input value is not (sub)class of Exposures.")
        self._exposures = value

    @property
    def impact_funcs(self):
        return self._impact_funcs

    @impact_funcs.setter
    def impact_funcs(self, value):
        if not isinstance(value, ImpactFuncs):
            raise ValueError("Input value is not (sub)class of ImpactFuncs.")
        self._impact_funcs = value

    @property
    def measures(self):
        return self._measures

    @measures.setter
    def measures(self, value):
        if not isinstance(value, Measures):
            raise ValueError("Input value is not (sub)class of Measures.")
        self._measures = value

    @property
    def discounts(self):
        return self._discounts

    @discounts.setter
    def discounts(self, value):
        if not isinstance(value, Discounts):
            raise ValueError("Input value is not (sub)class of Discounts.")
        self._discounts = value