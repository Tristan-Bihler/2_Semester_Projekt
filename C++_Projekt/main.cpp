#include "raylib.h"
#include "Player.hpp"
#include "Enemy.hpp"
#include "Bullet.hpp"
#include <vector>
#include <random>
#include <algorithm> // For std::remove_if
#include <ctime>
using namespace std;

int main() {
    const int screenWidth = 1000;
    const int screenHeight = 800;

    InitWindow(screenWidth, screenHeight, "DHBW SURVIVAL! Exams of Doom");


    Player player(screenWidth ,screenHeight, 50, 50, BLUE, 100, 10);

    vector<Enemy> enemies;
    random_device rd;
    mt19937 gen(rd());
    srand(time(0));

    // Set target FPS for smooth animation
    SetTargetFPS(60);

    // Game loop
    while (!WindowShouldClose()) {
        


        // Get frame time for consistent movement across different frame rates
        float deltaTime = GetFrameTime();
        // Update
        //----------------------------------------------------------------------------------
        player.Update(deltaTime);

        // Update enemies
        for (auto& enemy : enemies) {
            enemy.Update(deltaTime, {player.GetRect().x, player.GetRect().y});
        }

        /*// Spawn enemies
        enemySpawnTimer += deltaTime;
        if (enemySpawnTimer >= enemySpawnRate) {
            enemies.emplace_back(distribX, distribY, 50, 50, GREEN, 30, 100.0f); // Random X, above screen, 30 health, 100 speed
            enemySpawnTimer = 0.0f;
        }*/

        vector<Bullet>& playerBullets = player.GetBulletsMutable();
        for (size_t i = 0; i < playerBullets.size(); ) {
            bool bulletHit = false;
            for (size_t j = 0; j < enemies.size(); ) {
                if (CheckCollisionRecs(playerBullets[i].GetRect(), enemies[j].GetRect())) {
                    enemies[j].TakeDamage(20); // Bullet deals 20 damage
                    player.Increase_Level();
                    bulletHit = true; // Mark bullet for removal
                    // If enemy is dead, remove it
                    if (!enemies[j].IsActive()) {
                        enemies.erase(enemies.begin() + j);
                    } else {
                        ++j; // Move to next enemy
                    }
                } else {
                    ++j; // Move to next enemy
                }
            }
            if (bulletHit) {
                playerBullets.erase(playerBullets.begin() + i);
            } else {
                ++i; // Move to next bullet
            }
        }


        // Player-Enemy Collision (Player takes damage)
        for (auto& enemy : enemies) {
            if (enemy.IsActive() && CheckCollisionRecs(player.GetRect(), enemy.GetRect())) {
                player.TakeDamage(0.2 * player.GetLevel()); // Player takes 1 damage per frame if colliding
                // Optional: Push enemy away or make it stop for a moment
            }
        }

        // Remove dead enemies (using erase-remove idiom)
        enemies.erase(std::remove_if(enemies.begin(), enemies.end(),
                                     [](const Enemy& e){ return !e.IsActive(); }),
                      enemies.end());

        // Game over check
        if (player.GetHealth() <= 0) {
            // Handle game over (e.g., display message, restart game)
            // For now, we'll just close the window
            TraceLog(LOG_INFO, "GAME OVER! Player defeated.");
            break; // Exit game loop
        }

        BeginDrawing();

            ClearBackground(RAYWHITE);

            player.Draw(); 

            for (const auto& enemy : enemies) {
                enemy.Draw();
            }

            DrawText(TextFormat("Health: %i", player.GetHealth()), 10, 10, 20, BLACK);
            DrawText(TextFormat("Level: %i", player.GetLevel()), 500, 10, 20, BLACK);

        EndDrawing();
    }

    CloseWindow();

    return 0;
}
