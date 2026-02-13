# Índice Remissivo com Árvore AVL

Gestão da Informação
Projeto da disciplina de Estruturas de Dados 2 — UFU  
Alunos: Henrique Melo de Araújo e Murilo Rodrigues de Moura 
Professora: Maria Adriana Vidigal de Lima

---

## Introdução

### O problema

O trabalho pedia a criação de um índice remissivo para um documento de texto usando uma árvore binária de busca balanceada do tipo AVL. O documento usado foi o "Conto de Escola", de Machado de Assis, com 250 linhas.

Um índice remissivo é uma lista alfabética de todas as palavras do texto, com os números das linhas em que cada uma aparece — igual ao índice no final de um livro técnico. Por exemplo, a palavra `escola` aparece nas linhas 1, 2, 8, 9, 32, 37, 53, 55... e o índice precisa registrar tudo isso.

### Por que AVL?

A AVL foi a estrutura exigida, pois ela é uma árvore binária de busca que se balanceia automaticamente após cada inserção ou remoção, garantindo O(log n) nas operações principais. Além disso, um percurso em-ordem na árvore já entrega todas as palavras em ordem alfabética, sem precisar ordenar nada depois.

Se usássemos uma lista simples, a busca seria O(n). Com uma ABB comum sem balanceamento, no pior caso (palavras inseridas em ordem alfabética) a árvore viraria uma lista encadeada. A AVL evita isso mantendo a altura mínima através dos balanceamentos.

### Como funciona

O fluxo é direto:

1. Lê o arquivo linha por linha
2. Para cada palavra: remove pontuação, converte para minúsculas
3. Insere na AVL com o número da linha
   - Se a palavra já existe: só adiciona a linha à lista do nó
   - Se é nova: cria um nó novo e balanceia se necessário
4. Percurso em-ordem gera o índice em ordem alfabética

---

## Documentação do Código

### `no.py` — Classe `No`

Representa um nó da árvore. Cada nó guarda uma palavra e as linhas onde ela aparece.

```python
self.palavra  # ex: "escola"
self.linhas   # ex: [1, 2, 8, 9, 32, 37, 53, 55]
self.esquerda # filho esquerdo
self.direita  # filho direito
self.altura   # altura do nó (começa em 0)
```

A altura começa em `0` porque um nó folha (sem filhos) está a zero arestas de distância de si mesmo. Já a função `__altura()` retorna `-1` para `None`, o que faz a fórmula `1 + max(-1, -1) = 0` bater certinho para um nó folha.

**`__init__(self, palavra, linha)`**  
Cria o nó com a palavra em minúsculas e a primeira linha de ocorrência.

**`adicionar_linha(self, linha)`**  
Adiciona a linha à lista, mas verifica antes se ela já está lá, evitando duplicatas. Por exemplo, se a palavra `era` aparece duas vezes na linha 2, ela é registrada só uma vez.

**`remover_linha(self, linha)`**  
Remove uma linha da lista e retorna `True, True` se encontrou a palavra e a lista ficou vazia. Esse retorno é importante para a AVL saber se precisa remover o nó inteiro da árvore. 

**`__str__(self)`**  
Formata o nó para o índice. Saída: `escola 1,2,8,9,32,37,53,55`

---

### `avl.py` — Classe `ArvoreAVL`

Toda a lógica da árvore fica aqui.

---

#### Funções auxiliares

**`__altura(no)`**  
Retorna `-1` para `None` e `no.altura` para nós existentes. Esse `-1` é a convenção que permite calcular a altura de um nó folha corretamente: `1 + max(-1, -1) = 0`.

**`__fator_balanceamento(no)`**  
Calcula `altura(esquerda) - altura(direita)`. O resultado precisa estar entre `-1` e `1`. Se passar disso, a árvore está desbalanceada e precisa de rotação.

**`__atualizar_altura(no)`**  
Recalcula a altura do nó: `1 + max(altura_esq, altura_dir)`. Chamado sempre depois de inserções e remoções.

---

#### Rotações

Quando o fator de balanceamento de um nó passa de `1` ou fica abaixo de `-1`, uma rotação é feita para corrigir.

