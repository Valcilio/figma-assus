from casa_lib.vault import Vault
vault = Vault().create()

import src.context as c

# Configuração Slack
slack_oath_token = input('Digite o token do Slack bot ("Sistema de Alertas (BETA)"): ')
slack_channel = input('Canal Slack para os alertas (sem #): ')
c.vault.add_key('slackbot', oath_token=slack_oath_token, channel=slack_channel)

# Configuração Postgres
print()
postgres_host = input('Digite o host do Postgres: ')
postgres_port = input('Digite a porta do host: ')
postgres_user = input('Digite o usuário do Postgres: ')
postgres_pass = input('Digite a senha do usuário: ')
postgres_schema = input('Digite o schema: ')

c.vault.add_key('postgres',
                host=postgres_host,
                port=postgres_port,
                user=postgres_user,
                password=postgres_pass,
                db=postgres_schema
               )