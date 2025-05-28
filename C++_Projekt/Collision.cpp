#include "raylib.h"

int main() {
    const int screenWidth = 800;
    const int screenHeight = 1000;

    InitWindow(screenWidth, screenHeight, "2D Kollision mit Raylib");

    Texture2D backround = LoadTexture("XXXXXXXXassets/bild.png");
    Texture2D playerTexture = LoadTexture("XXXXXXXplayer.png");
    Rectangle player = { 100, 201, 50, 50 };
    Rectangle enemy = { 300, 500, 50, 50 };
    Vector2 position = { 201.0f, 201.0f };


    SetTargetFPS(60);

while (!WindowShouldClose()) {
        // Bewegung des Spielers mit Pfeiltasten
        if (IsKeyDown(KEY_RIGHT)&& (player.x<screenWidth-player.width)) player.x += 2.0f;
        if (IsKeyDown(KEY_LEFT)&& (player.x>0)) player.x -= 2.0f;
        if (IsKeyDown(KEY_DOWN)&& (player.y<screenHeight-player.height)) player.y += 2.0f;
        if (IsKeyDown(KEY_UP)&& (player.y>200)) player.y -= 2.0f;

        bool collision = CheckCollisionRecs(player, enemy);

        BeginDrawing();
        ClearBackground(RAYWHITE);

        //DrawText("Bewege das blaue Rechteck mit den Pfeiltasten", 10, 10, 20, DARKGRAY);
        DrawTexture(backround, 0, 201, WHITE);
        DrawTextureEx(playerTexture, (Vector2){player.x,player.y}, 0.0f, 1.0f, WHITE);
        DrawRectangleRec(enemy, RED);
        //DrawRectangleRec(player, collision ? GREEN : BLUE);

        if (collision) {
            DrawText("Kollision erkannt!", 10, 40, 20, MAROON);
        }

        EndDrawing();
    }

    CloseWindow();
    UnloadTexture(playerTexture);
    UnloadTexture(backround);
    return 0;
}
