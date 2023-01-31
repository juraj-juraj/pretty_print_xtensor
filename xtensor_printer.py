import gdb
import numpy as np


class printerInterface:
    """Interface for pretty printer implementation

    Defines prototype for children and to_string methods.
    """

    def __init__(self, value: gdb.Value):
        """Saving value to member called mValue"""
        self.value = value

    def children(self) -> tuple:
        """Implement iterator hich gives out data."""
        pass

    def to_string(self) -> str:
        """Implement method to cast whole object to string, printable to the output.
        This method is sort of complementary to children method"""
        pass


def c_to_py_type(c_name: str):
    match(c_name):
        case gdb.TYPE_CODE_FLT | gdb.TYPE_CODE_FLT:
            return float
        case gdb.TYPE_CODE_COMPLEX:
            return complex
        case gdb.TYPE_CODE_INT:
            return int


def fetch_array(begin_it: gdb.Value, end_it: gdb.Value) -> np.array:
    n_size = end_it - begin_it
    # get datatype of one value as is in C++
    d_type = c_to_py_type(begin_it.dereference().type.code)

    return np.fromiter(map(lambda index: d_type((begin_it+index).dereference()), range(n_size)), dtype=d_type)


def shape_from_object(in_val: gdb.Value) -> np.array:
    in_val = str(in_val).strip('{}').replace(' ', '').split(',')
    return np.array([int(i) for i in in_val])


class prettyXarray (printerInterface):
    def __init__(self, value: gdb.Value):
        super().__init__(value)
        if(str(self.value.type) == 'xt::xarray'):
            self.shape = fetch_array(
                self.value['m_shape']['m_begin'], self.value['m_shape']['m_end'])
        elif(str(self.value.type) == 'xt::xtensor'):
            self.shape = shape_from_object(self.value['m_shape']['_M_elems'])

    def children(self):
        if(np.sum(self.shape, dtype=int) == 0):
            return
        # F like fortran style, for collumn major
        order = "F" if str(
            self.value['m_layout']) == "xt::layout_type::column_major" else "C"
        indices = np.nditer(np.zeros(tuple(self.shape)),
                            flags=['multi_index'], order=order)
        it = self.value['m_storage']['p_begin']
        while(it != self.value['m_storage']['p_end']):
            yield(f"{indices.multi_index}", it.dereference())
            it += 1
            indices.iternext()

    def to_string(self):
        return f"{self.value.type} with shape {self.shape}"

    def display_hint(self):
        return 'string'


def xtensor_resolve(val):
    match str(val.type):
        case 'xt::xarray' | 'xt::xtensor':
            return prettyXarray(val)
        case _:
            return


gdb.pretty_printers.append(xtensor_resolve)
