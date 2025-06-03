#include "Enemy.hpp"
#include "raylib.h"
#include <cmath> // For std::sqrt

Enemy::Enemy(float x, float y, float width, float height, Color color, int health, float speed)
    : rect({x, y, width, height}), color(color),
      maxHealth(health), currentHealth(health), speed(speed) {
}

void Enemy::Update(float deltaTime, Vector2 playerPosition) {
    if (currentHealth <= 0) return; // Don't update dead enemies

    // Calculate direction vector to player
    float dx = playerPosition.x - rect.x;
    float dy = playerPosition.y - rect.y;

    // Normalize direction vector
    float distance = std::sqrt(dx * dx + dy * dy);
    if (distance > 0) {
        dx /= distance;
        dy /= distance;
    }

    rect.x += dx * speed * deltaTime;
    rect.y += dy * speed * deltaTime;
}

void Enemy::Draw() const{
    if (currentHealth <= 0) return; // Don't draw dead enemies

    DrawRectangleRec(rect, color);

    // Draw health bar for enemy
    float healthBarWidth = rect.width;
    float healthBarHeight = 3;
    float healthPercentage = (float)currentHealth / maxHealth;
    DrawRectangle(rect.x, rect.y - healthBarHeight - 3, healthBarWidth, healthBarHeight, DARKGRAY); // Background
    DrawRectangle(rect.x, rect.y - healthBarHeight - 3, healthBarWidth * healthPercentage, healthBarHeight, ORANGE); // Fill
}

void Enemy::TakeDamage(int amount) {
    currentHealth -= amount;
    if (currentHealth < 0) {
        currentHealth = 0;
    }
}