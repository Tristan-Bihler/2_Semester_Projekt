#include "raylib.h"

int main() {
    const int screenWidth = 800;
    const int screenHeight = 600;

    InitWindow(screenWidth, screenHeight, "2D Kollision mit Raylib");

    Rectangle player = { 100, 100, 50, 50 };
    Rectangle enemy = { 300, 200, 50, 50 };

    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        // Bewegung des Spielers mit Pfeiltasten
        if (IsKeyDown(KEY_RIGHT)) player.x += 2.0f;
        if (IsKeyDown(KEY_LEFT)) player.x -= 2.0f;
        if (IsKeyDown(KEY_DOWN)) player.y += 2.0f;
        if (IsKeyDown(KEY_UP)) player.y -= 2.0f;

        bool collision = CheckCollisionRecs(player, enemy);

        BeginDrawing();
        ClearBackground(RAYWHITE);

        DrawText("Bewege das blaue Rechteck mit den Pfeiltasten", 10, 10, 20, DARKGRAY);

        DrawRectangleRec(enemy, RED);
        DrawRectangleRec(player, collision ? GREEN : BLUE);

        if (collision) {
            DrawText("Kollision erkannt!", 10, 40, 20, MAROON);
        }

        EndDrawing();
    }

    CloseWindow();
    return 0;
}
