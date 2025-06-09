#pragma once

#include "raylib.h"                //C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/
#include <vector>               // managing der Schüsse
#include "Bullet.hpp"           // Deklarieren bzw. Einbinden der Bullet-Klasse
#include "Hindernisse.hpp"
#include <string>

using namespace std; 

class Player {
private:

    Rectangle rect;
    float screenWidth;
    float screenHeight;
    Color color;
    float speed;
    int maxHealth;
    int currentHealth;
    int currentLevel;
    Color bullet_color;
    int bullet_damage;
    int Inventar_platz = 1;
    string bohnen_art;

    float firerate;

    int previouspositionx;
    int previouspositiony;

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

public:
    Player(float screenWidth,float screenHeight, float width, float height, Color color, int maxHealth, int beginning_level);

    void Update(float deltaTime, float screenWidth, float screenHeight);   // deltaTime für konstante Bewegung
    void Draw();
    void TakeDamage(int amount);
    void Shoot();                   // Neue Methode um die Schüsse zu erstellen
    void Increase_Level();
    void Increase_Mental_Health_Points();
    void SetPosition(float x, float y);

    Rectangle GetRect() const { return rect; }
    int GetHealth() const { return currentHealth; }
    int GetLevel() const { return currentLevel; }
    int GetPositionX() const{ return rect.x; }
    int GetPreviousPositionX() const{ return previouspositionx; }
    int GetPreviousPositionY() const{ return previouspositiony; }
    string GetBohnenArt() const{return bohnen_art;}

    const std::vector<Bullet>& GetBullets() const { return bullets; }       // Zeichnungen und Kollisionsüberprüfung
    std::vector<Bullet>& GetBulletsMutable() { return bullets; }            // Ändern (modifizieren) und entfernen der Schüsse
};