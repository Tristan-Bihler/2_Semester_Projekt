#pragma once

#include "raylib.h"

class Enemy {
public:
    Enemy(float x, float y, float width, float height, Color color, int health, float speed);

    void Update(float deltaTime, Vector2 playerPosition); // Enemy moves towards player
    void Draw() const;
    void TakeDamage(int amount);

    Rectangle GetRect() const { return rect; }
    bool IsActive() const { return currentHealth > 0; } // Check if enemy is alive

private:
    Rectangle rect;
    Color color;
    int maxHealth;
    int currentHealth;
    float speed;
};