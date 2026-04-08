#pragma once

#include <string>
#include <vector>

struct ProductFeature {
    std::string title;
    int battery;
    int camera;
    int performance;
    int price;
};

class ComparisonEngine {
public:
    std::string recommend(
        const ProductFeature& first,
        const ProductFeature& second,
        const std::string& prompt
    ) const;
};
