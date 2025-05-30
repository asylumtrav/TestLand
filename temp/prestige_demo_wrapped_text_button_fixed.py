import pygame
import sys

# --- Setup ---
pygame.init()
window_width, window_height = 1000, 600
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Scrollable Upgrade Menu")
clock = pygame.time.Clock()

# --- Colors & Fonts ---
BG_COLOR = (25, 25, 30)
LEFT_BG = (40, 40, 50)
RIGHT_BG = (30, 30, 40)
BUTTON_BG = (50, 50, 70)
HIGHLIGHT_COLOR = (100, 150, 255)
TEXT_COLOR = (220, 220, 230)
TOOLTIP_BG = (60, 60, 80)

pygame.font.init()
FONT = pygame.font.SysFont(None, 28)
BIG_FONT = pygame.font.SysFont(None, 36)

# --- Images ---
fingerstorm_img = pygame.image.load("assets/fingerstorm.png")
clickcrossfit_img = pygame.image.load("assets/clickcrossfit.png")
infiniteindex_img = pygame.image.load("assets/infiniteindex.png")

icon_size = (48, 48)
fingerstorm_img = pygame.transform.scale(fingerstorm_img, icon_size)
clickcrossfit_img = pygame.transform.scale(clickcrossfit_img, icon_size)
infiniteindex_img = pygame.transform.scale(infiniteindex_img, icon_size)

# --- Tab State ---
tabs = ["CP", "CPS", "PRESTIGE"]
active_tab = "CP"
mouse_down = False
scroll_offset_cp = 0
scroll_offset_cps = 0
scroll_speed = 20

# --- Upgrade Lists ---
cp_upgrades = [
    {"text": "Pixel Puncher | Cost: 10 | Owned: 0 | CP +0.1"},
    {"text": "Fingerstorm | Cost: 25 | Owned: 0 | CP +0.2", "icon": fingerstorm_img},
    {"text": "ClickCrossfit | Cost: 60 | Owned: 0 | CP +0.3", "icon": clickcrossfit_img},
    {"text": "Infinite Index | Cost: 500 | Owned: 0 | CP +0.8", "icon": infiniteindex_img},
    {"text": "Carpal Karma | Cost: 1000 | Owned: 0 | CP +1.0"},
    {"text": "Mouse Melter | Cost: 2500 | Owned: 0 | CP +1.5"},
    {"text": "Quantum Click | Cost: 5000 | Owned: 0 | CP +2.0"},
    {"text": "Click Titan | Cost: 10000 | Owned: 0 | CP +3.0"},
    {"text": "Tap God | Cost: 20000 | Owned: 0 | CP +5.0"}
]

cps_upgrades = [
    {"text": "Street Sweeper | Cost: 50 | Owned: 0 | CPS +1.0"},
    {"text": "Golden Paws | Cost: 200 | Owned: 0 | CPS +2.0"},
    {"text": "Coin Roomba | Cost: 500 | Owned: 0 | CPS +4.0"},
    {"text": "Quarter Drone | Cost: 1000 | Owned: 0 | CPS +6.0"},
    {"text": "Money Magnet | Cost: 2500 | Owned: 0 | CPS +10.0"},
    {"text": "Piggy Pilot | Cost: 5000 | Owned: 0 | CPS +15.0"},
    {"text": "ATM Army | Cost: 10000 | Owned: 0 | CPS +25.0"},
    {"text": "Cash Cyclone | Cost: 20000 | Owned: 0 | CPS +40.0"},
    {"text": "Coin Forge | Cost: 50000 | Owned: 0 | CPS +65.0"}
]

# --- Helpers ---
def draw_button(surface, rect, enabled=True, hover=False):
    color = HIGHLIGHT_COLOR if hover else BUTTON_BG
    pygame.draw.rect(surface, color, rect, border_radius=15)

def draw_multiline_text_in_rect(surface, text, rect, font):
    segments = text.split(" | ")
    lines = []
    line = ""
    max_width = rect.width - 10

    for segment in segments:
        if font.size(line + segment)[0] <= max_width:
            line += segment + "  "
        else:
            lines.append(line.strip())
            line = segment + "  "
    if line:
        lines.append(line.strip())

    y = rect.centery - (len(lines) * font.get_height()) // 2
    for line in lines:
        txt_surf = font.render(line, True, TEXT_COLOR)
        txt_rect = txt_surf.get_rect(centerx=rect.centerx, y=y)
        surface.blit(txt_surf, txt_rect)
        y += font.get_height()

# --- Main Loop ---
running = True
while running:
    screen.fill(BG_COLOR)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEWHEEL:
            if active_tab == "CP":
                scroll_offset_cp += event.y * scroll_speed
            elif active_tab == "CPS":
                scroll_offset_cps += event.y * scroll_speed

    # Draw upgrade menu
    if active_tab == "CP":
        upgrades = cp_upgrades
        offset = scroll_offset_cp
    elif active_tab == "CPS":
        upgrades = cps_upgrades
        offset = scroll_offset_cps
    else:
        upgrades = []
        offset = 0

    start_y = 100 + offset
    for upgrade in upgrades:
        btn_rect = pygame.Rect(100, start_y, 800, 60)
        pygame.draw.rect(screen, BUTTON_BG, btn_rect, border_radius=10)
        if "icon" in upgrade:
            screen.blit(upgrade["icon"], (btn_rect.x + 6, btn_rect.y + 6))
            txt_rect = pygame.Rect(btn_rect.x + 60, btn_rect.y, btn_rect.width - 60, btn_rect.height)
        else:
            txt_rect = btn_rect
        draw_multiline_text_in_rect(screen, upgrade["text"], txt_rect, FONT)
        start_y += 70

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
