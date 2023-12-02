class AlocacaoContigua:
    def __init__(self, disk_space):
        self.disk_space = disk_space
        self.disk = [0] * disk_space  # Representação do disco como uma lista de 0s (espaços vazios)
        self.allocated_blocks = {}  # Dicionário para armazenar os blocos alocados

    def allocate_first_fit(self, file_name, file_size):
        start = -1
        count = 0
        for i, block in enumerate(self.disk):
            if block == 0:  # Verifica se o bloco está livre
                if start == -1:
                    start = i  # Marca o início do bloco livre
                count += 1  # Incrementa o contador de blocos livres
                if count == file_size:
                    for j in range(start, start + file_size):
                        self.disk[j] = 1  # Marca os blocos como alocados
                    self.allocated_blocks[file_name] = {'start': start, 'size': file_size}
                    return True  # Arquivo alocado com sucesso
            else:
                start = -1
                count = 0

        return False  # Não há espaço suficiente para alocar o arquivo
    
    def deallocate_blocks(self, file_name):
        if file_name in self.allocated_blocks:
            start = self.allocated_blocks[file_name]['start']
            size = self.allocated_blocks[file_name]['size']
            for i in range(start, start + size):
                self.disk[i] = 0  # Marca os blocos como desalocados
            del self.allocated_blocks[file_name]  # Remove o arquivo do dicionário de blocos alocados
            return True  # Blocos desalocados com sucesso
        else:
            return False  # Arquivo não encontrado ou não está alocado
    
    def display_disk_allocation(self):
        for i in range(self.disk_space):
            if self.disk[i] == 0:
                print(f"Block {i}: Free")
            else:
                allocated_file = None
                for file_name, data in self.allocated_blocks.items():
                    start = data['start']
                    size = data['size']
                    if i in range(start, start + size):
                        allocated_file = file_name
                        break

                if allocated_file:
                    print(f"Block {i}: Allocated to '{allocated_file}'")
                else:
                    print(f"Block {i}: Allocated to Unknown file (Possible inconsistency)")