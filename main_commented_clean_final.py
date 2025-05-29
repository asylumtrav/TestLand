import pygame
import pygame.mixer
import sys
import random
import math
import json
import time
import os

# --- Constants & initial window size ---
INITIAL_WINDOW_WIDTH = 1000
INITIAL_WINDOW_HEIGHT = 600
FPS = 60

PRICE_INCREASE = 1.15
LINEAR_INCREASE = 0.75


#loading images relative and not path specific
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

SOUND_PATH = os.path.join(ASSETS_DIR, "coinbag.mp3")

#os.path.join(ASSETS_DIR, "pixelpuncher.png")

BG_COLOR = (25, 25, 30)
LEFT_BG = (40, 40, 50)
RIGHT_BG = (30, 30, 40)
TEXT_COLOR = (220, 220, 230)
HIGHLIGHT_COLOR = (100, 150, 255)
BUTTON_BG = (50, 50, 70)
BUTTON_HOVER = (80, 80, 110)
BUTTON_DISABLED = (80, 80, 80)

ACHIEVEMENT_BG = BUTTON_BG
ACHIEVEMENT_HOVER = BUTTON_HOVER

ACHIEVEMENT_MENU_BG = (40, 45, 60)  # distinct bg for achievement menu
ACHIEVEMENT_MENU_BORDER = (90, 130, 190)

MULTIPLIERS = [1, 3, 5, 'max']


# --- Large Number Formatter ---
def format_large_number(n):
    if n < 1000:
        return str(int(n))
    names = [
        "", "thousand", "million", "billion", "trillion", "quadrillion", "quintillion",
        "sextillion", "septillion", "octillion", "nonillion", "decillion", "undecillion",
        "duodecillion", "tredecillion", "quattuordecillion", "quindecillion", "sexdecillion",
        "septendecillion", "octodecillion", "novemdecillion", "vigintillion", "unvigintillion",
        "duovigintillion", "trevigintillion", "quattuorvigintillion", "quinvigintillion",
        "sexvigintillion", "septenvigintillion", "octovigintillion", "novemvigintillion",
        "trigintillion", "untrigintillion", "duotrigintillion", "tretrigintillion",
        "quattuortrigintillion", "quintrigintillion", "sextrigintillion", "septentrigintillion",
        "octotrigintillion", "novemtrigintillion", "quadragintillion", "unquadragintillion",
        "duoquadragintillion", "trequadragintillion", "quattuorquadragintillion",
        "quinquadragintillion", "sexquadragintillion", "septenquadragintillion",
        "octoquadragintillion", "novemquadragintillion", "quinquagintillion",
        "unquinquagintillion", "duoquinquagintillion", "trequinquagintillion",
        "quattuorquinquagintillion", "quinquinquagintillion", "sexquinquagintillion",
        "septenquinquagintillion", "octoquinquagintillion", "novemquinquagintillion",
        "sexagintillion", "unsexagintillion", "duosexagintillion", "tresexagintillion",
        "quattuorsexagintillion", "quinsexagintillion", "sexsexagintillion",
        "septensexagintillion", "octosexagintillion", "novemsexagintillion",
        "septuagintillion", "unseptuagintillion", "duoseptuagintillion", "treseptuagintillion",
        "quattuorseptuagintillion", "quinseptuagintillion", "sexseptuagintillion",
        "septenseptuagintillion", "octoseptuagintillion", "novemseptuagintillion",
        "octogintillion", "unoctogintillion", "duooctogintillion", "treoctogintillion",
        "quattuoroctogintillion", "quinoctogintillion", "sexoctogintillion",
        "septoctogintillion", "octooctogintillion", "novemoctogintillion",
        "nonagintillion", "unnonagintillion", "duononagintillion", "trenonagintillion",
        "quattuornonagintillion", "quinnonagintillion", "sexnonagintillion",
        "septennonagintillion", "octononagintillion", "novemnonagintillion",
        "centillion"
    ]
    index = 0
    number = float(n)
    while number >= 1000 and index < len(names) - 1:
        number /= 1000.0
        index += 1
    if index == 0:
        return str(int(number))
    else:
        return f"{number:.2f} {names[index]}"

# --- Prestige cubic scaling starting at 20 billion coins ---
def calculate_prestige_level(all_time_coins, current_prestige):
    base = 20_000_000_000  # 20 billion
    n = int(math.floor((all_time_coins / base) ** (1/3)))
    return max(0, n - current_prestige)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(os.path.dirname(__file__))
    full_path = os.path.join(base_path, relative_path)
    print(f"Resolved path: {full_path}")
    return full_path


