cmake_minimum_required(VERSION 3.2)

#------------------------------------------------ DEPENDENCIES
if (NOT (DEFINED ENV{CHITECH_ROOT}))
    set(CHI_TECH_DIR    "/Users/zacharyhardy/Projects/chi-tech/chi-tech")
else()
    set(CHI_TECH_DIR    "$ENV{CHI_TECH_DIR}")
endif()
message(STATUS "CHI_TECH_DIR set to ${CHI_TECH_DIR}")

#================================================ Set project targets
SET(TARGET LBKEigenvalueSolver)
project(${TARGET} C CXX)

#================================================ Set cmake variables
if (NOT DEFINED CMAKE_RUNTIME_OUTPUT_DIRECTORY)
    set(CMAKE_RUNTIME_OUTPUT_DIRECTORY "${PROJECT_SOURCE_DIR}/bin")
    set(CONFIG_FILE_NAME "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/config.cmake")
endif()

#================================================ Include macros
include("${CHI_TECH_DIR}/ChiResources/Macros/Downstream.cmake")

#================================================ Default include directories
include_directories("${PROJECT_SOURCE_DIR}/LBKEigenvalueSolver")

#================================================ Define source directories
add_subdirectory("${PROJECT_SOURCE_DIR}/LBKEigenvalueSolver")

#================================================ Create executable
add_library(LBKESLib ${SOURCES})
add_executable(${TARGET} "run.cc")
target_link_libraries(LBKESLib ${CHI_LIBS})
target_link_libraries(${TARGET} LBKESLib)

# |------------ Write Makefile to root directory
file(WRITE ${PROJECT_SOURCE_DIR}/Makefile "subsystem:\n" "\t$(MAKE) -C chi_build \n\n"
        "clean:\n\t$(MAKE) -C chi_build clean\n")

