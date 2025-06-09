#pragma once

#include "raylib.h"

class Bullet {
private:
    Rectangle rect;
    int bullet_damage;
    Color color;
    //float speed;
    Vector2 velocity;
public:
    Bullet(float x, float y, float width, float height,int bullet_damage, Color color,  Vector2 velocity);

    void Update(float deltaTime);
    void Draw() const;
    bool IsOffScreen(int screenWidth, int screenHeight) const;

    int GetBulletDamage() const {return bullet_damage;};

    Rectangle GetRect() const { return rect; }


};