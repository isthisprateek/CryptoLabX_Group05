cmake_minimum_required(VERSION 3.12)
project(MonoalphabeticSubstitutionCipher)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_executable(mono_cipher
    main.cpp
    cipher.cpp
    analysis.cpp
    cryptanalysis.cpp
    utils.cpp
)
