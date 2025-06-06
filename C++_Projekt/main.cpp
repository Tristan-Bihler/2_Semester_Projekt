#include "raylib.h"
#include "Player.hpp"
#include "Enemy.hpp"
#include "Bullet.hpp"
#include "Rooms.hpp"
#include <vector>
#include <random>
#include <algorithm> // For std::remove_if
#include <ctime>
#define VIS_Count 10

using namespace std;

int main() {
    int monitor = GetCurrentMonitor();                                              // Aktuellen Monitor festlegen
    int screenWidth = 0;     
    int screenHeight = 0;     
    int ScreenPositionX;
    int ScreenPositionY;
    Texture2D visuals [VIS_Count] = {};
    Texture2D background;
    Rooms lobby;
    string pfad = ("assets");
    //lobby.preLoadTextures(pfad, visuals);
    background = visuals[0];


    InitWindow(screenWidth, screenHeight, "DHBW SURVIVAL! Exams of Doom");          // Intialisierung notwendig, um Monitorgröße auslesen zu können
    screenWidth = GetMonitorWidth(monitor) * 2 / 3;                                 //Monitorbreite auslesen mulitpliziert mit 2/3
    screenHeight = GetMonitorHeight(monitor) * 2 / 3 ;                              //Monitorhöhe auslesen mulitpliziert mit 2/3
    ScreenPositionX = (GetMonitorWidth(monitor) - screenWidth) / 2;
    ScreenPositionY = (GetMonitorHeight(monitor) - screenHeight) / 2;
    SetWindowSize(screenWidth, screenHeight);                                       // Größe des Fensters setzen 2/3 des Monitors
    SetWindowPosition(ScreenPositionX, ScreenPositionY);                            // Fenster Mittig positionieren
    
    HideCursor();
    Player player(screenWidth, screenHeight, 50, 50, BLUE, 100, 1);

    vector<Enemy> enemies;
    random_device rd;
    mt19937 gen(rd());
    srand(time(0));

    // Setze Ziel-Frames Per Second für flüssige Animation
    SetTargetFPS(60);

    //Start mit Leertaste
    while (!IsKeyPressed(KEY_SPACE)) {
    BeginDrawing();                                                                  // Beginnt das Zeichnen eines neuen Frames
    ClearBackground(RAYWHITE);                                                       // Setzt den Bildschirm auf WEISS
    DrawText("Drücke die Leertaste, um zu starten!", screenWidth / 2 - 200, screenHeight / 2, 20, BLACK);
    EndDrawing();
    }

    // Spiel-Schleife
    while (!WindowShouldClose()) {
        


        // Zeit pro Frame für gleichmäßige Bewegungen
        float deltaTime = GetFrameTime();

        // Update
        //----------------------------------------------------------------------------------
        player.Update(deltaTime);

        // Update Gegner
        for (Enemy& enemy : enemies) {
            enemy.Update(deltaTime, {player.GetRect().x, player.GetRect().y});
        }

        // Holt eine Referenz auf die Liste der vom Spieler abgefeuerten Geschosse
        vector<Bullet>& playerBullets = player.GetBulletsMutable();
        for (size_t i = 0; i < playerBullets.size(); ) {                                 // Durchläuft Geschosse des Spielers, prüft Kollisionen mit Gegnern
            bool bulletHit = false;                                                      // Ob Geschoss einen Gegner getroffen hat
            for (size_t j = 0; j < enemies.size(); ) {
                if (CheckCollisionRecs(playerBullets[i].GetRect(), enemies[j].GetRect())) {
                    enemies[j].TakeDamage(20);                                           // Gegner erhält 20 Schadenspunkte
                    bulletHit = true; 
                    // Entfernt Gegner wenn getroffen
                    if (!enemies[j].IsActive()) { 
                        enemies.erase(enemies.begin() + j);
                    } else {
                        ++j;                                                            // Nächster Gegner
                    }
                } else {
                    ++j;                                                                // Nächster Gegner
                }
            }

            // Falls das Geschoss einen Gegner getroffen hat, wird es aus der Liste entfernt.
            if (bulletHit) {
                playerBullets.erase(playerBullets.begin() + i);
            } else {
                ++i; // Nächster Schuss
            }
        }


        // Spieler - Feind Collision
        for (auto& enemy : enemies) {
            if (enemy.IsActive() && CheckCollisionRecs(player.GetRect(), enemy.GetRect())) {
                player.TakeDamage(0.2 * player.GetLevel());                                  // Spieler verliert 1 Lebenspunkt pro Frame, wenn mit Gegner kollidiert
            }
        }

        // Entferne tote Feinde 
        enemies.erase(std::remove_if(enemies.begin(), enemies.end(),
                                     [](const Enemy& e){ return !e.IsActive(); }),
                      enemies.end());
        
        lobby.enemyAlive = !enemies.empty();
        
        //Raumwechsel

        lobby.setDoor(lobby.enemyAlive);

        lobby.changeRoom(background, visuals, player, player.GetLevel(), enemies);


        // Überprüft Spielende
        if (player.GetHealth() <= 0) {
                // Spielende verwalten (z. B. Nachricht anzeigen, Spiel neu starten)  
                // Im Moment wird einfach das Fenster geschlossen 
            TraceLog(LOG_INFO, "GAME OVER! Player defeated.");
            break; // beendet Spiel-Schleife
        }

        BeginDrawing();

            ClearBackground(RAYWHITE);

            player.Draw();                                                             // Zeichnet den Spieler auf den Bildschirm

            for (const auto& enemy : enemies) {
                enemy.Draw();
            }
            // Zeichnet Lebensanzeige des Spielers
            //-> immer selbe Position und gleiche größe -> an bildschirm anpassen 
            // int GetScreenWidth(void);        

            DrawTexture(background, 0,200, WHITE);
            DrawText(TextFormat("Health: %i", player.GetHealth()), GetScreenWidth() * 0.01, GetScreenHeight() * 0.01, 20, BLACK);
            DrawText(TextFormat("Level: %i", player.GetLevel()), GetScreenWidth() * 0.5, GetScreenHeight() * 0.01, 20, BLACK);

        EndDrawing();
    }

    CloseWindow();

    return 0;
}