#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>   

#include <cstddef>

namespace py = pybind11;

// In-place scale (true zero-copy)

void scale_inplace(py::array_t<float> input, float factor) {
    py::buffer_info buf = input.request();

    if (buf.ndim != 1) {
        throw std::runtime_error("Input must be a 1-D array");
    }

    if (!input.writeable()) {
        throw std::runtime_error("Input array is not writeable");
    }

    float* ptr = static_cast<float*>(buf.ptr);
    size_t size = buf.shape[0];

    for (size_t i = 0; i < size; ++i) {
        ptr[i] *= factor;   
    }
}

// Return a new scaled NumPy array

py::array_t<float> scale_new(py::array_t<float> input, float factor) {
    py::buffer_info buf = input.request();

    if (buf.ndim != 1) {
        throw std::runtime_error("Input must be a 1-D array");
    }

    float* in_ptr = static_cast<float*>(buf.ptr);
    size_t size = buf.shape[0];

    py::array_t<float> output(size);
    py::buffer_info out_buf = output.request();
    float* out_ptr = static_cast<float*>(out_buf.ptr);

    for (size_t i = 0; i < size; ++i) {
        out_ptr[i] = in_ptr[i] * factor;
    }

    return output;  
}

PYBIND11_MODULE(fast_scale, module) {
    module.def("scale_inplace", &scale_inplace,
               pybind11::arg("input"),
               pybind11::arg("factor"),
               "Scale a NumPy array in-place (zero-copy)");

    module.def("scale_new", &scale_new,
               pybind11::arg("input"),
               pybind11::arg("factor"),
               "Return a new scaled NumPy array");
}