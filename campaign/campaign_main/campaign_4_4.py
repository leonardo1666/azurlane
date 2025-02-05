from campaign.campaign_main.campaign_4_1 import Config as Config41
from module.campaign.campaign_base import CampaignBase
from module.logger import logger
from module.map.map_base import CampaignMap
from module.map.map_grids import RoadGrids, SelectedGrids

MAP = CampaignMap('4-4')
MAP.shape = 'H6'
MAP.camera_data = ['D2', 'D4']
MAP.camera_data_spawn_point = ['E2', 'E4']
MAP.map_data = """
    ++ ++ MB ME SP -- ++ ++
    ++ ++ ME __ ME ME ++ ++
    ++ ++ -- ME -- -- -- SP
    ++ ++ -- ME ++ ME -- --
    ++ ++ ME -- ++ -- ME --
    MB ME -- ME -- ME -- SP
"""
MAP.weight_data = """
    50 50 10 20 50 50 50 50
    50 50 10 20 50 50 50 50
    50 50 10 20 50 50 50 50
    50 50 10 20 50 50 50 50
    50 50 10 20 50 50 50 50
    10 10 10 20 50 50 50 50
"""
MAP.spawn_data = [
    {'battle': 0, 'enemy': 3},
    {'battle': 1, 'enemy': 1},
    {'battle': 2, 'enemy': 2},
    {'battle': 3, 'enemy': 1},
    {'battle': 4, 'enemy': 2, 'boss': 1},
]
A1, B1, C1, D1, E1, F1, G1, H1, \
A2, B2, C2, D2, E2, F2, G2, H2, \
A3, B3, C3, D3, E3, F3, G3, H3, \
A4, B4, C4, D4, E4, F4, G4, H4, \
A5, B5, C5, D5, E5, F5, G5, H5, \
A6, B6, C6, D6, E6, F6, G6, H6, \
    = MAP.flatten()

road_main = RoadGrids([B6, [C4, D6], [C5, D4], [D3, C2], [C2, D1]])


class Config(Config41):
    MAP_MYSTERY_HAS_CARRIER = False


class Campaign(CampaignBase):
    MAP = MAP
    MAP_AMBUSH_OVERLAY_TRANSPARENCY_THRESHOLD = 0.3
    MAP_AIR_RAID_OVERLAY_TRANSPARENCY_THRESHOLD = 0.25
    MAP_ENEMY_SEARCHING_OVERLAY_TRANSPARENCY_THRESHOLD = 0.65

    def battle_0(self):
        if self.clear_roadblocks([road_main]):
            return True
        if self.clear_potential_roadblocks([road_main]):
            return True

        return self.battle_default()

    def battle_4(self):
        boss = self.map.select(is_boss=True)
        if boss:
            if not self.check_accessibility(boss[0], fleet='boss'):
                if self.clear_roadblocks([road_main]):
                    return True
                if self.clear_potential_roadblocks([road_main]):
                    return True

        return self.fleet_boss.clear_boss()
