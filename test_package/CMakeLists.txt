project(PackageTest)
cmake_minimum_required(VERSION 2.8)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

find_package(IlmBase ${ILMBASE_VERSION} EXACT REQUIRED)

message(STATUS "IlmBase libraries: ${ILMBASE_LIBRARIES}")
message(STATUS "IlmBase include dirs: ${ILMBASE_INCLUDE_DIRS}")

add_executable(testPackage main.cpp testMatrix.cpp)
target_link_libraries(testPackage ${ILMBASE_LIBRARIES})

