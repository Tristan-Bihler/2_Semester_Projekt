#include "Player.hpp"
#include "raylib.h"
#include "Bullet.hpp" // Sicherstellen Bullet.h ist eingebunden, für Schuss Erstellung 
#include <cmath>

// Implementierung des Constructors
Player::Player(float screenWidth,float screenHeight, float width, float height, Color color, int maxHealth, int beginning_level)
    : rect({(screenWidth / 2 - 25), (screenHeight - 75), width, height}), screenWidth(screenWidth), screenHeight(screenHeight), color(color), speed(200.0f), // Speed in pixels per second
      maxHealth(maxHealth), currentHealth(maxHealth), currentLevel(beginning_level),
      shootCooldown(0.2f), currentShootCooldown(0.0f) {
}

// Implementierungs Methode aktualisieren (nun deltaTime)
void Player::Update(float deltaTime) {
    // Bewegung
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
    if (IsKeyDown(KEY_F2)){
        ToggleFullscreen();
    }

    // Spiler bleibt innderhalb des Spielfensters
    if (rect.x < 0) rect.x = 0;
    if (rect.x + rect.width > screenWidth) rect.x = screenWidth - rect.width;
    if (rect.y < 0) rect.y = 0;
    if (rect.y + rect.height > screenHeight) rect.y = screenHeight - rect.height;

    // Schuss-Abklingzeit
    if (currentShootCooldown > 0) {
        currentShootCooldown -= deltaTime;
    }

    // Schießen mit der linken Maustaste
    if (IsMouseButtonDown(MOUSE_BUTTON_LEFT) && currentShootCooldown <= 0) {
        Shoot();
        currentShootCooldown = shootCooldown;
    }

    // aktuelle Schüsse aktualisieren
    for (size_t i = 0; i < bullets.size(); ) {
        bullets[i].Update(deltaTime);
        // Entfernen der Schüsse, welche außerhalb des Fensters sind
        if (bullets[i].IsOffScreen(screenWidth, screenHeight)) {
            bullets.erase(bullets.begin() + i);
        } else {
            ++i;
        }
    }
}

// Implementierung der Zeichen-Methode
void Player::Draw() {
    DrawRectangleRec(rect, color);

    // Zeichnen der Lebensanzeige
    float healthBarWidth = rect.width + 20 ;   
    float healthBarHeight = 15;
    float healthPercentage = (float)currentHealth / maxHealth;
    //DrawRectangle(rect.x, rect.y - healthBarHeight - 5, healthBarWidth, healthBarHeight, RED); // Hintergrund
    //DrawRectangle(rect.x, rect.y - healthBarHeight - 5, healthBarWidth * healthPercentage, healthBarHeight, GREEN); // Füllung

    DrawRectangle(10, 60 - healthBarHeight - 5, healthBarWidth, healthBarHeight, RED); // Hintergrund
    DrawRectangle(10, 60 - healthBarHeight - 5, healthBarWidth * healthPercentage, healthBarHeight, GREEN); // Füllung

    //("Health: %i", player.GetHealth()), x=10, x= 10, 20, BLACK);

    // Zeichnen der Schüsse
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
//     Erstellen eines neuen Schusses in der Mitte des Spielers, welcher nach oben weggeht
//     bullets.emplace_back(rect.x + rect.width / 2 - 2, rect.y, 4, 10, BLUE, 400.0f);
// }

void Player::Shoot() {

    Vector2 mousePos = GetMousePosition();     // Mausposition holen

    Vector2 bulletStart = { rect.x + rect.width / 2, rect.y + rect.height / 2 };        // Spielerzentrum als Ausgangspunkt für Kugel

    Vector2 direction = { mousePos.x - bulletStart.x, mousePos.y - bulletStart.y };     // Richtungsvektor von Spieler zu Maus

    float length = sqrt(direction.x * direction.x + direction.y * direction.y);         // Länge des Vektors berechnen
    
    // Normalisieren (damit die Geschwindigkeit konstant bleibt)
    if (length != 0) {
        direction.x /= length;
        direction.y /= length;
    }

    // Geschwindigkeit der Kugel setzen
    float bulletSpeed = 400.0f;
    Vector2 bulletVelocity = { direction.x * bulletSpeed, direction.y * bulletSpeed };

    // Kugel in Richtung der Maus feuern
    bullets.emplace_back(bulletStart.x, bulletStart.y, 4, 10, BROWN, bulletVelocity);
}
