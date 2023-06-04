
import Defines as g
from enemy.EnemyCenter import *


MARGIN = EnemyCenter.MARGIN
E_U = EnemyCenter.ENE_U
E_0 = EnemyCenter.ENE_E

Stage01_Tbl = [
    # State Info
    [EnemyCenter.STAGE_INFO, "STAGE 01"],
    
    # Enemy Start Position
    # (START_POS, stx, sty)
    (EnemyCenter.START_POS, 0, -32),
    (EnemyCenter.START_POS, 800, -32),
    
    # Enemy Offset
    # (KindOfEnemy, stNo, ofx, ofy)
    (E_U, 0, MARGIN * 0-2, MARGIN * -2),
    (E_U, 1, MARGIN * -1-2, MARGIN * -2), (E_U, 0, MARGIN * 1-2, MARGIN * -2),
    (E_U, 1, MARGIN * -2-2, MARGIN * -2), (E_U, 0, MARGIN * 2-2, MARGIN * -2),
    (E_U, 1, MARGIN * -3-2, MARGIN * -2), (E_U, 0, MARGIN * 3-2, MARGIN * -2),
    (E_U, 1, MARGIN * -4-2, MARGIN * -2), (E_U, 0, MARGIN * 4-2, MARGIN * -2),
    (E_U, 1, MARGIN * -5-2, MARGIN * -2), (E_U, 0, MARGIN * 5-2, MARGIN * -2),
    (E_U, 1, MARGIN * -6-2, MARGIN * -2), (E_U, 0, MARGIN * 6-2, MARGIN * -2),
    
    (E_0, 0, MARGIN * 0, MARGIN * -1),
    (E_0, 1, MARGIN * -1, MARGIN * -1), (E_0, 0, MARGIN * 1, MARGIN * -1),
    (E_0, 1, MARGIN * -2, MARGIN * -1), (E_0, 0, MARGIN * 2, MARGIN * -1),
    (E_0, 1, MARGIN * -3, MARGIN * -1), (E_0, 0, MARGIN * 3, MARGIN * -1),
    (E_0, 1, MARGIN * -4, MARGIN * -1), (E_0, 0, MARGIN * 4, MARGIN * -1),
    (E_0, 1, MARGIN * -5, MARGIN * -1), (E_0, 0, MARGIN * 5, MARGIN * -1),
    (E_0, 1, MARGIN * -6, MARGIN * -1), (E_0, 0, MARGIN * 6, MARGIN * -1),
    (E_0, 1, MARGIN * -7, MARGIN * -1), (E_0, 0, MARGIN * 7, MARGIN * -1),
    
    (E_0, 0, MARGIN * 0, MARGIN * 0),
    (E_0, 1, MARGIN * -1, MARGIN * 0), (E_0, 0, MARGIN * 1, MARGIN * 0),
    (E_0, 1, MARGIN * -2, MARGIN * 0), (E_0, 0, MARGIN * 2, MARGIN * 0),
    (E_0, 1, MARGIN * -3, MARGIN * 0), (E_0, 0, MARGIN * 3, MARGIN * 0),
    (E_0, 1, MARGIN * -4, MARGIN * 0), (E_0, 0, MARGIN * 4, MARGIN * 0),
    (E_0, 1, MARGIN * -5, MARGIN * 0), (E_0, 0, MARGIN * 5, MARGIN * 0),
    (E_0, 1, MARGIN * -6, MARGIN * 0), (E_0, 0, MARGIN * 6, MARGIN * 0),
    (E_0, 1, MARGIN * -7, MARGIN * 0), (E_0, 0, MARGIN * 7, MARGIN * 0),
    (E_0, 1, MARGIN * -8, MARGIN * 0), (E_0, 0, MARGIN * 8, MARGIN * 0),

    (E_0, 0, MARGIN * 0, MARGIN * 1),
    (E_0, 1, MARGIN * -1, MARGIN * 1), (E_0, 0, MARGIN * 1, MARGIN * 1),
    (E_0, 1, MARGIN * -2, MARGIN * 1), (E_0, 0, MARGIN * 2, MARGIN * 1),
    (E_0, 1, MARGIN * -3, MARGIN * 1), (E_0, 0, MARGIN * 3, MARGIN * 1),
    (E_0, 1, MARGIN * -4, MARGIN * 1), (E_0, 0, MARGIN * 4, MARGIN * 1),
    (E_0, 1, MARGIN * -5, MARGIN * 1), (E_0, 0, MARGIN * 5, MARGIN * 1),
    (E_0, 1, MARGIN * -6, MARGIN * 1), (E_0, 0, MARGIN * 6, MARGIN * 1),
    (E_0, 1, MARGIN * -7, MARGIN * 1), (E_0, 0, MARGIN * 7, MARGIN * 1),
    (E_0, 1, MARGIN * -8, MARGIN * 1), (E_0, 0, MARGIN * 8, MARGIN * 1),
    
    (E_0, 0, MARGIN * 0, MARGIN * 2),
    (E_0, 1, MARGIN * -1, MARGIN * 2), (E_0, 0, MARGIN * 1, MARGIN * 2),
    (E_0, 1, MARGIN * -2, MARGIN * 2), (E_0, 0, MARGIN * 2, MARGIN * 2),
    (E_0, 1, MARGIN * -3, MARGIN * 2), (E_0, 0, MARGIN * 3, MARGIN * 2),
    (E_0, 1, MARGIN * -4, MARGIN * 2), (E_0, 0, MARGIN * 4, MARGIN * 2),
    (E_0, 1, MARGIN * -5, MARGIN * 2), (E_0, 0, MARGIN * 5, MARGIN * 2),
    (E_0, 1, MARGIN * -6, MARGIN * 2), (E_0, 0, MARGIN * 6, MARGIN * 2),
    (E_0, 1, MARGIN * -7, MARGIN * 2), (E_0, 0, MARGIN * 7, MARGIN * 2),
    (E_0, 1, MARGIN * -8, MARGIN * 2), (E_0, 0, MARGIN * 8, MARGIN * 2),
]

