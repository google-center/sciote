######################
# DEFAULT PARAMETERS #
######################

# имя файла по умолчанию
FILENAME = 'data/chat.txt'

# коэффицент training/testing data
QUOTIENT = 0.5

# размер словаря (в словах)
DICT_SIZE = 20000

# лимит длины сообщения
LEN_LIMIT = 700

# количество пар блоков sepCNN и блоков пула
BLOCKS = 5

# размер конволюционного окна
KERN_SIZE = 4

# выходное разрешение скрытых слоёв
OUT_DIM = 50

# фактор уменьшения входа на слое MaxPooling
POOL_SIZE = 2

#
CONFIG_FOLDER = 'configs/'