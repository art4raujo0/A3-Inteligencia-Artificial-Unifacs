import random

# --- 1. O Tabuleiro ---
class Ambiente:
    def __init__(self):
        self.tabuleiro = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def desenhar(self):
        print("\n   0   1   2")
        print("  -----------")
        for i, linha in enumerate(self.tabuleiro):
            print(f"{i} | {' | '.join(linha)} |")
            print("  -----------")

    def esta_vazio(self, linha, coluna):
        return self.tabuleiro[linha][coluna] == " "

    def marcar(self, linha, coluna, simbolo):
        if self.esta_vazio(linha, coluna):
            self.tabuleiro[linha][coluna] = simbolo
            return True
        return False

    def desfazer(self, linha, coluna):
        self.tabuleiro[linha][coluna] = " "

    def verificar_vitoria(self, jogador):
        # Verifica linhas, colunas e diagonais
        tab = self.tabuleiro
        # Linhas
        for l in tab:
            if all(c == jogador for c in l): return True
        # Colunas
        for c in range(3):
            if all(tab[l][c] == jogador for l in range(3)): return True
        # Diagonais
        if all(tab[i][i] == jogador for i in range(3)): return True
        if all(tab[i][2-i] == jogador for i in range(3)): return True
        return False

    def verificar_empate(self):
        for linha in self.tabuleiro:
            if " " in linha: return False
        return True
    
    def obter_casas_vazias(self):
        vazias = []
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == " ":
                    vazias.append((i, j))
        return vazias


# --- 2. O AGENTE ---
class Agente:
    def __init__(self, simbolo):
        self.simbolo = simbolo # Pode ser 'X' ou 'O'

# --- 3. O AGENTE IA ---
class AgenteIA(Agente):
    def __init__(self, simbolo):
        super().__init__(simbolo)
        # Define quem o adversario
        self.inimigo = "X" if simbolo == "O" else "O"

    def pensar(self, ambiente):
        '''
        Recebe o ambiente e retorna a ação (linha, coluna).
        ''' 
        casas_vazias = ambiente.obter_casas_vazias()

        # REGRA 1: Tentar Ganhar
        for l, c in casas_vazias:
            ambiente.marcar(l, c, self.simbolo) # Simula
            if ambiente.verificar_vitoria(self.simbolo):
                ambiente.desfazer(l, c) # Limpa
                return l, c
            ambiente.desfazer(l, c)

        # REGRA 2: Bloquear Inimigo
        for l, c in casas_vazias:
            ambiente.marcar(l, c, self.inimigo) # Simula inimigo
            if ambiente.verificar_vitoria(self.inimigo):
                ambiente.desfazer(l, c)
                return l, c
            ambiente.desfazer(l, c)

        # REGRA 3: Centro
        if (1, 1) in casas_vazias:
            return 1, 1

        # REGRA 4: Cantos
        cantos = [(0, 0), (0, 2), (2, 0), (2, 2)]
        cantos_disponiveis = [c for c in cantos if c in casas_vazias]
        if cantos_disponiveis:
            return random.choice(cantos_disponiveis)

        # REGRA 5: Aleatório
        return random.choice(casas_vazias)

# --- 4. O LOOP DO JOGO ---
def main():
    # Cria os Objetos
    ambiente = Ambiente()
    humano = Agente("X")
    robo = AgenteIA("O")

    jogador_atual = humano # Começa com o humano

    print("=== JOGO DA VELHA: ===")

    while True:
        ambiente.desenhar()

        # Percepção e Ação
        if jogador_atual == humano:
            # Lógica do Humano
            print(f"\nSua vez ({humano.simbolo})!")
            try:
                l = int(input("Linha: "))
                c = int(input("Coluna: "))
                if not ambiente.marcar(l, c, humano.simbolo):
                    print("Jogada inválida! Tente de novo.")
                    continue
            except:
                print("Digite apenas números.")
                continue
        else:
            # Lógica da IA
            print(f"\nA IA ({robo.simbolo}) está analisando o ambiente...")
            l, c = robo.pensar(ambiente)
            ambiente.marcar(l, c, robo.simbolo)
            print(f"IA jogou na posição {l}, {c}")

        if ambiente.verificar_vitoria(jogador_atual.simbolo):
            ambiente.desenhar()
            vencedor = "VOCÊ" if jogador_atual == humano else "A IA"
            print(f"\n🎉 FIM DE JOGO! {vencedor} ganhou! 🎉")
            break
        
        if ambiente.verificar_empate():
            ambiente.desenhar()
            print("\n🤝 EMPATE! 🤝")
            break

        # Troca de turno
        jogador_atual = robo if jogador_atual == humano else humano

if __name__ == "__main__":
    main()