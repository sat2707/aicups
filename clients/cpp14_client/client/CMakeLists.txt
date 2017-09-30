cmake_minimum_required(VERSION 2.6)
project(cppclient)

SET(CMAKE_CXX_FLAGS "-D_LINUX -g -std=c++14 -g -Wall -Wno-unknown-pragmas")

FILE(GLOB sources core/*.cpp csimplesocket/*.cpp csimplesocket/*.h)
add_executable(cppclient main.cpp ${sources})

install(TARGETS cppclient RUNTIME DESTINATION bin)

