class Estado():

    def __init__(self, missionarios_left, missionarios_right, canibais_left, canibais_right, river_side):
        # Utiliza as informaões de quantidade de missionarios e canibais em cada lado, e em qual lado
        # está o barco para criar um estado
        self.missionarios_left = missionarios_left
        self.missionarios_right = missionarios_right
        self.canibais_left = canibais_left
        self.canibais_right = canibais_right
        self.river_side = river_side
        self.pai = None
        self.filhos = []

    def __str__(self):
        print('Lado Direito \t| Lado Esquerdo\n')
        # É a forma que cada estado está printado em string
        return 'Missionarios: {}\t| Missionarios: {}\nCanibais: {}\t| Canibais: {}'.format(
            self.missionarios_left, self.missionarios_right, self.canibais_left, self.canibais_right
        )

    def valid_state(self):
        # Não se pode gerar estados onde o número de canibais ou missionários em qualquer lado
        # do rio seja negativo
        # Verifica se o número de missionarios ou canibais é menor do que 0
        if ((self.missionarios_left < 0) or (self.missionarios_right < 0)
            or (self.canibais_left < 0) or (self.canibais_right < 0)):
            return False
        # Verifica se em ambas as margens do rio o número de missionários não é inferior ao número de canibais.
        return ((self.missionarios_left == 0 or self.missionarios_left >= self.canibais_left) and
                (self.missionarios_right == 0 or self.missionarios_right >= self.canibais_right))

    def final_state(self):
        # Verifica se o estado já é o estado final, ou seja, todos missionarios e canibais passaram corretamente
        resultado_left = self.missionarios_left == self.canibais_left == 0
        resultado_right = self.missionarios_right == self.canibais_right == 3
        return resultado_left and resultado_right

    def create_sons(self):
        # Vai gerar todos os filhos possiveis de um estado caso n seja um estado final
        # Encontra o novo lado do rio
        novo_river_side = 'right' if self.river_side == 'left' else 'left'
        # Gera a lista de possíveis movimentos
        movimentos = [
            {'missionarios': 2, 'canibais': 0},
            {'missionarios': 1, 'canibais': 0},
            {'missionarios': 1, 'canibais': 1},
            {'missionarios': 0, 'canibais': 1},
            {'missionarios': 0, 'canibais': 2},
        ]
        # Gera todos os possíveis estados e armazena apenas os válidos na lista de filhos
        # do estado atual
        for movimento in movimentos:
            if self.river_side == 'left':
                # Se o barco estiver a leftuerda do rio, os missionários e canibais saem da
                # margem leftuerda do rio e vão para a righteita
                missionarios_left = self.missionarios_left - movimento['missionarios']
                missionarios_right = self.missionarios_right + movimento['missionarios']
                canibais_left = self.canibais_left - movimento['canibais']
                canibais_right = self.canibais_right + movimento['canibais']
            else:
                # Caso contrário, os missionários e canibais saem da margem righteita do rio
                # e vão para a leftuerda
                missionarios_right = self.missionarios_right - movimento['missionarios']
                missionarios_left = self.missionarios_left + movimento['missionarios']
                canibais_right = self.canibais_right - movimento['canibais']
                canibais_left = self.canibais_left + movimento['canibais']
            # Cria o estado do filho e caso este seja válido, o adiciona à lista de filhos do pai
            filho = Estado(missionarios_left, missionarios_right, canibais_left,
                           canibais_right, novo_river_side)
            filho.pai = self
            if filho.valid_state():
                self.filhos.append(filho)

class Missionarios_Canibais():
    def __init__(self):
        # Inicializa uma instância do problema com uma raiz pré-definida sem solução
        # Insere a raiz na fila de execução, que será utilizada para fazer uma busca em largura
        self.fila_execucao = [Estado(3, 0, 3, 0, 'left')]
        self.solucao = None

    def create_solucion(self):
        # Utilizando a busca em largura encontra a solução para a árvore de estados gerada.
        # Realiza a busca em largura em busca da solução
        for elemento in self.fila_execucao:
            if elemento.final_state():
                # Se a solução foi encontrada, o caminho que compõe a solução é gerado realizando
                # o caminho de volta até a raiz da árvore de estados e então encerra a busca
                self.solucao = [elemento]
                while elemento.pai:
                    self.solucao.insert(0, elemento.pai)
                    elemento = elemento.pai
                break;
            # Caso o elemento não seja a solução, gera seus filhos e os adiciona na fila de execução
            elemento.create_sons()
            self.fila_execucao.extend(elemento.filhos)

def main():
    # Vai ser responsável por instanciar o problema e solucionar
    problema = Missionarios_Canibais()
    problema.create_solucion()
    vez = 0
    # Printando todas os passos e soluções
    for estado in problema.solucao:
        if(vez % 2 ==0 and vez != 0):
            print ('Direção: Esquerda --> Direita')
        elif(vez % 2 !=0 and vez != 0):
            print ('Direção: Direita --> Esquerda')
        else:
            print ('Problema dos Canibais e Missionarios')
            print ('------------------------------------')
        print (estado, '            Passo ', (vez+1))
        print ('------------------------------------')
        vez = vez+1
    

if __name__ == '__main__':
    main()
