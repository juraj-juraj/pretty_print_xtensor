#include <iostream>
#include <string>

#include <xtensor/xfixed.hpp>
#include <xtensor/xlayout.hpp>
#include <xtensor/xview.hpp>
#include <xtensor/xarray.hpp>

int main() {
  xt::xarray<int> a2 = {};
  xt::xarray<double> arr1{{1.0, 2.0, 3.0}, {2.0, 5.0, 7.0}, {2.0, 5.0, 7.0}};
  auto xview1 = xt::view(arr1, 1, xt::all());
  auto xrow1 = xt::row(arr1, 0);
  auto trans1 = xt::transpose(arr1);
  auto arr2 = arr1 + 5;
  auto arr3 = arr2 / 2;
  auto xview3 = xt::view(arr3, 1, xt::all());
  auto arr3_eval = xt::eval(arr3);
  auto arr3_t = xt::transpose(arr3);

  xt::xtensor<double, 2> xtens1{
      {1.0, 2.0, 3.0}, {2.0, 5.0, 7.0}, {2.0, 5.0, 7.0}};

  xt::xtensor<double, 2> xtens2;

  xt::xtensor_fixed<double, xt::xshape<3, 2>> xtensfix1{
      {1.0, 2.0}, {2.0, 5.0}, {2.0, 5.0}};

  xt::xtensor_fixed<double, xt::xshape<3, 2, 4>> xtensfix2{};
  xt::xarray<int> a3 = {{{1, 2, 3, 4}, {6, 7, 8, 9}}};

  xt::xarray<double, xt::layout_type::row_major> ar{
      {1.0, 2.0, 3.0}, {2.0, 5.0, 7.0}, {2.0, 5.0, 7.0}};
  xt::xarray<double, xt::layout_type::column_major> ac{
      {1.0, 2.5, 3.0}, {2.0, 5.0, 7.0}, {2.0, 5.0, 7.0}};
}