# --- Upgrade Data ---
click_upgrades = [
    {"name": "Pixel Puncher", "base_cost": 10, "click_power": 0.1, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Fingerstorm", "base_cost": 25, "click_power": 0.2, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "fingerstorm.png")},
    {"name": "Thumb Strength", "base_cost": 75, "click_power": 0.4, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "thumbstrength.png")},
    {"name": "Tendon Tornado", "base_cost": 200, "click_power": 0.6, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Infinite Index", "base_cost": 500, "click_power": 0.8, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Carpal Karma", "base_cost": 1000, "click_power": 1.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Mouse Melter", "base_cost": 2500, "click_power": 1.5, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Quantum Click", "base_cost": 5000, "click_power": 2.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Click Titan", "base_cost": 10000, "click_power": 3.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Tap God", "base_cost": 20000, "click_power": 5.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
]

auto_upgrades = [
    {"name": "Street Sweeper", "base_cost": 50, "cps": 1.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Golden Paws", "base_cost": 200, "cps": 2.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Coin Roomba", "base_cost": 500, "cps": 4.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Bankstorm", "base_cost": 1000, "cps": 6.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Money Magnet", "base_cost": 2500, "cps": 10.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Piggy Pilot", "base_cost": 5000, "cps": 15.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "ATM Army", "base_cost": 10000, "cps": 25.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Cash Cyclone", "base_cost": 20000, "cps": 40.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Cash Overlord", "base_cost": 50000, "cps": 65.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Crypto Kraken", "base_cost": 100000, "cps": 100.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Vault Vortex", "base_cost": 250000, "cps": 160.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Gold Blaster", "base_cost": 500000, "cps": 250.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Coin Geyser", "base_cost": 1000000, "cps": 400.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Cash Comet", "base_cost": 2500000, "cps": 650.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Capital Core", "base_cost": 5000000, "cps": 1000.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Bitcoin Barn", "base_cost": 10000000, "cps": 1600.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Compound Farm", "base_cost": 25000000, "cps": 2500.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Money Machine", "base_cost": 50000000, "cps": 4000.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "Rich Reactor", "base_cost": 100000000, "cps": 6500.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
    {"name": "The Moneyverse", "base_cost": 250000000, "cps": 10000.0, "owned": 0, "max_owned": 1000000, "image_path": os.path.join(ASSETS_DIR, "pixelpuncher.png")},
]

# If all buildings use the same thresholds, just do:
standard_requires_owned = [1, 10, 25, 50, 100, 200, 300, 400, 500, 600]

def generate_multiplier_upgrades(base_name, base_type, base_index, base_cost, requires_owned_list, num_levels=10):
    upgrades = []
    for i in range(num_levels):
        level = i + 1
        cost = base_cost * (1.15 ** level)
        boost = 0.02 * (1.15 ** level)
        requires_owned = requires_owned_list[i] if i < len(requires_owned_list) else level
        upgrades.append({
            "name": f"{base_name}",
            "associated_upgrade_index": base_index,
            "type": base_type,
            "level": level,
            "cost": round(cost),
            "boost_percent": round(boost, 4),
            "purchased": False,
            "requires_owned": requires_owned
        })
    return upgrades

cps_multipliers = []
for idx, upg in enumerate(auto_upgrades):
    cps_multipliers.extend(
        generate_multiplier_upgrades(
            upg["name"], "CPS", idx, upg["base_cost"], standard_requires_owned, num_levels=len(standard_requires_owned)
        )
    )

cp_multipliers = []
for idx, upg in enumerate(click_upgrades):
    cp_multipliers.extend(
        generate_multiplier_upgrades(
            upg["name"], "CP", idx, upg["base_cost"], standard_requires_owned, num_levels=len(standard_requires_owned)
        )
    )

# --- Achievement Data ---
def generate_achievements():
    achievements = []

    # Click achievements
    click_goals = [10, 100, 1000, 10000, 100000, 1_000_000]
    for goal in click_goals:
        achievements.append({
            "category": "click",
            "name": f"Clicker Tycoon: {goal}",
            "desc": f"Click the coin {goal:,} times. Your finger’s getting strong!",
            "goal": goal,
            "completed": False
        })

    # All-time money achievements
    money_goals = [10, 1000, 10000, 100000, 1_000_000, 100_000_000, 10**9, 10**12, 10**15, 10**18]
    money_names = [
        "Pocket Change",
        "Lunch Money",
        "Side Hustler",
        "Coin Collector",
        "Cash King",
        "Fortune Founder",
        "Tycoon Tactician",
        "Billionaire Brain",
        "Trillionaire Titan",
        "Quintillionaire Quest"
    ]
    for i, goal in enumerate(money_goals):
        name = money_names[i] if i < len(money_names) else f"Money Milestone: {goal}"
        achievements.append({
            "category": "money",
            "name": name,
            "desc": f"Accumulate {format_large_number(goal)} coins across all time. You’re on a roll!",
            "goal": goal,
            "completed": False
        })

    return achievements

    # Click achievements (category: 'click')
    click_goals = [10, 100, 1000, 10000, 100000, 1000000]
    for c in click_goals:
        achievements.append({
            "category": "click",
            "name": f"Clicker Tycoon: {format_large_number(c)} Clicks",
            "goal": c,
            "completed": False,
            "desc": f"Click the coin {format_large_number(c)} times.",
            "unlocked_time": None,
        })


    # All-time money achievements (category: 'money')
    money_goals = [
        10, 100, 1000, 10_000, 100_000, 1_000_000, 10_000_000,
        100_000_000, 1_000_000_000, 10_000_000_000, 100_000_000_000,
        1_000_000_000_000, 10_000_000_000_000, 100_000_000_000_000,
        1_000_000_000_000_000, 10_000_000_000_000_000, 100_000_000_000_000_000,
        1_000_000_000_000_000_000, 10_000_000_000_000_000_000, 100_000_000_000_000_000_000,
        1_000_000_000_000_000_000_000, 10_000_000_000_000_000_000_000  # up to 10 quintillion
    ]

    for m in money_goals:
        achievements.append({
            "category": "money",
            "name": f"Money Maven: {format_large_number(m)} Coins",
            "goal": m,
            "completed": False,
            "desc": f"Accumulate {format_large_number(m)} total coins earned.",
            "unlocked_time": None,
        })

    return achievements

# --- Game State ---
class GameState:
    def __init__(self):
        self.coins = 100000000000
        self.all_time_coins = 0.0
        self.prestige = 0
        self.base_click_power = 1.0
        self.click_upgrades = []
        for u in click_upgrades:
            copy_u = dict(u)
            copy_u["base_cost_initial"] = copy_u["base_cost"]
            self.click_upgrades.append(copy_u)
        self.auto_upgrades = []
        for u in auto_upgrades:
            copy_u = dict(u)
            copy_u["base_cost_initial"] = copy_u["base_cost"]
            self.auto_upgrades.append(copy_u)
        self.active_tab = "CP"
        self.upgrade_scroll = 0
        self.buy_multiplier_index = 0

        # Stats tracking
        self.total_clicks = 0
        self.click_times = []
        self.start_time = time.time()
        self.prestige_start_time = time.time()

        # Settings toggles
        self.coin_bag_shake_enabled = True
        self.sound_volume = 5  # 1 to 5, 5 = loudest, 1 = mute

        # Achievements
        achievements = generate_achievements()
        self.achievements = achievements if achievements is not None else []
        self.achievement_scroll = 0

        ##Animation when bought timer
        self.shop_box_flash_timers = [0] * 5  # one for each shop box

        # New for notification popup
        self.achievement_unlocked_queue = []  # queue of achievement names to announce
        self.achievement_popup_time = 0
        self.achievement_popup_duration = 4
        self.current_achievement_popup = None
        self.has_new_achievement = False  # for notification dot

        #Advancemant multipliers
        self.cp_multipliers =cp_multipliers
        self.cps_multipliers = cps_multipliers

        os.chdir(os.path.dirname(os.path.abspath(__file__)))

    def get_total_click_power(self):
        total = self.base_click_power
        for i, upg in enumerate(self.click_upgrades):
            base_power = upg["click_power"] * upg["owned"]

            # Apply multiplier boosts
            multiplier_boost = sum(m["boost_percent"] for m in self.cp_multipliers
                                if m["purchased"] and m["associated_upgrade_index"] == i)

            total += base_power * (1 + multiplier_boost)
        return total
    
    def get_total_multiplier_for_upgrade(self, index, upgrade_type):
        # Return the sum of purchased boosts for the correct type and index.
        if upgrade_type == "click":
            multipliers = self.cp_multipliers
        elif upgrade_type == "auto":
            multipliers = self.cps_multipliers
        else:
            return 1.0

        boost = sum(m["boost_percent"] for m in multipliers if m["purchased"] and m["associated_upgrade_index"] == index)
        return 1 + boost

    def get_total_cps(self):
        total = 0
        for i, upg in enumerate(self.auto_upgrades):
            base_power = upg["cps"] * upg["owned"]

            # Apply multiplier boosts
            multiplier_boost = sum(m["boost_percent"] for m in self.cps_multipliers
                                if m["purchased"] and m["associated_upgrade_index"] == i)

            total += base_power * (1 + multiplier_boost)
        return total

    def can_buy_upgrade(self, upgrade, levels=1):
        total_cost = self.calculate_multi_cost(upgrade, levels)
        return self.coins >= total_cost and (upgrade["owned"] + levels) <= upgrade["max_owned"]

    def buy_upgrade(self, upgrade, levels=1):
        base = upgrade["base_cost_initial"]
        start_level = upgrade["owned"]
        total_cost = self.calculate_multi_cost(upgrade, levels)
        if self.coins >= total_cost and (start_level + levels) <= upgrade["max_owned"]:
            self.coins -= total_cost
            upgrade["owned"] += levels
            upgrade["base_cost"] = self.calculate_cost(base, upgrade["owned"])
            return True
        return False
    
    def generate_multiplier_upgrades(base_name, base_type, base_index, base_cost, requires_owned_list, num_levels=10):
        upgrades = []
        for i in range(num_levels):
            level = i + 1
            cost = base_cost * (1.15 ** level)
            boost = 0.02 * (1.15 ** level)
            # Use the value from requires_owned_list, or fallback to level if not provided
            requires_owned = requires_owned_list[i] if i < len(requires_owned_list) else level
            upgrades.append({
                "name": f"{base_name} Boost Lv {level}",
                "associated_upgrade_index": base_index,
                "type": base_type,
                "level": level,
                "cost": round(cost),
                "boost_percent": round(boost, 4),
                "purchased": False,
                "requires_owned": requires_owned
            })
        return upgrades
    
    def generate_building_upgrades(upgrade_list, upgrade_type, base_multiplier=10, boost=1.0):
        all_multipliers = []
        unlocks = [1, 5, 25, 50, 100, 200, 300]  # Milestone unlocks
        for idx, upg in enumerate(upgrade_list):
            base_name = upg["name"]
            base_cost = upg["base_cost_initial"] if "base_cost_initial" in upg else upg["base_cost"]
            for tier, owned_required in enumerate(unlocks):
                cost = int(base_cost * (base_multiplier ** (tier + 1)))
                all_multipliers.append({
                    "name": f"{base_name} Boost Lv {tier+1}",
                    "associated_upgrade_index": idx,
                    "type": upgrade_type,
                    "level": tier + 1,
                    "cost": cost,
                    "boost_percent": boost,  # +100%
                    "purchased": False,
                    "requires_owned": owned_required,
                    "image_path": f"C:/Users/Administrator/Documents/Coin Game/assets/{base_name.lower().replace(' ', '').replace(':', '')}.png"
                })
        return all_multipliers
    
    for idx, upg in enumerate(auto_upgrades):
        cps_multipliers.extend(
            generate_multiplier_upgrades(
                upg["name"], "CPS", idx, upg["base_cost"], standard_requires_owned
            )
        )


    def calculate_cost(self, base_cost, level):
        return int(base_cost * (PRICE_INCREASE ** level) * (1 + LINEAR_INCREASE * level))

    def calculate_multi_cost(self, upgrade, n):
        base = upgrade["base_cost_initial"]
        start_level = upgrade["owned"]
        total_cost = 0
        for i in range(1, n + 1):
            lvl = start_level + i
            total_cost += self.calculate_cost(base, lvl)
        return total_cost

    def calculate_multi_gain(self, upgrade, n):
        gain_per_level = upgrade.get("click_power", 0) if self.active_tab == "CP" else upgrade.get("cps", 0)
        return gain_per_level * n

    def max_affordable_levels(self, upgrade):
        base = upgrade["base_cost_initial"]
        start_level = upgrade["owned"]
        max_levels = 0
        coins = self.coins
        while max_levels < (upgrade["max_owned"] - start_level):
            cost = self.calculate_cost(base, start_level + max_levels + 1)
            if cost <= coins:
                coins -= cost
                max_levels += 1
            else:
                break
        return max_levels

    def check_achievements(self):
        for ach in self.achievements:
            if ach["completed"]:
                continue
            if ach["category"] == "click" and self.total_clicks >= ach["goal"]:
                ach["completed"] = True
                ach["unlocked_time"] = time.time()
                self.achievement_unlocked_queue.append(ach["name"])
                self.has_new_achievement = True
            elif ach["category"] == "money" and self.all_time_coins >= ach["goal"]:
                ach["completed"] = True
                ach["unlocked_time"] = time.time()
                self.achievement_unlocked_queue.append(ach["name"])
                self.has_new_achievement = True

    def update_achievement_popup(self, dt):
        if self.current_achievement_popup is None and self.achievement_unlocked_queue:
            self.current_achievement_popup = self.achievement_unlocked_queue.pop(0)
            self.achievement_popup_time = 0
        elif self.current_achievement_popup is not None:
            self.achievement_popup_time += dt
            if self.achievement_popup_time > self.achievement_popup_duration:
                self.current_achievement_popup = None
                self.achievement_popup_time = 0

def get_save_file_path(filename="coin_clicker_save.json"):
    if getattr(sys, 'frozen', False):
        # Running as bundled exe
        base_path = sys._MEIPASS  # PyInstaller temp folder for resources
        # But save file should NOT go here — go to executable folder instead:
        base_path = os.path.dirname(sys.executable)
    else:
        # Running as a script
        base_path = os.path.dirname(os.path.abspath(__file__))

    save_dir = os.path.join(base_path, "saves")
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    return os.path.join(save_dir, filename)

SAVE_FILE = get_save_file_path()

# --- Save and Load Functions ---
def save_game(state):
    data = {
        "coins": state.coins,
        "all_time_coins": state.all_time_coins,
        "prestige": state.prestige,
        "click_upgrades": [{"owned": u["owned"]} for u in state.click_upgrades],
        "auto_upgrades": [{"owned": u["owned"]} for u in state.auto_upgrades],
        "last_saved_time": time.time(),
        "buy_multiplier_index": state.buy_multiplier_index,
        "total_clicks": state.total_clicks,
        "click_times": state.click_times,
        "start_time": state.start_time,
        "prestige_start_time": state.prestige_start_time,
        "coin_bag_shake_enabled": state.coin_bag_shake_enabled,
        "sound_volume": state.sound_volume,
        "achievements": [{"completed": a["completed"], "unlocked_time": a.get("unlocked_time", None)} for a in state.achievements],
        "achievement_scroll": state.achievement_scroll,
        "has_new_achievement": state.has_new_achievement,
        "achievement_unlocked_queue": state.achievement_unlocked_queue,
        "current_achievement_popup": state.current_achievement_popup,
        "achievement_popup_time": state.achievement_popup_time,
        "cp_multipliers": [m["purchased"] for m in state.cp_multipliers],
        "cps_multipliers": [m["purchased"] for m in state.cps_multipliers],
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def load_game(state):
    if not os.path.isfile(SAVE_FILE):
        return 0  # no save to load

    with open(SAVE_FILE, "r") as f:
        data = json.load(f)

    # ... your current loading code ...

    # Load click/auto upgrades
    for upg, saved in zip(state.click_upgrades, data.get("click_upgrades", [])):
        upg["owned"] = saved.get("owned", 0)

    for upg, saved in zip(state.auto_upgrades, data.get("auto_upgrades", [])):
        upg["owned"] = saved.get("owned", 0)

    # Load shop upgrade purchases 💡
    cp_purchases = data.get("cp_multipliers", [])
    cps_purchases = data.get("cps_multipliers", [])
    for m, purchased in zip(state.cp_multipliers, cp_purchases):
        m["purchased"] = purchased
    for m, purchased in zip(state.cps_multipliers, cps_purchases):
        m["purchased"] = purchased

    # ... achievements, etc ...

    return data.get("last_saved_time", 0)
# --- UI Helpers ---
def draw_text(surface, text, pos, font, color=TEXT_COLOR):
    txt = font.render(text, True, color)
    surface.blit(txt, pos)

def draw_button(surface, rect, enabled=True, hover=False):
    color = BUTTON_BG
    if not enabled:
        color = BUTTON_DISABLED
        #hover = rect.collidepoint(mouse_pos)
    elif hover:
        color = BUTTON_HOVER
    pygame.draw.rect(surface, color, rect, border_radius=15)

def draw_multiline_text_in_rect(surface, text, rect, font, color=TEXT_COLOR, line_spacing=2, padding=6):
    words = text.split()
    lines = []
    line = ""

    max_width = rect.width - 2 * padding
    for word in words:
        test_line = line + word + " "
        if font.size(test_line)[0] <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word + " "
    if line:
        lines.append(line)

    y = rect.top + padding
    for line in lines:
        rendered = font.render(line.strip(), True, color)
        surface.blit(rendered, (rect.left + padding, y))
        y += font.get_height() + line_spacing

def has_affordable_upgrades(state, upgrades):
    for upg in upgrades:
        if state.can_buy_upgrade(upg):
            return True
    return False

def draw_stats_screen(surface, window_width, window_height, state, big_font, font, mouse_pos, mouse_down):
    overlay_rect = pygame.Rect(100, 80, window_width - 200, window_height - 160)
    pygame.draw.rect(surface, (40, 45, 60), overlay_rect, border_radius=12)
    pygame.draw.rect(surface, (100, 150, 255), overlay_rect, width=3, border_radius=12)

    now = time.time()
    total_played_seconds = max(0, now - state.start_time)
    prestige_played_seconds = max(0, now - state.prestige_start_time)

    one_min_ago = now - 60
    state.click_times = [t for t in state.click_times if t >= one_min_ago]
    clicks_per_minute = len(state.click_times)

    def format_seconds(s):
        m = int(s // 60)
        sec = int(s % 60)
        return f"{m}m {sec}s"

    lines = [
        f"Total Coins Earned: {format_large_number(state.all_time_coins)}",
        f"Total Time Played: {format_seconds(total_played_seconds)}",
        f"Time Played This Prestige: {format_seconds(prestige_played_seconds)}",
        f"Clicks Per Minute: {clicks_per_minute}",
        f"Total Clicks: {state.total_clicks}",
    ]

    padding_left = overlay_rect.left + 20
    y = overlay_rect.top + 20
    line_spacing = 8

    for line in lines:
        text_surf = big_font.render(line, True, (220, 220, 230))
        surface.blit(text_surf, (padding_left, y))
        y += text_surf.get_height() + line_spacing

    # Small 'X' button top-right
    close_size = 30
    close_padding = 15
    close_rect = pygame.Rect(overlay_rect.right - close_size - close_padding, overlay_rect.top + close_padding, close_size, close_size)

    hover = close_rect.collidepoint(mouse_pos)
    color = HIGHLIGHT_COLOR if hover else BUTTON_BG
    pygame.draw.rect(surface, color, close_rect, border_radius=6)

    x_text = font.render("X", True, TEXT_COLOR)
    x_text_rect = x_text.get_rect(center=close_rect.center)
    surface.blit(x_text, x_text_rect)

    clicked_close = False
    if mouse_down and hover:
        clicked_close = True

    return clicked_close


def draw_settings_screen(surface, window_width, window_height, state, big_font, font, mouse_pos, mouse_down, coin_sound):
    overlay_rect = pygame.Rect(100, 80, window_width - 200, window_height - 160)
    pygame.draw.rect(surface, (40, 45, 60), overlay_rect, border_radius=12)
    pygame.draw.rect(surface, (100, 150, 255), overlay_rect, width=3, border_radius=12)

    title_surf = big_font.render("Settings", True, TEXT_COLOR)
    surface.blit(title_surf, (overlay_rect.left + 20, overlay_rect.top + 20))

    label_font = pygame.font.SysFont(None, 28)

    label_surf = label_font.render("Coin Bag Shake", True, TEXT_COLOR)
    surface.blit(label_surf, (overlay_rect.left + 50, overlay_rect.top + 75))

    button_width, button_height = 40, 40
    button_spacing = 10
    btn_x = overlay_rect.left + 50
    btn_y = overlay_rect.top + 100

    off_rect = pygame.Rect(btn_x, btn_y, button_width, button_height)
    off_hover = off_rect.collidepoint(mouse_pos)
    off_color = HIGHLIGHT_COLOR if not state.coin_bag_shake_enabled else BUTTON_BG
    pygame.draw.rect(surface, off_color, off_rect, border_radius=8)
    off_text = label_font.render("OFF", True, TEXT_COLOR)
    off_text_rect = off_text.get_rect(center=off_rect.center)
    surface.blit(off_text, off_text_rect)

    on_rect = pygame.Rect(btn_x + button_width + button_spacing, btn_y, button_width, button_height)
    on_hover = on_rect.collidepoint(mouse_pos)
    on_color = HIGHLIGHT_COLOR if state.coin_bag_shake_enabled else BUTTON_BG
    pygame.draw.rect(surface, on_color, on_rect, border_radius=8)
    on_text = label_font.render("ON", True, TEXT_COLOR)
    on_text_rect = on_text.get_rect(center=on_rect.center)
    surface.blit(on_text, on_text_rect)

    label_surf2 = label_font.render("Sound Volume", True, TEXT_COLOR)
    surface.blit(label_surf2, (btn_x, btn_y + 60))

    tick_size = 30
    tick_spacing = 20
    tick_start_x = btn_x
    tick_y = btn_y + 90

    volume_tick_rects = []

    for i in range(1, 6):
        rect = pygame.Rect(tick_start_x + (i - 1) * (tick_size + tick_spacing), tick_y, tick_size, tick_size)
        volume_tick_rects.append(rect)

        color = HIGHLIGHT_COLOR if state.sound_volume == i else BUTTON_BG
        pygame.draw.rect(surface, color, rect, border_radius=8)

        num_surf = label_font.render(str(i), True, TEXT_COLOR)
        num_rect = num_surf.get_rect(center=rect.center)
        surface.blit(num_surf, num_rect)

    # Small 'X' button top-right
    close_size = 30
    close_padding = 15
    close_rect = pygame.Rect(overlay_rect.right - close_size - close_padding, overlay_rect.top + close_padding, close_size, close_size)

    hover = close_rect.collidepoint(mouse_pos)
    color = HIGHLIGHT_COLOR if hover else BUTTON_BG
    pygame.draw.rect(surface, color, close_rect, border_radius=6)

    x_text = font.render("X", True, TEXT_COLOR)
    x_text_rect = x_text.get_rect(center=close_rect.center)
    surface.blit(x_text, x_text_rect)

    clicked_close = False
    if mouse_down and hover:
        clicked_close = True

    return clicked_close, off_rect, on_rect, volume_tick_rects


def draw_achievements_screen(surface, window_width, window_height, state, big_font, font, mouse_pos, mouse_down):
    overlay_height = window_height - 120
    overlay_rect = pygame.Rect(100, 80, window_width - 200, overlay_height)
    pygame.draw.rect(surface, ACHIEVEMENT_MENU_BG, overlay_rect, border_radius=12)
    pygame.draw.rect(surface, ACHIEVEMENT_MENU_BORDER, overlay_rect, width=3, border_radius=12)

    title_surf = big_font.render("Achievements", True, (220, 220, 230))
    surface.blit(title_surf, (overlay_rect.left + 20, overlay_rect.top + 20))

    # Sort achievements: incomplete first, then completed; within each by category then goal ascending
    sorted_achievements = sorted(state.achievements, key=lambda a: (a["completed"], a["category"], a["goal"]))

    container_rect = pygame.Rect(overlay_rect.left + 20, overlay_rect.top + 60, overlay_rect.width - 40, overlay_rect.height - 110)
    pygame.draw.rect(surface, (40, 45, 60), container_rect, border_radius=8)

    achievement_height = 70
    spacing = 10
    content_height = len(sorted_achievements) * (achievement_height + spacing)
    max_scroll = max(0, content_height - container_rect.height)
    state.achievement_scroll = max(0, min(state.achievement_scroll, max_scroll))

    surface.set_clip(container_rect)

    mouse_hovered_ach = None

    for i, ach in enumerate(sorted_achievements):
        y = container_rect.top + i * (achievement_height + spacing) - state.achievement_scroll
        rect = pygame.Rect(container_rect.left + 10, y, container_rect.width - 20, achievement_height)
        hover = rect.collidepoint(mouse_pos)
        if hover:
            hover = rect.collidepoint(mouse_pos)

        # Background color with hover effect
        color = ACHIEVEMENT_BG
        hover = rect.collidepoint(mouse_pos)
        if hover:
            color = ACHIEVEMENT_HOVER
        if ach["completed"]:
            # Slightly lighter if completed, but same hover logic
            base = BUTTON_BG
            hover_color = BUTTON_HOVER
            color = hover_color if hover else base

        pygame.draw.rect(surface, color, rect, border_radius=15)

        # Achievement name text
        name_color = (200, 230, 255) if ach["completed"] else (180, 200, 220)
        name_surf = big_font.render(ach["name"], True, name_color)
        # Center text vertically and horizontally within rect
        name_rect = name_surf.get_rect()
        name_rect.centery = rect.centery
        name_rect.left = rect.left + 15
        surface.blit(name_surf, name_rect)

        # Owned / Completed text on right side
        status_text = "Completed" if ach["completed"] else f"Goal: {format_large_number(ach['goal'])} clicks" if ach["category"] == "click" else f"Goal: {format_large_number(ach['goal'])} coins"
        status_surf = font.render(status_text, True, name_color)
        status_rect = status_surf.get_rect()
        status_rect.centery = rect.centery
        status_rect.right = rect.right - 15
        surface.blit(status_surf, status_rect)

        hover = rect.collidepoint(mouse_pos)
        if hover:
            mouse_hovered_ach = ach

    surface.set_clip(None)

    if max_scroll > 0:
        scrollbar_width = 12
        scrollbar_height = int(container_rect.height * container_rect.height / content_height)
        scrollbar_height = max(20, scrollbar_height)
        scrollbar_x = container_rect.right - scrollbar_width - 5
        scrollbar_y = container_rect.top + int(state.achievement_scroll * (container_rect.height - scrollbar_height) / max_scroll)

        pygame.draw.rect(surface, (60, 60, 80), (scrollbar_x, container_rect.top, scrollbar_width, container_rect.height), border_radius=6)
        pygame.draw.rect(surface, ACHIEVEMENT_MENU_BORDER, (scrollbar_x, scrollbar_y, scrollbar_width, scrollbar_height), border_radius=6)

    if mouse_hovered_ach:
        tooltip_rect = pygame.Rect(mouse_pos[0] + 15, mouse_pos[1] + 15, 300, 60)
        pygame.draw.rect(surface, (40, 40, 50), tooltip_rect, border_radius=8)
        pygame.draw.rect(surface, HIGHLIGHT_COLOR, tooltip_rect, 2, border_radius=8)

        draw_multiline_text_in_rect(surface, mouse_hovered_ach["desc"], tooltip_rect, font, color=(220, 220, 230))

    # Small 'X' button top-right
    close_size = 30
    close_padding = 15
    close_rect = pygame.Rect(overlay_rect.right - close_size - close_padding, overlay_rect.top + close_padding, close_size, close_size)

    hover = close_rect.collidepoint(mouse_pos)
    color = HIGHLIGHT_COLOR if hover else BUTTON_BG
    pygame.draw.rect(surface, color, close_rect, border_radius=6)

    x_text = font.render("X", True, TEXT_COLOR)
    x_text_rect = x_text.get_rect(center=close_rect.center)
    surface.blit(x_text, x_text_rect)

    clicked_close = False
    if mouse_down and hover:
        clicked_close = True

    return clicked_close


        ######################################
        # Draw tooltips at the very end so they render on top.
        ######################################
    for text, rect in tooltip_queue:
            pygame.draw.rect(screen, (40, 40, 50), rect, border_radius=8)
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 2, border_radius=8)
            draw_multiline_text_in_rect(screen, text, rect, FONT, TEXT_COLOR)
def draw_achievement_popup(surface, state, window_width, font):
    if state.current_achievement_popup:
        popup_width = window_width - 200
        popup_height = 50
        popup_x = 100
        popup_y = 20

        popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)
        pygame.draw.rect(surface, (40, 40, 60), popup_rect, border_radius=8)
        pygame.draw.rect(surface, HIGHLIGHT_COLOR, popup_rect, 2, border_radius=8)

        text = f"Achievement Unlocked: {state.current_achievement_popup}!"
        text_surf = font.render(text, True, (200, 230, 255))
        surface.blit(text_surf, (popup_x + 20, popup_y + (popup_height - text_surf.get_height()) // 2))




def main():
    pygame.init()
    pygame.mixer.init()
    

    window_width, window_height = INITIAL_WINDOW_WIDTH, INITIAL_WINDOW_HEIGHT
    screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
    pygame.display.set_caption("Coin Clicker")
    icon_path = resource_path("assets\icon.ico")  # adjust path to your icon file relative to project root or exe
    try:
        icon_surface = pygame.image.load(icon_path)
        pygame.display.set_icon(icon_surface)
    except Exception as e:
        print(f"Failed to load icon: {e}")

    

        ######################################
        # Initialize the tooltip queue for displaying hover info.
        ######################################
    tooltip_queue = []
    font_base_size = 24
    font_big_size = 32

    clock = pygame.time.Clock()

    state = GameState()

    shake_duration = 0.15
    shake_timer = 0

    try:
        coin_image_path = rplaceholder_path = os.path.join(ASSETS_DIR, "coin.png")
        coin_image_original = pygame.image.load(coin_image_path).convert_alpha()
    except Exception:
        coin_image_original = None

    try:
        coin_sound = pygame.mixer.Sound(SOUND_PATH)
    except Exception:
        coin_sound = None

    mouse_down = False

    showing_stats = False
    showing_settings = False
    showing_achievements = False

    offline_earned = 0
    show_offline_popup = False
    offline_popup_timer = 5.0

    last_saved_time = load_game(state)
    if last_saved_time > 0:
        elapsed = time.time() - last_saved_time
        offline_earned = elapsed * state.get_total_cps()
        if offline_earned >= 1:
            show_offline_popup = True
            state.coins += offline_earned
            state.all_time_coins += offline_earned

    auto_save_timer = 0

    if coin_sound:
        coin_sound.set_volume((state.sound_volume - 1) / 4)


        ######################################
        # This is the main game loop. It handles:
        # - Events
        # - Drawing
        # - Updating game state each frame
        ######################################
    while True:
        dt = clock.tick(FPS) / 1000.0
        tooltip_queue.clear()
        mouse_pos = pygame.mouse.get_pos()

        clicked_close_stats = False
        clicked_close_settings = False
        clicked_close_achievements = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game(state)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                window_width, window_height = event.w, event.h
                screen = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (1, 3):
                    mouse_down = True
                elif event.button == 4:  # Scroll up
                    if showing_achievements:
                        state.achievement_scroll = max(state.achievement_scroll - 30, 0)
                    elif state.active_tab in ("CP", "CPS"):
                        state.upgrade_scroll = max(state.upgrade_scroll - 30, 0)

                elif event.button == 5:  # Scroll down
                    if showing_achievements:
                        achievement_height = 70
                        spacing = 10
                        container_height = window_height - 160 - 80
                        content_height = len(state.achievements) * (achievement_height + spacing)
                        max_scroll = max(0, content_height - container_height)
                        state.achievement_scroll = min(state.achievement_scroll + 30, max_scroll)

                    elif state.active_tab in ("CP", "CPS"):
                        upgrades = state.click_upgrades if state.active_tab == "CP" else state.auto_upgrades
                        visible_height = window_height - (tab_y + tab_height + 20 + 50 + 20 + 90)  # accounts for tabs + shop boxes
                        upgrade_height = max(40, int(window_height * 0.09))
                        upgrade_margin = 10
                        max_scroll = max(0, len(upgrades) * (upgrade_height + upgrade_margin) - visible_height)
                        state.upgrade_scroll = min(state.upgrade_scroll + 30, max_scroll)
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    mouse_down = False
            elif event.type == pygame.MOUSEWHEEL:
                if showing_achievements:
                    achievement_height = 70
                    spacing = 10
                    container_height = window_height - 160 - 80
                    content_height = len(state.achievements) * (achievement_height + spacing)
                    max_scroll = max(0, content_height - container_height)
                    scroll_delta = -event.y * 30
                    state.achievement_scroll = max(0, min(state.achievement_scroll + scroll_delta, max_scroll))

        auto_save_timer += dt
        if auto_save_timer >= 10.0:
            save_game(state)
            auto_save_timer = 0

        left_width = window_width // 2
        right_width = window_width - left_width

        font_scale = max(12, int(font_base_size * (window_height / INITIAL_WINDOW_HEIGHT)))
        big_font_scale = max(16, int(font_big_size * (window_height / INITIAL_WINDOW_HEIGHT)))

        FONT = pygame.font.SysFont(None, font_scale)
        BIG_FONT = pygame.font.SysFont(None, big_font_scale)

        coin_radius = max(40, int(window_height * 0.15))
        coin_pos = (left_width // 2, window_height // 2)


        ######################################DRAWING##################################################

        screen.fill(BG_COLOR)

        # Draw left panel background
        pygame.draw.rect(screen, LEFT_BG, (0, 0, left_width, window_height))

        # Draw right panel background
        pygame.draw.rect(screen, RIGHT_BG, (left_width, 0, right_width, window_height))


        if shake_timer > 0 and state.coin_bag_shake_enabled:
            offset_x = random.randint(-5, 5)
            offset_y = random.randint(-5, 5)
        else:
            offset_x = 0
            offset_y = 0

        coin_pos_shaken = (coin_pos[0] + offset_x, coin_pos[1] + offset_y)

        if coin_image_original:
            coin_image = pygame.transform.smoothscale(coin_image_original, (coin_radius * 2, coin_radius * 2))
            coin_rect = coin_image.get_rect(center=coin_pos_shaken)
            screen.blit(coin_image, coin_rect)
        else:
            pygame.draw.circle(screen, (255, 215, 0), coin_pos_shaken, coin_radius)
            pygame.draw.circle(screen, (255, 255, 150), coin_pos_shaken, coin_radius - 6)
            coin_rect = pygame.Rect(coin_pos_shaken[0] - coin_radius, coin_pos_shaken[1] - coin_radius,
                                    coin_radius * 2, coin_radius * 2)

        if not showing_stats and not showing_settings and not showing_achievements and mouse_down and coin_rect.collidepoint(mouse_pos):
            gained = state.get_total_click_power()
            state.coins += gained
            state.all_time_coins += gained
            state.total_clicks += 1
            state.click_times.append(time.time())
            mouse_down = False
            shake_timer = shake_duration
            if coin_sound and state.sound_volume > 1:
                coin_sound.play()

            state.check_achievements()

        gained_cps = state.get_total_cps() * dt
        state.coins += gained_cps
        state.all_time_coins += gained_cps

        # --- Draw Stats, Achievements (with notif dot), and Settings buttons aligned bottom-left ---
        if not showing_stats and not showing_settings and not showing_achievements:
            padding = 10
            button_y = window_height - padding

            stats_text = FONT.render("Stats", True, (255, 255, 255))
            stats_rect = stats_text.get_rect()
            stats_rect.bottomleft = (padding, button_y)
            screen.blit(stats_text, stats_rect)

            margin_between = 30
            achievements_text = FONT.render("Achievements", True, (255, 255, 255))
            achievements_rect = achievements_text.get_rect()
            achievements_rect.bottomleft = (stats_rect.right + margin_between, button_y)
            screen.blit(achievements_text, achievements_rect)

            if state.has_new_achievement:
                dot_radius = 7
                dot_x = achievements_rect.right - 5
                dot_y = achievements_rect.top + 5
                pygame.draw.circle(screen, (220, 50, 50), (dot_x, dot_y), dot_radius)

            settings_text = FONT.render("Settings", True, (255, 255, 255))
            settings_rect = settings_text.get_rect()
            settings_rect.bottomleft = (achievements_rect.right + margin_between, button_y)
            screen.blit(settings_text, settings_rect)

        draw_text(screen, f"Coins: {format_large_number(state.coins)}", (20, 20), FONT)
        draw_text(screen, f"Click Power: {format_large_number(state.get_total_click_power())}", (20, 50), FONT)
        draw_text(screen, f"CPS: {format_large_number(state.get_total_cps())}", (20, 80), FONT)
        draw_text(screen, f"Gold Bars (Prestige): {state.prestige}", (20, 110), FONT)

        if showing_stats:
            clicked_close_stats = draw_stats_screen(screen, window_width, window_height, state, BIG_FONT, FONT, mouse_pos, mouse_down)
            if clicked_close_stats:
                showing_stats = False
                mouse_down = False

        if showing_settings:
            clicked_close_settings, off_rect, on_rect, volume_tick_rects = draw_settings_screen(screen, window_width, window_height, state, BIG_FONT, FONT, mouse_pos, mouse_down, coin_sound)
            if clicked_close_settings:
                showing_settings = False
                mouse_down = False

            if mouse_down:
                if off_rect.collidepoint(mouse_pos):
                    state.coin_bag_shake_enabled = False
                    mouse_down = False
                elif on_rect.collidepoint(mouse_pos):
                    state.coin_bag_shake_enabled = True
                    mouse_down = False

                for i, rect in enumerate(volume_tick_rects, start=1):
                    if rect.collidepoint(mouse_pos):
                        state.sound_volume = i
                        mouse_down = False
                        if coin_sound:
                            coin_sound.set_volume((state.sound_volume - 1) / 4)
                        break

        if showing_achievements:
            clicked_close_achievements = draw_achievements_screen(screen, window_width, window_height, state, BIG_FONT, FONT, mouse_pos, mouse_down)
            if clicked_close_achievements:
                showing_achievements = False
                mouse_down = False
                state.has_new_achievement = False

        if not showing_stats and not showing_settings and not showing_achievements:
            tab_padding = 20
            tab_spacing = 4
            tab_count = 3

            usable_width = right_width - 2 * tab_padding - tab_spacing * (tab_count - 1)
            tab_width = usable_width // tab_count
            tab_height = max(30, int(window_height * 0.08))
            tab_y = 20

            cp_tab_rect = pygame.Rect(left_width + tab_padding, tab_y, tab_width, tab_height)
            cps_tab_rect = pygame.Rect(left_width + tab_padding + tab_width + tab_spacing, tab_y, tab_width, tab_height)
            prestige_tab_rect = pygame.Rect(left_width + tab_padding + (tab_width + tab_spacing) * 2, tab_y, tab_width, tab_height)

            pygame.draw.rect(screen, BUTTON_BG, cp_tab_rect, border_radius=15)
            pygame.draw.rect(screen, BUTTON_BG, cps_tab_rect, border_radius=15)
            pygame.draw.rect(screen, BUTTON_BG, prestige_tab_rect, border_radius=15)

            if state.active_tab == "CP":
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, cp_tab_rect, border_radius=15)
            elif state.active_tab == "CPS":
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, cps_tab_rect, border_radius=15)
            elif state.active_tab == "PRESTIGE":
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, prestige_tab_rect, border_radius=15)

            # Center text horizontally and vertically inside tabs
            def draw_centered_text(text, rect, font, color=TEXT_COLOR):
                txt_surf = font.render(text, True, color)
                txt_rect = txt_surf.get_rect(center=rect.center)
                screen.blit(txt_surf, txt_rect)

            draw_centered_text("CP", cp_tab_rect, BIG_FONT)
            draw_centered_text("CPS", cps_tab_rect, BIG_FONT)
            draw_centered_text("Prestige", prestige_tab_rect, BIG_FONT)

            if state.active_tab == "CP":
                other_upgrades = state.auto_upgrades
                other_rect = cps_tab_rect
            elif state.active_tab == "CPS":
                other_upgrades = state.click_upgrades
                other_rect = cp_tab_rect
            else:
                other_upgrades = []
                other_rect = None

            radius = max(5, int(tab_height * 0.2))
            if other_rect and has_affordable_upgrades(state, other_upgrades):
                circle_x = other_rect.right - radius - 6
                circle_y = other_rect.top + radius + 6
                pygame.draw.circle(screen, (220, 50, 50), (circle_x, circle_y), radius)

            if pygame.mouse.get_pressed()[0]:
                if cp_tab_rect.collidepoint(mouse_pos) and state.active_tab != "CP":
                    state.active_tab = "CP"
                    state.buy_multiplier_index = 0
                elif cps_tab_rect.collidepoint(mouse_pos) and state.active_tab != "CPS":
                    state.active_tab = "CPS"
                    state.buy_multiplier_index = 0
                elif prestige_tab_rect.collidepoint(mouse_pos) and state.active_tab != "PRESTIGE":
                    state.active_tab = "PRESTIGE"
                    state.buy_multiplier_index = 0
               

            if state.active_tab in ("CP", "CPS"):
                upgrades = state.click_upgrades if state.active_tab == "CP" else state.auto_upgrades
                start_y = tab_y + tab_height + 20

                # 1. Assign active_multipliers based on tab
                if state.active_tab == "CP":
                    visible_multipliers = [
                        m for m in state.cp_multipliers
                        if (
                            not m["purchased"]
                            and m["associated_upgrade_index"] < len(state.click_upgrades)
                            and state.click_upgrades[m["associated_upgrade_index"]]["owned"] >= m["requires_owned"]
                        )
                    ][:5]
                elif state.active_tab == "CPS":
                    visible_multipliers = [
                        m for m in state.cps_multipliers
                        if (
                            not m["purchased"]
                            and m["associated_upgrade_index"] < len(state.auto_upgrades)
                            and state.auto_upgrades[m["associated_upgrade_index"]]["owned"] >= m["requires_owned"]
                        )
                    ][:5]
                else:
                    visible_multipliers = []
                # 2. Only after assignment, you can slice and use it
                shop_box_count = 5
                shop_box_margin = 20
                shop_box_gap = 20
                shop_box_height = max(50, int(window_height * 0.1))
                shop_box_y = start_y
                shop_content_width = right_width - 2 * shop_box_margin
                shop_box_width = int((shop_content_width - (shop_box_count - 1) * shop_box_gap) / shop_box_count)

                tooltip_drawn = False

                for i, m in enumerate(visible_multipliers):
                    # draw, flash, handle buy, etc.
                    pass

                from collections import defaultdict

                # Group upgrades by base name (e.g., Pixel Puncher, Fingerstorm)
                tooltip_text = None
                tooltip_rect = None
                grouped = defaultdict(list)
                for m in visible_multipliers:
                    if not m["purchased"]:
                        base_name = m["name"].split(" Boost")[0]
                        grouped[base_name].append(m)

                # Get the cheapest upgrade from each group
                cheapest_per_type = [min(group, key=lambda x: x["cost"]) for group in grouped.values()]

                # Sort those by cost and select the top 5
                visible_multipliers = sorted(cheapest_per_type, key=lambda m: m["cost"])[:5]

                tooltip_drawn = False  # Prevent multiple tooltips from showing at once
                for i, m in enumerate(visible_multipliers):

                    box_x = left_width + shop_box_margin + i * (shop_box_width + shop_box_gap)
                    rect = pygame.Rect(box_x, shop_box_y, shop_box_width, shop_box_height)
                    hover = rect.collidepoint(mouse_pos)
                    if hover:
                        hover = rect.collidepoint(mouse_pos)
                    can_afford = state.coins >= m["cost"]

                    # FIRST: draw background box BEFORE image
                    # 1. Draw the shop box background
                    pygame.draw.rect(screen, BUTTON_BG, rect, border_radius=8)

                    # 2. Draw the image
                    image_rendered = False
                    # === DRAW UPGRADE/SHOP IMAGE OR FALLBACK ===
                    image_path = m.get("image_path")
                    image_to_draw = None

                    image_path = m.get("image_path")
                    if image_path and os.path.exists(image_path):
                        try:
                            image = pygame.image.load(image_path).convert_alpha()
                        except Exception as e:
                            print(f"Failed to load image for {m['name']}: {e}")

                    # Fallback if image is missing or load failed
                    if image_to_draw is None:
                        placeholder_path = os.path.join(ASSETS_DIR, "pixelpuncher.png")
                        if os.path.exists(placeholder_path):
                            try:
                                image_to_draw = pygame.image.load(placeholder_path).convert_alpha()
                            except Exception as e:
                                print(f"Failed to load placeholder: {e}")
                        else:
                            print(f"Placeholder not found at {placeholder_path}")

                    # Only render if something was loaded
                    if image_to_draw:
                        image_to_draw = pygame.transform.smoothscale(image_to_draw, (rect.width, rect.height))
                        screen.blit(image_to_draw, rect.topleft)
                    else:
                        print(f"Nothing to render for {m['name']}")


                    # OVERLAY if too expensive
                    if not can_afford:
                        overlay = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                        overlay.fill((0, 0, 0, 100))
                        screen.blit(overlay, rect.topleft)

                    # HANDLE BUY
                    if mouse_down and hover and can_afford:
                        state.coins -= m["cost"]
                        m["purchased"] = True
                        state.shop_box_flash_timers[i] = pygame.time.get_ticks()  # ← trigger flash
                        mouse_down = False

                    # TOOLTIP (drawn last)
                    if hover and not tooltip_drawn:
                        tooltip_text = (
                            f"{m['name']}\n"
                            f"Level: {m['level']}\n"
                            f"Cost: {format_large_number(m['cost'])}\n"
                            f"Boost: +{int(m['boost_percent'] * 100)}%"
                        )
                        tooltip_width = 200
                        tooltip_height = 60
                        tooltip_x = rect.centerx - tooltip_width // 2
                        tooltip_y = rect.bottom + 10
                        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
                        tooltip_queue.append((tooltip_text, tooltip_rect))
                        tooltip_drawn = True  # ✅ Prevent other tooltips, but keep drawing other boxes


                # Move down for the main upgrade list
                start_y += shop_box_height + -50

               # --- Multiplier Upgrade Shop Boxes ---
                if state.active_tab == "CP":
                    visible_multipliers = [
                        m for m in state.cp_multipliers
                        if (
                            not m["purchased"]
                            and m["associated_upgrade_index"] < len(state.click_upgrades)
                            and state.click_upgrades[m["associated_upgrade_index"]]["owned"] >= m["requires_owned"]
                        )
                    ][:5]
                elif state.active_tab == "CPS":
                    visible_multipliers = [
                        m for m in state.cps_multipliers
                        if (
                            not m["purchased"]
                            and m["associated_upgrade_index"] < len(state.auto_upgrades)
                            and state.auto_upgrades[m["associated_upgrade_index"]]["owned"] >= m["requires_owned"]
                        )
                    ][:5]
                else:
                    visible_multipliers = []


                for i, m in enumerate(visible_multipliers):
                    box_x = left_width + shop_box_margin + i * (shop_box_width + shop_box_gap)
                    rect = pygame.Rect(box_x, shop_box_y, shop_box_width, shop_box_height)
                    hover = rect.collidepoint(mouse_pos)
                    can_afford = state.coins >= m["cost"]
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, rect, 2, border_radius=8)

                    # Buy logic
                    if mouse_down and hover and can_afford:
                        state.coins -= m["cost"]
                        m["purchased"] = True
                        state.shop_box_flash_timers[i] = pygame.time.get_ticks()
                        mouse_down = False

                # Push upgrade list below these boxes
                start_y += shop_box_height + 10

                upgrade_height = max(60, int(window_height * 0.09))
                upgrade_margin = 10
                visible_height = window_height - start_y - 90

                scroll_offset = state.upgrade_scroll
                max_scroll = max(0, len(upgrades) * (upgrade_height + upgrade_margin) - visible_height)
                state.upgrade_scroll = max(0, min(scroll_offset, max_scroll))

                clip_rect = pygame.Rect(left_width, start_y, right_width, visible_height)
                screen.set_clip(clip_rect)


                tooltip_text = None
                tooltip_rect = None
                show_tooltip = False

                # === UPGRADE BUTTONS, IMAGES, TEXT ===
                visible_upgrades = upgrades  # or paginate/slice if needed
                for i, upg in enumerate(visible_upgrades):
                    y = start_y + i * (upgrade_height + upgrade_margin) - state.upgrade_scroll
                    rect = pygame.Rect(left_width + 20, y, right_width - 40, upgrade_height)
                    hover = rect.collidepoint(mouse_pos)
                    label = ""
                    if state.active_tab == "CP":
                        multiplier = state.get_total_multiplier_for_upgrade(i, "click")
                        total_cp = round(upg["click_power"] * upg["owned"] * multiplier, 2)
                    elif state.active_tab == "CPS":
                        multiplier = state.get_total_multiplier_for_upgrade(i, "auto")
                        total_cps = round(upg["cps"] * upg["owned"] * multiplier, 2)
                        

                    if label:
                        small_font = pygame.font.SysFont(None, 18)
                        text_surf = small_font.render(label, True, TEXT_COLOR)
                        text_rect = text_surf.get_rect(center=(rect.centerx, rect.bottom + 12))
                        screen.blit(text_surf, text_rect)
                    if hover:
                        hover = rect.collidepoint(mouse_pos)

                    multi = MULTIPLIERS[state.buy_multiplier_index]
                    n_levels = state.max_affordable_levels(upg) if multi == 'max' else multi
                    total_cost = state.calculate_multi_cost(upg, n_levels) if n_levels > 0 else 0
                    total_gain = state.calculate_multi_gain(upg, n_levels)
                    can_buy = state.can_buy_upgrade(upg, n_levels) and n_levels > 0

                    display_cost = format_large_number(total_cost)
                    display_gain = (
                        f"CP +{int(round(total_gain))}" if state.active_tab == "CP"
                        else f"CPS +{format_large_number(total_gain)}"
                    )
                    # Build multiline upgrade text for inside button
                    lines = []

                    # Line 1: Name
                    lines.append(upg['name'])

                    # Line 2: Cost, Owned, Gain
                    lines.append(f"Cost: {display_cost} | Owned: {upg['owned']} | {display_gain}")

                    # Line 3: Total CP/CPS
                    if state.active_tab == "CP":
                        multiplier = state.get_total_multiplier_for_upgrade(i, "click")
                        total_cp = round(upg["click_power"] * upg["owned"] * multiplier, 2)
                        lines.append(f"Total CP: {format_large_number(total_cp)}")
                    elif state.active_tab == "CPS":
                        multiplier = state.get_total_multiplier_for_upgrade(i, "auto")
                        total_cps = round(upg["cps"] * upg["owned"] * multiplier, 2)
                        lines.append(f"Total CPS: {format_large_number(total_cps)}")


                    draw_button(screen, rect, enabled=can_buy, hover=hover)

                    # === IMAGE ===
                    image_size = rect.height - 10
                    filename = upg["name"].lower().replace(" ", "").replace(":", "") + ".png"
                    image_path = os.path.join(ASSETS_DIR, filename)
                    fallback_image_path = placeholder_path = os.path.join(ASSETS_DIR, "pixelpuncher.png")

                    try:
                        image = pygame.image.load(image_path).convert_alpha() if os.path.exists(image_path) \
                                else pygame.image.load(fallback_image_path).convert_alpha()
                        image = pygame.transform.smoothscale(image, (image_size, image_size))
                        image_pos = (rect.x + 5, rect.y + (rect.height - image_size) // 2)
                        screen.blit(image, image_pos)
                    except Exception as e:
                        print(f"Image load fail for {upg['name']}: {e}")

                    # === TEXT (right of image) ===
                    text_x = rect.x + image_size + 15
                    text_width = rect.width - image_size - 20
                    text_rect = pygame.Rect(text_x, rect.y, text_width, rect.height)
                    font_height = FONT.get_height()
                    for j, line in enumerate(lines):
                        rendered = FONT.render(line, True, TEXT_COLOR)
                        screen.blit(rendered, (text_x, rect.y + 5 + j * (font_height + 2)))

                    # === TOOLTIP LOGIC: Only store tooltip values for later drawing ===
                    hover = rect.collidepoint(mouse_pos)
                    hover_shop_multiplier = None
                    if hover:
                        tooltip_text = (
                            f"{m['name']}\n"
                            f"Level: {m['level']}\n"
                            f"Cost: {format_large_number(m['cost'])}\n"
                            f"Boost: +{int(m['boost_percent'] * 100)}%"
                        )

                        tooltip_width = 200
                        tooltip_height = 60
                        tooltip_x = rect.centerx - tooltip_width // 2
                        tooltip_y = rect.bottom + 10
                        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, tooltip_width, tooltip_height)
                        
                        tooltip_queue.append((tooltip_text, tooltip_rect))  # ✅ store for later


                    # === Click Logic ===
                    if mouse_down and hover and can_buy:
                        state.buy_upgrade(upg, n_levels)
                        mouse_down = False


                screen.set_clip(None)

                multiplier_btn_width = max(40, int(window_width * 0.06))
                multiplier_btn_height = max(30, int(window_height * 0.06))
                multiplier_btn_spacing = 10
                btn_rects = []

                base_x = left_width + 20
                base_y = window_height - multiplier_btn_height - 20

                font_small = pygame.font.SysFont(None, max(16, int(24 * window_height / INITIAL_WINDOW_HEIGHT)))
                for i, mult in enumerate(MULTIPLIERS):
                    rect = pygame.Rect(base_x + i * (multiplier_btn_width + multiplier_btn_spacing), base_y,
                                       multiplier_btn_width, multiplier_btn_height)
                    btn_rects.append(rect)
                    is_selected = (i == state.buy_multiplier_index)

                    color = (30, 50, 100)
                    if is_selected:
                        color = HIGHLIGHT_COLOR

                    pygame.draw.rect(screen, color, rect, border_radius=12)
                    text = f"x{mult}" if mult != 'max' else "MAX"
                    txt_surf = font_small.render(text, True, TEXT_COLOR)
                    txt_rect = txt_surf.get_rect(center=rect.center)
                    screen.blit(txt_surf, txt_rect)

                if mouse_down:
                    for i, rect in enumerate(btn_rects):
                        if rect.collidepoint(mouse_pos):
                            state.buy_multiplier_index = i
                            mouse_down = False
                            break

            elif state.active_tab == "PRESTIGE":
                pygame.draw.rect(screen, RIGHT_BG, (left_width, 0, right_width, window_height))
                pygame.draw.rect(screen, LEFT_BG, (0, 0, left_width, window_height))
                title_font = pygame.font.SysFont(None, max(36, int(40 * window_height / INITIAL_WINDOW_HEIGHT)))
                label_font = pygame.font.SysFont(None, max(24, int(28 * window_height / INITIAL_WINDOW_HEIGHT)))

                title_text = title_font.render("Prestige", True, TEXT_COLOR)
                screen.blit(title_text, (left_width + right_width // 2 - title_text.get_width() // 2, 100))

                current_gold = state.prestige
                all_time_coins = state.all_time_coins
                potential_gold = calculate_prestige_level(all_time_coins, state.prestige)

                gold_text = label_font.render(f"You have: {current_gold} gold bars", True, TEXT_COLOR)
                screen.blit(gold_text, (left_width + right_width // 2 - gold_text.get_width() // 2, 160))

                pending_text = label_font.render(f"Potential gold bars this run: {potential_gold}", True, (218, 165, 32))
                screen.blit(pending_text, (left_width + right_width // 2 - pending_text.get_width() // 2, 200))

                explanation_text = (
                    "Prestiging resets all coins and upgrades but gives gold bars based on all-time coins earned. "
                    "Each gold bar increases your CPS by 1%. Use this feature to progress faster in future runs."
                )

                wrapped_rect = pygame.Rect(left_width + 40, 240, right_width - 80, 100)
                draw_multiline_text_in_rect(screen, explanation_text, wrapped_rect, label_font)

                btn_width, btn_height = 200, 50
                btn_x = left_width + right_width // 2 - btn_width // 2
                btn_y = 450
                bonus_text = label_font.render("+1% CPS per gold bar", True, TEXT_COLOR)
                bonus_y = window_height - 200
                screen.blit(bonus_text, (left_width + right_width // 2 - bonus_text.get_width() // 2, bonus_y))
                prestige_button = pygame.Rect(btn_x, btn_y, btn_width, btn_height)

                hover = prestige_button.collidepoint(mouse_pos)
                pygame.draw.rect(screen, HIGHLIGHT_COLOR if hover else (30, 50, 100), prestige_button, border_radius=6)

                btn_font = pygame.font.SysFont(None, 28)
                p_text = btn_font.render("Prestige Now", True, TEXT_COLOR)
                screen.blit(p_text, (prestige_button.centerx - p_text.get_width() // 2, prestige_button.centery - p_text.get_height() // 2))

                if mouse_down and hover:
                    if potential_gold > 0:
                        state.prestige += potential_gold
                        state.coins = 0
                        state.all_time_coins = 0
                        for upg in state.click_upgrades:
                            upg["owned"] = 0
                            upg["base_cost"] = upg["base_cost_initial"]
                        for upg in state.auto_upgrades:
                            upg["owned"] = 0
                            upg["base_cost"] = upg["base_cost_initial"]
                        state.active_tab = "CP"
                    mouse_down = False

                # Close X button top-right on prestige overlay
                overlay_rect = pygame.Rect(left_width + 20, 80, right_width - 40, window_height - 160)
                close_size = 28
                close_padding = 20
                close_rect = pygame.Rect(
                    overlay_rect.right - close_size - close_padding,
                    overlay_rect.top + close_padding,
                    close_size,
                    close_size,
                )

                hover = close_rect.collidepoint(mouse_pos)
                color = HIGHLIGHT_COLOR if hover else BUTTON_BG
                pygame.draw.rect(screen, color, close_rect, border_radius=6)

                x_text = FONT.render("X", True, TEXT_COLOR)
                x_text_rect = x_text.get_rect(center=close_rect.center)
                screen.blit(x_text, x_text_rect)

                if mouse_down and hover:
                    state.active_tab = "CP"
                    mouse_down = False

        if show_offline_popup:
            popup_width, popup_height = 400, 120
            popup_x = window_width // 2 - popup_width // 2
            popup_y = window_height // 2 - popup_height // 2
            popup_rect = pygame.Rect(popup_x, popup_y, popup_width, popup_height)

            pygame.draw.rect(screen, (50, 50, 70), popup_rect, border_radius=10)
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, popup_rect, 3, border_radius=10)

            popup_font = pygame.font.SysFont(None, 28)
            text = f"You earned {format_large_number(offline_earned)} coins while offline!"
            text_surf = popup_font.render(text, True, TEXT_COLOR)
            screen.blit(text_surf, (popup_x + 20, popup_y + 30))

            close_btn_rect = pygame.Rect(popup_x + popup_width // 2 - 50, popup_y + 70, 100, 30)
            mouse_clicked = pygame.mouse.get_pressed()[0]
            btn_hover = close_btn_rect.collidepoint(mouse_pos)
            btn_color = HIGHLIGHT_COLOR if btn_hover else BUTTON_BG
            pygame.draw.rect(screen, btn_color, close_btn_rect, border_radius=8)
            close_text = popup_font.render("Close", True, TEXT_COLOR)
            screen.blit(close_text, (close_btn_rect.centerx - close_text.get_width() // 2, close_btn_rect.centery - close_text.get_height() // 2))

            if mouse_clicked and btn_hover:
                show_offline_popup = False
                pygame.time.wait(200)

        # Achievement popup drawn last on top
        state.update_achievement_popup(dt)
        draw_achievement_popup(screen, state, window_width, FONT)

        if not showing_stats and not showing_settings and not showing_achievements and mouse_down:
            if stats_rect.collidepoint(mouse_pos):
                showing_stats = True
                mouse_down = False
            elif achievements_rect.collidepoint(mouse_pos):
                showing_achievements = True
                mouse_down = False
                state.has_new_achievement = False
            elif settings_rect.collidepoint(mouse_pos):
                showing_settings = True
                mouse_down = False
        screen.set_clip(None)
        screen.set_clip(None)
        for tip_text, tip_rect in tooltip_queue:
            if isinstance(tip_rect, pygame.Rect):
                pygame.draw.rect(screen, (30, 30, 30), tip_rect, border_radius=8)
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, tip_rect, 2, border_radius=8)
                draw_multiline_text_in_rect(screen, tip_text, tip_rect, FONT, TEXT_COLOR)
            else:
                print("Invalid tooltip_rect:", tip_rect)

        # Always draw achievements last
        draw_achievement_popup(screen, state, window_width, FONT)
        screen.set_clip(None)
        for tip_text, tip_rect in tooltip_queue:
            try:
                if isinstance(tip_rect, pygame.Rect):
                    screen.set_clip(None)
                    pygame.draw.rect(screen, (30, 30, 30), tip_rect, border_radius=8)
                    pygame.draw.rect(screen, HIGHLIGHT_COLOR, tip_rect, 2, border_radius=8)
                    draw_multiline_text_in_rect(screen, tip_text, tip_rect, FONT, TEXT_COLOR)
            except Exception as e:
                print(f"Tooltip render error: {e} with rect: {tip_rect}")
            
        for tip_text, tip_rect in tooltip_queue:
            if isinstance(tip_rect, pygame.Rect):
                screen.set_clip(None)
                pygame.draw.rect(screen, (30, 30, 30), tip_rect, border_radius=8)
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, tip_rect, 2, border_radius=8)
                draw_multiline_text_in_rect(screen, tip_text, tip_rect, FONT, TEXT_COLOR)

                
        
        pygame.display.flip()

        shake_timer = max(0, shake_timer - dt)

if __name__ == "__main__":
    main()
