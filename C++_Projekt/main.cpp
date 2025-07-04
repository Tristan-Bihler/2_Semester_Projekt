#include "raylib.h"
#include "Player.hpp"
#include "Enemy.hpp"
#include "Bullet.hpp"
#include "Rooms.hpp"
#include "Hindernisse.hpp"

#include <vector>
#include <random>
#include <ctime>

using namespace std;

int main() {

    int screenWidth = 0;
    int screenHeight = 0;
    InitWindow(screenWidth, screenHeight, "DHBW SURVIVAL! Exams of Doom");          //Intialisierung notwendig, um Monitorgröße auslesen zu können
    Rooms lobby;
    
    Player player(lobby.getscreenWidth(), lobby.getscreenHeight(), 50, 50, BLUE, 100, 1);

    vector<Enemy> enemies;
    vector<Hindernisse> boxes;

    // Setze Ziel-Frames Per Second für flüssige Animation
    SetTargetFPS(60);

    //Start mit Leertaste
    while (!IsKeyPressed(KEY_SPACE) && !WindowShouldClose()) {
        BeginDrawing();                                                                  // Beginnt das Zeichnen eines neuen Frames
        ClearBackground(RAYWHITE);                                                       // Setzt den Bildschirm auf WEISS
        DrawText("Drücke die Leertaste, um zu starten!", lobby.getscreenWidth() / 2 - 200, lobby.getscreenHeight() / 2 + 150, 20, BLACK);
        DrawText("Steuerung:", lobby.getscreenWidth() / 2 - 200, lobby.getscreenHeight() / 2 - 300, 20, BLACK);
        DrawText("WASD:   Figur Bewegen", lobby.getscreenWidth() / 2 - 200, lobby.getscreenHeight() / 2 - 200, 20, BLACK);
        DrawText("Linke Maustaste:   Schießen", lobby.getscreenWidth() / 2 - 200, lobby.getscreenHeight() / 2 - 150, 20, BLACK);
        DrawText("F:   Wechseln der Monition", lobby.getscreenWidth() / 2 - 200, lobby.getscreenHeight() / 2 - 100, 20, BLACK);
        DrawText("F2:   Spiel nach dem Start im Vollbildmodus ausführen", lobby.getscreenWidth() / 2 - 200, lobby.getscreenHeight() / 2 - 50, 20, BLACK);
        EndDrawing();
    }
    

    // Spiel-Schleife
    while (!WindowShouldClose()) {
        // Zeit pro Frame für gleichmäßige Bewegungen
        float deltaTime = GetFrameTime();

        // Update  
        //----------------------------------------------------------------------------------
        player.Update(deltaTime, lobby.getscreenWidth(), lobby.getscreenHeight());

        // Update Gegner
        for (Enemy& enemy : enemies) {
            enemy.Update(deltaTime, {player.GetRect().x, player.GetRect().y});
        }




        // Überprüfen  
        //----------------------------------------------------------------------------------
        //Auf Kollision prüfen
        for (auto& box : boxes) {
            bool collision = CheckCollisionRecs(player.GetRect(), box.GetRect());

            if (collision)
            {
                player.SetPosition(player.GetPreviousPositionX(), player.GetPreviousPositionY());
            }
        }


        for (auto& box : boxes) {
            for (auto& enemy : enemies) {
                bool collision = CheckCollisionRecs(enemy.GetRect(), box.GetRect());
                if (collision && (enemy.GetPreviousPositionY()<box.GetRect().y))
                {
                    enemy.SetPosition(enemy.GetPreviousPositionX()+1, enemy.GetPreviousPositionY());
                }
                if (collision && ((enemy.GetPreviousPositionX()+enemy.GetRect().width)<box.GetRect().x))
                {
                    enemy.SetPosition(enemy.GetPreviousPositionX(), enemy.GetPreviousPositionY()-1);
                }
                if (collision && (enemy.GetPreviousPositionY()>(box.GetRect().y+box.GetRect().height)))
                {
                    enemy.SetPosition(enemy.GetPreviousPositionX()-1, enemy.GetPreviousPositionY());
                }
                if (collision && (enemy.GetPreviousPositionX()<(box.GetRect().x+box.GetRect().width)))
                {
                    enemy.SetPosition(enemy.GetPreviousPositionX(), enemy.GetPreviousPositionY()+1);
                }
            }
        }



        // Holt eine Referenz auf die Liste der vom Spieler abgefeuerten Geschosse
        vector<Bullet>& playerBullets = player.GetBulletsMutable();
        for (size_t i = 0; i < playerBullets.size(); ) {                                 // Durchläuft Geschosse des Spielers, prüft Kollisionen der Schüsse mit Gegnern
            bool bulletHit = false;                                                      // Ob Geschoss einen Gegner getroffen hat
            for (size_t j = 0; j < enemies.size(); ) {
                if (CheckCollisionRecs(playerBullets[i].GetRect(), enemies[j].GetRect())) {
                    enemies[j].TakeDamage(playerBullets[i].GetBulletDamage());           // Gegner erhält 20 Schadenspunkte
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

            for (size_t j = 0; j < boxes.size(); j++) {
                if (CheckCollisionRecs(playerBullets[i].GetRect(), boxes[j].GetRect())) {
                    bulletHit = true;
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
                player.TakeDamage(1 + 0.2 * (player.GetLevel() - 1));                                  // Spieler verliert 1 Lebenspunkt pro Frame, wenn mit Gegner kollidiert
            }
        }

        // Entferne tote Feinde 
        for (int i = 0; i < int(enemies.size()); ) // Notice no increment here
        {

        if (!enemies[i].IsActive())
            {
                enemies.erase(enemies.begin() + i); // Removes the element and shifts everything after it
                                                // 'i' does not increment, as the next element slides into 'i'
            }
        else
            {
                i++; // Only move to the next element if the current one was kept
            }
        }

        lobby.enemyAlive = !enemies.empty();
        
        //Raumwechsel

        lobby.setDoor(lobby.enemyAlive);

        lobby.changeRoom(player, player.GetLevel(), lobby.enemyAlive, enemies, boxes);

        // Überprüft Spielende
        if (player.GetHealth() <= 0) {
            Rooms lobby;

             while (!IsKeyPressed(KEY_SPACE) && !WindowShouldClose()) {
                BeginDrawing();                                                                  // Beginnt das Zeichnen eines neuen Frames
                ClearBackground(RAYWHITE);                                                       // Setzt den Bildschirm auf WEISS
                DrawText("Du wirst Exmatrikuliert. Drücke die Leertaste, um das Spiel zu Verlassen!", lobby.getscreenWidth() / 3, lobby.getscreenHeight() / 2, 20, BLACK);
                EndDrawing();
            }
            break; // beendet Spiel-Schleife
        }

        if (player.GetLevel() == 100) {
            Rooms lobby;

            while (!IsKeyPressed(KEY_SPACE) && !WindowShouldClose()) {
                BeginDrawing();                                                                  // Beginnt das Zeichnen eines neuen Frames
                ClearBackground(RAYWHITE);                                                       // Setzt den Bildschirm auf WEISS
                DrawText("Du hast die Klausurephase überstanden. Drücke die Leertaste, um in das echte Leben zurück zu kehren!", lobby.getscreenWidth() / 5, lobby.getscreenHeight() / 2, 20, BLACK);
                EndDrawing();
            }
            break; // beendet Spiel-Schleife
        }



        // Anzeigen  
        //----------------------------------------------------------------------------------
        BeginDrawing();

            ClearBackground(RAYWHITE);

            player.Draw();                                                               // Zeichnet den Spieler auf den Bildschirm

            for (const auto& box : boxes) {
                box.Draw();
            }

            for (const auto& enemy : enemies) {
                enemy.Draw();
            }
            // Zeichnet Lebensanzeige des Spielers
            //-> immer selbe Position und gleiche größe -> an bildschirm anpassen 
            // int GetScreenWidth(void);        

            DrawText(TextFormat("Health: %i", player.GetHealth()), GetScreenWidth() * 0.01, GetScreenHeight() * 0.01, 20, BLACK);
            DrawText(TextFormat("Level: %i", player.GetLevel()), GetScreenWidth() * 0.5, GetScreenHeight() * 0.01, 20, BLACK);
            DrawText(TextFormat("Bohne: %s", player.GetBohnenArt().c_str()), GetScreenWidth() * 0.25, GetScreenHeight() * 0.01, 20, BLACK);

        EndDrawing();
    }

    CloseWindow();

    return 0;
}