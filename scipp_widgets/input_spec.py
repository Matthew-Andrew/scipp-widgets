# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (c) 2020 Scipp contributors (https://github.com/scipp)
# @file
# @author Matthew Andrew
import ipywidgets as widgets


class InputSpec():
    """
    Controls creation and validaton of user-input widgets.
    """
    def __init__(self,
                 name,
                 validator=lambda input: input,
                 options=(),
                 tooltip='',
                 eval_input=False,
                 scope={}):
        """
        Parameters:
        name (str): Name of function argument this input corresponds to.
        validator (Callable[[str], Any]): Validator function.
        options (List[str]): List of dropdown options.
        tooltip (str): Widget placeholder text.
        eval_input (bool): Toggles evaluating input in calling scope.
        scope (Dict[str: Any]): Non default scope to use for evaluation.
        """
        self._name = name
        self._options = options
        self._tooltip = tooltip if tooltip else name

        if eval_input:
            scope = scope if scope else get_notebook_global_scope()
            self._validator = lambda input: validator(eval(input, scope))
        else:
            self._validator = validator

    def create_input_widget(self):
        """
        Creates and returns the relevant user-input ipywidget.
        """
        return widgets.Combobox(placeholder=self._tooltip,
                                continuous_update=False,
                                options=self._options)

    def validate(self, input):
        """
        Validates the user input. Throws if invalid,
        otherwise returns the input with pre-processing
        applied if applicable
        """
        return self._validator(input)

    @property
    def name(self):
        """
        Property holding name of function argument this input corresponds to.
        """
        return self._name


def get_notebook_global_scope():
    """
    This gets the global scope of the notebook. It
    assumes the first module called __main__ on the stack
    is the correct one.
    """
    import inspect
    for module in inspect.stack():
        if module[0].f_globals['__name__'] == '__main__':
            return module[0].f_globals
