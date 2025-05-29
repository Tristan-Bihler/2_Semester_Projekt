#include "raylib.h"
#include "Player.hpp"
#include "Enemy.hpp"
#include "Bullet.hpp"
#include <vector>
#include <random> // For random enemy spawning
#include <algorithm> // For std::remove_if

int main() {
    // Screen dimensions
    const int screenWidth = 800;
    const int screenHeight = 450;

    // Initialize Raylib window
    InitWindow(screenWidth, screenHeight, "Player, Enemies, Bullets, Life System (C++ Class)");

    // Create a Player object
    Player player(screenWidth / 2 - 25, screenHeight - 75, 50, 50, RED, 100); // 100 health

    // Enemy management
    std::vector<Enemy> enemies;
    float enemySpawnTimer = 0.0f;
    float enemySpawnRate = 2.0f; // Spawn an enemy every 2 seconds

    // Random number generation for enemy spawning
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> distribX(0, screenWidth - 50); // Enemy width is 50

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

        // Spawn enemies
        enemySpawnTimer += deltaTime;
        if (enemySpawnTimer >= enemySpawnRate) {
            enemies.emplace_back(distribX(gen), -50.0f, 50, 50, GREEN, 30, 100.0f); // Random X, above screen, 30 health, 100 speed
            enemySpawnTimer = 0.0f;
        }

        // Bullet-Enemy Collision
        // Iterate through bullets and enemies for collision detection
        std::vector<Bullet>& playerBullets = player.GetBulletsMutable();
        for (size_t i = 0; i < playerBullets.size(); ) {
            bool bulletHit = false;
            for (size_t j = 0; j < enemies.size(); ) {
                if (CheckCollisionRecs(playerBullets[i].GetRect(), enemies[j].GetRect())) {
                    enemies[j].TakeDamage(20); // Bullet deals 20 damage
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
                player.TakeDamage(1); // Player takes 1 damage per frame if colliding
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
        //----------------------------------------------------------------------------------

        // Draw
        //----------------------------------------------------------------------------------
        BeginDrawing();

            ClearBackground(RAYWHITE); // Clear the background each frame

            player.Draw(); // Draw the player and their bullets

            // Draw enemies
            for (const auto& enemy : enemies) {
                enemy.Draw();
            }

            // Draw current health
            DrawText(TextFormat("Health: %i", player.GetHealth()), 10, 10, 20, BLACK);

        EndDrawing();
        //----------------------------------------------------------------------------------
    }

    // Close window and free Raylib resources
    CloseWindow();

    return 0;
}