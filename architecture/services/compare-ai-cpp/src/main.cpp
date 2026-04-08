#include "comparison_engine.h"

#include <iostream>

int main() {
    ComparisonEngine engine;

    ProductFeature first{"iPhone 15 Pro", 3274, 48, 9, 12800000};
    ProductFeature second{"iPhone 15 Pro Max", 4422, 48, 10, 14500000};

    std::cout << engine.recommend(first, second, "Qaysi biri menga mos?") << std::endl;
    return 0;
}
