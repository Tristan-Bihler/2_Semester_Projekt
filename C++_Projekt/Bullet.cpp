#include "Bullet.hpp"
#include "raylib.h"

Bullet::Bullet(float x, float y, float width, float height, Color color, float speed)
    : rect({x, y, width, height}), color(color), speed(speed) {
}

void Bullet::Update(float deltaTime) {
    // Bullets move upwards
    rect.y -= speed * deltaTime;
}

void Bullet::Draw() const{
    DrawRectangleRec(rect, color);
}

bool Bullet::IsOffScreen(int screenWidth, int screenHeight) const {
    // Check if the bullet is completely outside the screen
    return rect.x < -rect.width || rect.x > screenWidth ||
           rect.y < -rect.height || rect.y > screenHeight;
}