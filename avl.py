# Módulo que implementa a árvore AVL para o índice remissivo
# Contém todas as operações de inserção, busca, remoção e funções auxiliares

from no import No

class ArvoreAVL:
    # Classe que implementa uma árvore AVL para índice remissivo

    def __init__(self):
        # Inicializa uma árvore AVL vazia.
        self.__raiz = None
        self.total_rotacoes = 0 # Contador de rotações realizadas
        self.palavras_descartadas = 0 # Contador de palavras repetidas
    
    def __altura(self, no):
        # Retorna a altura de um nó
        # Recebe a altura do nó e retorna -1 caso seja nulo
        if no is None:
            return -1
        return no.altura
    
    def __fator_balanceamento(self, no):
        # Calcula o fator de balanceamento de um nó
        # Fator de balanceamento = altura da subárvore esquerda - altura da subárvore direita
        if no is None:
            return 0
        return self.__altura(no.esquerda) - self.__altura(no.direita)
    
    def __atualizar_altura(self, no):
        # Atualiza a altura de um nó baseado nas alturas de seus filhos
        if no is not None:
            altura_esquerda = self.__altura(no.esquerda)
            altura_direita = self.__altura(no.direita)
            no.altura = 1 + max(altura_esquerda, altura_direita)
    
    def __rotacao_LL(self, A):
        # Recebe o nó desbalanceado
        # Realiza uma rotação simples à direita
        B = A.esquerda
        A.esquerda = B.direita
        B.direita = A
        self.__atualizar_altura(A)
        self.__atualizar_altura(B)
        return B

    def __rotacao_RR(self, A):
        # Recebe o nó desbalanceado
        # Realiza uma rotação simples à esquerda
        B = A.direita
        A.direita = B.esquerda
        B.esquerda = A
        self.__atualizar_altura(A)
        self.__atualizar_altura(B)
        return B

    def __rotacao_LR(self, A):
        # Recebe o nó desbalanceado
        # Realiza uma rotação simples à esquerda no nó esquerdo do nó desbalanceado
        # Realiza uma rotação simples à direita no nó desbalanceado
        A.esquerda = self.__rotacao_RR(A.esquerda)
        A = self.__rotacao_LL(A)
        return A

    def __rotacao_RL(self, A):
        # Recebe o nó desbalanceado
        # Realiza uma rotação simples à direita no nó direito do nó desbalanceado
        # Realiza uma rotação simples à esquerda no nó desbalanceado
        A.direita = self.__rotacao_LL(A.direita)
        A = self.__rotacao_RR(A)
        return A
    
    def inserir(self, palavra, linha):
        # Recebe o nó desbalanceado
        # Insere uma palavra e sua linha na árvore
        # A função recebe a palavra a ser inserida e o número da linha onde a palavra aparece
        self.__raiz = self.__inserir_recursivo(self.__raiz, palavra.lower(), linha)
    
    def __inserir_recursivo(self, no, palavra, linha):
        # Função recursiva para inserir um nó na árvore
        # A função recebe o nó atual da recursão, a palavra a ser inserida e o número da linha e retorna a raiz da subárvore atualizada
        
        # Caso base: encontrou a posição para inserir
        if no is None:
            return No(palavra, linha)
        
        # Se a palavra já existe, apenas adiciona a linha e aumenta 1 no contador de palavras descartadas
        if palavra == no.palavra:
            no.adicionar_linha(linha)
            self.palavras_descartadas += 1
            return no
        
        # Caminha pela árvore
        if palavra < no.palavra:
            no.esquerda = self.__inserir_recursivo(no.esquerda, palavra, linha)
        else:
            no.direita = self.__inserir_recursivo(no.direita, palavra, linha)
        
        # Atualiza a altura do nó atual
        self.__atualizar_altura(no)
        
        # Verifica o balanceamento e realiza rotações se necessário
        balanceamento = self.__fator_balanceamento(no)
        
        # Caso Esquerda-Esquerda
        if balanceamento > 1 and palavra < no.esquerda.palavra:
            self.total_rotacoes += 1
            return self.__rotacao_LL(no)
        
        # Caso Direita-Direita
        if balanceamento < -1 and palavra > no.direita.palavra:
            self.total_rotacoes += 1
            return self.__rotacao_RR(no)
        
        # Caso Esquerda-Direita
        if balanceamento > 1 and palavra > no.esquerda.palavra:
            self.total_rotacoes += 1
            return self.__rotacao_LR(no)
        
        # Caso Direita-Esquerda
        if balanceamento < -1 and palavra < no.direita.palavra:
            self.total_rotacoes += 1
            return self.__rotacao_RL(no)
        
        return no
    
    def buscar(self, palavra):
        # Busca uma palavra a ser buscada na árvore
        # Recebe a palavra a ser procurada e chama uma função recursiva 
        return self.__buscar_recursivo(self.__raiz, palavra.lower())
    
    def __buscar_recursivo(self, no, palavra):
        # Função recursiva para buscar uma palavra
        # Recebe o nó atual da recursão e a palavra a ser procurada

        # Caso base 1: nó vazio 
        if no is None:
            return False

        # Caso base 2: palavra encontrada
        if no.palavra == palavra:
            return no
        
        # Caminha pela árvore
        if palavra < no.palavra:
            return self.__buscar_recursivo(no.esquerda, palavra)
        else:
            return self.__buscar_recursivo(no.direita, palavra)
    
    def buscar_por_prefixo(self, prefixo):
        # Busca todas as palavras que começam com um determinado prefixo.
        # Recebe o prefixo a ser procurado e chama função recursiva

        resultado = []
        self.__buscar_prefixo_recursivo(self.__raiz, prefixo.lower(), resultado)
        # Retorna a lista de prefixos em ordem alfabética
        return sorted(resultado)
    
    def __buscar_prefixo_recursivo(self, no, prefixo, resultado):
        # Função recursiva para buscar palavras por prefixo.
        # Recebe o nó atual da recursão, o prefixo procurado e a lista a ser adicionado o resultado
        if no is None:
            return
        
        # Verifica se a palavra atual começa com o prefixo
        if no.palavra[:len(prefixo)] == prefixo:
            resultado.append(no.palavra)
        
        # Se o prefixo pode estar à esquerda, busca lá
        if prefixo < no.palavra:
            self.__buscar_prefixo_recursivo(no.esquerda, prefixo, resultado)
        
        # Se o prefixo pode estar à direita, busca lá
        if prefixo >= no.palavra[:len(prefixo)]:
            self.__buscar_prefixo_recursivo(no.direita, prefixo, resultado)

    def __contar_elementos(self, no):
        # Conta o número de elementos de uma subárvore
        # Recebe a raiz da subárvore
        if no is None:
            return 0
        return 1 + self.__contar_elementos(no.esquerda) + self.__contar_elementos(no.direita)

    def buscar_com_medidor_equilibrio(self, palavra):
        # Busca uma palavra e retorna um medidor de equilibrio
        # Recebe a palavra a ser buscada
        no = self.buscar(palavra)
        if not no:
            return -1
        
        # Conta elementos nas subárvores
        elementos_esquerda = self.__contar_elementos(no.esquerda)
        elementos_direita = self.__contar_elementos(no.direita)
        
        me = elementos_esquerda - elementos_direita
        
        if me == 0:
            return 0
        else:
            print(f"Medidor de Equilíbrio (ME) para '{palavra}': {me}")
            return 1
    
    def palavra_mais_frequente(self):
        # Encontra a palavra que aparece em mais linhas diferente
        # Retorna uma lista: [palavra, número de linhas] caso a árvore não estiver vazia

        # Caso a árvore estiver vazia, retorna a tupla: (None, 0)
        if self.__raiz is None:
            return None, 0
        
        max_palavra = [None, 0]  # [palavra, quantidade de linhas]
        self.__encontrar_mais_frequente(self.__raiz, max_palavra)
        return max_palavra
    
    def __encontrar_mais_frequente(self, no, max_palavra):
        # Função recursiva para encontrar a palavra mais frequente
        if no is None:
            return
        
        # Verifica se este nó tem mais linhas que o máximo atual
        num_linhas = len(no.linhas)
        if num_linhas > max_palavra[1]:
            max_palavra[0] = no.palavra
            max_palavra[1] = num_linhas
        
        # Continua a busca nas subárvores
        self.__encontrar_mais_frequente(no.esquerda, max_palavra)
        self.__encontrar_mais_frequente(no.direita, max_palavra)

    def remover(self, palavra, linha=None):
        # Remove uma palavra ou uma linha específica de uma palavra
        # Recebe a palavra a ser removida e uma linha (opcional) a ser removida
        # Retorna True se for bem sucedido, False se contrário

        palavra = palavra.lower()
        resultado = [False]
        self.__raiz = self.__remover_recursivo(self.__raiz, palavra, linha, resultado)
        return resultado[0]

    def __remover_recursivo(self, no, palavra, linha, resultado):
        # Função recursiva para remover um nó ou linha
        # Recebe o nó atual da recursão, a paavra a ser removida, a linha (se não tiver, None) e o resultado(booleano)
        if no is None:
            return no
        
        # Navega até encontrar a palavra
        if palavra < no.palavra:
            no.esquerda = self.__remover_recursivo(no.esquerda, palavra, linha, resultado)
        elif palavra > no.palavra:
            no.direita = self.__remover_recursivo(no.direita, palavra, linha, resultado)
        else:
            # Palavra encontrada
            if linha is not None:
                # Remove apenas a linha específica
                encontrou, ficou_vazia = no.remover_linha(linha)
                if not encontrou:
                    return no  # linha não existia, não marca sucesso
                if not ficou_vazia:
                    resultado[0] = True
                    return no
                
            # Se ficou vazia ou remoção total, continua para remover o nó
            resultado[0] = True
            
            # Caso 1: Nó sem filhos ou com apenas um filho
            if no.esquerda is None:
                return no.direita
            elif no.direita is None:
                return no.esquerda
            
            # Caso 2: Nó com dois filhos
            # Encontra o sucessor (menor valor da subárvore direita)
            sucessor = self.__encontrar_minimo(no.direita)
            
            # Copia os dados do sucessor para este nó
            no.palavra = sucessor.palavra
            no.linhas = sucessor.linhas.copy()
            
            # Remove o sucessor
            no.direita = self.__remover_recursivo(no.direita, sucessor.palavra, None, resultado)
        
        if no is None:
            return no
        
        # Atualiza altura e balanceia
        self.__atualizar_altura(no)
        balanceamento = self.__fator_balanceamento(no)
        
        # Rebalanceia se necessário
        # Caso Esquerda-Esquerda
        if balanceamento > 1 and self.__fator_balanceamento(no.esquerda) >= 0:
            self.total_rotacoes += 1
            return self.__rotacao_LL(no)
        
        # Caso Esquerda-Direita
        if balanceamento > 1 and self.__fator_balanceamento(no.esquerda) < 0:
            self.total_rotacoes += 1
            return self.__rotacao_LR(no)
        
        # Caso Direita-Direita
        if balanceamento < -1 and self.__fator_balanceamento(no.direita) <= 0:
            self.total_rotacoes += 1
            return self.__rotacao_RR(no)
        
        # Caso Direita-Esquerda
        if balanceamento < -1 and self.__fator_balanceamento(no.direita) > 0:
            self.total_rotacoes += 1
            return self.__rotacao_RL(no)
        
        return no
        
        # Atualiza altura e balanceia
        self.__atualizar_altura(no)
        balanceamento = self.__fator_balanceamento(no)
        
        # Rebalanceia se necessário
        # Caso Esquerda-Esquerda
        if balanceamento > 1 and self.__fator_balanceamento(no.esquerda) >= 0:
            self.total_rotacoes += 1
            return self.__rotacao_LL(no)
        
        # Caso Esquerda-Direita
        if balanceamento > 1 and self.__fator_balanceamento(no.esquerda) < 0:
            self.total_rotacoes += 1
            return self.__rotacao_LR(no)
        
        # Caso Direita-Direita
        if balanceamento < -1 and self.__fator_balanceamento(no.direita) <= 0:
            self.total_rotacoes += 1
            return self.__rotacao_RR(no)
        
        # Caso Direita-Esquerda
        if balanceamento < -1 and self.__fator_balanceamento(no.direita) > 0:
            self.total_rotacoes += 1
            return self.__rotacao_RL(no)
        
        return no
    
    def __encontrar_minimo(self, no):
        # Encontra o nó com menor valor em uma subárvore
        atual = no
        while atual.esquerda is not None:
            atual = atual.esquerda
        return atual
    
    def imprimir_indice(self):
        # Imprime o índice remissivo completo em ordem alfabética
        # Retorna uma lista de string
        resultado = []
        self.__percorrer_em_ordem(self.__raiz, resultado)
        return resultado
    
    def __percorrer_em_ordem(self, no, resultado):
        # Percorre a árvore no percurso "em-ordem"
        # Recebe uma lista para armazenar o resultado
        if no is not None:
            self.__percorrer_em_ordem(no.esquerda, resultado)
            resultado.append(str(no))
            self.__percorrer_em_ordem(no.direita, resultado)
    
    def contar_palavras_total(self):
        # Conta o total de palavras no índice (inclui repetições em diferentes linhas)
        return self.__contar_palavras_recursivo(self.__raiz)
    
    def __contar_palavras_recursivo(self, no):
        # Conta recursivamente as palavras
        # Recebe o no atual da recursão
        if no is None:
            return 0
        
        # Conta as ocorrências desta palavra + as das subárvores
        total_linhas = len(no.linhas)
        return total_linhas + self.__contar_palavras_recursivo(no.esquerda) + self.__contar_palavras_recursivo(no.direita)
    
    def contar_palavras_distintas(self):
        # Conta o número de palavras distintas
        return self.__contar_elementos(self.__raiz)