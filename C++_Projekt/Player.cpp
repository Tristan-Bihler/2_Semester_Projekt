#include "Player.hpp"
#include "raylib.h"
#include "Bullet.hpp" //Einbinden einer anderen Klasse um deren Funktionen nutzen zu können
#include <cmath>

// Implementierung des Constructors
Player::Player(float screenWidth,float screenHeight, float width, float height, Color color, int maxHealth, int beginning_level)
    : rect({(screenWidth / 10 * 1), (screenHeight / 10 * 5), width, height}), screenWidth(screenWidth), screenHeight(screenHeight), color(color), speed(200.0f), // Speed in pixels per second
      maxHealth(maxHealth), currentHealth(maxHealth), currentLevel(beginning_level),
      shootCooldown(0.2f), currentShootCooldown(0.0f) {
}

// Implementierungs Methode aktualisieren (nun deltaTime)
void Player::Update(float deltaTime, float screenWidth, float screenHeight) {
    // Bewegung

    previouspositionx = rect.x;
    previouspositiony = rect.y;


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
    if (IsKeyPressed(KEY_F)){
        Inventar_platz = Inventar_platz + 1;
    }

    switch (Inventar_platz) {
        case 1:
            bullet_color = BLUE;
            firerate = 1;
            bullet_damage = 3;
            bohnen_art = "Entkoffiniert";
            break;
        case 2:
            bullet_color = BROWN;
            firerate = 0.5;
            bullet_damage= 10;
            bohnen_art = "Kaffee";
            break;
        case 3:
            bullet_color = BLACK;
            firerate = 0.1;
            bullet_damage= 50;
            Inventar_platz = 0; 
            bohnen_art = "Espresso";
            break;
    };

    // Spieler bleibt innderhalb des Spielfensters
    if (rect.x < 0) rect.x = 0;
    if (rect.x + rect.width > screenWidth) rect.x = screenWidth - rect.width;
    if (rect.y < 0) rect.y = 0;
    if (rect.y + rect.height > screenHeight) rect.y = screenHeight - rect.height;

    // Schuss-Abklingzeit
    if (currentShootCooldown > 0) {
        currentShootCooldown -= deltaTime * firerate;
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

void Player::Increase_Mental_Health_Points(){
    maxHealth = 100 * pow((1.015), (currentLevel - 1));
    currentHealth = maxHealth;
}

void Player::Shoot() {

    mousePos = GetMousePosition();     // Mausposition holen

    bulletStart = { rect.x + rect.width / 2, rect.y + rect.height / 2 };        // Spielerzentrum als Ausgangspunkt für Kugel

    direction = { mousePos.x - bulletStart.x, mousePos.y - bulletStart.y };     // Richtungsvektor von Spieler zu Maus

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
    bullets.emplace_back(bulletStart.x, bulletStart.y, 10, 10, bullet_color, bulletVelocity);
}

void Player::SetPosition(float x, float y){
    rect.x = x;
    rect.y = y;
}
