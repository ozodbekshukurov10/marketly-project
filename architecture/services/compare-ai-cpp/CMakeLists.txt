cmake_minimum_required(VERSION 3.16)
project(compare_ai_cpp)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(compare-ai
    src/main.cpp
    src/comparison_engine.cpp
)
