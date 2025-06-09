#pragma once

#include "raylib.h"

class Hindernisse {
public:
    Hindernisse(float x, float y, float width, float height, Color color);

    void Draw() const;

    Rectangle GetRect() const { return rect; }
    int GetPositionX(rect.x);
    int GetPositionY(rect.y);

private:
    Rectangle rect;
    Color color;
};