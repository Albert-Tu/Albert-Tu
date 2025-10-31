import gamelib
import random
import math
import json
from sys import maxsize


class AlgoStrategy(gamelib.AlgoCore):
    def __init__(self):
        super().__init__()
        seed = random.randrange(maxsize)
        random.seed(seed)
        gamelib.debug_write('=== WORLD CHAMPIONSHIP AI ONLINE ===')
        
        # Advanced memory and learning systems
        self.enemy_breach_map = {}
        self.enemy_attack_patterns = []
        self.our_successful_attacks = {}
        self.enemy_weak_points = []
        self.enemy_defense_grid = {}
        self.enemy_playstyle = {'rush': 0, 'turtle': 0, 'economic': 0, 'demolisher': 0, 'scout': 0, 'interceptor': 0}
        self.damage_dealt_history = []
        self.last_enemy_health = 30
        self.attack_success_rate = []
        self.defense_efficiency = []
        self.turn_strategy_log = []

    def on_game_start(self, config):
        gamelib.debug_write('World-class AI initialized')
        self.config = config
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = config["unitInformation"][0]["shorthand"]
        SUPPORT = config["unitInformation"][1]["shorthand"]
        TURRET = config["unitInformation"][2]["shorthand"]
        SCOUT = config["unitInformation"][3]["shorthand"]
        DEMOLISHER = config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0

    def on_turn(self, turn_state):
        game_state = gamelib.GameState(self.config, turn_state)
        turn = game_state.turn_number
        gamelib.debug_write(f'\n{"="*60}\nTURN {turn} - CHAMPIONSHIP MODE\n{"="*60}')
        game_state.suppress_warnings(True)
        
        self.deep_analysis(game_state)
        self.execute_master_strategy(game_state)
        
        game_state.submit_turn()

    def execute_master_strategy(self, game_state):
        """Ultimate strategy controller"""
        turn = game_state.turn_number
        sp = game_state.get_resource(SP)
        mp = game_state.get_resource(MP)
        
        # Dynamic phase selection
        if turn < 3:
            self.perfect_opening(game_state)
        elif turn < 8:
            self.early_dominance(game_state)
        elif turn < 15:
            self.mid_control(game_state)
        else:
            self.late_supremacy(game_state)
        
        # Always active systems
        self.adaptive_defense(game_state)
        self.intelligent_offense(game_state)
        
        if sp > 15:
            self.economy_boost(game_state)

    def perfect_opening(self, game_state):
        """Optimal opening build"""
        core_turrets = [[3, 13], [24, 13], [13, 12], [14, 12], [7, 11], [20, 11]]
        core_walls = [[13, 13], [14, 13], [6, 11], [21, 11]]
        
        game_state.attempt_spawn(TURRET, core_turrets)
        game_state.attempt_spawn(WALL, core_walls)
        game_state.attempt_upgrade([[13, 13], [14, 13]])

    def early_dominance(self, game_state):
        """Build fortress with overlapping fire"""
        turrets = [[0, 13], [1, 13], [26, 13], [27, 13], [5, 12], [22, 12], [9, 11], [18, 11], [11, 10], [16, 10]]
        walls = [[4, 12], [23, 12], [8, 11], [19, 11], [10, 10], [17, 10], [12, 9], [15, 9]]
        
        game_state.attempt_spawn(TURRET, turrets)
        game_state.attempt_spawn(WALL, walls)
        game_state.attempt_upgrade([[3, 13], [24, 13], [13, 12], [14, 12]])
        
        if game_state.get_resource(MP) >= 3:
            safe_path = self.find_safest_path(game_state)
            if safe_path:
                game_state.attempt_spawn(SCOUT, safe_path, 1)

    def mid_control(self, game_state):
        """Total map control"""
        dense_turrets = [[2, 13], [25, 13], [4, 12], [23, 12], [10, 12], [17, 12], [6, 11], [21, 11], [8, 10], [19, 10], [13, 9], [14, 9]]
        supports = [[13, 8], [14, 8], [10, 7], [17, 7], [12, 6], [15, 6], [7, 8], [20, 8]]
        walls = [[5, 12], [22, 12], [7, 11], [20, 11], [9, 10], [18, 10], [11, 9], [16, 9]]
        
        game_state.attempt_spawn(TURRET, dense_turrets)
        game_state.attempt_spawn(SUPPORT, supports)
        game_state.attempt_spawn(WALL, walls)
        
        game_state.attempt_upgrade(supports)
        game_state.attempt_upgrade(walls)
        self.upgrade_all_turrets(game_state)

    def late_supremacy(self, game_state):
        """Maximum fortification"""
        all_positions = []
        for x in range(28):
            for y in [13, 12, 11, 10]:
                if not game_state.contains_stationary_unit([x, y]):
                    all_positions.append([x, y])
        
        game_state.attempt_spawn(TURRET, all_positions[:20])
        game_state.attempt_spawn(WALL, all_positions[20:])
        
        extended_supports = [[13, 7], [14, 7], [11, 6], [16, 6], [9, 7], [18, 7], [10, 5], [17, 5]]
        game_state.attempt_spawn(SUPPORT, extended_supports)
        
        self.upgrade_everything(game_state)
        
        if game_state.get_resource(MP) >= 5:
            game_state.attempt_spawn(INTERCEPTOR, [13, 0], 3)

    def adaptive_defense(self, game_state):
        """Learning defense system"""
        for loc_str, data in self.enemy_breach_map.items():
            if data['count'] >= 2:
                loc = eval(loc_str)
                self.counter_breach(game_state, loc)
        
        predicted = self.predict_attack(game_state)
        if predicted:
            self.preemptive_build(game_state, predicted)
        
        self.repair_structures(game_state)

    def intelligent_offense(self, game_state):
        """Multi-strategy offense"""
        mp = game_state.get_resource(MP)
        if mp < 5:
            return
        
        weak_spots = self.find_weaknesses(game_state)
        
        if self.should_demo_strike(game_state):
            self.demo_strike(game_state)
        elif self.should_scout_swarm(game_state, weak_spots):
            self.scout_swarm(game_state, weak_spots)
        elif self.should_interceptor_raid(game_state):
            self.interceptor_raid(game_state, weak_spots)
        elif mp >= 15 and game_state.turn_number % 3 == 0:
            self.combined_assault(game_state, weak_spots)

    def should_demo_strike(self, game_state):
        """Check if demolisher attack is optimal"""
        front_count = self.count_front_enemies(game_state)
        mp = game_state.get_resource(MP)
        return front_count > 6 and mp >= 9

    def demo_strike(self, game_state):
        """Demolisher assault"""
        platform = [[x, 11] for x in range(18, 26)]
        game_state.attempt_spawn(WALL, platform)
        
        spawns = [[24, 10], [23, 10], [22, 10]]
        for s in spawns:
            game_state.attempt_spawn(DEMOLISHER, s, 2)
        
        game_state.attempt_spawn(INTERCEPTOR, [20, 6], 3)

    def should_scout_swarm(self, game_state, weak_spots):
        """Check if scout swarm is optimal"""
        mp = game_state.get_resource(MP)
        min_damage = self.min_path_damage(game_state)
        return mp >= 12 and min_damage < 150 and len(weak_spots) > 0

    def scout_swarm(self, game_state, weak_spots):
        """Mass scout attack"""
        mp = game_state.get_resource(MP)
        paths = self.find_best_paths(game_state, 3)
        
        if paths:
            scouts_per = int(mp * 0.8 / len(paths))
            for p in paths:
                game_state.attempt_spawn(SCOUT, p, scouts_per)
            game_state.attempt_spawn(INTERCEPTOR, [13, 0], int(mp * 0.2))

    def should_interceptor_raid(self, game_state):
        """Check if interceptor raid is optimal"""
        mp = game_state.get_resource(MP)
        return mp >= 8

    def interceptor_raid(self, game_state, weak_spots):
        """Fast interceptor attack"""
        mp = game_state.get_resource(MP)
        spawns = [[3, 10], [24, 10], [13, 0], [14, 0]]
        
        total = int(mp * 0.9)
        for s in spawns:
            if total > 0 and game_state.can_spawn(INTERCEPTOR, s):
                game_state.attempt_spawn(INTERCEPTOR, s, min(3, total))
                total -= 3

    def combined_assault(self, game_state, weak_spots):
        """Ultimate combined attack"""
        mp = game_state.get_resource(MP)
        best = weak_spots[0] if weak_spots else [14, 0]
        
        game_state.attempt_spawn(INTERCEPTOR, best, int(mp * 0.2))
        
        demo_pos = [24, 10] if best[0] > 14 else [3, 10]
        if game_state.can_spawn(DEMOLISHER, demo_pos):
            game_state.attempt_spawn(DEMOLISHER, demo_pos, int(mp * 0.25 / 3))
        
        game_state.attempt_spawn(SCOUT, best, int(mp * 0.45))
        game_state.attempt_spawn(INTERCEPTOR, best, int(mp * 0.1))

    def find_weaknesses(self, game_state):
        """Find enemy weak points"""
        tests = []
        for x in range(28):
            for y in range(0, 5):
                tests.append([x, y])
        
        analysis = []
        for loc in tests:
            if game_state.can_spawn(SCOUT, loc):
                dmg = self.calc_path_damage(game_state, loc)
                path = game_state.find_path_to_edge(loc)
                if path and len(path) > 0:
                    score = dmg / len(path)
                    analysis.append((loc, score))
        
        analysis.sort(key=lambda x: x[1])
        return [a[0] for a in analysis[:3]]

    def calc_path_damage(self, game_state, loc):
        """Calculate path damage"""
        path = game_state.find_path_to_edge(loc)
        if not path:
            return 999999
        
        total = 0
        for p in path:
            attackers = game_state.get_attackers(p, 0)
            for a in attackers:
                if a.unit_type == TURRET:
                    dmg = a.damage_i
                    if a.upgraded:
                        dmg *= 2
                    total += dmg
        return total

    def find_safest_path(self, game_state):
        """Find safest spawn location"""
        options = [[13, 0], [14, 0], [12, 1], [15, 1]]
        min_dmg = 999999
        best = None
        
        for opt in options:
            if game_state.can_spawn(SCOUT, opt):
                dmg = self.calc_path_damage(game_state, opt)
                if dmg < min_dmg:
                    min_dmg = dmg
                    best = opt
        return best

    def find_best_paths(self, game_state, count):
        """Find multiple good paths"""
        all_spawns = []
        for x in range(28):
            for y in range(0, 4):
                all_spawns.append([x, y])
        
        scored = []
        for s in all_spawns:
            if game_state.can_spawn(SCOUT, s):
                dmg = self.calc_path_damage(game_state, s)
                path = game_state.find_path_to_edge(s)
                if path:
                    score = dmg / len(path)
                    scored.append((s, score))
        
        scored.sort(key=lambda x: x[1])
        return [s[0] for s in scored[:count]]

    def deep_analysis(self, game_state):
        """Analyze enemy deeply"""
        structures = self.count_enemy_structures(game_state)
        
        if structures['turrets'] > 20:
            self.enemy_playstyle['turtle'] += 1
        if structures['walls'] > 25:
            self.enemy_playstyle['turtle'] += 1
        if structures['supports'] > 10:
            self.enemy_playstyle['economic'] += 1
        
        health = game_state.enemy_health
        if health < self.last_enemy_health:
            dmg = self.last_enemy_health - health
            self.damage_dealt_history.append(dmg)
        self.last_enemy_health = health

    def count_enemy_structures(self, game_state):
        """Count enemy structures"""
        counts = {'turrets': 0, 'walls': 0, 'supports': 0}
        
        for x in range(28):
            for y in range(14, 28):
                if game_state.contains_stationary_unit([x, y]):
                    for unit in game_state.game_map[[x, y]]:
                        if unit.player_index == 1:
                            if unit.unit_type == TURRET:
                                counts['turrets'] += 1
                            elif unit.unit_type == WALL:
                                counts['walls'] += 1
                            elif unit.unit_type == SUPPORT:
                                counts['supports'] += 1
        return counts

    def count_front_enemies(self, game_state):
        """Count front enemy units"""
        count = 0
        for x in range(28):
            for y in [14, 15]:
                if game_state.contains_stationary_unit([x, y]):
                    for unit in game_state.game_map[[x, y]]:
                        if unit.player_index == 1:
                            count += 1
        return count

    def min_path_damage(self, game_state):
        """Get minimum path damage"""
        options = [[13, 0], [14, 0]]
        damages = []
        for opt in options:
            if game_state.can_spawn(SCOUT, opt):
                damages.append(self.calc_path_damage(game_state, opt))
        return min(damages) if damages else 999

    def predict_attack(self, game_state):
        """Predict enemy attack location"""
        if not self.enemy_breach_map:
            return None
        most = max(self.enemy_breach_map.items(), key=lambda x: x[1]['count'])
        return eval(most[0])

    def counter_breach(self, game_state, loc):
        """Counter breach point"""
        x, y = loc
        positions = [
            [x, min(13, y + 1)],
            [max(0, x - 1), min(13, y + 1)],
            [min(27, x + 1), min(13, y + 1)]
        ]
        game_state.attempt_spawn(TURRET, positions[:2])
        game_state.attempt_spawn(WALL, positions[2:])

    def preemptive_build(self, game_state, target):
        """Build before attack"""
        x, y = target
        positions = [[x, min(13, y + 1)], [max(0, x - 1), min(13, y + 1)]]
        game_state.attempt_spawn(TURRET, positions)

    def repair_structures(self, game_state):
        """Repair damaged structures"""
        for x in range(28):
            for y in range(14):
                if game_state.contains_stationary_unit([x, y]):
                    for unit in game_state.game_map[[x, y]]:
                        if unit.player_index == 0 and unit.health < unit.max_health * 0.5:
                            game_state.attempt_spawn(unit.unit_type, [x, y])

    def economy_boost(self, game_state):
        """Boost economy with supports"""
        supports = [[13, 7], [14, 7], [12, 6], [15, 6], [11, 7], [16, 7]]
        game_state.attempt_spawn(SUPPORT, supports)
        game_state.attempt_upgrade(supports)

    def upgrade_all_turrets(self, game_state):
        """Upgrade all turrets"""
        for x in range(28):
            for y in range(14):
                if game_state.contains_stationary_unit([x, y]):
                    for unit in game_state.game_map[[x, y]]:
                        if unit.player_index == 0 and unit.unit_type == TURRET:
                            game_state.attempt_upgrade([x, y])

    def upgrade_everything(self, game_state):
        """Upgrade all structures"""
        for x in range(28):
            for y in range(14):
                if game_state.contains_stationary_unit([x, y]):
                    for unit in game_state.game_map[[x, y]]:
                        if unit.player_index == 0 and not unit.upgraded:
                            game_state.attempt_upgrade([x, y])

    def on_action_frame(self, turn_string):
        """Learn from game events"""
        state = json.loads(turn_string)
        events = state["events"]
        breaches = events["breach"]
        
        for breach in breaches:
            location = breach[0]
            is_ours = breach[4] == 1
            
            if not is_ours:
                loc_key = str(location)
                if loc_key not in self.enemy_breach_map:
                    self.enemy_breach_map[loc_key] = {'count': 0, 'units_used': []}
                self.enemy_breach_map[loc_key]['count'] += 1
            else:
                self.our_successful_attacks[str(location)] = self.our_successful_attacks.get(str(location), 0) + 1


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
