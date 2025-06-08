#include "raylib.h"
#include <cmath> // For std::sqrt
#include "Hindernisse.hpp"

Hindernisse::Hindernisse(float x, float y, float width, float height, Color color)
    : rect({x, y, width, height}), color(color){
    }

void Hindernisse::Draw() const{
    DrawRectangleRec(rect, color);
}

