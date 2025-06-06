#include "Player.hpp"
#include "raylib.h"
#include "Bullet.hpp" // Ensure Bullet.h is included for Bullet creation
#include <cmath>

// Constructor implementation
Player::Player(float x, float y, float width, float height, Color color, int maxHealth, int beginning_level)
    : rect({x, y, width, height}), color(color), speed(200.0f), // Speed in pixels per second
      maxHealth(maxHealth), currentHealth(maxHealth), currentLevel(beginning_level),
      shootCooldown(0.2f), currentShootCooldown(0.0f) {
}

// Update method implementation (now takes deltaTime)
void Player::Update(float deltaTime) {
    // Movement
    if (IsKeyDown(KEY_W)) {
        rect.y -= speed * deltaTime;
    }
    if (IsKeyDown(KEY_S)) {
        rect.y += speed * deltaTime;
    }
    if (IsKeyDown(KEY_A)) {
        rect.x -= speed * deltaTime;
    }
    if (IsKeyDown(KEY_D)) {
        rect.x += speed * deltaTime;
    }

    // Keep player within screen bounds (adjust if screen dimensions change)
    const int screenWidth = 800; // Hardcoded for simplicity, pass as parameter for flexibility
    const int screenHeight = 800;
    if (rect.x < 0) rect.x = 0;
    if (rect.x + rect.width > screenWidth) rect.x = screenWidth - rect.width;
    if (rect.y < 0) rect.y = 0;
    if (rect.y + rect.height > screenHeight) rect.y = screenHeight - rect.height;

    // Shooting cooldown
    if (currentShootCooldown > 0) {
        currentShootCooldown -= deltaTime;
    }

    // Shoot on Mouse Button press
    if (IsMouseButtonDown(MOUSE_BUTTON_LEFT) && currentShootCooldown <= 0) {
        Shoot();
        currentShootCooldown = shootCooldown;
    }

    // Update active bullets
    for (size_t i = 0; i < bullets.size(); ) {
        bullets[i].Update(deltaTime);
        // Remove bullets that are off-screen
        if (bullets[i].IsOffScreen(screenWidth, screenHeight)) {
            bullets.erase(bullets.begin() + i);
        } else {
            ++i;
        }
    }
}

// Draw method implementation
void Player::Draw() {
    DrawRectangleRec(rect, color);

    // Draw health bar
    float healthBarWidth = rect.width + 20 ;   
    float healthBarHeight = 15;
    float healthPercentage = (float)currentHealth / maxHealth;
    //DrawRectangle(rect.x, rect.y - healthBarHeight - 5, healthBarWidth, healthBarHeight, RED); // Background
    //DrawRectangle(rect.x, rect.y - healthBarHeight - 5, healthBarWidth * healthPercentage, healthBarHeight, GREEN); // Fill

    DrawRectangle(10, 60 - healthBarHeight - 5, healthBarWidth, healthBarHeight, RED); // Background
    DrawRectangle(10, 60 - healthBarHeight - 5, healthBarWidth * healthPercentage, healthBarHeight, GREEN); // Fill

    //("Health: %i", player.GetHealth()), x=10, x= 10, 20, BLACK);

    // Draw bullets
    for (const auto& bullet : bullets) {
        bullet.Draw();
    }
}

void Player::TakeDamage(int amount) {
    currentHealth -= amount;
    if (currentHealth < 0) {
        currentHealth = 0;
    }
}

void Player::Increase_Level() {
    currentLevel = currentLevel + 1;
}

// void Player::Shoot() {
//     Create a new bullet at the player's center, moving upwards
//     bullets.emplace_back(rect.x + rect.width / 2 - 2, rect.y, 4, 10, BLUE, 400.0f);
// }

void Player::Shoot() {
    // Mausposition holen
    Vector2 mousePos = GetMousePosition();

    // Spielerzentrum als Ausgangspunkt für Kugel
    Vector2 bulletStart = { rect.x + rect.width / 2, rect.y + rect.height / 2 };

    // Richtungsvektor von Spieler zu Maus
    Vector2 direction = { mousePos.x - bulletStart.x, mousePos.y - bulletStart.y };

    // Länge des Vektors berechnen
    float length = sqrt(direction.x * direction.x + direction.y * direction.y);
    
    // Normalisieren (damit die Geschwindigkeit konstant bleibt)
    if (length != 0) {
        direction.x /= length;
        direction.y /= length;
    }

    // Geschwindigkeit der Kugel setzen
    float bulletSpeed = 400.0f;
    Vector2 bulletVelocity = { direction.x * bulletSpeed, direction.y * bulletSpeed };

    // Kugel in Richtung der Maus feuern
    bullets.emplace_back(bulletStart.x, bulletStart.y, 4, 10, BLUE, bulletVelocity);
}