**`__rotacao_LL(A)`** — Rotação simples à direita. O filho esquerdo `B` sobe, e `A` desce para a direita de `B`.

```
    A                B
   /        →       / \
  B               C    A
 /
C
```

**`__rotacao_RR(A)`** — Rotação simples à esquerda. O filho direito `B` sobe, e `A` desce para a esquerda de `B`.

```
A                  B
 \        →       / \
  B               A   C
   \
    C
```

**`__rotacao_LR(A)`** — Rotação dupla. Faz uma RR no filho esquerdo e depois uma LL no nó `A`. Usada quando o desbalanceamento está no desvio esquerda-direita.

**`__rotacao_RL(A)`** — Rotação dupla. Faz uma LL no filho direito e depois uma RR no nó `A`. Usada quando o desbalanceamento está no desvio direita-esquerda.

---

#### Inserção

**`inserir(palavra, linha)`**  
Método público. Converte para minúsculas e chama a inserção recursiva.

**`__inserir_recursivo(no, palavra, linha)`**  
Percorre a árvore comparando palavras. Ao chegar num nó `None`, cria o nó novo. Se a palavra já existe, só adiciona a linha. Depois da inserção, atualiza a altura e verifica o balanceamento — aplicando a rotação adequada (LL, RR, LR ou RL) se necessário.

---

#### Busca

**`buscar(palavra)`**  
Busca exata. Retorna o nó se encontrar, ou `False` se não encontrar. Retorna `False` (e não `None`) para poder usar `if not no:` de forma mais natural no código.

**`buscar_por_prefixo(prefixo)`**  
Retorna lista ordenada com todas as palavras que começam com o prefixo. A busca pode ir para os dois lados da árvore porque palavras com o mesmo prefixo podem estar em subárvores diferentes — por exemplo, buscando `"es"`, tanto `"escola"` quanto `"escrita"` precisam ser encontradas, mas podem estar em lados opostos de algum nó intermediário.

**`buscar_com_medidor_equilibrio(palavra)`**  
Busca a palavra e calcula o Medidor de Equilíbrio (ME): `qtd_nós_esquerda - qtd_nós_direita`. Retorna `0` se equilibrado, `1` se não, ou `-1` se a palavra não existe.

---

#### Remoção

**`remover(palavra, linha=None)`**  
O parâmetro `linha` é opcional. Se `linha` for informado, remove só aquela ocorrência da palavra. Se não for informado (ou seja, `linha=None`), remove o nó inteiro com todas as suas linhas. Isso permite dois comportamentos distintos com a mesma função:

```python
arvore.remover("escola", 9)   # remove só a linha 9 da palavra "escola"
arvore.remover("escola")      # remove "escola" completamente da árvore
```

**`__remover_recursivo(no, palavra, linha, resultado)`**  
O parâmetro `resultado` é uma **lista com um booleano** (`[False]`), não um booleano direto. O motivo é que Python não passa tipos simples (int, bool, str) por referência — se passássemos `False` diretamente e fizéssemos `resultado = True` dentro da função recursiva, estaríamos criando uma variável local nova, sem alterar o valor original em `remover()`. Usando uma lista, alteramos `resultado[0] = True` e essa mudança se reflete fora da função:

Quando remove um nó com dois filhos, encontra o **sucessor** (o menor nó da subárvore direita), copia os dados dele para o nó atual e remove o sucessor. Depois da remoção, rebalanceia se necessário.

---

#### Outras funções

**`palavra_mais_frequente()`**  
Percorre toda a árvore e retorna a palavra que aparece em mais linhas distintas.

**`imprimir_indice()`**  
Percurso em-ordem, retorna lista com todas as palavras em ordem alfabética no formato `"palavra linha1,linha2,..."`.

**`contar_palavras_distintas()`**  
Conta os nós da árvore — cada nó é uma palavra distinta.

**`contar_palavras_total()`**  
Soma todas as ocorrências: para cada nó, conta quantas linhas ele tem.

---

### `main.py`

**`limpar_palavra(palavra)`**  
Remove pontuação mantendo letras acentuadas. Não usa bibliotecas — só percorre a palavra e mantém o que estiver na string de letras válidas. Assim `"escola,"` vira `"escola"` e `"Raimundo"` vira `"raimundo"`.

