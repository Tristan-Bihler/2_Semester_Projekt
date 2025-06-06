#pragma once

#include "raylib.h"
#include <vector> // For managing bullets
#include "Bullet.hpp" // Forward declaration or include for Bullet class

class Player {
public:
    Player(int screenWidth,int screenHeight, float width, float height, Color color, int maxHealth, int beginning_level);

    void Update(float deltaTime); // deltaTime for consistent movement
    void Draw();
    void TakeDamage(int amount);
    void Shoot(); // New method to create bullets
    void Increase_Level();

    Rectangle GetRect() const { return rect; }
    int GetHealth() const { return currentHealth; }
    int GetLevel() const { return currentLevel; }
    int GetPositionX() const{ return rect.x; }
    int GetPositionY() const{ return rect.y; }

    const std::vector<Bullet>& GetBullets() const { return bullets; } // For drawing and collision checks
    std::vector<Bullet>& GetBulletsMutable() { return bullets; } // For modifying (removing) bullets

private:
    Rectangle rect;
    Color color;
    float speed;
    int maxHealth;
    int currentHealth;
    int currentLevel;
    int screenWidth;
    int screenHeight;

    // Bullet shooting mechanics
    float shootCooldown;
    float currentShootCooldown;
    std::vector<Bullet> bullets; // Player's active bullets

    // Idiotentest Mauszeiger bewegen
    Vector2 mousePos;
    Vector2 bulletStart;
    Vector2 direction;
    float length;
    float bulletSpeed;
    Vector2 bulletVelocity;



};