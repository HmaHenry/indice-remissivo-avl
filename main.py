# main.py
# Arquivo principal do projeto Índice Remissivo com AVL
# Alunos: Henrique Melo e Murilo Rodrigues
# Professora: Maria Adriana

# Importando a biblioteca "time" do python para calcular o tempo de execução do programa
import time
from avl import ArvoreAVL


def limpar_palavra(palavra):
    # Remove pontuação e caracteres especiais da palavra
    # Mantém apenas letras (inclusive acentuadas)
    letras = "abcdefghijklmnopqrstuvwxyzáàãâäéèêëíìîïóòõôöúùûüýÿçñ"
    resultado = ""
    for caractere in palavra.lower():
        if caractere in letras:
            resultado += caractere
    
    return resultado


def construir_indice(caminho_arquivo):
    # Lê o arquivo txt e constrói a AVL com as palavras e número das linhas
    # A função retorna a árvore, o número que representa o total de palavras e o tempo de construção/execução
    arvore = ArvoreAVL()
    total_palavras = 0

    inicio = time.time()

    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        for numero_linha, linha in enumerate(arquivo, start=1):
            palavras = linha.strip().split()

            for palavra in palavras:
                palavra_limpa = limpar_palavra(palavra).lower()

                if palavra_limpa != "":
                    total_palavras += 1
                    # Inserção na AVL
                    arvore.inserir(palavra_limpa, numero_linha)

    fim = time.time()
    tempo_construcao = fim - inicio

    return arvore, total_palavras, tempo_construcao


def salvar_indice_em_arquivo(arvore, total_palavras, tempo_construcao):
    # Gera o arquivo final com índice em ordem alfabética e as cinco linhas finais:
    #  (total de palavras, total de palavras distintas, total de palavras descartadas (por serem repetidas), tempo de construção, total de rotações executadas)

    indice = arvore.imprimir_indice()
    total_distintas = arvore.contar_palavras_distintas()
    descartadas = arvore.palavras_descartadas
    rotacoes = arvore.total_rotacoes

    with open("indice_remissivo.txt", "w", encoding="utf-8") as arquivo:
        for linha in indice:
            arquivo.write(linha + "\n")

        arquivo.write("\n")
        arquivo.write(f"Número total de palavras: {total_palavras}\n")
        arquivo.write(f"Número de palavras distintas: {total_distintas}\n")
        arquivo.write(f"Número de palavras descartadas: {descartadas}\n")
        arquivo.write(f"Tempo de construção do índice usando árvore AVL: {tempo_construcao:.6f}s\n")
        arquivo.write(f"Total de rotações executadas: {rotacoes}\n")


def menu():
    # Menu interativo para testar as funcioanlidades exigidas
    caminho = "ContoDeEscola.txt"

    print("Construindo índice...")
    arvore, total_palavras, tempo_construcao = construir_indice(caminho)
    print("Índice construído com sucesso!\n")

    while True:
        print("\n===== MENU =====")
        print("1 - Buscar palavra (com Medidor de Equilíbrio)")
        print("2 - Buscar por prefixo")
        print("3 - Remover palavra ou linha")
        print("4 - Mostrar palavra mais frequente")
        print("5 - Gerar arquivo índice completo")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            palavra = input("Digite a palavra para buscar: ").lower()
            resultado = arvore.buscar_com_medidor_equilibrio(palavra)

            if resultado == -1:
                print("Palavra não encontrada.")
            elif resultado == 0:
                print("Palavra encontrada. Nó perfeitamente equilibrado (ME = 0).")
            elif resultado == 1:
                print("Palavra encontrada. Nó NÃO está perfeitamente equilibrado.")

        elif opcao == "2":
            prefixo = input("Digite o prefixo: ").lower()
            palavras = arvore.buscar_por_prefixo(prefixo)

            if palavras:
                print("Palavras encontradas:")
                for p in palavras:
                    print(p)
            else:
                print("Nenhuma palavra encontrada com esse prefixo.")

        elif opcao == "3":
            palavra = input("Digite a palavra para remover: ").lower()
            linha = input("Digite a linha (ou pressione Enter para remover a palavra inteira): ")

            if linha.strip() == "":
                sucesso = arvore.remover(palavra)
            else:
                sucesso = arvore.remover(palavra, int(linha))

            if sucesso:
                print("Remoção realizada com sucesso.")
            else:
                print("Palavra ou linha não encontrada.")

        elif opcao == "4":
            palavra, quantidade = arvore.palavra_mais_frequente()

            if palavra:
                print(f"Palavra mais frequente: '{palavra}' aparece em {quantidade} linhas.")
            else:
                print("Árvore vazia.")

        elif opcao == "5":
            salvar_indice_em_arquivo(arvore, total_palavras, tempo_construcao)
            print("Arquivo 'indice_remissivo.txt' gerado com sucesso.")

        elif opcao == "0":
            print("Encerrando programa...")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu()