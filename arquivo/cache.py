
import numpy as np; # type: ignore
import matplotlib.pyplot as plt; # type: ignore


with open("referencia1.dat", 'r') as arquivo1:
    referencia1 = [int(linha.strip()) for linha in arquivo1]
with open("referencia2.dat", 'r') as arquivo2:
    referencia2 = [int(linha.strip()) for linha in arquivo2]

## definindo classe de variaveis cache

class Cache:
    def __init__(self, tam_cache_kb, tam_bloco_bit):
        self.tam_cache_kb = tam_cache_kb                        #tamanho da memori cache
        self.tam_bloco_bit = tam_bloco_bit                      #tamanho dos blocos de memoria
        self.blocos = tam_cache_kb * 1024 // tam_bloco_bit      #numero de blocos
        self.cache = {}

    def leitura(self, endereco):
        end_bloco = endereco // self.tam_bloco_bit              #endereço da memoria principal
        index_bloco = end_bloco % self.blocos                   #indice dos blocos
        if index_bloco in self.cache and self.cache[index_bloco] == end_bloco:
            return True
        else:
            self.cache[index_bloco] = end_bloco
            return False
    
# tipos da cache

def verifica_cache(cache, referencias):
    acertos = 0
    for endereco in referencias:
        if cache.leitura(endereco):
            acertos += 1
    return acertos / len(referencias) * 100

def cache_diretamente_mapeada(tam_blocos, tam_cache_kb, referencia1):
    acertos_direto = []
    print("Cache diretamente mapeada:")
    for tam_bloco in tam_blocos:
        cache_direto = Cache(tam_cache_kb, tam_bloco)
        acertos = verifica_cache(cache_direto, referencia1)
        acertos_direto.append(acertos)
        print(f"Taxa de acertos para bloco de {tam_bloco} palavras: {acertos:.2f}%")
    return acertos_direto

def cache_conjunto_2_vias(tam_blocos, tam_cache_kb, referencia2):
    acertos_assoc = []
    print("\nCache associativa em conjunto de 2 vias:")
    for tam_bloco in tam_blocos:
        cache_assoc = Cache(tam_cache_kb, tam_bloco * 2)
        acertos = verifica_cache(cache_assoc, referencia2)
        acertos_assoc.append(acertos)
        print(f"Taxa de acertos para bloco de {tam_bloco} words: {acertos:.2f}%")
    return acertos_assoc 



tam_blocos = [1, 2, 4, 8, 16]
tam_cache_kb = 1

## Simulação da cache diretamente mapeada
acertos_direto = cache_diretamente_mapeada(tam_blocos, tam_cache_kb, referencia1)

## Simulação cache associativa em conjunto de 2 vias
acertos_assoc = cache_conjunto_2_vias(tam_blocos, tam_cache_kb, referencia2)


plt.figure(figsize=(10, 6))

## Linha para Cache Diretamente Mapeada
plt.plot(tam_blocos, acertos_direto, marker='o', label='Cache Diretamente Mapeada')
for i, txt in enumerate(acertos_direto):
    plt.annotate(f'{txt:.2f}%', (tam_blocos[i], acertos_direto[i]), textcoords="offset points", xytext=(0,5), ha='center')

## Linha para Cache Associativa em Conjunto de 2 Vias
plt.plot(tam_blocos, acertos_assoc, marker='s', label='Cache Associativa em Conjunto de 2 Vias')
for i, txt in enumerate(acertos_assoc):
    plt.annotate(f'{txt:.2f}%', (tam_blocos[i], acertos_assoc[i]), textcoords="offset points", xytext=(0,5), ha='center')

plt.xlabel('Tamanho do Bloco (words)')
plt.ylabel('Taxa de Acertos (%)')
plt.title('Taxa de Acertos das Caches')
plt.xticks(2*tam_blocos)
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.show()
