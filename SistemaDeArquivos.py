class SimpleOSSimulated:
    def _init_(self):
        self.filesystem = {'root': {'type': 'directory', 'content': {}}}
        self.current_directory = self.filesystem['root']

    def command_prompt(self):
        while True:
            command = input("SimpleOS> ").strip().split()
            if not command:
                continue
            if command[0] == "exit":
                print("Encerrando o SimpleOS...")
                break
            elif command[0] == "ls":
                self.list_directory()
            elif command[0] == "touch":
                if len(command) > 1:
                    self.create_file(command[1])
                else:
                    print("Nome do arquivo não especificado.")
            # Adicione os comandos para os novos recursos aqui
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
            elif command[0] == "cp":
                if len(command) > 2:
                    self.copy_file(command[1], command[2])
                else:
                    print("Nome do arquivo ou diretório de destino não especificado.")
            else:
                print(f"Comando '{command[0]}' não reconhecido.")

    def list_directory(self):
        for name, data in self.current_directory['content'].items():
            if data['type'] == 'directory':
                print(f"[DIR] {name}")
            else:
                print(f"[FILE] {name}")

    def create_file(self, filename):
        if filename in self.current_directory['content']:
            print(f"Arquivo '{filename}' já existe.")
        else:
            self.current_directory['content'][filename] = {'type': 'file'}
            print(f"Arquivo '{filename}' criado com sucesso.")

    def remove_file(self, filename):
        if filename in self.current_directory:
            del self.current_directory[filename]
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
        # Encontrar o diretório pai dado um diretório atual
        for content in self.filesystem.values():
            if 'content' in content and current_directory in content['content'].values():
                return content
        return None

    def rename_file(self, old_name, new_name):
        if old_name in self.current_directory['content']:
            self.current_directory['content'][new_name] = self.current_directory['content'].pop(old_name)
            print(f"Arquivo '{old_name}' renomeado para '{new_name}' com sucesso.")
        else:
            print(f"Arquivo '{old_name}' não encontrado.")

    def copy_file(self, file_name, destination_directory):
        if file_name in self.current_directory['content']:
            file_data = self.current_directory['content'][file_name]
            self.filesystem[destination_directory]['content'][file_name] = file_data.copy()
            print(f"Arquivo '{file_name}' copiado para '{destination_directory}' com sucesso.")
        else:
            print(f"Arquivo '{file_name}' não encontrado.")

# Inicialização do SimpleOS Simulado
simple_os = SimpleOSSimulated()

# Execução do prompt de comando
simple_os.command_prompt()
