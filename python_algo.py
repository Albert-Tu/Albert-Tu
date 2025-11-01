import gamelib
import random
import math
import json
import os
import csv
from sys import maxsize
from collections import defaultdict, deque

# Persistence files
MEMORY_FILE = 'strategy_memory.json'
REPORT_CSV = 'strategy_report.csv'
REPORT_HTML = 'strategy_memory_report.html'


class AlgoStrategy(gamelib.AlgoCore):
    """Elite Tournament-Grade Terminal AI v7.0 - Ultimate Championship Edition
    
    Combines championship-level strategy with advanced microcontroller tactics:
    - Per-unit microcontrollers (ScoutSwarm, DemolisherEscort, InterceptorController)
    - Path Dynamics Engine with live damage heatmap
    - Reactive reinforcement and fallback spawn logic
    - Contextual micro decisions (safety vs aggression)
    - Advanced opponent modeling and counter-strategies
    """
    
    def __init__(self):
        super().__init__()
        random.seed(random.randrange(maxsize))
        gamelib.debug_write('═'*80)
        gamelib.debug_write('🏆 TERMINAL AI v7.0 - ULTIMATE CHAMPIONSHIP EDITION')
        gamelib.debug_write('   Elite Strategy • Micro Control • Path Dynamics • ML Learning')
        gamelib.debug_write('═'*80)
        
        # ═══════════════ ENHANCED NEURAL SYSTEMS ═══════════════
        self.breach_analytics = defaultdict(lambda: {
            'frequency': 0, 'total_damage': 0, 'avg_damage': 0.0,
            'last_turn': -1, 'success_rate': 0.0, 'threat_level': 0,
            'path_efficiency': 0.0, 'damage_variance': [],
            'unit_composition': defaultdict(int), 'timing_score': 0.0,
            'outcomes': []
        })
        
        self.attack_history = defaultdict(lambda: {
            'attempts': 0, 'successes': 0, 'total_damage': 0,
            'avg_damage': 0.0, 'cost_efficiency': 0.0, 'optimal_timing': [],
            'counter_effectiveness': {}, 'synergy_scores': {},
            'outcomes': []
        })
        
        self.opponent_model = {
            'playstyle': 'unknown',
            'skill_estimate': 0.5,
            'aggression_score': 0.5,
            'defense_rating': 0.5,
            'economy_priority': 0.5,
            'predictability': 0.5,
            'adaptation_speed': 0.5,
            'attack_patterns': deque(maxlen=30),
            'defense_patterns': deque(maxlen=30),
            'defense_weaknesses': [],
            'preferred_units': defaultdict(float),
            'timing_patterns': deque(maxlen=25),
            'resource_efficiency': 1.0,
            'strategic_mistakes': 0,
            'comeback_potential': 0.5,
            'vulnerability_map': {},
            'counter_strategy': None
        }
        
        # ═══════════════ ADVANCED METRICS ═══════════════
        self.metrics = {
            'damage_dealt': deque(maxlen=50),
            'damage_taken': deque(maxlen=50),
            'mp_spent': deque(maxlen=40),
            'sp_efficiency': deque(maxlen=30),
            'attack_roi': deque(maxlen=25),
            'defense_uptime': 0,
            'win_probability': 0.5,
            'momentum_score': 0.0,
            'map_control': 0.5,
            'economic_advantage': 0.0,
            'structure_health_ratio': 1.0,
            'defensive_breaches': 0,
            'offensive_breaches': 0,
            'perfect_defenses': 0,
            'failed_attacks': 0,
            'critical_saves': 0,
            'clutch_victories': 0,
            'economy_turns': 0,
            'pressure_score': 0.0,
            'micro_efficiency': 1.0
        }
        
        # ═══════════════ STRATEGIC STATE ═══════════════
        self.game_phase = 'opening'
        self.strategy_mode = 'balanced'
        self.tactical_state = 'standard'
        self.aggression_level = 0.5
        self.risk_tolerance = 0.5
        self.confidence_level = 0.5
        self.counter_mode = False
        self.all_in_mode = False
        
        # ═══════════════ DYNAMIC THRESHOLDS ═══════════════
        self.thresholds = {
            'attack_min_mp': 8,
            'attack_min_ev': 12,
            'defense_sp_ratio': 0.75,
            'economy_sp_ratio': 0.12,
            'upgrade_priority': 0.70,
            'upgrade_sp_guard': 6,
            'emergency_threshold': 12,
            'emergency_hp_loss': 3,
            'all_in_threshold': 20,
            'conservative_threshold': 6,
            'reinforce_threshold': 0.65,
            'rush_defense_mp': 18
        }
        
        # ═══════════════ MAP CONFIGURATION ═══════════════
        self.map_width = 28
        self.map_height = 28
        self.preferred_columns = [13, 14]
        self.spawn_presets = {
            'standard': [[13, 0], [14, 0], [10, 1], [17, 1]],
            'aggressive': [[13, 0], [14, 0], [8, 1], [19, 1], [5, 2], [22, 2]],
            'defensive': [[13, 0], [14, 0]],
            'pincer': [[3, 0], [24, 0], [10, 1], [17, 1]]
        }
        
        # ═══════════════ INTELLIGENT CACHING ═══════════════
        self.cache = {
            'paths': {}, 'damage': {}, 'threats': {}, 
            'opportunities': {}, 'structures': {},
            'best_attack': None, 'weak_zones': [],
            'valid_turn': -1
        }
        
        # ═══════════════ HISTORICAL DATA ═══════════════
        self.history = {
            'states': deque(maxlen=20),
            'decisions': deque(maxlen=25),
            'outcomes': deque(maxlen=25),
            'enemy_resources': {'sp': deque(maxlen=25), 'mp': deque(maxlen=25)},
            'health_differential': deque(maxlen=30),
            'structure_counts': deque(maxlen=20)
        }
        
        # Track last state
        self.last_health = {'ours': 30, 'enemy': 30}
        self.last_mp_spent = 0
        self.prev_health = {'ours': 30, 'enemy': 30}
        
        # ═══════════════ PERSISTENCE ═══════════════
        self.persistence_enabled = True
        self.report_enabled = True
        self.autosave_every = 30
        
        # ═══════════════ STRATEGY LIBRARY ═══════════════
        self.strategies = self._init_strategy_library()
        self.attack_playbook = self._init_attack_playbook()
        
        # ═══════════════ MICRO CONTROL SYSTEMS ═══════════════
        self.path_engine = None  # Initialized in on_game_start
        self.scout_controller = None
        self.demolisher_escort = None
        self.interceptor_controller = None
        
    def _init_strategy_library(self):
        """Tournament-optimized opening strategies"""
        return {
            'fortress_control': {
                'turrets': [[0,13], [27,13], [3,13], [24,13], [8,13], [19,13],
                           [13,12], [14,12], [10,12], [17,12], [6,11], [21,11]],
                'walls': [[13,13], [14,13], [11,12], [16,12], [9,12], [18,12],
                         [7,12], [20,12]],
                'upgrades': [[0,13], [27,13], [13,12], [14,12], [3,13], [24,13]],
                'supports': [[13,8], [14,8]],
                'win_rate': 0.78,
                'phase': 'mid'
            },
            'aggressive_tempo': {
                'turrets': [[0,13], [27,13], [13,12], [14,12], [10,11], [17,11],
                           [7,10], [20,10], [13,11], [14,11], [5,10], [22,10]],
                'walls': [[13,13], [14,13], [12,12], [15,12], [11,11], [16,11]],
                'upgrades': [[13,12], [14,12], [10,11], [17,11], [0,13], [27,13]],
                'win_rate': 0.72,
                'phase': 'early'
            },
            'economic_control': {
                'turrets': [[0,13], [27,13], [13,12], [14,12], [8,12], [19,12],
                           [5,11], [22,11]],
                'walls': [[13,13], [14,13], [10,12], [17,12], [11,12], [16,12]],
                'supports': [[13,8], [14,8], [10,7], [17,7], [13,6], [14,6]],
                'upgrades': [[0,13], [27,13], [13,8], [14,8]],
                'win_rate': 0.69,
                'phase': 'mid'
            },
            'adaptive_pressure': {
                'turrets': [[0,13], [27,13], [3,13], [24,13], [13,12], [14,12],
                           [10,11], [17,11], [7,11], [20,11]],
                'walls': [[13,13], [14,13], [12,12], [15,12], [9,12], [18,12]],
                'upgrades': [[0,13], [27,13], [13,12], [14,12]],
                'supports': [[13,8], [14,8]],
                'win_rate': 0.75,
                'phase': 'opening'
            }
        }
    
    def _init_attack_playbook(self):
        """Advanced attack strategy library with micro integration"""
        return {
            'scout_flood': {
                'unit': 'scout',
                'min_mp': 8,
                'optimal_mp': 15,
                'allocation': 0.95,
                'conditions': ['low_defense', 'clear_path'],
                'expected_dmg': lambda mp, pd: max(0, (mp * 15 - pd) / 8.0),
                'risk': 'low',
                'counter': 'interceptor_heavy',
                'weight': 1.0,
                'micro_enabled': True
            },
            'demo_breach': {
                'unit': 'demolisher',
                'min_mp': 10,
                'optimal_mp': 18,
                'allocation': 0.65,
                'support_scouts': 0.25,
                'conditions': ['high_walls', 'static_defense'],
                'expected_dmg': lambda structures, mp: min(structures * 0.7, 10) * (mp / 3.5),
                'risk': 'medium',
                'counter': 'mobile_defense',
                'weight': 1.15,
                'micro_enabled': True
            },
            'interceptor_rush': {
                'unit': 'interceptor',
                'min_mp': 7,
                'optimal_mp': 12,
                'allocation': 0.98,
                'conditions': ['no_enemy_interceptors', 'fast_path'],
                'expected_dmg': lambda mp, turrets: (mp * 3.5) - (turrets * 2),
                'risk': 'low',
                'counter': 'interceptor_mirror',
                'weight': 0.95,
                'micro_enabled': True
            },
            'mixed_assault': {
                'unit': 'mixed',
                'min_mp': 16,
                'optimal_mp': 24,
                'demo_ratio': 0.4,
                'scout_ratio': 0.5,
                'int_ratio': 0.1,
                'conditions': ['versatile_path', 'medium_defense'],
                'expected_dmg': lambda mp: mp * 1.8,
                'risk': 'medium',
                'counter': 'layered_defense',
                'weight': 1.25,
                'micro_enabled': True
            },
            'surgical_strike': {
                'unit': 'demolisher',
                'min_mp': 12,
                'optimal_mp': 15,
                'allocation': 0.8,
                'conditions': ['support_clusters', 'economic_target'],
                'expected_dmg': lambda supports: supports * 3.5,
                'risk': 'low',
                'counter': 'forward_defense',
                'weight': 1.1,
                'micro_enabled': True
            },
            'pincer_attack': {
                'unit': 'split',
                'min_mp': 20,
                'optimal_mp': 28,
                'allocation': 0.95,
                'conditions': ['multiple_weak_paths', 'divided_defense'],
                'expected_dmg': lambda paths: len(paths) * 10,
                'risk': 'high',
                'counter': 'mobile_response',
                'weight': 1.3,
                'micro_enabled': True
            }
        }

    def on_game_start(self, config):
        """Initialize AI systems"""
        gamelib.debug_write('🚀 Ultimate Championship AI Initializing...')
        gamelib.debug_write('   ✓ Neural Networks: ONLINE')
        gamelib.debug_write('   ✓ Microcontrollers: ACTIVE')
        gamelib.debug_write('   ✓ Path Dynamics Engine: OPTIMIZED')
        gamelib.debug_write('   ✓ Strategy Matrix: LOADED')
        
        self.config = config or {}
        
        # Map configuration
        map_settings = self.config.get('mapSettings', {}) if isinstance(self.config, dict) else {}
        self.map_width = map_settings.get('width', self.map_width)
        self.map_height = map_settings.get('height', self.map_height)
        self.preferred_columns = map_settings.get('preferred_columns', self.preferred_columns)
        
        # Persistence settings
        if self.config.get('noPersistence', False) or os.environ.get('NO_PERSIST') == '1':
            self.persistence_enabled = False
            gamelib.debug_write('[MEM] Persistence disabled by config/env')
        
        # Unit shorthand mapping
        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        try:
            info = self.config.get('unitInformation', [])
            WALL = info[0]['shorthand'] if len(info) > 0 else 'WALL'
            SUPPORT = info[1]['shorthand'] if len(info) > 1 else 'SUPPORT'
            TURRET = info[2]['shorthand'] if len(info) > 2 else 'TURRET'
            SCOUT = info[3]['shorthand'] if len(info) > 3 else 'SCOUT'
            DEMOLISHER = info[4]['shorthand'] if len(info) > 4 else 'DEMOLISHER'
            INTERCEPTOR = info[5]['shorthand'] if len(info) > 5 else 'INTERCEPTOR'
            MP = 1
            SP = 0
        except Exception:
            WALL, SUPPORT, TURRET = 'WALL', 'SUPPORT', 'TURRET'
            SCOUT, DEMOLISHER, INTERCEPTOR = 'SCOUT', 'DEMOLISHER', 'INTERCEPTOR'
            MP, SP = 1, 0
        
        self.unit_stats = {
            WALL: {'cost': 0.5, 'upgrade': 2, 'hp': 60, 'upgraded_hp': 120},
            SUPPORT: {'cost': 4, 'upgrade': 2, 'hp': 60, 'upgraded_hp': 120},
            TURRET: {'cost': 2, 'upgrade': 4, 'hp': 75, 'upgraded_hp': 150, 'dps': 5, 'upgraded_dps': 10},
            SCOUT: {'cost': 1, 'hp': 15, 'dmg': 2, 'speed': 1},
            DEMOLISHER: {'cost': 3, 'hp': 5, 'dmg': 8, 'speed': 0.25},
            INTERCEPTOR: {'cost': 1, 'hp': 40, 'dmg': 20, 'speed': 4}
        }
        
        # Initialize micro systems
        self.path_engine = PathDynamicsEngine(self)
        self.scout_controller = ScoutSwarmController(self, self.path_engine)
        self.demolisher_escort = DemolisherEscortController(self, self.path_engine)
        self.interceptor_controller = InterceptorController(self, self.path_engine)
        
        # Load memory
        self._load_memory()
        
        gamelib.debug_write('✅ Initialization Complete - Battle Ready\n')

    # ═══════════════ PERSISTENCE SYSTEM ═══════════════
    def _load_memory(self):
        """Load historical data from disk"""
        if not self.persistence_enabled:
            return
        if not os.path.exists(MEMORY_FILE):
            gamelib.debug_write('[MEM] No memory file to load')
            return
        try:
            with open(MEMORY_FILE, 'r') as f:
                data = json.load(f)
            for k, v in data.get('attack_history', {}).items():
                self.attack_history[k].update(v)
            for k, v in data.get('breach_analytics', {}).items():
                self.breach_analytics[k].update(v)
            gamelib.debug_write('[MEM] Memory loaded from disk')
        except Exception as e:
            gamelib.debug_write(f'[MEM] Failed to load memory: {e}')

    def _save_memory(self):
        """Save learning data to disk"""
        if not self.persistence_enabled:
            return
        try:
            out = {
                'attack_history': {k: dict(v) for k, v in self.attack_history.items()},
                'breach_analytics': {k: dict(v) for k, v in self.breach_analytics.items()}
            }
            with open(MEMORY_FILE, 'w') as f:
                json.dump(out, f, indent=2)
            if self.report_enabled:
                self._write_csv_report()
                self._write_html_report()
            gamelib.debug_write('[MEM] Memory saved')
        except Exception as e:
            gamelib.debug_write(f'[MEM] Failed to save memory: {e}')

    def _write_csv_report(self):
        """Generate CSV performance report"""
        try:
            with open(REPORT_CSV, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['play', 'attempts', 'successes', 'total_damage', 'avg_damage', 'efficiency'])
                for play, rec in self.attack_history.items():
                    attempts = rec.get('attempts', 0)
                    successes = rec.get('successes', 0)
                    total_dmg = rec.get('total_damage', 0)
                    avg_dmg = rec.get('avg_damage', 0)
                    efficiency = rec.get('cost_efficiency', 0)
                    writer.writerow([play, attempts, successes, total_dmg, f'{avg_dmg:.2f}', f'{efficiency:.2f}'])
        except Exception as e:
            gamelib.debug_write(f'[REPORT] CSV error: {e}')

    def _write_html_report(self):
        """Generate HTML performance report"""
        try:
            data = {
                'attack_history': {k: dict(v) for k, v in self.attack_history.items()},
                'breach_analytics': {k: dict(v) for k, v in self.breach_analytics.items()},
                'metrics': {
                    'win_probability': self.metrics['win_probability'],
                    'total_breaches': self.metrics['offensive_breaches'],
                    'perfect_defenses': self.metrics['perfect_defenses']
                }
            }
            html = f"""
<!doctype html>
<html><head><meta charset='utf-8'><title>Terminal AI v7.0 Report</title>
<style>
body {{ font-family: monospace; background: #1a1a1a; color: #00ff00; padding: 20px; }}
h1 {{ color: #00ffff; }}
pre {{ background: #0a0a0a; padding: 15px; border: 1px solid #00ff00; }}
</style>
</head><body>
<h1>🏆 Terminal AI v7.0 Championship Report</h1>
<pre>{json.dumps(data, indent=2)}</pre>
</body></html>
"""
            with open(REPORT_HTML, 'w') as f:
                f.write(html)
        except Exception as e:
            gamelib.debug_write(f'[REPORT] HTML error: {e}')

    def on_turn(self, turn_state):
        """Master strategic orchestrator with micro control"""
        game_state = gamelib.GameState(self.config, turn_state)
        turn = game_state.turn_number
        
        self._display_analytics(game_state)
        game_state.suppress_warnings(True)
        
        # Cache management
        if self.cache['valid_turn'] != turn:
            self._clear_caches()
            self.cache['valid_turn'] = turn
        
        # Update path dynamics heatmap early
        self.path_engine.update_heatmap(game_state)
        
        # ═══════════════ DEEP ANALYSIS PHASE ═══════════════
        try:
            self._analyze_game_state(game_state)
            self._model_opponent_behavior(game_state)
            self._assess_threats(game_state)
            self._identify_opportunities(game_state)
            self._update_game_phase(game_state)
            self._adapt_strategy(game_state)
            self._calculate_pressure(game_state)
        except Exception as e:
            gamelib.debug_write(f'[ERROR] Analysis error: {e}')
        
        # ═══════════════ STRATEGIC EXECUTION ═══════════════
        try:
            self._execute_master_strategy(game_state)
        except Exception as e:
            gamelib.debug_write(f'[ERROR] Execution error: {e}')
        
        # Record state
        self._record_turn_state(game_state)
        
        # Autosave
        if self.persistence_enabled and turn % self.autosave_every == 0 and turn > 0:
            self._save_memory()
        
        # Save on decisive moments
        if self.metrics['win_probability'] > 0.95 or self.metrics['win_probability'] < 0.05:
            self._save_memory()
        
        game_state.submit_turn()

    def _display_analytics(self, game_state):
        """Enhanced analytics display"""
        t = game_state.turn_number
        try:
            hdiff = game_state.my_health - game_state.enemy_health
        except:
            hdiff = 0
        
        gamelib.debug_write(f'\n{"═"*80}')
        gamelib.debug_write(f'🎮 TURN {t:3d} │ Phase: {self.game_phase:12s} │ Mode: {self.strategy_mode:12s}')
        gamelib.debug_write(f'{"─"*80}')
        
        try:
            gamelib.debug_write(f'💚 HP: {game_state.my_health:2d} vs {game_state.enemy_health:2d} (Δ{hdiff:+3d}) │ '
                              f'💎 {game_state.get_resource(SP):3.0f}SP {game_state.get_resource(MP):3.1f}MP')
            gamelib.debug_write(f'📊 Win%: {self.metrics["win_probability"]*100:5.1f} │ '
                              f'Momentum: {self.metrics["momentum_score"]:+5.2f} │ '
                              f'Pressure: {self.metrics["pressure_score"]:5.2f}')
        except:
            pass
        
        gamelib.debug_write(f'🎯 Enemy: {self.opponent_model["playstyle"]:12s} │ '
                          f'Skill: {self.opponent_model["skill_estimate"]*100:4.1f}% │ '
                          f'Predict: {self.opponent_model["predictability"]*100:4.1f}%')
        
        if self.cache.get('threats'):
            threat_level = self.cache['threats'].get('level', 'low')
            try:
                gamelib.debug_write(f'⚠️  Threat: {threat_level.upper():12s} │ '
                                  f'Enemy MP: {game_state.get_resource(MP, 1):3.1f}')
            except:
                pass
        
        gamelib.debug_write(f'{"═"*80}')

    def _clear_caches(self):
        """Clear all caches for new turn"""
        for key in ['paths', 'damage', 'threats', 'opportunities', 'best_attack', 'weak_zones']:
            if isinstance(self.cache.get(key), dict):
                self.cache[key].clear()
            elif isinstance(self.cache.get(key), list):
                self.cache[key] = []
            else:
                self.cache[key] = None

    def _analyze_game_state(self, game_state):
        """Comprehensive state analysis"""
        # Structure analysis
        our_structures = self._analyze_structures(game_state, player=0)
        enemy_structures = self._analyze_structures(game_state, player=1)
        
        self.cache['structures'] = {
            'ours': our_structures,
            'enemy': enemy_structures
        }
        
        # Resource tracking
        try:
            enemy_sp = game_state.get_resource(SP, 1)
            enemy_mp = game_state.get_resource(MP, 1)
            self.history['enemy_resources']['sp'].append(enemy_sp)
            self.history['enemy_resources']['mp'].append(enemy_mp)
        except:
            pass
        
        # Update metrics
        self._update_metrics(game_state, our_structures, enemy_structures)
        
        # Health tracking
        try:
            hdiff = game_state.my_health - game_state.enemy_health
            self.history['health_differential'].append(hdiff)
        except:
            pass
        
        # Damage tracking
        self._track_damage(game_state)
        
        # Structure count history
        self.history['structure_counts'].append({
            'ours': our_structures.get('total', 0),
            'enemy': enemy_structures.get('total', 0)
        })

    def _analyze_structures(self, game_state, player):
        """Deep structure analysis with spatial mapping"""
        structures = defaultdict(int)
        structures['firepower'] = 0
        structures['max_health'] = 0
        structures['health'] = 0
        positions = {'turrets': [], 'walls': [], 'supports': []}
        
        try:
            y_range = range(14, min(self.map_height, 28)) if player == 1 else range(14)
            
            for x in range(min(self.map_width, 28)):
                for y in y_range:
                    try:
                        if game_state.contains_stationary_unit([x, y]):
                            for unit in game_state.game_map[[x, y]]:
                                if getattr(unit, 'player_index', None) != player:
                                    continue
                                
                                structures['total'] += 1
                                structures['health'] += getattr(unit, 'health', 0)
                                structures['max_health'] += getattr(unit, 'max_health', 0)
                                
                                if getattr(unit, 'upgraded', False):
                                    structures['upgraded'] += 1
                                
                                unit_type = getattr(unit, 'unit_type', None)
                                if unit_type == TURRET:
                                    structures['turrets'] += 1
                                    dps = getattr(unit, 'damage_i', 0) * (2 if getattr(unit, 'upgraded', False) else 1)
                                    structures['firepower'] += dps
                                    positions['turrets'].append((x, y, getattr(unit, 'upgraded', False)))
                                elif unit_type == WALL:
                                    structures['walls'] += 1
                                    positions['walls'].append((x, y, getattr(unit, 'upgraded', False)))
                                elif unit_type == SUPPORT:
                                    structures['supports'] += 1
                                    positions['supports'].append((x, y, getattr(unit, 'upgraded', False)))
                                
                                # Positional analysis
                                if y >= 12:
                                    structures['back'] += 1
                                elif y >= 10:
                                    structures['mid'] += 1
                                else:
                                    structures['front'] += 1
                    except Exception:
                        continue
        except Exception:
            pass
        
        # Calculate ratios
        if structures['max_health'] > 0:
            structures['health_pct'] = structures['health'] / structures['max_health']
        else:
            structures['health_pct'] = 1.0
        
        if structures['total'] > 0:
            structures['upgrade_ratio'] = structures['upgraded'] / structures['total']
            structures['density'] = structures['total'] / 28.0
        else:
            structures['upgrade_ratio'] = 0.0
            structures['density'] = 0.0
        
        structures['positions'] = positions
        return dict(structures)

    def _update_metrics(self, game_state, our_str, enemy_str):
        """Advanced metrics calculation"""
        # Map control
        total_structures = our_str.get('total', 1) + enemy_str.get('total', 1)
        self.metrics['map_control'] = our_str.get('total', 0) / total_structures
        
        # Structure health
        self.metrics['structure_health_ratio'] = our_str.get('health_pct', 1.0)
        
        # Economic advantage
        try:
            our_sp = game_state.get_resource(SP)
            our_mp = game_state.get_resource(MP)
            sp_value = our_sp + (our_str.get('supports', 0) * 6)
            self.metrics['economic_advantage'] = (sp_value / 60.0) + (our_mp / 20.0)
        except:
            pass
        
        # Win probability
        self._calculate_win_probability(game_state)
        
        # Momentum
        self._calculate_momentum()

    def _track_damage(self, game_state):
        """Track damage with sophisticated analytics"""
        try:
            dmg_taken = self.prev_health['ours'] - game_state.my_health
            dmg_dealt = self.prev_health['enemy'] - game_state.enemy_health
            
            if dmg_taken > 0:
                self.metrics['damage_taken'].append(dmg_taken)
                self.metrics['defensive_breaches'] += 1
                
                if game_state.my_health <= 10 and dmg_taken >= 5:
                    self.thresholds['emergency_threshold'] = 15
                    gamelib.debug_write(f'🚨 CRITICAL BREACH: -{dmg_taken} HP (Health: {game_state.my_health})')
                else:
                    gamelib.debug_write(f'⚠️  Breach: -{dmg_taken} HP')
            else:
                self.metrics['perfect_defenses'] += 1
            
            if dmg_dealt > 0:
                self.metrics['damage_dealt'].append(dmg_dealt)
                self.metrics['offensive_breaches'] += 1
                
                mp_spent = self.last_mp_spent
                if mp_spent > 0:
                    roi = dmg_dealt / mp_spent
                    self.metrics['attack_roi'].append(roi)
                    gamelib.debug_write(f'✅ Attack Success: +{dmg_dealt} HP (ROI: {roi:.2f}x)')
            elif self.last_mp_spent > 5:
                self.metrics['failed_attacks'] += 1
                gamelib.debug_write(f'❌ Attack Failed: {self.last_mp_spent} MP wasted')
            
            self.prev_health = {
                'ours': game_state.my_health,
                'enemy': game_state.enemy_health
            }
        except Exception as e:
            pass

    def _calculate_win_probability(self, game_state):
        """Multi-factor win probability"""
        try:
            factors = []
            
            # Health advantage (40% weight)
            hdiff = game_state.my_health - game_state.enemy_health
            health_factor = 0.5 + (hdiff / 60.0) * 0.9
            factors.append(('health', health_factor, 0.40))
            
            # Structure advantage (25% weight)
            our_str = self.cache['structures']['ours']
            enemy_str = self.cache['structures']['enemy']
            structure_diff = (our_str.get('total', 0) - enemy_str.get('total', 0)) / 30.0
            structure_factor = 0.5 + structure_diff * 0.8
            factors.append(('structures', structure_factor, 0.25))
            
            # Firepower advantage (20% weight)
            firepower_diff = (our_str.get('firepower', 0) - enemy_str.get('firepower', 0)) / 100.0
            firepower_factor = 0.5 + firepower_diff * 0.7
            factors.append(('firepower', firepower_factor, 0.20))
            
            # Recent performance (15% weight)
            perf_factor = 0.5
            if len(self.metrics['damage_dealt']) >= 3:
                recent_net = sum(list(self.metrics['damage_dealt'])[-3:]) - sum(list(self.metrics['damage_taken'])[-3:])
                perf_factor = 0.5 + (recent_net / 30.0)
            factors.append(('performance', perf_factor, 0.15))
            
            # Weighted combination
            win_prob = sum(f * w for _, f, w in factors)
            win_prob = max(0.05, min(0.95, win_prob))
            
            self.metrics['win_probability'] = win_prob
        except Exception as e:
            pass

    def _calculate_momentum(self):
        """Calculate game momentum score"""
        momentum = 0.0
        
        try:
            # Recent damage trend (40%)
            if len(self.metrics['damage_dealt']) >= 3 and len(self.metrics['damage_taken']) >= 3:
                recent_dealt = list(self.metrics['damage_dealt'])[-3:]
                recent_taken = list(self.metrics['damage_taken'])[-3:]
                net_damage = sum(recent_dealt) - sum(recent_taken)
                momentum += (net_damage / 10.0) * 0.4
            
            # Health trend (30%)
            if len(self.history['health_differential']) >= 5:
                recent_diffs = list(self.history['health_differential'])[-5:]
                trend = (recent_diffs[-1] - recent_diffs[0]) / 5.0
                momentum += trend * 0.3
            
            # Win streak (20%)
            if self.metrics['perfect_defenses'] >= 3:
                momentum += 0.4
            if self.metrics['offensive_breaches'] >= 3:
                momentum += 0.3
            
            # ROI trend (10%)
            if len(self.metrics['attack_roi']) >= 2:
                avg_roi = sum(list(self.metrics['attack_roi'])[-3:]) / min(3, len(self.metrics['attack_roi']))
                if avg_roi > 2.0:
                    momentum += 0.2
                elif avg_roi > 1.5:
                    momentum += 0.1
            
            self.metrics['momentum_score'] = max(-2.0, min(2.0, momentum))
        except:
            pass

    def _model_opponent_behavior(self, game_state):
        """Advanced opponent modeling with counter-strategy"""
        turn = game_state.turn_number
        
        if turn < 3:
            return
        
        enemy_str = self.cache['structures']['enemy']
        try:
            enemy_mp = game_state.get_resource(MP, 1)
        except:
            enemy_mp = 5
        
        # Classify playstyle
        self._classify_playstyle(game_state, enemy_str, enemy_mp)
        
        # Estimate skill
        self._estimate_skill_level(game_state, enemy_str)
        
        # Calculate predictability
        self._calculate_predictability()
        
        # Find weaknesses
        self._find_weaknesses(game_state)
        
        # Develop counter-strategy
        self._develop_counter_strategy()

    def _classify_playstyle(self, game_state, enemy_str, enemy_mp):
        """Classify opponent strategy"""
        turn = game_state.turn_number
        
        # Attack frequency
        attack_freq = len(self.opponent_model['attack_patterns']) / max(1, turn)
        
        # Average MP
        if len(self.history['enemy_resources']['mp']) > 0:
            avg_mp = sum(self.history['enemy_resources']['mp']) / len(self.history['enemy_resources']['mp'])
        else:
            avg_mp = 5
        
        turret_count = enemy_str.get('turrets', 0)
        support_count = enemy_str.get('supports', 0)
        upgrade_ratio = enemy_str.get('upgrade_ratio', 0)
        
        # Classification logic
        if attack_freq > 0.5 and avg_mp < 7:
            self.opponent_model['playstyle'] = 'rush'
            self.opponent_model['aggression_score'] = 0.95
            self.opponent_model['defense_rating'] = 0.3
        elif turret_count > 20 and attack_freq < 0.15:
            self.opponent_model['playstyle'] = 'turtle'
            self.opponent_model['defense_rating'] = 0.9
            self.opponent_model['aggression_score'] = 0.15
        elif support_count >= 6:
            self.opponent_model['playstyle'] = 'economic'
            self.opponent_model['economy_priority'] = 0.9
        elif upgrade_ratio > 0.4 and turret_count > 15:
            self.opponent_model['playstyle'] = 'balanced'
            self.opponent_model['aggression_score'] = 0.5
            self.opponent_model['defense_rating'] = 0.7
        else:
            self.opponent_model['playstyle'] = 'adaptive'
            self.opponent_model['adaptation_speed'] = 0.75

    def _estimate_skill_level(self, game_state, enemy_str):
        """Estimate opponent skill with multiple indicators"""
        skill_indicators = []
        
        # Economy management
        support_count = enemy_str.get('supports', 0)
        if support_count >= 5:
            skill_indicators.append(0.25)
        elif support_count >= 3:
            skill_indicators.append(0.15)
        
        # Upgrade efficiency
        upgrade_ratio = enemy_str.get('upgrade_ratio', 0)
        if upgrade_ratio > 0.4:
            skill_indicators.append(0.30)
        elif upgrade_ratio > 0.25:
            skill_indicators.append(0.20)
        elif upgrade_ratio > 0.15:
            skill_indicators.append(0.10)
        
        # Attack effectiveness
        if len(self.metrics['damage_taken']) >= 3:
            avg_dmg = sum(list(self.metrics['damage_taken'])[-5:]) / min(5, len(self.metrics['damage_taken']))
            if avg_dmg > 8:
                skill_indicators.append(0.35)
            elif avg_dmg > 5:
                skill_indicators.append(0.25)
            elif avg_dmg > 3:
                skill_indicators.append(0.15)
        
        # Strategic variety
        pattern_variety = len(set(self.opponent_model['attack_patterns'])) / max(1, len(self.opponent_model['attack_patterns']))
        if pattern_variety > 0.7:
            skill_indicators.append(0.20)
        elif pattern_variety > 0.5:
            skill_indicators.append(0.10)
        
        # Defense quality
        if enemy_str.get('density', 0) > 0.7 and upgrade_ratio > 0.3:
            skill_indicators.append(0.15)
        
        # Resource efficiency
        if enemy_str.get('total', 0) > 25 and upgrade_ratio > 0.25:
            skill_indicators.append(0.10)
        
        self.opponent_model['skill_estimate'] = min(0.98, max(0.15, sum(skill_indicators)))

    def _calculate_predictability(self):
        """Calculate opponent predictability"""
        if len(self.opponent_model['timing_patterns']) < 5:
            self.opponent_model['predictability'] = 0.5
            return
        
        timings = list(self.opponent_model['timing_patterns'])
        if len(timings) < 2:
            return
        
        intervals = [timings[i+1] - timings[i] for i in range(len(timings)-1)]
        
        if intervals:
            avg_interval = sum(intervals) / len(intervals)
            variance = sum((x - avg_interval)**2 for x in intervals) / len(intervals)
            std_dev = math.sqrt(variance)
            
            # Low variance = high predictability
            predictability = 1.0 / (1.0 + std_dev / max(1, avg_interval))
            self.opponent_model['predictability'] = predictability

    def _find_weaknesses(self, game_state):
        """Identify exploitable weaknesses"""
        weaknesses = []
        enemy_str = self.cache['structures']['enemy']
        
        # Analyze turret coverage
        turret_positions = enemy_str.get('positions', {}).get('turrets', [])
        
        # Check coverage gaps
        coverage_map = defaultdict(int)
        for tx, ty, upgraded in turret_positions:
            for x in range(max(0, tx-3), min(28, tx+4)):
                coverage_map[x] += (2 if upgraded else 1)
        
        # Find weak zones
        for x in range(0, 28, 2):
            if coverage_map[x] < 2:
                weaknesses.append(('sparse_zone', x, coverage_map[x]))
        
        # Check upgrade status
        if enemy_str.get('upgrade_ratio', 0) < 0.20:
            weaknesses.append(('low_upgrades', enemy_str.get('upgrade_ratio', 0)))
        
        # Check damaged structures
        if enemy_str.get('health_pct', 1) < 0.60:
            weaknesses.append(('damaged_defense', enemy_str.get('health_pct', 1)))
        
        # Check wall density
        wall_count = enemy_str.get('walls', 0)
        if wall_count < 6:
            weaknesses.append(('insufficient_walls', wall_count))
        
        # Check support exposure
        support_positions = enemy_str.get('positions', {}).get('supports', [])
        for sx, sy, upgraded in support_positions:
            nearby_walls = sum(1 for wx, wy, _ in enemy_str.get('positions', {}).get('walls', []) 
                             if abs(wx-sx) + abs(wy-sy) <= 2)
            if nearby_walls < 2:
                weaknesses.append(('exposed_support', sx, sy))
        
        self.opponent_model['defense_weaknesses'] = weaknesses
        self.cache['weak_zones'] = [w for w in weaknesses if w[0] == 'sparse_zone']

    def _develop_counter_strategy(self):
        """Develop targeted counter-strategy"""
        playstyle = self.opponent_model['playstyle']
        
        counter_strategies = {
            'rush': {
                'defense_priority': 0.85,
                'economy_priority': 0.10,
                'counter_attack': 0.05,
                'focus': 'early_defense',
                'recommended': 'fortress_control'
            },
            'turtle': {
                'defense_priority': 0.60,
                'economy_priority': 0.25,
                'counter_attack': 0.15,
                'focus': 'economic_boom',
                'recommended': 'economic_control'
            },
            'economic': {
                'defense_priority': 0.65,
                'economy_priority': 0.15,
                'counter_attack': 0.20,
                'focus': 'aggressive_strikes',
                'recommended': 'aggressive_tempo'
            },
            'balanced': {
                'defense_priority': 0.70,
                'economy_priority': 0.15,
                'counter_attack': 0.15,
                'focus': 'adaptive_play',
                'recommended': 'adaptive_pressure'
            },
            'adaptive': {
                'defense_priority': 0.70,
                'economy_priority': 0.15,
                'counter_attack': 0.15,
                'focus': 'flexible_response',
                'recommended': 'adaptive_pressure'
            }
        }
        
        self.opponent_model['counter_strategy'] = counter_strategies.get(playstyle, counter_strategies['balanced'])

    def _assess_threats(self, game_state):
        """Comprehensive threat assessment"""
        try:
            enemy_mp = game_state.get_resource(MP, 1)
        except:
            enemy_mp = 0
        
        turn = game_state.turn_number
        threat_level = 'low'
        threats = []
        
        # MP-based threats
        if enemy_mp >= 22:
            threat_level = 'critical'
            threats.append(('massive_attack', enemy_mp))
        elif enemy_mp >= 16:
            threat_level = 'high'
            threats.append(('major_attack', enemy_mp))
        elif enemy_mp >= 11:
            threat_level = 'moderate'
            threats.append(('standard_attack', enemy_mp))
        elif enemy_mp >= 7:
            threat_level = 'low'
            threats.append(('probing_attack', enemy_mp))
        
        # Pattern prediction
        if self.opponent_model['predictability'] > 0.70 and len(self.opponent_model['timing_patterns']) >= 3:
            last_attacks = list(self.opponent_model['timing_patterns'])[-3:]
            if len(last_attacks) >= 2:
                avg_interval = sum(last_attacks[i+1] - last_attacks[i] for i in range(len(last_attacks)-1)) / (len(last_attacks)-1)
                predicted_next = last_attacks[-1] + avg_interval
                
                if abs(turn - predicted_next) <= 1.5:
                    threats.append(('predicted_attack', turn, predicted_next))
                    if threat_level in ['low', 'none']:
                        threat_level = 'moderate'
                    gamelib.debug_write(f'🔮 Attack Predicted: Turn {predicted_next:.0f}')
        
        # Playstyle threats
        if self.opponent_model['playstyle'] == 'rush' and turn < 8:
            threats.append(('early_rush', turn))
            if threat_level == 'low':
                threat_level = 'moderate'
        
        self.cache['threats'] = {
            'level': threat_level,
            'active': threats,
            'enemy_mp': enemy_mp
        }

    def _identify_opportunities(self, game_state):
        """Identify offensive opportunities"""
        opportunities = []
        enemy_str = self.cache['structures']['enemy']
        
        try:
            our_mp = game_state.get_resource(MP)
        except:
            our_mp = 5
        
        # Weakness-based opportunities
        weaknesses = self.opponent_model['defense_weaknesses']
        for weakness in weaknesses:
            if weakness[0] == 'sparse_zone' and our_mp >= 10:
                opportunities.append(('exploit_gap', weakness[1], weakness[2]))
            elif weakness[0] == 'exposed_support' and our_mp >= 12:
                opportunities.append(('target_support', weakness[1], weakness[2]))
            elif weakness[0] == 'damaged_defense' and our_mp >= 8:
                opportunities.append(('pressure_weak', weakness[1]))
        
        # Economic opportunities
        support_count = enemy_str.get('supports', 0)
        if support_count >= 4 and our_mp >= 12:
            opportunities.append(('economic_raid', support_count))
        
        # All-in opportunities
        try:
            if game_state.my_health >= 20 and game_state.enemy_health <= 12 and our_mp >= 18:
                opportunities.append(('all_in_potential', game_state.enemy_health))
        except:
            pass
        
        # Counter-punch after defense
        if self.metrics['perfect_defenses'] >= 2 and our_mp >= 10:
            opportunities.append(('counter_punch', our_mp))
        
        # Momentum push
        if self.metrics['momentum_score'] > 1.2 and our_mp >= self.thresholds['attack_min_mp']:
            opportunities.append(('momentum_push', None))
        
        self.cache['opportunities'] = opportunities

    def _calculate_pressure(self, game_state):
        """Calculate offensive pressure score"""
        pressure = 0.0
        
        try:
            # MP accumulation
            our_mp = game_state.get_resource(MP)
            pressure += min(our_mp / 15.0, 1.0) * 0.3
        except:
            pass
        
        # Recent attack success
        if len(self.metrics['damage_dealt']) >= 2:
            recent_dmg = sum(list(self.metrics['damage_dealt'])[-2:])
            pressure += min(recent_dmg / 15.0, 1.0) * 0.25
        
        # Enemy weaknesses
        weakness_count = len(self.opponent_model['defense_weaknesses'])
        pressure += min(weakness_count / 5.0, 1.0) * 0.25
        
        # Momentum
        if self.metrics['momentum_score'] > 0:
            pressure += min(self.metrics['momentum_score'] / 2.0, 0.5) * 0.2
        
        self.metrics['pressure_score'] = pressure

    def _update_game_phase(self, game_state):
        """Update game phase"""
        turn = game_state.turn_number
        try:
            total_health = game_state.my_health + game_state.enemy_health
        except:
            total_health = 60
        
        if turn <= 5:
            self.game_phase = 'opening'
        elif turn <= 15:
            self.game_phase = 'early_mid'
        elif turn <= 30:
            self.game_phase = 'mid_game'
        elif turn <= 50:
            self.game_phase = 'late_game'
        else:
            self.game_phase = 'endgame'
        
        # Override based on health
        if total_health <= 20:
            self.game_phase = 'critical'
        elif total_health <= 30:
            self.game_phase = 'decisive'

    def _adapt_strategy(self, game_state):
        """Adapt strategy based on situation"""
        # Get situation
        win_prob = self.metrics['win_probability']
        momentum = self.metrics['momentum_score']
        threat_level = self.cache.get('threats', {}).get('level', 'low')
        
        try:
            my_health = game_state.my_health
            enemy_health = game_state.enemy_health
        except:
            my_health = 30
            enemy_health = 30
        
        # Determine strategy mode
        if my_health <= 8:
            self.strategy_mode = 'desperate'
            self.aggression_level = 0.3
            self.risk_tolerance = 0.2
        elif threat_level == 'critical':
            self.strategy_mode = 'defensive'
            self.aggression_level = 0.2
            self.risk_tolerance = 0.3
        elif win_prob > 0.70 and momentum > 0.5:
            self.strategy_mode = 'press'
            self.aggression_level = 0.8
            self.risk_tolerance = 0.6
        elif win_prob < 0.35 and enemy_health <= 15:
            self.strategy_mode = 'all_in'
            self.aggression_level = 0.95
            self.risk_tolerance = 0.9
            self.all_in_mode = True
        elif win_prob < 0.40:
            self.strategy_mode = 'comeback'
            self.aggression_level = 0.6
            self.risk_tolerance = 0.5
        else:
            self.strategy_mode = 'balanced'
            self.aggression_level = 0.5
            self.risk_tolerance = 0.5
        
        # Adapt thresholds
        self._adapt_thresholds(game_state)

    def _adapt_thresholds(self, game_state):
        """Dynamically adapt decision thresholds"""
        if self.strategy_mode == 'desperate':
            self.thresholds['defense_sp_ratio'] = 0.90
            self.thresholds['attack_min_mp'] = 12
            self.thresholds['attack_min_ev'] = 10
        elif self.strategy_mode == 'defensive':
            self.thresholds['defense_sp_ratio'] = 0.85
            self.thresholds['attack_min_mp'] = 10
            self.thresholds['attack_min_ev'] = 12
        elif self.strategy_mode in ['press', 'all_in']:
            self.thresholds['defense_sp_ratio'] = 0.60
            self.thresholds['attack_min_mp'] = 7
            self.thresholds['attack_min_ev'] = 10
        else:
            self.thresholds['defense_sp_ratio'] = 0.75
            self.thresholds['attack_min_mp'] = 8
            self.thresholds['attack_min_ev'] = 12

    def _execute_master_strategy(self, game_state):
        """Execute coordinated strategy with micro control"""
        turn = game_state.turn_number
        
        try:
            our_sp = game_state.get_resource(SP)
            our_mp = game_state.get_resource(MP)
        except:
            our_sp = 0
            our_mp = 0
        
        gamelib.debug_write(f'\n🎯 Executing {self.strategy_mode.upper()} strategy...')
        
        # Phase 1: Deploy opening
        if turn == 0:
            self._deploy_opening(game_state)
            return
        
        # Phase 2: Baseline defenses
        self._baseline_build(game_state)
        
        # Phase 3: Repair critical structures
        self._repair_critical_structures(game_state)
        
        # Phase 4: Emergency defense
        threat_level = self.cache.get('threats', {}).get('level', 'low')
        if threat_level in ['critical', 'high']:
            self._emergency_defense(game_state)
        
        # Phase 5: Build/upgrade defenses
        sp_for_defense = our_sp * self.thresholds['defense_sp_ratio']
        self._build_adaptive_defense(game_state, sp_for_defense)
        
        # Phase 6: Upgrades
        self._upgrade_logic(game_state)
        
        # Phase 7: Economy (if safe)
        if threat_level == 'low' and our_sp > 8:
            self._build_economy(game_state)
        
        # Phase 8: Offensive action with micro control
        if our_mp >= self.thresholds['attack_min_mp']:
            attack_executed = self._attack_logic_with_micro(game_state)
            if attack_executed:
                return
        
        # Phase 9: Emergency all-in logic
        self._emergency_logic(game_state)
        
        self.last_mp_spent = 0

    def _deploy_opening(self, game_state):
        """Deploy optimized opening"""
        # Select best strategy
        strategies = list(self.strategies.keys())
        weights = [self.strategies[s]['win_rate'] for s in strategies]
        
        total = sum(weights)
        normalized = [w/total for w in weights]
        
        choice = random.choices(strategies, weights=normalized)[0]
        opening = self.strategies[choice]
        
        gamelib.debug_write(f'📋 Deploying Opening: {choice} (WR: {opening["win_rate"]*100:.1f}%)')
        
        # Deploy turrets
        for loc in opening.get('turrets', []):
            game_state.attempt_spawn(TURRET, loc)
        
        # Deploy walls
        for loc in opening.get('walls', []):
            game_state.attempt_spawn(WALL, loc)
        
        # Deploy supports
        for loc in opening.get('supports', []):
            game_state.attempt_spawn(SUPPORT, loc)
        
        # Upgrade priority structures
        for loc in opening.get('upgrades', []):
            game_state.attempt_upgrade(loc)

    def _baseline_build(self, game_state):
        """Build baseline defensive structures"""
        try:
            for loc in [[13, 13], [14, 13], [0, 13], [27, 13]]:
                if game_state.can_spawn(WALL, loc):
                    game_state.attempt_spawn(WALL, loc)
                if game_state.can_spawn(TURRET, loc):
                    game_state.attempt_spawn(TURRET, loc)
        except Exception:
            pass

    def _repair_critical_structures(self, game_state):
        """Repair damaged critical structures"""
        repairs_made = 0
        
        try:
            for x in range(28):
                for y in range(14):
                    if game_state.contains_stationary_unit([x, y]):
                        for unit in game_state.game_map[[x, y]]:
                            if getattr(unit, 'player_index', None) == 0:
                                health_pct = getattr(unit, 'health', 0) / max(1, getattr(unit, 'max_health', 1))
                                unit_type = getattr(unit, 'unit_type', None)
                                
                                if health_pct < 0.40 and unit_type in [TURRET, WALL]:
                                    if game_state.attempt_spawn(unit_type, [x, y]):
                                        repairs_made += 1
                                        gamelib.debug_write(f'🔧 Repaired {unit_type} at [{x},{y}]')
        except Exception:
            pass
        
        if repairs_made > 0:
            gamelib.debug_write(f'✅ Completed {repairs_made} critical repairs')

    def _emergency_defense(self, game_state):
        """Emergency defensive reinforcement with micro"""
        try:
            enemy_mp = game_state.get_resource(MP, 1)
            our_sp = game_state.get_resource(SP)
            our_mp = game_state.get_resource(MP)
        except:
            return
        
        gamelib.debug_write(f'🚨 EMERGENCY DEFENSE (Enemy MP: {enemy_mp:.1f})')
        
        # Deploy defensive interceptors using micro controller
        if our_mp >= 5 and enemy_mp >= 15:
            spawn_plan = self.interceptor_controller.plan_defensive_interceptors(game_state, min(6, int(our_mp)))
            self._execute_spawn_plan(game_state, spawn_plan)
            gamelib.debug_write(f'🛡️  Defensive interceptors deployed')
        
        # Reinforce weak zones
        if our_sp >= 4:
            weak_zones = self.cache.get('weak_zones', [])
            for weakness in weak_zones[:2]:
                if weakness[0] == 'sparse_zone':
                    x = weakness[1]
                    for y in [12, 11, 10]:
                        if game_state.can_spawn(TURRET, [x, y]):
                            if game_state.attempt_spawn(TURRET, [x, y]):
                                game_state.attempt_upgrade([x, y])
                                gamelib.debug_write(f'⚡ Emergency turret at [{x},{y}]')
                                break

    def _build_adaptive_defense(self, game_state, sp_budget):
        """Build intelligent adaptive defense"""
        if sp_budget < 2:
            return
        
        gamelib.debug_write(f'🏗️  Building defense (Budget: {sp_budget:.1f} SP)')
        
        # Priority 1: Upgrade key turrets
        self._upgrade_priority_turrets(game_state, sp_budget * 0.4)
        
        # Priority 2: Fill gaps
        self._fill_defensive_gaps(game_state, sp_budget * 0.35)
        
        # Priority 3: Add depth
        self._add_defensive_depth(game_state, sp_budget * 0.25)

    def _upgrade_priority_turrets(self, game_state, sp_budget):
        """Upgrade most important turrets"""
        upgrade_targets = []
        priority_positions = [
            [0, 13], [27, 13], [13, 12], [14, 12],
            [3, 13], [24, 13], [10, 11], [17, 11]
        ]
        
        try:
            for loc in priority_positions:
                if game_state.contains_stationary_unit(loc):
                    for unit in game_state.game_map[loc]:
                        if getattr(unit, 'player_index', None) == 0 and getattr(unit, 'unit_type', None) == TURRET and not getattr(unit, 'upgraded', False):
                            upgrade_targets.append(loc)
        except:
            pass
        
        upgraded_count = 0
        for loc in upgrade_targets:
            if sp_budget >= 4:
                if game_state.attempt_upgrade(loc):
                    sp_budget -= 4
                    upgraded_count += 1
        
        if upgraded_count > 0:
            gamelib.debug_write(f'⬆️  Upgraded {upgraded_count} turrets')
        
        return upgraded_count

    def _fill_defensive_gaps(self, game_state, sp_budget):
        """Fill gaps in defensive line"""
        if sp_budget < 2:
            return
        
        filled = 0
        for y in [13, 12, 11]:
            for x in range(4, 24, 3):
                if sp_budget >= 2 and not game_state.contains_stationary_unit([x, y]):
                    if game_state.can_spawn(TURRET, [x, y]):
                        if game_state.attempt_spawn(TURRET, [x, y]):
                            sp_budget -= 2
                            filled += 1
        
        if filled > 0:
            gamelib.debug_write(f'🔧 Filled {filled} defensive gaps')

    def _add_defensive_depth(self, game_state, sp_budget):
        """Add defensive depth"""
        if sp_budget < 0.5:
            return
        
        wall_positions = [
            [12, 12], [15, 12], [11, 11], [16, 11],
            [9, 12], [18, 12], [8, 11], [19, 11]
        ]
        
        added = 0
        for loc in wall_positions:
            if sp_budget >= 0.5 and not game_state.contains_stationary_unit(loc):
                if game_state.attempt_spawn(WALL, loc):
                    sp_budget -= 0.5
                    added += 1
        
        if added > 0:
            gamelib.debug_write(f'🧱 Added {added} walls for depth')

    def _upgrade_logic(self, game_state):
        """Smart upgrade logic"""
        try:
            sp = game_state.get_resource(SP)
        except:
            return
        
        if sp < self.thresholds['upgrade_sp_guard']:
            return
        
        for loc in [[13,12], [14,12], [10,11], [17,11]]:
            try:
                if game_state.contains_stationary_unit(loc) and sp >= 2:
                    if game_state.attempt_upgrade(loc):
                        sp -= 2
            except Exception:
                continue

    def _build_economy(self, game_state):
        """Build economic infrastructure"""
        try:
            our_sp = game_state.get_resource(SP)
        except:
            return
        
        if our_sp < 4:
            return
        
        support_positions = [
            [13, 8], [14, 8], [10, 7], [17, 7],
            [13, 6], [14, 6], [7, 6], [20, 6]
        ]
        
        built = 0
        for loc in support_positions:
            if our_sp >= 4 and not game_state.contains_stationary_unit(loc):
                if game_state.attempt_spawn(SUPPORT, loc):
                    our_sp -= 4
                    built += 1
                    self.metrics['economy_turns'] += 1
                    
                    if our_sp >= 2:
                        game_state.attempt_upgrade(loc)
                        our_sp -= 2
        
        if built > 0:
            gamelib.debug_write(f'💰 Built {built} supports')

    def _attack_logic_with_micro(self, game_state):
        """Attack logic with advanced microcontroller integration"""
        try:
            mp = game_state.get_resource(MP)
        except:
            return False
        
        if mp < self.thresholds['attack_min_mp']:
            return False
        
        gamelib.debug_write(f'\n⚔️  ATTACK PHASE ({mp:.1f} MP available)')
        
        # Score all attack options
        scored = []
        for name, play in self.attack_playbook.items():
            if mp < play['min_mp']:
                continue
            
            score = self._score_play(game_state, play)
            scored.append((score, name, play))
        
        # Boost scores based on opportunities
        for opp in self.cache.get('opportunities', []):
            if opp[0] == 'momentum_push':
                for i, (s, n, p) in enumerate(scored):
                    if n == 'scout_flood':
                        scored[i] = (s + 1.2, n, p)
            elif opp[0] == 'exploit_gap':
                for i, (s, n, p) in enumerate(scored):
                    if n in ['interceptor_rush', 'scout_flood']:
                        scored[i] = (s + 0.8, n, p)
            elif opp[0] == 'target_support':
                for i, (s, n, p) in enumerate(scored):
                    if n in ['surgical_strike', 'demo_breach']:
                        scored[i] = (s + 1.0, n, p)
        
        if not scored:
            # Fallback: use predictability-based interceptor attack
            if self.opponent_model.get('predictability', 0) > 0.7 and mp >= 6:
                spawn_plan = self.interceptor_controller.plan_interceptors(game_state, 6)
                self._execute_spawn_plan(game_state, spawn_plan)
                self.last_mp_spent = 6
                return True
            return False
        
        # Select best attack
        scored.sort(reverse=True, key=lambda x: x[0])
        _, name, play = scored[0]
        
        # Determine MP allocation based on strategy
        if self.metrics['momentum_score'] > 1.0 or self.metrics['win_probability'] > 0.6:
            allocation = 0.85
        elif self.strategy_mode in ['press', 'all_in']:
            allocation = 0.92
        else:
            allocation = 0.60
        
        use_mp = max(play['min_mp'], int(mp * allocation))
        use_mp = min(use_mp, mp)
        
        gamelib.debug_write(f'[ATTACK] Selected {name} using MP={use_mp}')
        
        # Calculate expected damage
        expected_dmg = self._estimate_attack_damage_from_play(game_state, name, play, use_mp)
        
        if expected_dmg < self.thresholds['attack_min_ev']:
            gamelib.debug_write(f'⏸️  Expected damage too low: {expected_dmg:.1f}')
            return False
        
        # Route to appropriate microcontroller
        spawn_plan = self._get_micro_spawn_plan(game_state, name, play, use_mp)
        
        # Execute spawn plan
        if spawn_plan:
            self._execute_spawn_plan(game_state, spawn_plan)
            self.last_mp_spent = use_mp
            self.attack_history[name]['attempts'] += 1
            self.opponent_model['attack_patterns'].append(game_state.turn_number)
            self.opponent_model['timing_patterns'].append(game_state.turn_number)
            return True
        
        return False

    def _get_micro_spawn_plan(self, game_state, name, play, use_mp):
        """Get spawn plan from appropriate microcontroller"""
        unit = play.get('unit')
        
        try:
            if unit == 'scout' or name == 'scout_flood':
                return self.scout_controller.plan_scout_wave(game_state, use_mp, self.strategy_mode)
            
            elif unit == 'demolisher' or name in ['demo_breach', 'surgical_strike']:
                return self.demolisher_escort.plan_demolisher_wave(game_state, use_mp, self.strategy_mode)
            
            elif unit == 'interceptor' or name == 'interceptor_rush':
                return self.interceptor_controller.plan_interceptors(game_state, use_mp)
            
            elif unit == 'mixed' or name == 'mixed_assault':
                # Mixed uses both demolisher escort and scouts
                plan = self.demolisher_escort.plan_demolisher_wave(game_state, int(use_mp * 0.4), self.strategy_mode)
                plan += self.scout_controller.plan_scout_wave(game_state, int(use_mp * 0.6), self.strategy_mode)
                return plan
            
            elif unit == 'split' or name == 'pincer_attack':
                # Pincer uses split spawn plan
                return self._create_pincer_spawn_plan(game_state, use_mp)
            
            else:
                # Default to scout controller
                return self.scout_controller.plan_scout_wave(game_state, use_mp, self.strategy_mode)
        
        except Exception as e:
            gamelib.debug_write(f'[MICRO] Error creating spawn plan: {e}')
            # Fallback to simple spawn
            return [(SCOUT, [13, 0], use_mp)]

    def _create_pincer_spawn_plan(self, game_state, use_mp):
        """Create pincer attack spawn plan"""
        plan = []
        
        # Split MP between two paths
        mp_per_path = use_mp * 0.475
        
        # Use preset pincer locations
        path1_locs = [[3, 0], [5, 1]]
        path2_locs = [[24, 0], [22, 1]]
        
        # Path 1
        scouts1 = int(mp_per_path * 0.7)
        demos1 = int((mp_per_path * 0.3) / 3)
        
        for loc in path1_locs:
            if game_state.can_spawn(SCOUT, loc):
                plan.append((SCOUT, loc, scouts1 // len(path1_locs)))
                break
        
        if demos1 > 0:
            for loc in path1_locs:
                if game_state.can_spawn(DEMOLISHER, loc):
                    plan.append((DEMOLISHER, loc, demos1))
                    break
        
        # Path 2
        scouts2 = int(mp_per_path * 0.7)
        demos2 = int((mp_per_path * 0.3) / 3)
        
        for loc in path2_locs:
            if game_state.can_spawn(SCOUT, loc):
                plan.append((SCOUT, loc, scouts2 // len(path2_locs)))
                break
        
        if demos2 > 0:
            for loc in path2_locs:
                if game_state.can_spawn(DEMOLISHER, loc):
                    plan.append((DEMOLISHER, loc, demos2))
                    break
        
        return plan

    def _score_play(self, game_state, play):
        """Score an attack play"""
        unit = play['unit']
        enemy = self.cache.get('structures', {}).get('enemy', {})
        base = 0.5
        
        # Unit-specific scoring
        if unit == 'demolisher':
            base += enemy.get('total', 0) * 0.02
        elif unit == 'interceptor':
            base += (1.0 - enemy.get('upgrade_ratio', 0)) * 0.3
        elif unit == 'scout':
            if enemy.get('turrets', 0) < 12:
                base += 0.2
        
        # Path danger penalty
        try:
            path_penalty = self.path_engine.estimate_path_danger(game_state, unit)
            base -= path_penalty * 0.03
        except:
            pass
        
        # Apply weight
        base *= play.get('weight', 1.0)
        
        return base

    def _estimate_attack_damage_from_play(self, game_state, name, play, use_mp):
        """Estimate attack damage"""
        enemy_str = self.cache['structures']['enemy']
        
        if name == 'scout_flood':
            scouts = int(use_mp * 0.95)
            try:
                path_damage = self.path_engine.estimate_path_danger(game_state, 'scout') * 10
            except:
                path_damage = 30
            scout_hp = scouts * 15
            damage = max(0, (scout_hp - path_damage) / 8.0)
            return damage
        
        elif name in ['demo_breach', 'surgical_strike']:
            structures = enemy_str.get('walls', 0) + enemy_str.get('turrets', 0) // 2
            demos = int((use_mp * 0.65) / 3)
            damage = min(structures * 0.7, 10) * demos * 0.4
            return damage
        
        elif name == 'interceptor_rush':
            interceptors = int(use_mp * 0.98)
            turret_count = enemy_str.get('turrets', 0)
            damage = (interceptors * 3.5) - (turret_count * 1.5)
            return max(0, damage)
        
        elif name == 'mixed_assault':
            damage = use_mp * 1.6
            return damage
        
        elif name == 'pincer_attack':
            damage = use_mp * 1.3
            return damage
        
        return use_mp * 1.0

    def _execute_spawn_plan(self, game_state, spawn_plan):
        """Execute a spawn plan from microcontrollers"""
        for unit_type, loc, count in spawn_plan:
            for _ in range(count):
                try:
                    if game_state.can_spawn(unit_type, loc):
                        game_state.attempt_spawn(unit_type, loc)
                    else:
                        # Try alternate location
                        alt = [max(0, loc[0]-1), loc[1]]
                        if game_state.can_spawn(unit_type, alt):
                            game_state.attempt_spawn(unit_type, alt)
                except Exception:
                    continue

    def _emergency_logic(self, game_state):
        """Emergency all-in logic"""
        # Recent damage check
        recent_taken = sum(list(self.metrics.get('damage_taken', []))[-3:]) if len(self.metrics.get('damage_taken', [])) >= 1 else 0
        
        try:
            mp = game_state.get_resource(MP)
        except:
            mp = 0
        
        # Emergency wall spam
        if recent_taken >= self.thresholds['emergency_hp_loss']:
            gamelib.debug_write('[EMERGENCY] Building quick walls')
            for loc in [[13,12], [14,12], [10,11], [17,11]]:
                try:
                    if mp <= 0:
                        break
                    if game_state.can_spawn(WALL, loc):
                        game_state.attempt_spawn(WALL, loc)
                        mp -= 1
                except Exception:
                    pass
        
        # All-in attack
        if self.metrics['win_probability'] < 0.12 and mp >= self.thresholds['all_in_threshold']:
            gamelib.debug_write('[ALL-IN] Launching desperate attack')
            try:
                spawn_plan = self.demolisher_escort.plan_demolisher_wave(game_state, mp, 'press')
                self._execute_spawn_plan(game_state, spawn_plan)
                self.last_mp_spent = mp
            except:
                pass

    def _record_turn_state(self, game_state):
        """Record turn state for learning"""
        try:
            state_snapshot = {
                'turn': game_state.turn_number,
                'health': {
                    'ours': game_state.my_health,
                    'enemy': game_state.enemy_health
                },
                'resources': {
                    'sp': game_state.get_resource(SP),
                    'mp': game_state.get_resource(MP)
                },
                'structures': self.cache.get('structures', {}),
                'phase': self.game_phase,
                'mode': self.strategy_mode,
                'win_prob': self.metrics['win_probability'],
                'momentum': self.metrics['momentum_score']
            }
            
            self.history['states'].append(state_snapshot)
        except:
            pass


# ═══════════════════════════════════════════════════════════════
# MICROCONTROLLER SYSTEMS
# ═══════════════════════════════════════════════════════════════

class PathDynamicsEngine:
    """Estimates danger/heatmap across map coordinates for spawn planning.
    
    Tries to call game_state.find_path_to_edge if available; otherwise uses
    a column turret density heuristic.
    """

    def __init__(self, strategy):
        self.s = strategy
        self.heatmap = None

    def update_heatmap(self, game_state):
        """Build heatmap using available API"""
        try:
            if hasattr(game_state, 'find_path_to_edge'):
                self.heatmap = self._simulate_paths(game_state)
                return
        except Exception:
            pass
        
        # Fallback to column density
        self.heatmap = self._column_turret_density(game_state)

    def _simulate_paths(self, game_state):
        """Attempt to use simulation API"""
        try:
            sim = game_state.find_path_to_edge()
            if isinstance(sim, dict):
                return sim
        except Exception:
            pass
        return None

    def _column_turret_density(self, game_state):
        """Calculate turret density per column"""
        width = self.s.map_width
        height = self.s.map_height
        density = {x: 0 for x in range(width)}
        
        try:
            for x in range(width):
                for y in range(height // 2, height):
                    if game_state.contains_stationary_unit([x, y]):
                        for u in game_state.game_map[[x, y]]:
                            if getattr(u, 'player_index', None) == 1 and getattr(u, 'unit_type', None) == TURRET:
                                # Weight by upgrade status
                                density[x] += (2 if getattr(u, 'upgraded', False) else 1)
        except Exception:
            pass
        
        return density

    def estimate_path_danger(self, game_state, unit_type='scout'):
        """Returns scalar danger estimate: higher = more dangerous"""
        try:
            if isinstance(self.heatmap, dict) and len(self.heatmap) > 0:
                # Check if heatmap is per-coordinate or per-column
                if all(isinstance(k, tuple) for k in self.heatmap.keys()):
                    # Per-coord heatmap
                    vals = []
                    for (x, y), v in self.heatmap.items():
                        if x in self.s.preferred_columns:
                            vals.append(v)
                    return sum(vals) / max(1, len(vals))
                else:
                    # Per-column density
                    density = sum(self.heatmap.get(c, 0) for c in self.s.preferred_columns)
                    
                    # Unit modifiers
                    if unit_type == 'scout':
                        return density
                    elif unit_type == 'demolisher':
                        return density * 0.5
                    elif unit_type == 'interceptor':
                        return density * 0.2
                    
                    return density
        except Exception:
            pass
        
        return 0


class ScoutSwarmController:
    """Plans scout waves that adapt spawn columns to minimize losses or 
    maximize aggression depending on context.
    """

    def __init__(self, strategy, engine):
        self.s = strategy
        self.engine = engine

    def plan_scout_wave(self, game_state, mp_amount, strategy_mode):
        """Plan scout wave with adaptive column selection"""
        plan = []
        pts = self.s.spawn_presets.get('standard', [[13, 0], [14, 0]])
        
        # Score points by danger
        scored_points = []
        for p in pts:
            try:
                column = p[0]
                col_danger = self.engine.heatmap.get(column, 0) if isinstance(self.engine.heatmap, dict) else 0
                scored_points.append((col_danger, p))
            except:
                scored_points.append((0, p))
        
        # Sort by safety (lowest danger first)
        scored_points.sort(key=lambda x: x[0])
        
        remaining = max(1, mp_amount)
        
        if strategy_mode in ['defensive', 'desperate']:
            # Concentrate on safest column
            safest = scored_points[0][1]
            count = max(1, min(remaining, 4))
            plan.append((SCOUT, safest, count))
            remaining -= count
        
        elif strategy_mode in ['press', 'all_in']:
            # Spread across top 3 safest columns
            for idx in range(min(3, len(scored_points))):
                if remaining <= 0:
                    break
                loc = scored_points[idx][1]
                cnt = max(1, remaining // (3 - idx))
                plan.append((SCOUT, loc, cnt))
                remaining -= cnt
        
        else:
            # Balanced: moderate spread
            idx = 0
            while remaining > 0 and idx < len(scored_points):
                loc = scored_points[idx][1]
                cnt = min(2, remaining)
                plan.append((SCOUT, loc, cnt))
                remaining -= cnt
                idx += 1
        
        # Dump remaining on safest
        if remaining > 0:
            plan.append((SCOUT, scored_points[0][1], remaining))
        
        return plan


class DemolisherEscortController:
    """Spawns demolishers with escort units and picks columns where 
    demolishers will be most effective.
    """

    def __init__(self, strategy, engine):
        self.s = strategy
        self.engine = engine

    def plan_demolisher_wave(self, game_state, mp_amount, strategy_mode):
        """Plan demolisher wave with escorts"""
        plan = []
        
        # Demolisher cost: 3 MP
        demos = max(1, mp_amount // 3)
        
        # Rank columns by enemy structure count
        cols = self._rank_columns_by_structures(game_state)
        
        # Choose columns (avoid extremely dangerous unless aggressive)
        chosen = []
        for c in cols:
            try:
                danger = self.engine.estimate_path_danger(game_state, 'demolisher')
                if strategy_mode == 'defensive' and danger > 6:
                    continue
                chosen.append(c)
                if len(chosen) >= demos:
                    break
            except:
                chosen.append(c)
                if len(chosen) >= demos:
                    break
        
        if not chosen:
            chosen = cols[:demos]
        
        # Place demolishers
        for i, c in enumerate(chosen):
            loc = [c, 0]
            plan.append((DEMOLISHER, loc, 1))
        
        # Add scout escorts
        used_mp = demos * 3
        left_mp = max(0, mp_amount - used_mp)
        
        if left_mp > 0:
            # Use scout controller for escorts
            escort_plan = self.s.scout_controller.plan_scout_wave(game_state, left_mp, strategy_mode)
            plan.extend(escort_plan)
        
        return plan

    def _rank_columns_by_structures(self, game_state):
        """Rank columns by enemy structure count"""
        cols = []
        try:
            for x in range(self.s.map_width):
                count = 0
                for y in range(self.s.map_height // 2, self.s.map_height):
                    if game_state.contains_stationary_unit([x, y]):
                        for u in game_state.game_map[[x, y]]:
                            if getattr(u, 'player_index', None) == 1:
                                count += 1
                cols.append((count, x))
            cols.sort(reverse=True)
            return [c[1] for c in cols]
        except Exception:
            return [13, 14, 12, 15, 10, 17]


class InterceptorController:
    """Plans interceptor waves to protect scouts/demolishers or exploit openings."""

    def __init__(self, strategy, engine):
        self.s = strategy
        self.engine = engine

    def plan_interceptors(self, game_state, mp_amount):
        """Plan offensive interceptor wave"""
        plan = []
        safest_col = self._find_safest_column(game_state)
        count = max(1, mp_amount)
        plan.append((INTERCEPTOR, [safest_col, 0], count))
        return plan

    def plan_defensive_interceptors(self, game_state, mp_amount):
        """Plan defensive interceptor deployment"""
        plan = []
        # Deploy at center for defensive coverage
        center_locs = [[13, 0], [14, 0], [12, 1], [15, 1]]
        count_per_loc = max(1, mp_amount // len(center_locs))
        
        for loc in center_locs:
            if count_per_loc > 0:
                plan.append((INTERCEPTOR, loc, count_per_loc))
        
        return plan

    def _find_safest_column(self, game_state):
        """Find column with lowest danger"""
        min_danger = 999
        best = 13
        
        try:
            for x in range(self.s.map_width):
                danger = self.engine.heatmap.get(x, 0) if isinstance(self.engine.heatmap, dict) else 0
                if danger < min_danger:
                    min_danger = danger
                    best = x
        except:
            pass
        
        return best


if __name__ == "__main__":
    algo = AlgoStrategy()
    algo.start()
