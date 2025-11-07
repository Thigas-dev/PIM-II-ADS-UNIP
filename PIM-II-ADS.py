import json
import os

class Aluno:
    def __init__(self, nome):
        self.nome = nome
        self.notas = {}

    def adicionar_nota(self, atividade, nota):
        self.notas[atividade] = nota

    def media(self):
        if not self.notas:
            return 0
        return sum(self.notas.values()) / len(self.notas)

    def atividades_reforco(self):
        return [atv for atv, nota in self.notas.items() if nota < 6]


class Turma:
    def __init__(self, nome):
        self.nome = nome
        self.alunos = []
        self.atividades = []

    def adicionar_aluno(self, aluno):
        self.alunos.append(aluno)

    def adicionar_atividade(self, atividade):
        self.atividades.append(atividade)

    def salvar_json(self, arquivo="turma.json"):
        dados = {
            "atividades": self.atividades,
            "alunos": [{"nome": a.nome, "notas": a.notas} for a in self.alunos]
        }
        with open(arquivo, "w") as f:
            json.dump(dados, f, indent=4)
        print("Dados salvos com sucesso!")

    def carregar_json(self, arquivo="turma.json"):
        if not os.path.exists(arquivo):
            return
        with open(arquivo, "r") as f:
            dados = json.load(f)
        self.atividades = dados.get("atividades", [])
        self.alunos = []
        for a in dados.get("alunos", []):
            aluno = Aluno(a["nome"])
            aluno.notas = a["notas"]
            self.alunos.append(aluno)
        print("Dados carregados com sucesso!")


def buscar_aluno(nome, lista_alunos):
    resultados = []
    for aluno in lista_alunos:
        if nome.lower() in aluno.nome.lower():
            resultados.append(aluno)
    return resultados

def buscar_atividade(palavra, turma):
    resultados = []
    for a in turma.atividades:
        if palavra.lower() in a.lower():
            resultados.append(a)
    return resultados

def relatorio_notas(turma):
    if not turma.alunos:
        print("\nNenhum aluno cadastrado ainda.")
        return

    print("\n❰ RELATÓRIO DE NOTAS ❱")
    for a in turma.alunos:
        print(f"\nAluno: {a.nome}")
        if not a.notas:
            print("Sem notas ainda.")
        else:
            for atv, nota in a.notas.items():
                print(f"  {atv}: {nota}")
        print(f"Média: {a.media():.2f}")

def menu():
    turma = Turma("Turma ADS")
    turma.carregar_json()
    print(" ❰ SISTEMA ACADÊMICO UNIP ❱")
    while True:
        print("\n1. Cadastrar aluno")
        print("2. Cadastrar atividade")
        print("3. Lançar nota")
        print("4. Buscar aluno")
        print("5. Buscar atividade")
        print("6. Relatório de notas")
        print("7. Sugestão de reforço (IA simples)")
        print("8. Salvar dados")
        print("0. Sair")
        opcao = input("Escolha: ")
        if opcao == "1":
            nome = input("Nome do aluno: ").strip()
            if not nome:
                print("Nome inválido.")
                continue
            turma.adicionar_aluno(Aluno(nome))
            print("Aluno cadastrado com sucesso!")
        elif opcao == "2":
            atv = input("Nome da atividade: ").strip()
            if not atv:
                print("Nome da atividade inválido.")
                continue
            turma.adicionar_atividade(atv)
            print("Atividade cadastrada!")
        elif opcao == "3":
            nome = input("Nome do aluno: ")
            aluno_encontrado = buscar_aluno(nome, turma.alunos)
            if not aluno_encontrado:
                print("Aluno não encontrado.")
                continue
            aluno = aluno_encontrado[0]
            if not turma.atividades:
                print("Nenhuma atividade cadastrada ainda.")
                continue
            print("\nAtividades disponíveis:")
            for a in turma.atividades:
                print("-", a)
            atv = input("Atividade: ")
            if atv not in turma.atividades:
                print("Atividade não encontrada.")
                continue
            try:
                nota = float(input("Nota (0 a 10): "))
                if nota < 0 or nota > 10:
                    raise ValueError
            except ValueError:
                print("Nota inválida. Digite um número entre 0 e 10.")
                continue
            aluno.adicionar_nota(atv, nota)
            print("Nota lançada com sucesso!")
        elif opcao == "4":
            nome = input("Digite o nome para busca: ")
            resultados = buscar_aluno(nome, turma.alunos)
            if resultados:
                print("\n❰ RESULTADOS ❱")
                for a in resultados:
                    print(f"- {a.nome}")
            else:
                print("Nenhum aluno encontrado.")
        elif opcao == "5":
            palavra = input("Palavra-chave da atividade: ")
            resultados = buscar_atividade(palavra, turma)
            if resultados:
                print("\nAtividades encontradas:")
                for r in resultados:
                    print("-", r)
            else:
                print("Nenhuma atividade encontrada.")
        elif opcao == "6":
            relatorio_notas(turma)
        elif opcao == "7":
            nome = input("Nome do aluno: ")
            aluno_encontrado = buscar_aluno(nome, turma.alunos)
            if not aluno_encontrado:
                print("Aluno não encontrado.")
                continue
            aluno = aluno_encontrado[0]
            sugestoes = aluno.atividades_reforco()
            print("\n❰ SUGESTÃO DE REFORÇO ❱")
            if sugestoes:
                for s in sugestoes:
                    print(f"{s} — nota abaixo de 6")
            else:
                print("Nenhuma atividade precisa de reforço! Parabéns!")
        elif opcao == "8":
            turma.salvar_json()
        elif opcao == "0":
            turma.salvar_json()
            print("Encerrando o sistema...")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    menu()
