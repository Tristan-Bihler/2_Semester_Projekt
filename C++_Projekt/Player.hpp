#pragma once

#include "raylib.h"                //C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/
#include <vector>               // managing der Schüsse
#include "Bullet.hpp"           // Deklarieren bzw. Einbinden der Bullet-Klasse

class Player {
public:
    Player(float screenWidth,float screenHeight, float width, float height, Color color, int maxHealth, int beginning_level);

    void Update(float deltaTime);   // deltaTime für konstante Bewegung
    void Draw();
    void TakeDamage(int amount);
    void Shoot();                   // Neue Methode um die Schüsse zu erstellen
    void Increase_Level();
    void SetPosition(float x, float y);

    Rectangle GetRect() const { return rect; }
    int GetHealth() const { return currentHealth; }
    int GetLevel() const { return currentLevel; }
    int GetPositionX() const{ return rect.x; }


    const std::vector<Bullet>& GetBullets() const { return bullets; }       // Zeichnungen und Kollisionsüberprüfung
    std::vector<Bullet>& GetBulletsMutable() { return bullets; }            // Ändern (modifizieren) und entfernen der Schüsse

private:
    Rectangle rect;
    Color color;
    float speed;
    int maxHealth;
    int currentHealth;
    int currentLevel;
    int screenWidth;
    int screenHeight;

    // Schüsse abgeben
    float shootCooldown;
    float currentShootCooldown;
    std::vector<Bullet> bullets;        // Schüsse des Spielers aktiviert

    // Mauszeiger bewegen
    Vector2 mousePos;
    Vector2 bulletStart;
    Vector2 direction;
    float length;
    float bulletSpeed;
    Vector2 bulletVelocity;



};