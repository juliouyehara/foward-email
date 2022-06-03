import requests as r
import urllib.parse
import re
from bs4 import BeautifulSoup
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import urllib3
import psycopg2 as pg

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_emails(url, index, subject, log):

    try:
        p = {'index': f'{index}_sellers_gmail',
             'subjects': f'{subject}',
             'dt_from': f'{(datetime.date.today() - datetime.timedelta(1)).strftime("%Y-%m-%dT00:00:00")}',
             'dt_to': f'{(datetime.date.today() - datetime.timedelta(1)).strftime("%Y-%m-%dT23:59:59")}',
             'read': 'false',
             'get_read': 'true',
             'sent': 'false',
             'csv': 'false'

             }
        p_str = urllib.parse.urlencode(p, safe='%')
        return r.get(url, params=p_str, verify=False)
    except:
        log.warning('ERRO FUNÇÃO GET EMAILS')


msg_type1 = []
msg_type2 = []
msg_type3 = []
msg_type4 = []
msg_type5 = []
msg_type6 = []
msg_type7 = []
msg_type8 = []
msg_type9 = []
msg_type10 = []
msg_type11 = []
msg_type12 = []
msg_type13 = []
msg_type14 = []
msg_type15 = []
msg_type16 = []
msg_type17 = []
msg_type18 = []

to1 = []
to2 = []
to3 = []
to4 = []
to5 = []
to6 = []
to7 = []
to8 = []
to9 = []
to10 = []
to11 = []
to12 = []
to13 = []
to14 = []
to15 = []
to16 = []
to17 = []
to18 = []

seller_id_type_1 = []
seller_id_type_2 = []
seller_id_type_3 = []
seller_id_type_4 = []
seller_id_type_5 = []
seller_id_type_6 = []
seller_id_type_7 = []
seller_id_type_8 = []
seller_id_type_9 = []
seller_id_type_10 = []
seller_id_type_11 = []
seller_id_type_12 = []
seller_id_type_13 = []
seller_id_type_14 = []
seller_id_type_15 = []
seller_id_type_16 = []
seller_id_type_17 = []
seller_id_type_18 = []


email_cliente_type_1 = []
email_cliente_type_2 = []
email_cliente_type_3 = []
email_cliente_type_4 = []
email_cliente_type_5 = []
email_cliente_type_6 = []
email_cliente_type_7 = []
email_cliente_type_8 = []
email_cliente_type_9 = []
email_cliente_type_10 = []
email_cliente_type_11 = []
email_cliente_type_12 = []
email_cliente_type_13 = []
email_cliente_type_14 = []
email_cliente_type_15 = []
email_cliente_type_16 = []
email_cliente_type_17 = []
email_cliente_type_18 = []


