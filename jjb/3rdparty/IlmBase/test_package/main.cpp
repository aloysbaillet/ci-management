#include <iostream>

#include <ImathVec.h>

using namespace IMATH_INTERNAL_NAMESPACE;


int main (int argc, char *argv[])
{
    Vec2<float> v(3, 4);
    std::cout << "IlmBase math library says length(3,4) is " << v.length() << std::endl;
    return EXIT_SUCCESS;
}
