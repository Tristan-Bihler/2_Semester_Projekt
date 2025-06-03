#include <raylib.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>

#define MAX_ROOMS 5
#define SCREEN_WIDTH 800
#define SCREEN_HEIGHT 1000

typedef struct Raum {
    int id;
    const char* bildPfad;
    Texture2D textur;
    int nachbarn[4]; // 0 = oben, 1 = rechts, 2 = unten, 3 = links
} Raum;

Raum raeume[MAX_ROOMS];
int aktuellerRaum = 0;

Rectangle player = {400, 600, 50, 50};
Texture2D playerTexture;
const float speed = 4.0f;

// Türen
Rectangle tueren[4] = {
    {350, 201, 100, 30},  // oben
    {770, 551, 30, 100},  // rechts
    {350, 970, 100, 30},  // unten
    {0, 551, 30, 100}     // links
};

void InitRaeume() {
    static char pfade[MAX_ROOMS][64];  // statischer Speicher für Pfade

    for (int i = 0; i < MAX_ROOMS; i++) {
        sprintf(pfade[i], "C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/raum%d.png", i);  // Pfad in statisches Array schreiben
        raeume[i].id = i;
        raeume[i].bildPfad = pfade[i];              // Zeiger auf den statischen Pfad
        raeume[i].textur = LoadTexture(pfade[i]);

        for (int j = 0; j < 4; j++) {
            raeume[i].nachbarn[j] = -1;
        }
    }

    // Zufällige Verknüpfung (linearer Pfad)
    for (int i = 0; i < MAX_ROOMS - 1; i++) {
        int richtung = GetRandomValue(0, 3);
        int gegenrichtung = (richtung + 2) % 4;
        raeume[i].nachbarn[richtung] = i + 1;
        raeume[i + 1].nachbarn[gegenrichtung] = i;
    }
}


void WechselRaum(int richtung) {
    int ziel = raeume[aktuellerRaum].nachbarn[richtung];
    if (ziel != -1) {
        aktuellerRaum = ziel;
        // Spielerposition anpassen
        switch (richtung) {
            case 0: player.y = SCREEN_HEIGHT - (player.height + 35); break; // oben → unten erscheinen
            case 1: player.x = 40; break; // rechts → links erscheinen
            case 2: player.y = 240; break; // unten → oben erscheinen
            case 3: player.x = SCREEN_WIDTH - (player.width + 35); break; // links → rechts erscheinen
        }
    }
}

int main() {
    InitWindow(SCREEN_WIDTH, SCREEN_HEIGHT, "Zufällige Räume mit Rückkehr");
    SetTargetFPS(60);
    srand(time(NULL));

    InitRaeume();
    playerTexture = LoadTexture("C:/Users/finnes/Documents/GitHub/2_Semester_Projekt/C++_Projekt/assets/player.png");

    while (!WindowShouldClose()) {
        // Bewegung
        if (IsKeyDown(KEY_D) && player.x < SCREEN_WIDTH - player.width) player.x += speed;
        if (IsKeyDown(KEY_A) && player.x > 0) player.x -= speed;
        if (IsKeyDown(KEY_S) && player.y < SCREEN_HEIGHT - player.height) player.y += speed;
        if (IsKeyDown(KEY_W) && player.y > 200) player.y -= speed;

        // Tür-Kollision prüfen
        for (int i = 0; i < 4; i++) {
            if (CheckCollisionRecs(player, tueren[i])) {
                WechselRaum(i);
                break;
            }
        }

        // Zeichnen
        BeginDrawing();
        ClearBackground(RAYWHITE);
        DrawTexture(raeume[aktuellerRaum].textur, 0, 201, WHITE);

        for (int i = 0; i < 4; i++) {
            if (raeume[aktuellerRaum].nachbarn[i] != -1)
                DrawRectangleRec(tueren[i], BROWN);
        }

        DrawTextureEx(playerTexture, (Vector2){player.x, player.y}, 0.0f, 0.1f, WHITE);
        DrawText(TextFormat("Raum: %d", aktuellerRaum), 10, 10, 20, DARKGRAY);
        EndDrawing();
    }

    // Ressourcen freigeben
    for (int i = 0; i < MAX_ROOMS; i++) {
        UnloadTexture(raeume[i].textur);
        free((void*)raeume[i].bildPfad);
    }
    UnloadTexture(playerTexture);
    CloseWindow();
    return 0;
}