# Módulo que define a estrutura de um nó da árvore AVL.
# Cada nó armazena uma palavra, as linhas onde ela aparece e os ponteiros para os filhos.

class No:    
    def __init__(self, palavra, linha):
        # Inicializa um novo nó da árvore.
        # Tem como parâmetro a palavra a ser armazenada e o número da linha

        self.palavra = palavra.lower()  # Armazena em minúsculas
        self.linhas = [linha]  # Lista com a primeira linha
        self.esquerda = None
        self.direita = None
        self.altura = 0  # Novo nó começa com altura 0

    def adicionar_linha(self, linha):
        # Adiciona uma nova linha à lista caso ela ainda não exista
        if linha not in self.linhas:
            self.linhas.append(linha)

    def remover_linha(self, linha):
        # Remove uma linha específica da lista
        # Retorna (encontrou, ficou_vazia)
        if linha in self.linhas:
            self.linhas.remove(linha)
            return True, len(self.linhas) == 0
        return False, False
    
    def __str__(self):
        # Formata a saida do nó como string
        # Ordena a lista com os números das linhas
        # Transforma todos os elementos em str
        # Formata a saida do nó como string sem modificar a lista original - usando list comprehension
        linhas_str = ','.join(str(l) for l in sorted(self.linhas)) 
        return f"{self.palavra} {linhas_str}" # Formatação: "palavra x, y, z"