**`construir_indice(caminho_arquivo)`**  
Lê o arquivo, limpa cada palavra e insere na árvore. Mede o tempo de construção com `time.time()`.

**`salvar_indice_em_arquivo(arvore, ...)`**  
Gera o `indice_remissivo.txt` com o índice e as estatísticas finais.

**`menu()`**  
Menu interativo com as opções disponíveis.

---

## Exemplos de Uso

Os exemplos abaixo usam o `ContoDeEscola.txt` real.

### Exemplo 1 — Construção do índice

```
Construindo índice...
Índice construído com sucesso!
```

Internamente, processando as primeiras linhas do conto:

```
Linha 2: "A escola era na rua do Costa, um sobradinho de grade de pau."
  -> inserir("escola", 2)   # novo nó: escola → [2]
  -> inserir("era", 2)      # novo nó: era → [2]
  -> inserir("rua", 2)      # novo nó: rua → [2]
  -> inserir("costa", 2)    # novo nó: costa → [2]

Linha 8: "era o problema. De repente disse comigo que o melhor era a escola."
  -> inserir("era", 8)      # já existe: era → [2, 8]
  -> inserir("escola", 8)   # já existe: escola → [2, 8]
```

---

### Exemplo 2 — Busca exata com Medidor de Equilíbrio (opção 1)

```
Escolha uma opção: 1
Digite a palavra para buscar: escola

Medidor de Equilíbrio (ME) para 'escola': 4
Palavra encontrada. Nó NÃO está perfeitamente equilibrado.
```

```
Escolha uma opção: 1
Digite a palavra para buscar: mestre

Palavra encontrada. Nó perfeitamente equilibrado (ME = 0).
```

```
Escolha uma opção: 1
Digite a palavra para buscar: tambor

Palavra não encontrada.
```

---

### Exemplo 3 — Busca por prefixo (opção 2)

```
Escolha uma opção: 2
Digite o prefixo: esc

Palavras encontradas:
escada
escadinhas
escondera
escrever
escrita
escrúpulo
escola
```

```
Escolha uma opção: 2
Digite o prefixo: rai

Palavras encontradas:
raimundo
raiva
```

---

### Exemplo 4 — Remoção de uma linha específica (opção 3)

A palavra `escola` aparece em várias linhas. Removendo só a linha 9:

```
Escolha uma opção: 3
Digite a palavra para remover: escola
Digite a linha (ou pressione Enter para remover a palavra inteira): 9

Remoção realizada com sucesso.
```

Após isso, uma busca por `escola` ainda a encontra, mas sem a linha 9 na lista.

---

### Exemplo 5 — Remoção do nó inteiro (opção 3)

Pressionando Enter sem digitar linha, remove a palavra completamente:

```
Escolha uma opção: 3
Digite a palavra para remover: curvelo
Digite a linha (ou pressione Enter para remover a palavra inteira): 

Remoção realizada com sucesso.
```

---

### Exemplo 6 — Palavra mais frequente (opção 4)

```
Escolha uma opção: 4

Palavra mais frequente: 'e' aparece em 87 linhas.
```

---

### Exemplo 7 — Gerar arquivo (opção 5)

```
Escolha uma opção: 5
Arquivo 'indice_remissivo.txt' gerado com sucesso.
```

Trecho do arquivo gerado:

```
a 2,4,8,9,16,18,20,22,24,25,29,31,36,41,42,43,44,45,48,51,56,...
acabando 47
acabar 47
acabasse 165
...
escola 1,2,8,9,32,37,53,55,166,182,225,229,235,245
era 2,5,8,12,17,28,31,33,36,37,39,46,60,61,71,72,74,79,84,85,87,88,102,103,122,125,131,162,248
...
raimundo 28,29,57,60,67,73,93,104,111,122,142,146,159,248
...

Número total de palavras: 2820
Número de palavras distintas: 1007
Número de palavras descartadas: 1813
Tempo de construção do índice usando árvore AVL: 0.010715s
Total de rotações executadas: 443
```

---

### Aprendizados

- Importância do balanceamento em árvores binárias para garantir eficiência
- Aplicação prática de recursão em estruturas de dados
- Importância de testes exaustivos em estruturas complexas