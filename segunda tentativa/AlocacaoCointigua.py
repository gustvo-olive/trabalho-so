class Arquivo:
    def __init__(self, nome, conteudo=""):
        self.nome = nome
        self.conteudo = conteudo

class Bloco:
    def __init__(self, tamanho, ocupado=False):
        self.tamanho = tamanho
        self.ocupado = ocupado
        self.arquivo = None

class Diretorio:
    def __init__(self, nome, tamanho_disco):
        self.nome = nome
        self.tamanho_disco = tamanho_disco
        self.blocos = [Bloco(1) for _ in range(tamanho_disco)]
        self.subdiretorios = {}  # Adicionando a estrutura para subdiretórios
        self.arquivos = {}

    def alocacao_first_fit(self, arquivo):
        tamanho_arquivo = len(arquivo.conteudo)

        for i in range(self.tamanho_disco):
            if not self.blocos[i].ocupado and i + tamanho_arquivo <= self.tamanho_disco:
                # Encontrou espaço disponível para o arquivo
                for j in range(i, i + tamanho_arquivo):
                    self.blocos[j].ocupado = True
                    self.blocos[j].arquivo = arquivo
                self.arquivos[arquivo.nome] = (i, tamanho_arquivo)
                return True

        return False

    # Implemente as estratégias best-fit e worst-fit

    def remover_arquivo(self, nome_arquivo):
        if nome_arquivo in self.arquivos:
            inicio, tamanho = self.arquivos[nome_arquivo]
            for i in range(inicio, inicio + tamanho):
                self.blocos[i].ocupado = False
                self.blocos[i].arquivo = None
            del self.arquivos[nome_arquivo]
            return True
        return False
    

