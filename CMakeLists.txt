cmake_minimum_required(VERSION 3.16)
set (CMAKE_CXX_STANDARD 17)
project("sample_class")
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(class_samp class_samp.cpp)
target_link_libraries(class_samp ${CONAN_LIBS})
