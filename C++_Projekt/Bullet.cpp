#include "Bullet.hpp"
#include "raylib.h"

Bullet::Bullet(float x, float y, float width, float height, Color color, Vector2 velocity)
    : rect({x, y, width, height}), color(color), velocity(velocity) {
}

// void Bullet::Update(float deltaTime) {
//     // Bullets move upwards
//     rect.y -= speed * deltaTime;
// }

void Bullet::Update(float deltaTime) {
    // Bewegung in x- und y-Richtung
    rect.x += velocity.x * deltaTime;
    rect.y += velocity.y * deltaTime;
}

void Bullet::Draw() const{
    DrawRectangleRec(rect, color);
}

 //Überprüfen, ob Schüsse auserhalb des Fensters sind
bool Bullet::IsOffScreen(int screenWidth, int screenHeight) const {                
    return rect.x < -rect.width || rect.x > screenWidth ||
           rect.y < -rect.height || rect.y > screenHeight;
}