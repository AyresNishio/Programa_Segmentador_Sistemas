import numpy as np

from Rede.Rede import *
from Rede.funcObservabilidade import*
from Rede.funcPlanoMed import *

num_barras = 300

rede = Rede(300,369)


rede.plano_med = complementar_plano_med(rede,5)

rede.plano_med = remove_medidas_desativaddas(rede)

salva_Caso(rede)
print()