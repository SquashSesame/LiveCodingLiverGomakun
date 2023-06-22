
import Defines as g
from enemy.EnemyCenter import *


MARGIN = EnemyCenter.MARGIN
E_U = EnemyCenter.ENE_U
E_0 = EnemyCenter.ENE_E

Stage03_Tbl = [
    # State Info
    [EnemyCenter.STAGE_INFO, "STAGE 03"],
    
    # Enemy Start Position
    # (START_POS, stx, sty)
    (EnemyCenter.START_POS, -32, 32),  # 0
    (EnemyCenter.START_POS, 832, 32),  # 1
    (EnemyCenter.START_POS, -32, 568),  # 2
    (EnemyCenter.START_POS, 832, 568),  # 3
    
    # Enemy Offset
    # (KindOfEnemy, stNo, ofx, ofy)
    (E_U, 3, MARGIN * -2-2, MARGIN * -2), (E_U, 2, MARGIN * 2-2, MARGIN * -2),
    (E_U, 1, MARGIN * -3-2, MARGIN * 2), (E_U, 0, MARGIN * 3-2, MARGIN * 2),

    (E_U, 3, MARGIN * -3-2, MARGIN * -2), (E_U, 2, MARGIN * 3-2, MARGIN * -2),
    (E_U, 1, MARGIN * -4-2, MARGIN * 2), (E_U, 0, MARGIN * 4-2, MARGIN * 2),

    (E_U, 3, MARGIN * -4-2, MARGIN * -2), (E_U, 2, MARGIN * 4-2, MARGIN * -2),
    (E_U, 1, MARGIN * -5-2, MARGIN * 2), (E_U, 0, MARGIN * 5-2, MARGIN * 2),

    (E_U, 3, MARGIN * -5-2, MARGIN * -2), (E_U, 2, MARGIN * 5-2, MARGIN * -2),
    (E_U, 1, MARGIN * -6-2, MARGIN * 2), (E_U, 0, MARGIN * 6-2, MARGIN * 2),

    (E_U, 3, MARGIN * -2.5-2, MARGIN * -1), (E_U, 2, MARGIN * 2.5-2, MARGIN * -1),
    (E_U, 1, MARGIN * -2.5-2, MARGIN * 3), (E_U, 0, MARGIN * 2.5-2, MARGIN * 3),

    (E_U, 3, MARGIN * -3.5-2, MARGIN * -1), (E_U, 2, MARGIN * 3.5-2, MARGIN * -1),
    (E_U, 1, MARGIN * -3.5-2, MARGIN * 3), (E_U, 0, MARGIN * 3.5-2, MARGIN * 3),

    (E_U, 3, MARGIN * -4.5-2, MARGIN * -1), (E_U, 2, MARGIN * 4.5-2, MARGIN * -1),
    (E_U, 1, MARGIN * -4.5-2, MARGIN * 3), (E_U, 0, MARGIN * 4.5-2, MARGIN * 3),

    (E_U, 3, MARGIN * -5.5-2, MARGIN * -1), (E_U, 2, MARGIN * 5.5-2, MARGIN * -1),
    (E_U, 1, MARGIN * -5.5-2, MARGIN * 3), (E_U, 0, MARGIN * 5.5-2, MARGIN * 3),

    (E_U, 3, MARGIN * -3-2, MARGIN * 0), (E_U, 2, MARGIN * 3-2, MARGIN * 0),
    (E_U, 1, MARGIN * -2-2, MARGIN * 4), (E_U, 0, MARGIN * 2-2, MARGIN * 4),

    (E_U, 3, MARGIN * -4-2, MARGIN * 0), (E_U, 2, MARGIN * 4-2, MARGIN * 0),
    (E_U, 1, MARGIN * -3-2, MARGIN * 4), (E_U, 0, MARGIN * 3-2, MARGIN * 4),

    (E_U, 3, MARGIN * -5-2, MARGIN * 0), (E_U, 2, MARGIN * 5-2, MARGIN * 0),
    (E_U, 1, MARGIN * -4-2, MARGIN * 4), (E_U, 0, MARGIN * 4-2, MARGIN * 4),

    (E_U, 3, MARGIN * -6-2, MARGIN * 0), (E_U, 2, MARGIN * 6-2, MARGIN * 0),
    (E_U, 1, MARGIN * -5-2, MARGIN * 4), (E_U, 0, MARGIN * 5-2, MARGIN * 4),

    (E_U, 3, MARGIN * -3.5-2, MARGIN * 1), (E_U, 2, MARGIN * 3.5-2, MARGIN * 1),
    (E_U, 3, MARGIN * -4.5-2, MARGIN * 1), (E_U, 2, MARGIN * 4.5-2, MARGIN * 1),
    (E_U, 3, MARGIN * -5.5-2, MARGIN * 1), (E_U, 2, MARGIN * 5.5-2, MARGIN * 1),
    (E_U, 3, MARGIN * -6.5-2, MARGIN * 1), (E_U, 2, MARGIN * 6.5-2, MARGIN * 1),

]

