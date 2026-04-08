#include "comparison_engine.h"

#include <sstream>

std::string ComparisonEngine::recommend(
    const ProductFeature& first,
    const ProductFeature& second,
    const std::string& prompt
) const {
    int firstScore = first.camera + first.performance + first.battery;
    int secondScore = second.camera + second.performance + second.battery;

    const ProductFeature& winner = firstScore >= secondScore ? first : second;
    const ProductFeature& loser = firstScore >= secondScore ? second : first;

    std::ostringstream out;
    out << "Prompt: " << prompt << "\n";
    out << "Recommended: " << winner.title << "\n";
    out << winner.title << " looks stronger for the current scoring profile than " << loser.title << ".";
    return out.str();
}
