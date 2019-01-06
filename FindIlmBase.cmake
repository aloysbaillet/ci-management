
set(ILMBASE_ROOT ${CONAN_ILMBASE_ROOT} CACHE PATH "Path to ILMBase root path")

# Find include dirs
find_path(ILMBASE_INCLUDE_DIRS
	NAMES IlmBaseConfig.h
	HINTS ${ILMBASE_ROOT}/include ${ILMBASE_ROOT}/include/OpenEXR
)

# Look for libraries
foreach(LIBNAME Half Iex IexMath IlmThread Imath)
	find_library(ILMBASE_${LIBNAME}_LIBRARY
		NAMES ${LIBNAME}
        HINTS ${ILMBASE_ROOT}/lib
        PATH_SUFFIXES lib
        )
endforeach()

# Check version
file(STRINGS ${ILMBASE_INCLUDE_DIRS}/IlmBaseConfig.h TMP REGEX "#define ILMBASE_VERSION_STRING.*$")
string(REGEX MATCHALL "[0-9.]+" ILMBASE_VERSION ${TMP})

# handle the QUIETLY and REQUIRED arguments and set xxx_FOUND to TRUE
include(FindPackageHandleStandardArgs)
find_package_handle_standard_args(IlmBase
    REQUIRED_VARS
        ILMBASE_INCLUDE_DIRS
        ILMBASE_Half_LIBRARY
        ILMBASE_Iex_LIBRARY
        ILMBASE_IexMath_LIBRARY
        ILMBASE_IlmThread_LIBRARY
        ILMBASE_Imath_LIBRARY
    VERSION_VAR
        ILMBASE_VERSION
)


# Create imported targets
if(ILMBASE_FOUND)
    # TODO: Create imported targets (CMake version?)
    set(ILMBASE_LIBRARIES ${CONAN_LIBS_ILMBASE})
endif()


mark_as_advanced(MYPACKAGE_LIBRARY
    ILMBASE_Half_LIBRARY
    ILMBASE_Iex_LIBRARY
    ILMBASE_IexMath_LIBRARY
    ILMBASE_IlmThread_LIBRARY
    ILMBASE_Imath_LIBRARY)

if(ILMBASE_FOUND)
	mark_as_advanced(ILMBASE_ROOT)
endif()
