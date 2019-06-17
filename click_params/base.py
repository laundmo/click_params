"""Base classes to implement various parameter types"""
import click

from .annotations import Min, Max


class RangeParamType(click.ParamType):

    def __init__(self, param_type: click.ParamType, minimum: Min = None, maximum: Max = None, clamp: bool = False):
        self._minimum = minimum
        self._maximum = maximum
        self._clamp = clamp
        self._param_type = param_type

    def convert(self, value, param, ctx):
        converted_value = self._param_type.convert(value, param, ctx)
        inferior_to_minimum = self._minimum is not None and converted_value < self._minimum
        superior_to_maximum = self._maximum is not None and converted_value > self._maximum

        if self._clamp:
            if inferior_to_minimum:
                return self._minimum
            if superior_to_maximum:
                return self._maximum

        if inferior_to_minimum or superior_to_maximum:
            if self._minimum is None:
                self.fail(f'{converted_value} is bigger than the maximum valid value {self._maximum}.', param, ctx)
            elif self._maximum is None:
                self.fail(f'{converted_value} is smaller than the minimum valid value {self._minimum}.', param, ctx)
            else:
                self.fail(f'{converted_value} is not in the valid range of {self._minimum} to {self._maximum}.',
                          param, ctx)
        return converted_value

    def __repr__(self):
        parts = self.name.split(' ')
        titles = [part.title() for part in parts]
        new_name = ''.join(titles)
        return f'{new_name}({repr(self._minimum)}, {repr(self._maximum)})'