class SistemaArquivos:
    def __init__(self):
        self.raiz = Diretorio('Raiz', tamanho_disco=20)

    def menu(self):
        while True:
            print("\n==== Menu ====")
            print("1. Criar arquivo")
            print("2. Criar diretório")
            print("3. Remover arquivo")
            print("4. Listar diretório atual")
            print("5. Obter atributos")
            
            print("6. Sair")

            escolha = input("Escolha a operação que deseja realizar (1-6): ")

            if escolha == '1':
                self.criar_arquivo()
            elif escolha == '2':
                self.criar_diretorio()
            elif escolha == '3':
                self.remover_arquivo()
            elif escolha == '4':
                self.listar_diretorio_atual()
            elif escolha == '5':
                self.obter_atributos()
            elif escolha == '6':
                print("Saindo do programa. Até logo!")
                break
            else:
                print("Opção inválida. Escolha um número de 1 a 6.")
                
    def criar_arquivo(self):
        caminho = input("Digite o caminho do diretório onde deseja criar o arquivo (ou deixe em branco para o diretório raiz): ")
        nome_arquivo = input("Digite o nome do arquivo a ser criado: ")
        tamanho_arquivo = int(input("Digite a quantidade de blocos desse arquivo: "))
        conteudo_arquivo = input("Digite o conteúdo do arquivo: ")

        diretorio_atual = self.raiz

        if caminho:  # Se um caminho foi fornecido
            caminho_split = caminho.split('/')
            for diretorio_nome in caminho_split:
                if diretorio_nome in diretorio_atual.subdiretorios:
                    diretorio_atual = diretorio_atual.subdiretorios[diretorio_nome]
                else:
                    print(f"O diretório '{caminho}' não existe.")
                    return

        novo_arquivo = Arquivo(nome_arquivo, conteudo_arquivo)

        blocos_necessarios = []

        for i in range(len(diretorio_atual.blocos)):
            if not diretorio_atual.blocos[i].ocupado:
                blocos_necessarios.append(i)
                if len(blocos_necessarios) == tamanho_arquivo:
                    for bloco_idx in blocos_necessarios:
                        diretorio_atual.blocos[bloco_idx].ocupado = True
                        diretorio_atual.blocos[bloco_idx].arquivo = novo_arquivo
                    diretorio_atual.arquivos[nome_arquivo] = (blocos_necessarios[0], tamanho_arquivo)
                    print(f"Arquivo '{nome_arquivo}' criado com sucesso em '{caminho}'.")
                    return

        print(f"Espaço insuficiente para criar o arquivo '{nome_arquivo}' em '{caminho}'.")

    def criar_diretorio(self):
        caminho = input("Digite o caminho do diretório onde deseja criar o novo diretório (ou deixe em branco para o diretório raiz): ")
        nome_diretorio = input("Digite o nome do novo diretório: ")

        diretorio_atual = self.raiz

        if caminho:  # Se um caminho foi fornecido
            caminho_split = caminho.split('/')
            for diretorio_nome in caminho_split:
                if diretorio_nome in diretorio_atual.subdiretorios:
                    diretorio_atual = diretorio_atual.subdiretorios[diretorio_nome]
                else:
                    print(f"O diretório '{caminho}' não existe.")
                    return

        novo_diretorio = Diretorio(nome_diretorio, tamanho_disco=20)
        diretorio_atual.subdiretorios[nome_diretorio] = novo_diretorio

        print(f"Diretório '{nome_diretorio}' criado com sucesso em '{caminho}'.")

    def remover_arquivo(self):
        caminho = input("Digite o caminho do diretório onde está o arquivo a ser removido: ")
        nome_arquivo = input("Digite o nome do arquivo a ser removido: ")

        diretorio_atual = self.raiz

        if caminho:  # Se um caminho foi fornecido
            caminho_split = caminho.split('/')
            for diretorio_nome in caminho_split:
                if diretorio_nome in diretorio_atual.subdiretorios:
                    diretorio_atual = diretorio_atual.subdiretorios[diretorio_nome]
                else:
                    print(f"O diretório '{caminho}' não existe.")
                    return

        if nome_arquivo in diretorio_atual.arquivos:
            inicio, tamanho = diretorio_atual.arquivos[nome_arquivo]
            for i in range(inicio, inicio + tamanho):
                diretorio_atual.blocos[i].ocupado = False
                diretorio_atual.blocos[i].arquivo = None

            del diretorio_atual.arquivos[nome_arquivo]
            print(f"Arquivo '{nome_arquivo}' removido com sucesso de '{caminho}'.")
        else:
            print(f"O arquivo '{nome_arquivo}' não foi encontrado em '{caminho}'.")
    
    def obter_atributos(self):
        caminho = input("Digite o caminho do diretório onde está o arquivo: ")
        nome_arquivo = input("Digite o nome do arquivo: ")

        diretorio_atual = self.raiz

        if caminho:  # Se um caminho foi fornecido
            caminho_split = caminho.split('/')
            for diretorio_nome in caminho_split:
                if diretorio_nome in diretorio_atual.subdiretorios:
                    diretorio_atual = diretorio_atual.subdiretorios[diretorio_nome]
                else:
                    print(f"O diretório '{caminho}' não existe.")
                    return

        if nome_arquivo in diretorio_atual.arquivos:
            inicio, tamanho = diretorio_atual.arquivos[nome_arquivo]
            print(f"O arquivo '{nome_arquivo}' está armazenado a partir do bloco {inicio} e ocupa {tamanho} blocos.")
        else:
            print(f"O arquivo '{nome_arquivo}' não foi encontrado em '{caminho}'.")

    def listar_diretorio_atual(self, diretorio=None, nivel=0):
        if diretorio is None:
            diretorio = self.raiz

        # Imprime arquivos no diretório atual
        for nome_arquivo, arquivo in diretorio.arquivos.items():
            print(" " * nivel * 4 + f"[FILE] {nome_arquivo}")

        # Imprime subdiretórios no diretório atual
        for nome_subdiretorio, subdiretorio in diretorio.subdiretorios.items():
            print(" " * nivel * 4 + f"[DIR] {nome_subdiretorio}")
            self.listar_diretorio_atual(subdiretorio, nivel + 1)
        

    # Implemente as outras operações: remover, renomear, abrir, escrever, ler arquivos, etc.

# Exemplo de uso:
sistema = SistemaArquivos()
sistema.menu()

# Aqui você pode implementar outras operações necessárias no sistema de arquivos
