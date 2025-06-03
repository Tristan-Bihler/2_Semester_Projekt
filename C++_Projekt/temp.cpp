#include "raylib.h"



void WechselRaum(Texture2D* background, const char* neuerRaumPfad);

int main() {
    const int screenWidth = 800;
    const int screenHeight = 1000;
    

    InitWindow(screenWidth, screenHeight, "2D Kollision mit Raylib");

    Texture2D backround = LoadTexture("C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/raum1.png");
    Texture2D playerTexture = LoadTexture("C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/player.png");
    Rectangle player = { 100, 201, 50, 50 };
    Rectangle enemy = { 300, 500, 50, 50 };
    Rectangle door = { 750, 450, 50, 100 }; // z. B. rechte Seite des Raums
    Vector2 position = { 201.0f, 201.0f };


    SetTargetFPS(60);

while (!WindowShouldClose()) {
        // Bewegung des Spielers mit WASD
        if (IsKeyDown(KEY_D)&& (player.x<screenWidth-player.width)) player.x += 2.0f;
        if (IsKeyDown(KEY_A)&& (player.x>0)) player.x -= 2.0f;
        if (IsKeyDown(KEY_S)&& (player.y<screenHeight-player.height)) player.y += 2.0f;
        if (IsKeyDown(KEY_W)&& (player.y>200)) player.y -= 2.0f;

        /*if (CheckCollisionRecs(player, door)) {
        WechselRaum(&backround, "C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/raum2.png");
        player.x = 10; // Spieler neu positionieren
        player.y = 450;*/

        bool collision = CheckCollisionRecs(player, enemy);

        BeginDrawing();
        ClearBackground(RAYWHITE);

        //DrawText("Bewege das blaue Rechteck mit den Pfeiltasten", 10, 10, 20, DARKGRAY);
        DrawTexture(backround, 0, 201, WHITE);
        DrawTextureEx(playerTexture, (Vector2){player.x,player.y}, 0.0f, 0.1f, WHITE);
        DrawRectangleRec(enemy, RED);
        DrawRectangleRec(door, BROWN);
        //DrawRectangleRec(player, collision ? GREEN : BLUE);

        if (collision) {
            DrawText("Kollision erkannt!", 10, 40, 20, MAROON);
        }
        
        if (CheckCollisionRecs(player, door)) {
        WechselRaum(&backround, "C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/raum2.png");
        player.x = 10; // Spieler neu positionieren
        player.y = 450;
}


        EndDrawing();
    }

    CloseWindow();
    UnloadTexture(playerTexture);
    UnloadTexture(backround);
    return 0;
}

void WechselRaum(Texture2D* background, const char* neuerRaumPfad) {
    UnloadTexture(*background);
    *background = LoadTexture(neuerRaumPfad);
}


