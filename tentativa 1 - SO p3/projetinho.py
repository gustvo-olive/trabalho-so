from alocacao_contigua import AlocacaoContigua
import os

class SimpleOSSimulated:
    def __init__(self):
        self.filesystem = {'root': {'type': 'directory', 'content': {}}}
        self.current_directory = self.filesystem['root']

        self.file_allocation = AlocacaoContigua(disk_space=24)

    def command_prompt(self):
        self.clear_screen()
        while True:
            command = input("SimpleOS> ").strip().split()
            if not command:
                continue
            if command[0] == "exit":
                print("Encerrando o SimpleOS...")
                break
            elif command[0] == "ls":
                self.list_directory()
            elif command[0] == "clean":
                self.clear_screen()
            elif command[0] == "help":
                self.help()
            elif command[0] == "create":
                if len(command) > 3:
                    self.create_file(command[1], command[2], command[3])
                else:
                    print("Nome do arquivo, tamanho do arquivo ou tipo de alocacao não especificados.")
            elif command[0] == "mkdir":
                if len(command) > 1:
                    self.create_directory(command[1])
                else:
                    print("Nome do diretório não especificado.")
            elif command[0] == "cd":
                if len(command) > 1:
                    self.change_directory(command[1])
                else:
                    print("Nome do diretório não especificado.")
            elif command[0] == "rename":
                if len(command) > 2:
                    self.rename_file(command[1], command[2])
                else:
                    print("Nomes não especificados para renomear o arquivo.")
            elif command[0] == "remove":
                if len(command) > 1:
                    self.remove_file(command[1])
                else:
                    print("Nome do arquivo não especificado")
            elif command[0] == "disk":
                self.file_allocation.display_disk_allocation()
            elif command[0] == "open":
                if len(command) > 2:
                    self.open_file(command[1], command[2])
                else:
                    print("Nome do arquivo ou modo não especificado.")
            elif command[0] == "write":
                if len(command) > 1:  
                    content_to_write = ' '.join(command[1:])  
                    self.write_to_file(content_to_write)  
                else:
                    print("Conteúdo não especificado para escrita.")
            elif command[0] == "read":
                if len(command) > 1:
                    self.read_from_file(command[1])
                else:
                    print("Nome do arquivo não especificado.")
            elif command[0] == "close":
                if len(command) > 1:
                    self.close_file(command[1])
                else:
                    print("Nome do arquivo não especificado.")
            else:
                print(f"Comando '{command[0]}' não reconhecido.")
    
    def help(self):
        print("""
        Comandos disponíveis:
        - ls: Listar conteúdo do diretório atual.
        - create <nome_arquivo> <tamanho> <algoritmo>: Criar um arquivo com um algoritmo de alocação (first-fit, best-fit, worst-fit).
        - mkdir <nome_diretório>: Criar um diretório.
        - cd <nome_diretório>: Mudar para um diretório.
        - rename <nome_antigo> <novo_nome>: Renomear um arquivo.
        - remove <nome_arquivo>: Remover um arquivo.
        - disk: Mostrar alocação de disco.
        - open <nome_arquivo> <modo>: Abrir um arquivo.
        - write <conteúdo>: Escrever conteúdo em um arquivo aberto.
        - read <nome_arquivo>: Ler conteúdo de um arquivo.
        - close <nome_arquivo>: Fechar um arquivo aberto.
        - clean: Limpar a tela. 
        - exit: Encerrar o SimpleOS.
        """)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def list_directory(self):
        print(f"Diretório atual: C:{self.get_current_directory_path()}")
        for name, data in self.current_directory['content'].items():
            if data['type'] == 'directory':
                print(f"[DIR] {name}")
            else:
                print(f"[FILE] {name}")
        # Mostrar o diretório atual

    def list_directory(self):
        print(f"Diretório atual: C:{self.get_current_directory_path()}")

        for name, data in self.current_directory['content'].items():
            if data['type'] == 'directory':
                print(f"[DIR] {name}")
            else:
                print(f"[FILE] {name}")
        # Mostrar o diretório atual
        

    def get_current_directory_path(self, current_dir=None):
        # Se o diretório atual não for passado, assume-se como o diretório raiz
        if current_dir is None:
            current_dir = self.current_directory

        # Obtém o nome do diretório atual
        path = [""]
        for name, content in self.filesystem['root']['content'].items():
            if content == current_dir:
                path[0] = name
                break

        # Se não for o diretório raiz, continua a recursão para os diretórios pai
        if current_dir != self.filesystem['root']:
            parent = self.get_parent_directory(current_dir)
            if parent:
                path.insert(0, self.get_current_directory_path(parent))

        return '/'.join(path)
    
    def create_file(self, filename, file_size, allocation_algorithm):
        try:
            file_size = int(file_size)
        except ValueError:
            print("Tamanho do arquivo deve ser um número inteiro positivo.")
            return

        if file_size <= 0:
            print("Tamanho do arquivo deve ser um número inteiro positivo.")
            return

        if allocation_algorithm not in ["first-fit", "best-fit", "worst-fit"]:
            print("Algoritmo de alocação não reconhecido.")
            return

        if filename in self.current_directory['content']:
            print(f"Arquivo '{filename}' já existe.")
        else:
            allocated_blocks = None

            if allocation_algorithm == "first-fit":
                allocated_blocks = self.file_allocation.allocate_first_fit(filename, file_size)
            elif allocation_algorithm == "best-fit":
                allocated_blocks = self.file_allocation.allocate_best_fit(filename, file_size)
            elif allocation_algorithm == "worst-fit":
                allocated_blocks = self.file_allocation.allocate_worst_fit(filename, file_size)

            if allocated_blocks:
                self.current_directory['content'][filename] = {
                    'type': 'file',
                    'size': file_size,
                    'allocation': allocated_blocks
                }
                print(f"Arquivo '{filename}' criado com sucesso.")
            else:
                print(f"Espaço insuficiente para alocar o arquivo '{filename}' de tamanho {file_size}.")    


    def remove_file(self, filename):
        if filename in self.current_directory['content']:
            file_info = self.current_directory['content'][filename]
            allocated_block = file_info.get('allocation')

            if allocated_block is not None:
                success = self.file_allocation.deallocate_blocks(filename)
                if success:
                    del self.current_directory['content'][filename]
                    print(f"Arquivo '{filename}' removido com sucesso e blocos desalocados.")
                else:
                    print(f"Falha ao desalocar blocos do arquivo '{filename}'.")
            else:
                del self.current_directory['content'][filename]
                print(f"Arquivo '{filename}' removido com sucesso.")    
        else:
            print(f"Arquivo '{filename}' não encontrado.")

    def create_directory(self, directory_name):
        if directory_name in self.current_directory['content']:
            print(f"O diretório '{directory_name}' já existe.")
        else:
            self.current_directory['content'][directory_name] = {'type': 'directory', 'content': {}}
            print(f"Diretório '{directory_name}' criado com sucesso.")

    def change_directory(self, directory_name):
        if directory_name == "..":
            # Se o comando for para subir um nível (diretório pai)
            if self.current_directory != self.filesystem['root']:
                parent_dir = self.get_parent_directory(self.current_directory)
                if parent_dir:
                    self.current_directory = parent_dir
                    print("Retornou ao diretório pai.")
                else:
                    print("Erro ao acessar o diretório pai.")
            else:
                print("Você já está no diretório raiz.")
        elif directory_name in self.current_directory['content'] and self.current_directory['content'][directory_name]['type'] == 'directory':
            # Se o comando for para entrar em um diretório existente
            self.current_directory = self.current_directory['content'][directory_name]
            print(f"Entrou no diretório '{directory_name}'.")
        else:
            print(f"Diretório '{directory_name}' não encontrado.")

    def get_parent_directory(self, current_directory):
        """Obtém o diretório pai do diretório atual."""
        for content in self.filesystem.values():
            if 'content' in content and current_directory in content['content'].values():
                return content
        return None
    
    def rename_file(self, old_name, new_name):
        if old_name in self.current_directory['content']:
            old_file = self.current_directory['content'][old_name]

            # Renomeia o arquivo no diretório
            self.current_directory['content'][new_name] = old_file

            # Remove a entrada do arquivo antigo do diretório
            del self.current_directory['content'][old_name]

            # Atualiza a entrada de alocação se o arquivo estava alocado
            if old_name in self.file_allocation.allocated_blocks:
                allocation_info = self.file_allocation.allocated_blocks.pop(old_name)
                self.file_allocation.allocated_blocks[new_name] = allocation_info

            print(f"Arquivo '{old_name}' renomeado para '{new_name}' com sucesso.")
        else:
            print(f"Arquivo '{old_name}' não encontrado.")

    def open_file(self, file_name, mode):
        try:
            if file_name in self.current_directory['content'] and self.current_directory['content'][file_name]['type'] == 'file':
                self.current_file = self.current_directory['content'][file_name]
                print(f"Arquivo '{file_name}' aberto no modo '{mode}'.")
            else:
                print(f"Arquivo '{file_name}' não encontrado ou não é um arquivo.")
                self.current_file = None  # Se não foi possível abrir, define como None
        except KeyError:
            print("Erro ao abrir o arquivo.")

    def write_to_file(self, content):
        try:
            if self.current_file and self.current_file['type'] == 'file':
                self.current_file['content'] = content  # Sobrescreve o conteúdo do arquivo
                print("Conteúdo escrito com sucesso.")
            else:
                print("Nenhum arquivo aberto para escrita ou o arquivo é inválido.")
        except KeyError:
            print("Erro ao escrever no arquivo.")

    def read_from_file(self, file_name):
        try:
            if file_name in self.current_directory['content'] and self.current_directory['content'][file_name]['type'] == 'file':
                content = self.current_directory['content'][file_name]['content']
                print("Conteúdo do arquivo:")
                print(content)
            else:
                print(f"Arquivo '{file_name}' não encontrado ou não é um arquivo.")
        except KeyError:
            print("Erro ao ler o arquivo.")

    def close_file(self, file_name):
        try:
            if file_name in self.current_directory['content'] and self.current_directory['content'][file_name]['type'] == 'file':
                print(f"Arquivo '{file_name}' fechado com sucesso.")
                self.current_file = None  # Após fechar, define como None
            else:
                print(f"Arquivo '{file_name}' não encontrado ou não é um arquivo.")
        except KeyError:
            print("Erro ao fechar o arquivo.")
    
    

# Inicialização do SimpleOS Simulado
simple_os = SimpleOSSimulated()

# Execução do prompt de comando
simple_os.command_prompt()
