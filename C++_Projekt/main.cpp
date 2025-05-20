#include "raylib.h"


typedef struct Player {
    Vector2 position;
    float speed;
} Player;

#define PLAYER_HOR_SPD 200.0f


void UpdatePlayer(Player *player, float delta);

int main(void)
{
    const int screenWidth = 800;
    const int screenHeight = 450;

    InitWindow(screenWidth, screenHeight, "raylib [core] example - basic window");

    SetTargetFPS(60);

    Camera2D camera = { 0 };
    camera.zoom = 1.0f;

    Player player = { 0 };
    player.position = (Vector2){ 400, 280 };

    SetTargetFPS(60);

    while (!WindowShouldClose())
    {
        float deltaTime = GetFrameTime();

        UpdatePlayer(&player, deltaTime);

        BeginDrawing();

            ClearBackground(LIGHTGRAY);

            BeginMode2D(camera);

                Rectangle playerRect = { player.position.x - 20, player.position.y - 40, 40.0f, 40.0f };
                DrawRectangleRec(playerRect, RED);
                
                DrawCircleV(player.position, 5.0f, GOLD);

            EndMode2D();
        EndDrawing();
    }

    CloseWindow();

    return 0;
}

void UpdatePlayer(Player *player, float delta)
{
    if (IsKeyDown(KEY_LEFT)) player->position.x -= PLAYER_HOR_SPD*delta;
    if (IsKeyDown(KEY_RIGHT)) player->position.x += PLAYER_HOR_SPD*delta;
    if (IsKeyDown(KEY_UP)) player->position.y += PLAYER_HOR_SPD*delta;
    if (IsKeyDown(KEY_DOWN)) player->position.y -= PLAYER_HOR_SPD*delta;
}
