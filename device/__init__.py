import collections

from . import MM32F0010
from . import MM32F0020
from . import MM32F0x40
from . import MM32F103
# from . import STM32F103
# from . import STM32F103_LS
# from . import STM32F405
# from . import STM32F405_LS
# from . import NUM480
# from . import MT7687

Devices = collections.OrderedDict([
    ('MM32F0010',    MM32F0010.MM32F0010),
    ('MM32F0020',    MM32F0020.MM32F0020),
    ('MM32F0040',    MM32F0x40.MM32F0040),
    ('MM32F0140',    MM32F0x40.MM32F0140),
    ('MM32F103C8',   MM32F103.MM32F103C8),
    ('MM32F103CB',   MM32F103.MM32F103CB),
    # ('STM32F103C8',    STM32F103.STM32F103C8),
    # ('STM32F103C8-LS', STM32F103_LS.STM32F103C8),
    # ('STM32F103RC',    STM32F103.STM32F103RC),
   	# ('STM32F103RC-LS', STM32F103_LS.STM32F103RC),
    # ('STM32F405RG',    STM32F405.STM32F405RG),
    # ('STM32F405RG-LS', STM32F405_LS.STM32F405RG),
    # ('NUM480',         NUM480.NUM480),
    # ('MT7687',         MT7687.MT7687),
])