from funcionalidades.funcionalidade_lembretes.manipulacao_de_embed import adiciona_info
from discord.embeds import Embed
from servicos import Bancos_De_Dados


class Lembrete():
    def __init__(self):
        self.caminho = 'funcionalidades/funcionalidade_lembretes/bancos'
        self.tabela = "Lembretes"
        self.banco_de_dados = Bancos_De_Dados(self.caminho)
        self.dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
        self.comandos = [["/klembretes", "Lista todos os lembretes do servidor."],
                    ["/kadicionar_lembrete (nome) (dia) (informação adicional)",
                     "Adiciona um lembrete"],
                    ["/kremover_lembrete (nome)", "Remove um lembrete do servidor."],
                         ["/khoje", "Exibe os lembretes correspondentes ao dia atual."],
                         ["/keditar_informacao_adicional (nome)",
                          "Edita as informações adicionais de um lembrete."],
                         ["/keditar_dia (nome)", "Edita o dia de um lembrete."],
                         ["/kmensagens_diarias",
                          "Informa os requisitos para implementar mensagens diarias no servidor."]]
        
    def ajuda(self):
        embed = Embed(title="Lista de Comandos:")
        comandos = self.comandos
        for comando in comandos:
            embed.add_field(name=comando[0], value=comando[1], inline=False)
        
        return adiciona_info(embed)

    def listar_lembretes_por_atributo(self, atributo, cursor, embed, atributo_especifico):
        cursor.execute("SELECT * FROM Lembretes WHERE Dia=?", (atributo,))
        lembretes_dia = cursor.fetchall()
        numero_lembretes = len(lembretes_dia)

        if lembretes_dia:
            if atributo_especifico:
                embed.description = 'Há {} lembrete(s)'.format(numero_lembretes)
            else:
                embed = embed.add_field(name="**{}**".format(atributo), value='Há {} lembrete(s)'.format(numero_lembretes), inline=False)

        for lembrete in lembretes_dia:
            descricao = "*Informação: %s*" % (lembrete[2])
            embed.add_field(name="> {}".format(lembrete[0]), value="> {}".format(descricao), inline=True)
        return embed

    def mostra_lembretes(self, nome_do_servidor, dia=None, autor=None):
        print('\nFunção mostra lembretes')
        banco_existe = self.banco_de_dados.verifica_banco(nome_do_servidor)
        dia_especifico = False
        if banco_existe:
            banco = self.banco_de_dados.acessar_banco(nome_do_servidor)
            cursor = banco.cursor()
            if dia:
                dia_especifico = True
                embed = Embed(title="Lembretes de **{}**".format(dia))
                embed = self.listar_lembretes_por_atributo(dia, cursor, embed, dia_especifico)
                if not embed.fields:
                    embed = Embed(title="Não há lembretes para **%s**" % dia)
                    embed = adiciona_info(embed, autor)
                    return embed
            else:
                embed = Embed(title="**Lembretes**")
                for dia in self.dias:
                    embed = self.listar_lembretes_por_atributo(dia, cursor, embed, dia_especifico)
                if not embed.fields:
                    embed = Embed(title="Não há lembretes neste servidor")
                    embed = adiciona_info(embed, autor)
                    return embed
            print("Mostra lembretes finalizada\n")
            embed = adiciona_info(embed, autor)
            return embed
        else:
            print("Mostrar_lembretes finalizada\n")
            embed = Embed(title="Este servidor não possui lembretes")
            embed = adiciona_info(embed, autor)
            return embed

    def adiciona_lembretes(self, nome_do_servidor, autor, nome, dia, adicional):
        print('\nFunção adicionar lembrete')
        dados = {"Nome": nome, "Dia": dia, "Adicional": adicional}
        if not self.banco_de_dados.insere_dados(nome_do_servidor, self.tabela, dados, "Nome"):
            embed = Embed(title="Falha ao inserir lembrete (nome já existe na lista?)")
            embed = adiciona_info(embed)
            print("Falha ao adicionar lembrete")
            return embed
        embed = Embed(title="Lembrete Inserido\n")
        embed = adiciona_info(embed, autor)
        embed.add_field(name=nome, value="Dia: %s\nInformação Adicional: %s" % (dia, adicional))
        print("Lembrete inserido com sucesso\n")
        return embed

    def remove_lembretes(self, nome_do_servidor, autor, nome):
        print('\nFunção remover lembrete')
        if not self.banco_de_dados.remove_dados(nome_do_servidor, self.tabela, nome, "Nome"):
            embed = Embed(title="Falha ao remover lembrete (nome não existe na lista?)")
            embed = adiciona_info(embed, autor)
            print("Falha ao remover lembrete\n")
            return embed
        embed = Embed(title="Lembrete para %s removido :)" % nome)
        embed = adiciona_info(embed, autor)
        print('Lembrete removido com sucesso\n')
        return embed

    def editar_lembrete(self, nome_do_servidor, autor, atributo, nome, dado):
        print("\nFunção editar lembretes")
        if not self.banco_de_dados.edita_dados(nome_do_servidor, self.tabela, atributo, dado, nome, "Nome"):
            embed = Embed(title="Falha ao editar lembrete (nome não existe na lista?)")
            embed = adiciona_info(embed, autor)
            print('Falha ao editar lembrete\n')
            return embed
        embed = Embed(title="Lembrete Atualizado")
        embed = adiciona_info(embed, autor)
        embed.add_field(name=nome, value="%s: %s" % (atributo, dado))
        print('Lembrete editado com sucesso\n')
        return embed
