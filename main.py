import pygame
from utils import WIDTH, HEIGHT, COLORS
from grid import Grid
from searching_algorithms import bfs, dfs, astar, dls, greedy, h_euclidian_distance, h_manhattan_distance, ida, iddfs, ucs

pygame.init()

if __name__ == "__main__":
    WIN = pygame.display.set_mode((WIDTH, HEIGHT + 60))

    # set a caption for the window
    pygame.display.set_caption("Pretty Pink Pathfinding Algorithm Visualizer")

    BUTTON_HEIGHT = 40
    BUTTONS = [
        ("BFS", bfs),
        ("DFS", dfs),
        ("A*", astar),
        ("DLS", lambda d, g, s, e: dls(d, g, s, e, get_depth_limit())),
        ("UCS", ucs),
        ("Greedy", greedy),
        ("IDDFS", lambda d, g, s, e: iddfs(d, g, s, e, get_depth_limit())),
        ("IDA*", ida),
    ]
    button_rects = []

    HEURISTICS = {
        "Manhattan": h_manhattan_distance,
        "Euclidean": h_euclidian_distance,
    }
    selected_heuristic_name = "Manhattan" # by default, Manhattan distance
    heuristic_dropdown_open = False

    ROWS = 50  # number of rows
    COLS = 50  # number of columns
    grid = Grid(WIN, ROWS, COLS, WIDTH, HEIGHT)

    font = pygame.font.SysFont(None, 24) # sadly keep default for portable code

    def draw_buttons(selected_name):
        y = HEIGHT + 10
        x = 10
        for name, _ in BUTTONS:
            rect = pygame.Rect(x, y, 90, BUTTON_HEIGHT)
            button_rects.append((rect, name))
            if name == selected_name:
                color = COLORS['ORANGE']
            else:
                color = COLORS['DARK PINK']
            pygame.draw.rect(WIN, color, rect)
            pygame.draw.rect(WIN, COLORS['WHITE'], rect, 2)
            text = font.render(name, True, COLORS['WHITE'])
            text_rect = text.get_rect(center=rect.center)
            WIN.blit(text, text_rect)
            x += 100

    input_box_active = False
    input_text = ""
    input_box_rect = pygame.Rect(0, 0, 0, 0)
    def draw_input_depth_limit():
        global input_box_rect
        BAR_HEIGHT = 60
        pygame.draw.rect(WIN, COLORS['DARK PINK'], (0, 0, WIDTH, BAR_HEIGHT))
        padding_y = 10

        label_text = "Depth Limit:"
        label_surface = font.render(label_text, True, COLORS['WHITE'])
        label_rect = label_surface.get_rect()
        label_rect.topleft = (WIDTH - 250, (BAR_HEIGHT - label_rect.height) // 2)

        input_width = 80
        input_height = label_rect.height + padding_y * 2
        x = label_rect.right + 10
        y = (BAR_HEIGHT - input_height) // 2

        input_box_rect.update(x, y, input_width, input_height)
        border_color = COLORS['ORANGE'] if input_box_active else COLORS['WHITE']
        pygame.draw.rect(WIN, COLORS['PINK'], input_box_rect)
        pygame.draw.rect(WIN, border_color, input_box_rect, 2)

        text_surface = font.render(input_text or "Type...", True, COLORS['WHITE'])
        WIN.blit(label_surface, label_rect.topleft)
        WIN.blit(text_surface, (input_box_rect.x + 5, input_box_rect.y + 5))

    def get_depth_limit():
        try:
            return int(input_text)
        except ValueError:
            return 0
        
    def draw_heuristic_dropdown():
        BAR_HEIGHT = 60
        pygame.draw.rect(WIN, COLORS['DARK PINK'], (0, 0, WIDTH, BAR_HEIGHT))

        padding_x = 20
        padding_y = 10

        text = f"Heuristic: {selected_heuristic_name}"
        text_surface = font.render(text, True, COLORS['WHITE'])
        text_width, text_height = font.size(text)

        rect_width = text_width + padding_x * 2
        rect_height = text_height + padding_y * 2
        x = WIDTH - rect_width - 20
        y = (BAR_HEIGHT - rect_height) // 2

        dropdown_rect = pygame.Rect(x, y, rect_width, rect_height)

        pygame.draw.rect(WIN, COLORS['PINK'], dropdown_rect)
        pygame.draw.rect(WIN, COLORS['WHITE'], dropdown_rect, 2)
        text_rect = text_surface.get_rect(center=dropdown_rect.center)
        WIN.blit(text_surface, text_rect)

        if heuristic_dropdown_open:
            for i, name in enumerate(HEURISTICS.keys()):
                option = font.render(name, True, COLORS['WHITE'])
                option_width, option_height = font.size(name)
                option_rect = pygame.Rect(x, BAR_HEIGHT + i * rect_height, max(rect_width, option_width + padding_x * 2), rect_height)
                pygame.draw.rect(WIN, COLORS['DARK PINK'], option_rect)
                pygame.draw.rect(WIN, COLORS['WHITE'], option_rect, 2)
                option_text_rect = option.get_rect(center=option_rect.center)
                WIN.blit(option, option_text_rect)

    def get_clicked_button(pos):
        for rect, name in button_rects:
            if rect.collidepoint(pos):
                return name
        return None
    
    def handle_dropdown_click(pos):
        global heuristic_dropdown_open, selected_heuristic_name # global keyword to modify vars outside function

        BAR_HEIGHT = 60
        padding_x, padding_y = 20, 10
        text = f"Heuristic: {selected_heuristic_name}"
        text_width, text_height = font.size(text)
        rect_width = text_width + padding_x * 2
        rect_height = text_height + padding_y * 2
        x = WIDTH - rect_width - 20
        y = (BAR_HEIGHT - rect_height) // 2

        dropdown_rect = pygame.Rect(x, y, rect_width, rect_height)
        if dropdown_rect.collidepoint(pos):
            heuristic_dropdown_open = not heuristic_dropdown_open
            return True # user clicked on dropdown button, not grid

        if heuristic_dropdown_open:
            for i, name in enumerate(HEURISTICS.keys()):
                option_rect = pygame.Rect(x, BAR_HEIGHT + i * rect_height, rect_width, rect_height)
                if option_rect.collidepoint(pos):
                    selected_heuristic_name = name
                    heuristic_dropdown_open = False
                    return True # user clicked on dropdown option, not grid
        return False

    def draw_instructions():
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 0))
        text = font.render("Press SPACE to run | Press C to clear the grid", True, COLORS['PURPLE'])
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
        pygame.draw.rect(overlay, COLORS['WHITE'], text_rect.inflate(20, 10))
        overlay.blit(text, text_rect)
        WIN.blit(overlay, (0, 0))

    start = None
    end = None
    selected_algorithm_name = None
    selected_algorithm_func = None

    # flags for running the main loop
    run = True
    started = False

    while run:
        grid.draw(update_display=False)  # draw grid without updating display
        button_rects.clear()
        draw_instructions()
        draw_buttons(selected_algorithm_name)
        if selected_algorithm_name in ["A*", "Greedy", "IDA*"]:
            draw_heuristic_dropdown()
        if selected_algorithm_name in ["DLS", "IDDFS"]:
            draw_input_depth_limit()
        pygame.display.update()   

        for event in pygame.event.get():
            # verify what events happened
            if event.type == pygame.QUIT:
                run = False

            if started:
                # do not allow any other interaction if the algorithm has started
                continue  # ignore other events if algorithm started

            if pygame.mouse.get_pressed()[0]:  # LEFT CLICK
                pos = pygame.mouse.get_pos()
                if selected_algorithm_name in ["DLS", "IDDFS"]:
                    if input_box_rect.collidepoint(event.pos):
                        input_box_active = True
                    else:
                        input_box_active = False

                if handle_dropdown_click(pos):
                    continue

                if pos[1] > HEIGHT:
                    clicked = get_clicked_button(pos)
                    if clicked:
                        selected_algorithm_name = clicked
                        selected_algorithm_func = dict(BUTTONS)[clicked]
                    continue
                row, col = grid.get_clicked_pos(pos)

                if row >= ROWS or row < 0 or col >= COLS or col < 0:
                    continue  # ignore clicks outside the grid

                spot = grid.grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT CLICK
                pos = pygame.mouse.get_pos()
                if pos[1] > HEIGHT:
                    clicked = get_clicked_button(pos)
                    if clicked:
                        selected_algorithm_name = clicked
                        selected_algorithm_func = dict(BUTTONS)[clicked]
                    continue
                row, col = grid.get_clicked_pos(pos)
                spot = grid.grid[row][col]
                spot.reset()

                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if input_box_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.unicode.isdigit():  # only allow numbers
                        input_text += event.unicode

                if event.key == pygame.K_SPACE and not started:
                    if start and end and selected_algorithm_func:
                        for row in grid.grid:
                            for spot in row:
                                spot.update_neighbors(grid.grid)
                        started = True

                        if selected_algorithm_name in ["A*", "Greedy", "IDA*"]:
                            selected_algorithm_func(lambda: grid.draw(), grid, start, end, heuristic=HEURISTICS[selected_heuristic_name])
                        else:
                            selected_algorithm_func(lambda: grid.draw(), grid, start, end)
                        started = False

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid.reset()
                    selected_algorithm_name = None
    pygame.quit()
