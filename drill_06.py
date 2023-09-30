from pico2d import *
import random
import math

TUK_WIDTH, TUK_HEIGHT = 1280, 720
open_canvas(TUK_WIDTH, TUK_HEIGHT)
tuk_ground = load_image('TUK_GROUND.png')
character = load_image('animation_sheet.png')
hand_image = load_image('hand_arrow.png')

def handle_events():
    global running
    global x, y
    global m_x, m_y
    global h_x, h_y
    global hand_positions

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_MOUSEMOTION:
            m_x, m_y = event.x, TUK_HEIGHT - 1 - event.y
        elif event.type == SDL_MOUSEBUTTONDOWN:
            hand_positions.append((m_x, m_y))

        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False

running = True
frame = 0
m_x, m_y = TUK_WIDTH // 2, TUK_HEIGHT // 2
x, y = TUK_WIDTH // 2, TUK_HEIGHT // 2
hide_cursor()
hand_positions = []  # 클릭한 순서대로 저장할 손 이미지의 목표 위치 리스트
current_target_index = 0  # 현재 이동 중인 목표 위치의 인덱스

while running:
    clear_canvas()
    tuk_ground.draw(TUK_WIDTH // 2, TUK_HEIGHT // 2)
    hand_image.draw(m_x, m_y)

    if current_target_index < len(hand_positions):
        # 현재 이동 중인 목표 위치로 이동
        target_x, target_y = hand_positions[current_target_index]
        dx, dy = target_x - x, target_y - y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            x += dx / distance * 10
            y += dy / distance * 10

        if dx >= 0:
            character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
        elif dx < 0:
            character.clip_composite_draw(frame * 100, 100 * 1, 100, 100, 0, 'h', x, y, 100, 100)

        # 현재 목표 위치에 도착한 경우 다음 목표 위치로 이동
        if distance <= 30:
            #current_target_index += 1
            del hand_positions[0]
    else:
        character.clip_draw(frame * 100, 100 * 1, 100, 100, x, y)
    # 클릭한 위치에 손 이미지 그리기
    for pos in hand_positions:
        hand_image.draw(pos[0], pos[1])

    update_canvas()
    handle_events()
    frame = (frame + 1) % 8
    delay(0.05)

close_canvas()