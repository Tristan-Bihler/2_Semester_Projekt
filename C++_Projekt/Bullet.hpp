#pragma once

#include "raylib.h"

class Bullet {
public:
    Bullet(float x, float y, float width, float height, Color color,  Vector2 velocity);

    void Update(float deltaTime);
    void Draw() const;
    bool IsOffScreen(int screenWidth, int screenHeight) const;

    Rectangle GetRect() const { return rect; }

private:
    Rectangle rect;
    Color color;
    //float speed;
    Vector2 velocity;
};