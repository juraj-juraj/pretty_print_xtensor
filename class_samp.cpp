#include <iostream>
#include <string>
#include <xtensor/xarray.hpp>
#include <xtensor/xview.hpp>
#include <xtensor/xfixed.hpp>

class Person{
public:
    Person(std::string name) : mName(std::move(name)) { }

    size_t getLen()
    {
        return mName.length();
    }

private:
    std::string mName;
};

int main(){
    Person p1("Person1");
    int a = 0;
    xt::xarray<double> arr1
        {{1.0, 2.0, 3.0},
         {2.0, 5.0, 7.0},
         {2.0, 5.0, 7.0}};
    auto arr2 = arr1 + 5;
    auto arr3 = arr2 /2;
    auto xview3 = xt::view(arr3, 1, xt::all());
    auto arr3_eval = xt::eval(arr3);
    auto arr3_t = xt::transpose(arr3);

    xt::xtensor<double, 2> xtens1
        {{1.0, 2.0, 3.0},
         {2.0, 5.0, 7.0},
         {2.0, 5.0, 7.0}};


    xt::xtensor_fixed<double, xt::xshape<3, 2>> xtensfix1
        {{1.0, 2.0},
         {2.0, 5.0},
         {2.0, 5.0}};
    
    xt::xtensor_fixed<double, xt::xshape<3, 2, 4>> xtensfix2 {};

    std::cout << "Person len: " << p1.getLen() << std::endl;
}