def rewrite(type, emails, log, df):
    if type == '1':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_1 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 1. Nodis e-mail {seller_id}')
                    continue
                info = df[df['id'].str.match(id_type_1, na=False)]
                email_lista = "".join(info['email'].tolist())
                data = open('static/bloqueia.html').read()
                soup = BeautifulSoup(data, "html.parser")
                body = emails['emails'][i]['body']
                regex_valor = r"(?s)(?<=Valor: R\$).*?(?= <br>)"
                regex_valor2 = r"(?s)(?<=R\$ <br> ).*?(?=. <br>)"
                try:
                    valor = re.search(regex_valor, body).group(0)
                except:
                    pass
                    try:
                        valor = re.search(regex_valor2, body).group(0)
                    except:
                        valor = '-'
                string = str(soup)
                if valor == '-':
                    saldo = 'Saldo Negativo'
                    string = re.sub('insert_valor', saldo, string)
                elif valor != '-':
                    string = re.sub('insert_valor', f'Saldo Negativo de R$ {valor}', string)
                if email_lista == '':
                    log.warning(
                        f'Seller id não localizado na base de dados. FUNÇÃO INFO type = 1. Seller id {seller_id_type_1}')
                    continue
                else:
                    if email_lista not in email_cliente_type_1:
                        email_cliente_type_1.append(email_lista)
                    else:
                        continue
                msg_type1.append(string)
                to1.append(emails['emails'][i]['to'])
                seller_id_type_1.append(id_type_1)
            log.info(f'Quantidade e-mails type = 1: {len(msg_type1)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 1')

    elif type == '2':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_2 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type =2. Nodis e-mail{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_2]
                email_lista = "".join(info['email'].tolist())
                if email_lista == '':
                    log.info(f'O seller {id_type_2}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_2:
                        email_cliente_type_2.append(email_lista)
                    else:
                        continue
                data = open('static/alteracao_dados_bancarios.html').read()
                soup = BeautifulSoup(data, "html.parser")
                seller_id_type_2.append(id_type_2)
                msg_type2.append(str(soup))
                to2.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 2: {len(msg_type2)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 2')

    elif type == '3':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_3 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 3. Nodis e-mail {seller_id}')
                    continue
                info = df[df['id'].str.match(id_type_3, na=False)]
                email_lista = "".join(info['email'].tolist())
                data = open('static/saldo_negativo.html').read()
                soup = BeautifulSoup(data,"html.parser")
                name = emails['emails'][i]['body']
                regex_saldo = r"(?s)(?<=R\$ ).*?(?=Data)"
                regex_data = r"[^Data Início Negativo: ]\d+/\d+/\d+"
                try:
                    saldo = re.search(regex_saldo, name).group(0)
                    data_negativado = re.search(regex_data, name).group(0)
                except:
                    log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÂO REWRITE type = 3. Nodis e-mail {seller_id}')
                    continue
                if email_lista == '':
                    log.warning(
                        f'Seller id não localizado na base de dados. FUNÇÃO INFO type = 3. Seller id {id_type_3}')
                    continue
                else:
                    if email_lista not in email_cliente_type_3:
                        email_cliente_type_3.append(email_lista)
                    else:
                        continue
                string = str(soup)
                string = re.sub(r'saldoneg', saldo, string)
                string = re.sub(r'dataneg', data_negativado, string)
                seller_id_type_3.append(id_type_3)
                msg_type3.append(string)
                to3.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 3: {len(msg_type3)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 3')

    elif type == '4':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_4 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 4. Nodis e-mail {seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_4]
                email_lista = "".join(info['email'].tolist())
                data = open('static/politica_frete.html').read()
                soup = BeautifulSoup(data,"html.parser")
                name = emails['emails'][i]['body']
                regex_desconto = r"(?<=\bseu desconto no frete:\s)(\d+\%)"
                regex_desconto2 = r"(?<=\bpermanecerá na faixa de\s)(\d+\%)"
                try:
                    desconto = re.search(regex_desconto, name).group(0)
                except:
                    pass
                    try:
                        desconto = re.search(regex_desconto2, name).group(0)
                    except:
                        log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÂO REWRITE type = 4. Nodis e-mail, i {seller_id, i}')
                        continue
                if desconto == '0%':
                    grupo = 'Grupo 1'
                    percent_env = 'menos de 87%'
                elif desconto == '40%':
                    grupo = 'Grupo 2'
                    percent_env = 'de 87% à 97%'
                elif desconto == '75%':
                    grupo = 'Grupo 3'
                    percent_env = 'mais de 97%'
                if email_lista == '':
                    log.info(f'O seller {id_type_4}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_4:
                        email_cliente_type_4.append(email_lista)
                    else:
                        continue
                string = str(soup)
                string = re.sub(r'0% de', desconto, string)
                string = re.sub(r'Grupo 1', grupo, string)
                string = re.sub(r'menos de 87%', percent_env, string)
                seller_id_type_4.append(id_type_4)
                msg_type4.append(string)
                to4.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 4: {len(msg_type4)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 4')

    elif type == '5':
        try:
            for i in range(emails['qty']):
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                seller_id = emails['emails'][i]['to']
                try:
                    id_type_5 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 5. Nodis e-mail {seller_id, i}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_5]
                email_lista = "".join(info['email'].tolist())
                data = open('static/politica_frete.html').read()
                soup = BeautifulSoup(data, "html.parser")
                name = emails['emails'][i]['body']
                regex_desconto = r"(?<=\bFaixa do seu desconto no frete:\s)(\d+\%)"
                try:
                    desconto = re.search(regex_desconto, name).group(0)
                except:
                    log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÂO REWRITE type = 5. Nodis e-mail {seller_id}')
                    continue
                if desconto == '0%':
                    grupo = 'Grupo 1'
                    percent_env = 'menos de 87%'
                elif desconto == '40%':
                    grupo = 'Grupo 2'
                    percent_env = 'de 87% à 97%'
                elif desconto == '75%':
                    grupo = 'Grupo 3'
                    percent_env = 'mais de 97%'
                if email_lista == '':
                    log.info(f'O seller {id_type_5}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_5:
                        email_cliente_type_5.append(email_lista)
                    else:
                        continue
                string = str(soup)
                string = re.sub(r'0% de', desconto, string)
                string = re.sub(r'Grupo 1', grupo, string)
                string = re.sub(r'menos de 87%', percent_env, string)
                seller_id_type_5.append(id_type_5)
                msg_type5.append(string)
                to5.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 5: {len(msg_type5)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 5')
    elif type == '6':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_6 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 6. Nodis e-mail{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_6]
                email_lista = "".join(info['email'].tolist())
                data = open('static/alteracao_local_mglu.html').read()
                soup = BeautifulSoup(data, "html.parser")
                name = emails['emails'][i]['body']
                regex_data = r"(?<=\bpara ocorrer no dia\s)(\d+\/[0-9]+)"
                regex_endereco = r"(?s)(?<=Magazine Luiza no endereço: ).*?(?=. Legal, né?)"
                regex_endereco2 = r"(?s)(?<=Magazine Luiza no endereço abaixo:\n).*?(?=\nLegal)"
                try:
                    data = re.search(regex_data, name).group(0)
                except:
                    log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÃO REWRITE type = 6. Nodis e-mail {seller_id}')
                    continue
                try:
                    endereco = re.search(regex_endereco, name).group(0)
                except:
                    pass
                    try:
                        endereco = re.search(regex_endereco2, name).group(0)
                    except:
                        log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÃO REWRITE type = 6. Nodis e-mail {seller_id}')
                        continue
                if email_lista == '':
                    log.info(f'O seller {id_type_6}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_6:
                        email_cliente_type_6.append(email_lista)
                    else:
                        continue
                string = str(soup)
                string = re.sub(r'insertdata', data, string)
                string = re.sub(r'insertendereco', endereco, string)
                seller_id_type_6.append(id_type_6)
                msg_type6.append(string)
                to6.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 6: {len(msg_type6)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 6')

    elif type == '7':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_7 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 7. Nodis e-mail{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_7]
                email_lista = "".join(info['email'].tolist())
                data = open('static/alteracao_local_mglu.html').read()
                soup = BeautifulSoup(data, "html.parser")
                name = emails['emails'][i]['body']
                regex_data = r"[0-9]{2}\/[0-9]{2}"
                regex_data2 = r"(?<=\bpara ocorrer no dia\s)(\d+\/[0-9]+)"
                regex_endereco = r"(?s)(?<=Magazine Luiza no endereço: ).*?(?=. Legal, né?)"
                regex_endereco2 = r"(?s)(?<=Magazine Luiza no endereço: ).*?(?=.Legal)"
                try:
                    data = re.search(regex_data, name).group(0)
                except:
                    try:
                        data = re.search(regex_data2, name).group(0)
                    except:
                        log.warning(f'Não foi possível localizar a Data. FUNÇÃO REWRITE type = 7. Nodis e-mail {seller_id}')
                        continue
                try:
                    endereco = re.search(regex_endereco, name).group(0)
                except:
                    try:
                        endereco = re.search(regex_endereco2, name).group(0)
                    except:
                        log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÃO REWRITE type = 7. Nodis e-mail {seller_id}')
                        continue
                if email_lista == '':
                    log.info(f'O seller {id_type_7}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_7:
                        email_cliente_type_7.append(email_lista)
                    else:
                        continue
                string = str(soup)
                string = re.sub(r'insertdata', data, string)
                string = re.sub(r'insertendereco', endereco, string)
                seller_id_type_7.append(id_type_7)
                msg_type7.append(string)
                to7.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 7: {len(msg_type7)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 7')

    elif type =='8':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_8 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 8. Nodis e-mails{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_8]
                email_lista = "".join(info['email'].tolist())
                data = open('static/nota_fiscal.html').read()
                soup = BeautifulSoup(data, "html.parser")
                name = emails['emails'][i]['body']
                regex_divergente = r"(?s)(?<=por conta de <br> ).*?(?= <br> Isso acontece)"
                regex_divergente2 = r"(?s)(?<=por conta de ).*?(?= <br> Isso acontece)"
                regex_divergente3 = r"(?s)(?<=por conta de\n).*?(?=\nIsso acontece)"
                try:
                    divergente = re.search(regex_divergente, name).group(0)
                except:
                    pass
                    try:
                        divergente = re.search(regex_divergente2, name).group(0)
                    except:
                        pass
                        try:
                            divergente = re.search(regex_divergente3, name).group(0)
                        except:
                            log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÃO REWRITE type = 8. Nodis e-mail {seller_id}')
                            continue
                if email_lista == '':
                    log.info(f'O seller {id_type_8}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_8:
                        email_cliente_type_8.append(email_lista)
                    else:
                        continue
                string = str(soup)
                string = re.sub(r'default', divergente, string)
                seller_id_type_8.append(id_type_8)
                msg_type8.append(string)
                to8.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 8: {len(msg_type8)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 8')

    elif type == '9':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_9 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 9. Nodis e-mail{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_9]
                email_lista = "".join(info['email'].tolist())
                if email_lista == '':
                    log.info(f'O seller {id_type_9}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_9:
                        email_cliente_type_9.append(email_lista)
                    else:
                        continue
                data = open('static/alteracao_dados_magalu.html').read()
                soup = BeautifulSoup(data, "html.parser")
                seller_id_type_9.append(id_type_9)
                msg_type9.append(str(soup))
                to9.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 9: {len(msg_type9)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 9')


    elif type =='10':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_10 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 10. Nodis e-mails{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_10]
                email_lista = "".join(info['email'].tolist())
                name = emails['emails'][i]['body']
                regex_produtos = r"(?s)(?<=PRODUTO ).*?(?= <br> \|)"
                regex_produtos2 = r"(?s)(?<=PRODUTO ).*?(?=\n|\nCOMO RESOLVER)"
                regex_resolver = r"(?s)(?<=COMO RESOLVER ).*?(?=. <br>)"
                regex_resolver2 = r"(?s)(?<=COMO RESOLVER ).*?(?=\n)"
                produtos = re.findall(regex_produtos, name)
                if len(produtos) == 0:
                    produtos = re.findall(regex_produtos2, name)
                    if len(produtos) == 0:
                        continue
                if len(produtos) > 1:
                    n = 2
                    splited = []
                    len_produtos = len(produtos)
                    for i in range(n):
                        start = int(i * len_produtos / n)
                        end = int((i + 1) * len_produtos / n)
                        splited.append(produtos[start:end])
                else:
                    print('Produtos = 1')
                    continue
                if len(splited[1]) <= 2:
                    string = open('static/produtos_inativos1.html').read()
                elif len(splited[1]) > 2 and len(splited[1]) <= 4:
                    string = open('static/produtos_inativos2.html').read()
                elif len(splited[1]) > 4 and len(splited[1]) <= 6:
                    string = open('static/produtos_inativos3.html').read()
                elif len(splited[1]) > 6:
                    string = open('static/produtos_inativos4.html').read()
                if len(splited[1]) <= 6:
                    for i in range(len(splited[1])):
                        string = re.sub(f'insert_produto{i+1}', f'PRODUTO {splited[1][i]}', string)
                    for i in range(6 - len(splited[1])):
                        string = re.sub(f'insert_produto{6-i}', '', string)
                elif len(splited[1]) > 6:
                    for i in range(len(splited[1])):
                        string = re.sub(f'insert_produto{i+1}', f'PRODUTO {splited[1][i]}', string)
                    for i in range(21 - len(splited[1])):
                        string = re.sub(f'insert_produto{21-i}', '', string)
                resolver = re.findall(regex_resolver, name)
                if len(resolver) == 0:
                    resolver = re.findall(regex_resolver2, name)
                    if len(resolver) == 0:
                        continue
                if len(resolver) > 1:
                    n = 2
                    splited2 = []
                    len_resolver = len(resolver)
                    for i in range(n):
                        start = int(i * len_resolver / n)
                        end = int((i + 1) * len_resolver / n)
                        splited2.append(resolver[start:end])
                else:
                    continue
                if len(splited2[1]) <= 6:
                    for i in range(len(splited2[1])):
                        string = re.sub(f'insert_prod{i + 1}', f'COMO RESOLVER {splited2[1][i]}', string)
                    for i in range(6 - len(splited2[1])):
                        string = re.sub(f'insert_prod{6 - i}', '', string)
                elif len(splited2[1]) > 6:
                    for i in range(len(splited2[1])):
                        string = re.sub(f'insert_prod{i + 1}', f'COMO RESOLVER {splited2[1][i]}', string)
                    for i in range(21 - len(splited2[1])):
                        string = re.sub(f'insert_prod{21 - i}', '', string)
                if email_lista == '':
                    log.info(f'O seller {id_type_10}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_10:
                        email_cliente_type_10.append(email_lista)
                    else:
                        continue
                seller_id_type_10.append(id_type_10)
                msg_type10.append(string)
            log.info(f'Quantidade e-mails type = 10: {len(msg_type10)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 10')

    # elif type == '11':
    #     try:
    #         for i in range(emails['qty']):
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_11 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 11. Nodis e-mail{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_11]
    #             email_lista = "".join(info['email'].tolist())
    #             data = open('static/alteracao_local_mglu.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             name = emails['emails'][i]['body']
    #             regex_data = r"(?<=\bpara ocorrer no dia\s)(\d+\/[0-9]+)"
    #             regex_endereco = r"(?s)(?<=Magazine Luiza no endereço: ).*?(?=. Legal, né?)"
    #             regex_endereco2 = r"(?s)(?<=Magazine Luiza no endereço abaixo:\n).*?(?=\nLegal)"
    #             try:
    #                 data = re.search(regex_data, name).group(0)
    #             except:
    #                 continue
    #             try:
    #                 endereco = re.search(regex_endereco, name).group(0)
    #             except:
    #                 pass
    #                 try:
    #                     endereco = re.search(regex_endereco2, name).group(0)
    #                 except:
    #                     log.warning(
    #                         f'Não foi possível localizar as informações corretamente. FUNÇÃO REWRITE type = 11. Nodis e-mail {seller_id}')
    #                     continue
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_11}, consta como churn na base')
    #                 continue
    #             else:
    #                 if email_lista not in email_cliente_type_11:
    #                     email_cliente_type_11.append(email_lista)
    #                 else:
    #                     continue
    #             string = str(soup)
    #             string = re.sub(r'insertdata', data, string)
    #             string = re.sub(r'insertendereco', endereco, string)
    #             seller_id_type_11.append(id_type_11)
    #             msg_type11.append(string)
    #             to11.append(emails['emails'][i]['to'])
    #         log.info(f'Quantidade e-mails type = 11: {len(msg_type11)}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 11')

    elif type == '12':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                regex_ticket = r"abra um novo ticket"
                body = emails['emails'][i]['body']
                try:
                    re.search(regex_ticket, body).group(0)
                    continue
                except:
                    pass
                try:
                    id_type_12 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 12. Nodis e-mail{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_12]
                email_lista = "".join(info['email'].tolist())
                if email_lista == '':
                    log.info(f'O seller {id_type_12}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_12:
                        email_cliente_type_12.append(email_lista)
                    else:
                        continue
                data = open('static/desligamento15dias.html').read()
                soup = BeautifulSoup(data, "html.parser")
                seller_id_type_12.append(id_type_12)
                msg_type12.append(str(soup))
                to12.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 12: {len(msg_type12)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 12')

    elif type == '13':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                regex_ticket = r"abra um novo ticket"
                body = emails['emails'][i]['body']
                try:
                    re.search(regex_ticket, body).group(0)
                    continue
                except:
                    pass
                try:
                    id_type_13 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 13. Nodis e-mail{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_13]
                email_lista = "".join(info['email'].tolist())
                if email_lista == '':
                    log.info(f'O seller {id_type_13}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_13:
                        email_cliente_type_13.append(email_lista)
                    else:
                        continue
                data = open('static/desligamento30dias.html').read()
                soup = BeautifulSoup(data, "html.parser")
                seller_id_type_13.append(id_type_13)
                msg_type13.append(str(soup))
                to13.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 13: {len(msg_type13)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 13')

    elif type =='14':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_14 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 14. Nodis e-mails{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_14]
                email_lista = "".join(info['email'].tolist())
                data = open('static/produtos_inativos_b2w.html').read()
                soup = BeautifulSoup(data, "html.parser")
                name = emails['emails'][i]['body']
                regex_titular = r"(?s)(?<=direitos).*?(?= alegando)"
                regex_produto = r"(?s)(?<=Nome do produto: ).*?(?= <br>)"
                regex_propriedade = r"(?s)(?<=Intelectual\(is\) <br> ).*?(?= <br>)"
                regex_tipo = r"(?s)(?<=Tipo: ).*?(?= <br>)"
                try:
                    titular = re.search(regex_titular, name).group(0)
                except:
                    continue
                try:
                    produto = re.search(regex_produto,name).group(0)
                except:
                    continue
                try:
                    propriedade = re.search(regex_propriedade, name).group(0)
                except:
                    continue
                try:
                    tipo = re.search(regex_tipo, name).group(0)
                except:
                    continue
                if email_lista == '':
                    log.info(f'O seller {id_type_14}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_14:
                        email_cliente_type_14.append(email_lista)
                    else:
                        continue
                string = str(soup)
                string = re.sub(r'FULANO', titular, string)
                string = re.sub(r'insert_produto', produto, string)
                string = re.sub(r'insert_propriedade', propriedade, string)
                string = re.sub(r'insert_tipo', f'Tipo: {tipo}', string)
                seller_id_type_14.append(id_type_14)
                msg_type14.append(string)
                to14.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 14: {len(msg_type14)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 14')

    elif type == '15':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_15 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 15. Nodis e-mail{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_15]
                email_lista = "".join(info['email'].tolist())
                if email_lista == '':
                    log.info(f'O seller {id_type_15}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_15:
                        email_cliente_type_15.append(email_lista)
                    else:
                        continue
                data = open('static/pedidos_atrasados_b2w.html').read()
                soup = BeautifulSoup(data, "html.parser")
                seller_id_type_15.append(id_type_15)
                msg_type15.append(str(soup))
                to15.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 15: {len(msg_type15)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 15')

    elif type == '16':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                regex_ticket = r"para abrir um ticket"
                body = emails['emails'][i]['body']
                try:
                    re.search(regex_ticket, body).group(0)
                    continue
                except:
                    pass
                try:
                    id_type_16 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 16. Nodis e-mail{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_16]
                email_lista = "".join(info['email'].tolist())
                if email_lista == '':
                    log.info(f'O seller {id_type_16}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_16:
                        email_cliente_type_16.append(email_lista)
                    else:
                        continue
                data = open('static/pedidos_atrasados_magalu.html').read()
                soup = BeautifulSoup(data, "html.parser")
                seller_id_type_16.append(id_type_16)
                msg_type16.append(str(soup))
                to16.append(emails['emails'][i]['to'])
            log.info(f'Quantidade e-mails type = 16: {len(msg_type16)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 16')

    # elif type == '17':
    #     try:
    #         for i in range(emails['qty']):
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_17 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 17. Nodis e-mail{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_17]
    #             email_lista = "".join(info['email'].tolist())
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_17}, consta como churn na base')
    #                 continue
    #             else:
    #                 if email_lista not in email_cliente_type_17:
    #                     email_cliente_type_17.append(email_lista)
    #                 else:
    #                     continue
    #             data = open('static/pedidos_atrasados_b2w.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             seller_id_type_17.append(id_type_17)
    #             msg_type17.append(str(soup))
    #             to17.append(emails['emails'][i]['to'])
    #         log.info(f'Quantidade e-mails type = 17: {len(msg_type17)}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 17')

    elif type =='18':
        try:
            for i in range(emails['qty']):
                seller_id = emails['emails'][i]['to']
                regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
                try:
                    id_type_18 = re.search(regex_id, seller_id).group(0)
                except:
                    log.warning(
                        f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 18. Nodis e-mails{seller_id}')
                    continue
                filtro_churn = df.loc[df['churn'] == False]
                info = filtro_churn.loc[filtro_churn['id'] == id_type_18]
                email_lista = "".join(info['email'].tolist())
                name = emails['emails'][i]['body']
                regex_produtos = r"(?s)(?<=PRODUTO ).*?(?= <br> \|)"
                regex_resolver = r"(?s)(?<=COMO RESOLVER ).*?(?=. <br>)"
                regex_produtos2 = r"(?s)(?<=PRODUTO).*?(?=\n|\nCOMO RESOLVER)"
                regex_resolver2 = r"(?s)(?<=COMO RESOLVER ).*?(?=.\nPor)"
                produtos = re.findall(regex_produtos, name)
                if len(produtos) == 0:
                    produtos = re.findall(regex_produtos2, name)
                    if len(produtos) == 0:
                        continue
                if len(produtos) > 1:
                    n = 2
                    splited = []
                    len_produtos = len(produtos)
                    for i in range(n):
                        start = int(i * len_produtos / n)
                        end = int((i + 1) * len_produtos / n)
                        splited.append(produtos[start:end])
                else:
                    continue
                if len(splited[1]) <= 2:
                    string = open('static/produtos_inativos1.html').read()
                elif len(splited[1]) > 2 and len(splited[1]) <= 4:
                    string = open('static/produtos_inativos2.html').read()
                elif len(splited[1]) > 4 and len(splited[1]) <= 6:
                    string = open('static/produtos_inativos3.html').read()
                elif len(splited[1]) > 6:
                    string = open('static/produtos_inativos4.html').read()
                if len(splited[1]) <= 6:
                    for i in range(len(splited[1])):
                        string = re.sub(f'insert_produto{i+1}', f'PRODUTO {splited[1][i]}', string)
                    for i in range(6 - len(splited[1])):
                        string = re.sub(f'insert_produto{6-i}', '', string)
                elif len(splited[1]) > 6:
                    for i in range(len(splited[1])):
                        string = re.sub(f'insert_produto{i+1}', f'PRODUTO {splited[1][i]}', string)
                    for i in range(21 - len(splited[1])):
                        string = re.sub(f'insert_produto{21-i}', '', string)
                resolver = re.findall(regex_resolver, name)
                if len(resolver) == 0:
                    resolver = re.findall(regex_resolver2, name)
                    if len(resolver) == 0:
                        continue
                if len(resolver) > 1:
                    n = 2
                    splited2 = []
                    len_resolver = len(resolver)
                    for i in range(n):
                        start = int(i * len_resolver / n)
                        end = int((i + 1) * len_resolver / n)
                        splited2.append(resolver[start:end])
                else:
                    continue
                if len(splited2[1]) <= 6:
                    for i in range(len(splited2[1])):
                        string = re.sub(f'insert_prod{i + 1}', f'COMO RESOLVER {splited2[1][i]}', string)
                    for i in range(6 - len(splited2[1])):
                        string = re.sub(f'insert_prod{6 - i}', '', string)
                elif len(splited2[1]) > 6:
                    for i in range(len(splited2[1])):
                        string = re.sub(f'insert_prod{i + 1}', f'COMO RESOLVER {splited2[1][i]}', string)
                    for i in range(21 - len(splited2[1])):
                        string = re.sub(f'insert_prod{21 - i}', '', string)
                if email_lista == '':
                    log.info(f'O seller {id_type_18}, consta como churn na base')
                    continue
                else:
                    if email_lista not in email_cliente_type_18:
                        email_cliente_type_18.append(email_lista)
                    else:
                        continue
                seller_id_type_18.append(id_type_18)
                msg_type18.append(string)
            log.info(f'Quantidade e-mails type = 18: {len(msg_type18)}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 18')

def send(key, type, log):

    if type == '1':
        try:
            for i in range(len(msg_type1)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails= email_cliente_type_1[i],
                    subject=f" Você possui um saldo negativo com a Americanas Marketplace!",
                    html_content=msg_type1[i])
                para = email_cliente_type_1[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 1, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 1')

    elif type == '2':
        try:
            for i in range(len(msg_type2)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_2[i],
                    subject="Atualize seus dados bancários para receber o seu repasse!",
                    html_content=msg_type2[i])
                para =  email_cliente_type_2[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 2, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 2')

    elif type == '3':
        try:
            for i in range(len(msg_type3)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_3[i],
                    subject="Você possui um saldo negativo com a Americanas Marketplace!",
                    html_content=msg_type3[i])
                para = email_cliente_type_3[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 3, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 3')
    elif type == '4':
        try:
            for i in range(len(msg_type4)):

                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails= email_cliente_type_4[i],
                    subject=f"Sua pontuação para desconto na comissão MagaLu chegou! 👀",
                    html_content=msg_type4[i])
                para = email_cliente_type_4[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 4, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 4')

    elif type == '5':
       try:
            for i in range(len(msg_type5)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_5[i],
                    subject=f"Sua pontuação para desconto na comissão MagaLu chegou! 👀",
                    html_content=msg_type5[i])
                para = email_cliente_type_5[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 5, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
       except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 5')

    elif type == '6':
        try:
            for i in range(len(msg_type6)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails= email_cliente_type_6[i],
                    subject=" IMPORTANTE: O local de postagem dos seus produtos foi alterado!",
                    html_content=msg_type6[i])
                para = email_cliente_type_6[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 6, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 6')

    elif type == '7':
        try:
            for i in range(len(msg_type7)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails= email_cliente_type_7[i],
                    subject=" IMPORTANTE: O local de postagem dos seus produtos foi alterado!",
                    html_content=msg_type7[i])
                para = email_cliente_type_7[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 7, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 7')

    elif type == '8':
        try:
            for i in range(len(msg_type8)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails= email_cliente_type_8[i],
                    subject="Aviso Importante: Sua loja possui notas fiscais inválidas no Magalu Marketplace!",
                    html_content=msg_type8[i])
                para = email_cliente_type_8[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 8, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 8')

    elif type == '9':
        try:
            for i in range(len(msg_type9)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_9[i],
                    subject="Atualize seus dados bancários para receber o seu repasse!",
                    html_content=msg_type9[i])
                para =  email_cliente_type_9[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 9, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 9')

    elif type == '10':
        try:
            for i in range(len(msg_type10)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_10[i],
                    subject="Aviso Importante: Alguns de seus produtos no Magalu Marketplace podem ser inativados!",
                    html_content=msg_type10[i])
                para =  email_cliente_type_10[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 10, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 10')

    elif type == '11':
        try:
            for i in range(len(msg_type11)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_11[i],
                    subject="IMPORTANTE: O local de postagem dos seus produtos foi alterado!",
                    html_content=msg_type11[i])
                para = email_cliente_type_11[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 11, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 11')

    elif type == '12':
        try:
            for i in range(len(msg_type12)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_12[i],
                    subject="Importante: Sua loja no Magalu será desligada por 15 dias!",
                    html_content=msg_type12[i])
                para = email_cliente_type_12[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 12, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 12')

    elif type == '13':
        try:
            for i in range(len(msg_type13)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_13[i],
                    subject="Importante: Sua loja no Magalu será desligada por mais 30 dias!",
                    html_content=msg_type13[i])
                para = email_cliente_type_13[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 13, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 13')

    elif type == '14':
        try:
            for i in range(len(msg_type14)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_14[i],
                    subject="Importante: Você recebeu uma denúncia de infração de propriedade intelectual na Americanas!",
                    html_content=msg_type14[i])
                para = email_cliente_type_14[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 14, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 14')

    elif type == '15':
        try:
            for i in range(len(msg_type15)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_15[i],
                    subject="IMPORTANTE: Você possui pedidos com expedição em atraso!!",
                    html_content=msg_type15[i])
                para = email_cliente_type_15[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 15, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 15')

    elif type == '16':
        try:
            for i in range(len(msg_type16)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_16[i],
                    subject="IMPORTANTE: Você possui pedidos com expedição em atraso!!",
                    html_content=msg_type16[i])
                para = email_cliente_type_16[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 16, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 16')

    # elif type == '17':
    #     try:
    #         for i in range(len(msg_type17)):
    #             message = Mail(
    #                 from_email='atendimento@nodis.com.br',
    #                 to_emails=email_cliente_type_17[i],
    #                 subject="IMPORTANTE: Você possui pedidos com expedição em atraso!!",
    #                 html_content=msg_type17[i])
    #             para = email_cliente_type_17[i]
    #             try:
    #                 sg = SendGridAPIClient(key)
    #                 response = sg.send(message)
    #                 log.info(f'{response.status_code} e-mail type = 17, encaminhado para: {para}')
    #             except Exception as e:
    #                 print(e.body)
    #     except:
    #         log.warning('ERRO FUNÇÃO SEND TYPE = 17')

    elif type == '18':
        try:
            for i in range(len(msg_type18)):
                message = Mail(
                    from_email='atendimento@nodis.com.br',
                    to_emails=email_cliente_type_18[i],
                    subject="Aviso Importante: Alguns de seus produtos no Magalu Marketplace podem ser inativados!",
                    html_content=msg_type18[i])
                para = email_cliente_type_18[i]
                try:
                    sg = SendGridAPIClient(key)
                    response = sg.send(message)
                    log.info(f'{response.status_code} e-mail type = 18, encaminhado para: {para}')
                except Exception as e:
                    print(e.body)
        except:
            log.warning('ERRO FUNÇÃO SEND TYPE = 18')

def postgre(type, subject, log, key_postgre):

    if type == '1':
            for i in range(len(msg_type1)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_1[i]}','{subject}','1','{email_cliente_type_1[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 1')

    elif type == '2':

            for i in range(len(msg_type2)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_2[i]}','{subject}','2','{email_cliente_type_2[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 2')

    elif type == '3':

            for i in range(len(msg_type3)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_3[i]}','{subject}','3','{email_cliente_type_3[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    print('ERRO FUNÇÃO POSTGRE TYPE = 3')

    elif type == '4':
            for i in range(len(msg_type4)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_4[i]}','{subject}','4','{email_cliente_type_4[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 4')

    elif type == '5':

            for i in range(len(msg_type5)):

                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_5[i]}','{subject}','5','{email_cliente_type_5[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 5')

    elif type == '6':

            for i in range(len(msg_type6)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_6[i]}','{subject}','6','{email_cliente_type_6[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 6')

    elif type == '7':

            for i in range(len(msg_type7)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_7[i]}','{subject}','7','{email_cliente_type_7[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 7')

    elif type == '8':
            for i in range(len(msg_type8)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_8[i]}','{subject}','8','{email_cliente_type_8[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 8')

    elif type == '9':

            for i in range(len(msg_type9)):

                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_9[i]}','{subject}','9','{email_cliente_type_9[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 9')

    elif type == '10':

            for i in range(len(msg_type10)):

                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_10[i]}','{subject}','10','{email_cliente_type_10[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 10')

    elif type == '11':

            for i in range(len(msg_type11)):

                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_11[i]}','{subject}','11','{email_cliente_type_11[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 11')

    elif type == '12':

            for i in range(len(msg_type12)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_12[i]}','{subject}','12','{email_cliente_type_12[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 12')

    elif type == '13':

            for i in range(len(msg_type13)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_13[i]}','{subject}','13','{email_cliente_type_13[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 13')

    elif type == '14':

            for i in range(len(msg_type14)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_14[i]}','{subject}','14','{email_cliente_type_14[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 14')

    elif type == '15':

            for i in range(len(msg_type15)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_15[i]}','{subject}','15','{email_cliente_type_15[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 15')

    elif type == '16':

            for i in range(len(msg_type16)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_16[i]}','{subject}','16','{email_cliente_type_16[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 16')

    # elif type == '17':
    #
    #         for i in range(len(msg_type17)):
    #             try:
    #                 conection = pg.connect(key_postgre)
    #                 sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_17[i]}','{subject}','17','{email_cliente_type_17[i]}')"
    #                 curs = conection.cursor()
    #                 curs.execute(sql)
    #                 conection.commit()
    #                 conection.close()
    #                 curs.close()
    #             except:
    #                 log.info('ERRO FUNÇÃO POSTGRE TYPE = 17')

    elif type == '18':

            for i in range(len(msg_type18)):
                try:
                    conection = pg.connect(key_postgre)
                    sql = f"INSERT INTO sc_email_foward (send_date, seller_id, subject,email_type, email_ds) VALUES ('{datetime.date.today()}','{seller_id_type_18[i]}','{subject}','18','{email_cliente_type_18[i]}')"
                    curs = conection.cursor()
                    curs.execute(sql)
                    conection.commit()
                    conection.close()
                    curs.close()
                except:
                    log.info('ERRO FUNÇÃO POSTGRE TYPE = 18')
