import requests as r
import urllib.parse
import re
from bs4 import BeautifulSoup
import datetime
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import urllib3
import psycopg2 as pg
from psycopg2 import extras

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_emails(url, index, subject, log):

    try:
        p = {'index': f'{index}_sellers_gmail',
             'subjects': f'{subject}',
             'dt_from': f'{(datetime.date.today() - datetime.timedelta(18)).strftime("%Y-%m-%dT00:00:00")}',
             'dt_to': f'{(datetime.date.today() - datetime.timedelta(15)).strftime("%Y-%m-%dT23:59:59")}',
             'read': 'false',
             'get_read': 'true',
             'sent': 'false',
             'csv': 'false'

             }
        p_str = urllib.parse.urlencode(p, safe='%')
        return r.get(url, params=p_str, verify=False)
    except:
        log.warning('ERRO FUNÇÃO GET EMAILS')


resp = []


def rewrite(type, emails, log, df):

    if type == '1':
        count = 0
        try:
            for i in range(emails['qty']):
                inf = {}
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
                        f'Seller id não localizado na base de dados. FUNÇÃO INFO type = 1. Seller id {id_type_1}')
                    continue
                else:
                    inf.update({'email': 'testeautonodis@outlook.com'})
                # inf.update({'msg': string})
                # inf.update({'email_nodis': emails['emails'][i]['to']})
                inf.update({'id': id_type_1})
                inf.update({'type': '1'})
                inf.update({'titulo': emails['emails'][i]['subject']})
                # inf.update({
                #     'titulo_nodis': 'Você possui um saldo negativo com a Americanas Marketplace!'
                #         })
                inf.update({'date': datetime.date.today()})
                if inf not in resp:
                    resp.append(inf)
                else:
                    continue
                count += 1
            log.info(f'Quantidade e-mails type = 1: {count}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 1')

    # elif type == '2':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_2 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type =2. Nodis e-mail{seller_id}'
    #                 )
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_2]
    #             email_lista = "".join(info['email'].tolist())
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_2}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             data = open('static/alteracao_dados_bancarios.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             inf.update({'id': id_type_2})
    #             inf.update({'msg': str(soup)})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '2'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'Atualize seus dados bancários para receber o seu repasse!'
    #                        })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 2: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 2')

    elif type == '3':
        count = 0
        try:
            for i in range(emails['qty']):
                inf = {}
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
                    log.warning(
                        f'Não foi possível localizar as informações corretamente. FUNÇÂO REWRITE type = 3. Nodis e-mail {seller_id}'
                    )
                    continue
                if email_lista == '':
                    log.warning(
                        f'Seller id não localizado na base de dados. FUNÇÃO INFO type = 3. Seller id {id_type_3}')
                    continue
                else:
                    inf.update({'email': 'testeautonodis@outlook.com'})
                string = str(soup)
                string = re.sub(r'saldoneg', saldo, string)
                string = re.sub(r'dataneg', data_negativado, string)
                inf.update({'id': id_type_3})
                # inf.update({'msg': string})
                # inf.update({'email_nodis': emails['emails'][i]['to']})
                inf.update({'type': '3'})
                inf.update({'titulo': emails['emails'][i]['subject']})
                # inf.update({
                #     'titulo_nodis': 'Você possui um saldo negativo com a Americanas Marketplace!'
                #     })
                inf.update({'date': datetime.date.today()})
                if inf not in resp:
                    resp.append(inf)
                else:
                    continue
                count += 1
            log.info(f'Quantidade e-mails type = 3: {count}')
        except:
            log.warning('ERRO FUNÇÃO REWRITE TYPE = 3')

    # elif type == '4':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_4 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 4. Nodis e-mail {seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_4]
    #             email_lista = "".join(info['email'].tolist())
    #             data = open('static/politica_frete.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             name = emails['emails'][i]['body']
    #             regex_desconto = r"(?<=\bseu desconto no frete:\s)(\d+\%)"
    #             regex_desconto2 = r"(?<=\bpermanecerá na faixa de\s)(\d+\%)"
    #             try:
    #                 desconto = re.search(regex_desconto, name).group(0)
    #             except:
    #                 pass
    #                 try:
    #                     desconto = re.search(regex_desconto2, name).group(0)
    #                 except:
    #                     log.warning(
    #                         f'Não foi possível localizar as informações corretamente. FUNÇÂO REWRITE type = 4. Nodis e-mail, i {seller_id}'
    #                     )
    #                     continue
    #             if desconto == '0%':
    #                 grupo = 'Grupo 1'
    #                 percent_env = 'menos de 87%'
    #             elif desconto == '40%':
    #                 grupo = 'Grupo 2'
    #                 percent_env = 'de 87% à 97%'
    #             elif desconto == '75%':
    #                 grupo = 'Grupo 3'
    #                 percent_env = 'mais de 97%'
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_4}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             string = str(soup)
    #             string = re.sub(r'0% de', desconto, string)
    #             string = re.sub(r'Grupo 1', grupo, string)
    #             string = re.sub(r'menos de 87%', percent_env, string)
    #             inf.update({'id': id_type_4})
    #             inf.update({'msg': string})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '3'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'Sua pontuação para desconto na comissão MagaLu chegou! 👀'
    #                      })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 4: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 4')
    #
    # elif type == '5':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             seller_id = emails['emails'][i]['to']
    #             try:
    #                 id_type_5 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 5. Nodis e-mail {seller_id, i}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_5]
    #             email_lista = "".join(info['email'].tolist())
    #             data = open('static/politica_frete.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             name = emails['emails'][i]['body']
    #             regex_desconto = r"(?<=\bFaixa do seu desconto no frete:\s)(\d+\%)"
    #             try:
    #                 desconto = re.search(regex_desconto, name).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar as informações corretamente. FUNÇÂO REWRITE type = 5. Nodis e-mail {seller_id}'
    #                 )
    #                 continue
    #             if desconto == '0%':
    #                 grupo = 'Grupo 1'
    #                 percent_env = 'menos de 87%'
    #             elif desconto == '40%':
    #                 grupo = 'Grupo 2'
    #                 percent_env = 'de 87% à 97%'
    #             elif desconto == '75%':
    #                 grupo = 'Grupo 3'
    #                 percent_env = 'mais de 97%'
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_5}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             string = str(soup)
    #             string = re.sub(r'0% de', desconto, string)
    #             string = re.sub(r'Grupo 1', grupo, string)
    #             string = re.sub(r'menos de 87%', percent_env, string)
    #             inf.update({'id': id_type_5})
    #             inf.update({'msg': string})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '5'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'Sua pontuação para desconto na comissão MagaLu chegou! 👀'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 5: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 5')
    #
    # elif type == '6':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_6 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 6. Nodis e-mail{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_6]
    #             email_lista = "".join(info['email'].tolist())
    #             data = open('static/alteracao_local_mglu.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             name = emails['emails'][i]['body']
    #             regex_data = r"(?<=\bpara ocorrer no dia\s)(\d+\/[0-9]+)"
    #             regex_endereco = r"(?s)(?<=Magazine Luiza no endereço: ).*?(?=. Legal, né?)"
    #             try:
    #                 data = re.search(regex_data, name).group(0)
    #                 endereco = re.search(regex_endereco, name).group(0)
    #             except:
    #                 log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÃO REWRITE type = 6. Nodis e-mail {seller_id}')
    #                 continue
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_6}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             string = str(soup)
    #             string = re.sub(r'insertdata', data, string)
    #             string = re.sub(r'insertendereco', endereco, string)
    #             inf.update({'id': id_type_6})
    #             inf.update({'msg': string})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '6'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'O local de postagem dos seus produtos foi alterado!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 6: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 6')
    #
    # elif type == '7':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_7 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 7. Nodis e-mail{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_7]
    #             email_lista = "".join(info['email'].tolist())
    #             data = open('static/alteracao_local_mglu.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             name = emails['emails'][i]['body']
    #             regex_data = r"[0-9]{2}\/[0-9]{2}"
    #             regex_data2 = r"(?<=\bpara ocorrer no dia\s)(\d+\/[0-9]+)"
    #             regex_endereco = r"(?s)(?<=Magazine Luiza no endereço: ).*?(?=. Legal, né?)"
    #             regex_endereco2 = r"(?s)(?<=Magazine Luiza no endereço: ).*?(?=.Legal)"
    #             try:
    #                 data = re.search(regex_data, name).group(0)
    #             except:
    #                 try:
    #                     data = re.search(regex_data2, name).group(0)
    #                 except:
    #                     log.warning(f'Não foi possível localizar a Data. FUNÇÃO REWRITE type = 7. Nodis e-mail {seller_id}')
    #                     continue
    #             try:
    #                 endereco = re.search(regex_endereco, name).group(0)
    #             except:
    #                 try:
    #                     endereco = re.search(regex_endereco2, name).group(0)
    #                 except:
    #                     log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÃO REWRITE type = 7. Nodis e-mail {seller_id}')
    #                     continue
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_7}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             string = str(soup)
    #             string = re.sub(r'insertdata', data, string)
    #             string = re.sub(r'insertendereco', endereco, string)
    #             inf.update({'id': id_type_7})
    #             inf.update({'msg': string})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type':  '7'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'O local de postagem dos seus produtos foi alterado!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 7: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 7')
    #
    # elif type == '8':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_8 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 8. Nodis e-mails{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_8]
    #             email_lista = "".join(info['email'].tolist())
    #             data = open('static/nota_fiscal.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             name = emails['emails'][i]['body']
    #             regex_divergente = r"(?s)(?<=por conta de <br> ).*?(?= <br> Isso acontece)"
    #             regex_divergente2 = r"(?s)(?<=por conta de ).*?(?= <br> Isso acontece)"
    #             regex_divergente3 = r"(?s)(?<=por conta de\n).*?(?=\nIsso acontece)"
    #             try:
    #                 divergente = re.search(regex_divergente, name).group(0)
    #             except:
    #                 pass
    #                 try:
    #                     divergente = re.search(regex_divergente2, name).group(0)
    #                 except:
    #                     pass
    #                     try:
    #                         divergente = re.search(regex_divergente3, name).group(0)
    #                     except:
    #                         log.warning(f'Não foi possível localizar as informações corretamente. FUNÇÃO REWRITE type = 8. Nodis e-mail {seller_id}')
    #                         continue
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_8}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             string = str(soup)
    #             string = re.sub(r'default', divergente, string)
    #             inf.update({'email': id_type_8})
    #             inf.update({'msg': string})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update(({'type': '8'}))
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'Aviso Importante: Sua loja possui notas fiscais inválidas no Magalu Marketplace!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 8: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 8')
    #
    # elif type == '9':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_9 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 9. Nodis e-mail{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_9]
    #             email_lista = "".join(info['email'].tolist())
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_9}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             data = open('static/alteracao_dados_magalu.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             inf.update({'id': id_type_9})
    #             inf.update({'msg': str(soup)})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '9'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'Atualize seus dados bancários para receber o seu repasse!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 9: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 9')
    #
    # elif type =='10':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_10 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 10. Nodis e-mails{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_10]
    #             email_lista = "".join(info['email'].tolist())
    #             name = emails['emails'][i]['body']
    #             regex_produtos = r"(?s)(?<=PRODUTO ).*?(?= <br> \|)"
    #             regex_produtos2 = r"(?s)(?<=PRODUTO ).*?(?=\n|\nCOMO RESOLVER)"
    #             regex_resolver = r"(?s)(?<=COMO RESOLVER ).*?(?=. <br>)"
    #             regex_resolver2 = r"(?s)(?<=COMO RESOLVER ).*?(?=\n)"
    #             produtos = re.findall(regex_produtos, name)
    #             if len(produtos) == 0:
    #                 produtos = re.findall(regex_produtos2, name)
    #                 if len(produtos) == 0:
    #                     continue
    #             if len(produtos) > 1:
    #                 n = 2
    #                 splited = []
    #                 len_produtos = len(produtos)
    #                 for i in range(n):
    #                     start = int(i * len_produtos / n)
    #                     end = int((i + 1) * len_produtos / n)
    #                     splited.append(produtos[start:end])
    #             else:
    #                 print('Produtos = 1')
    #                 continue
    #             if len(splited[1]) <= 2:
    #                 string = open('static/produtos_inativos1.html').read()
    #             elif len(splited[1]) > 2 and len(splited[1]) <= 4:
    #                 string = open('static/produtos_inativos2.html').read()
    #             elif len(splited[1]) > 4 and len(splited[1]) <= 6:
    #                 string = open('static/produtos_inativos3.html').read()
    #             elif len(splited[1]) > 6:
    #                 string = open('static/produtos_inativos4.html').read()
    #             if len(splited[1]) <= 6:
    #                 for i in range(len(splited[1])):
    #                     string = re.sub(f'insert_produto{i+1}', f'PRODUTO {splited[1][i]}', string)
    #                 for i in range(6 - len(splited[1])):
    #                     string = re.sub(f'insert_produto{6-i}', '', string)
    #             elif len(splited[1]) > 6:
    #                 for i in range(len(splited[1])):
    #                     string = re.sub(f'insert_produto{i+1}', f'PRODUTO {splited[1][i]}', string)
    #                 for i in range(21 - len(splited[1])):
    #                     string = re.sub(f'insert_produto{21-i}', '', string)
    #             resolver = re.findall(regex_resolver, name)
    #             if len(resolver) == 0:
    #                 resolver = re.findall(regex_resolver2, name)
    #                 if len(resolver) == 0:
    #                     continue
    #             if len(resolver) > 1:
    #                 n = 2
    #                 splited2 = []
    #                 len_resolver = len(resolver)
    #                 for i in range(n):
    #                     start = int(i * len_resolver / n)
    #                     end = int((i + 1) * len_resolver / n)
    #                     splited2.append(resolver[start:end])
    #             else:
    #                 continue
    #             if len(splited2[1]) <= 6:
    #                 for i in range(len(splited2[1])):
    #                     string = re.sub(f'insert_prod{i + 1}', f'COMO RESOLVER {splited2[1][i]}', string)
    #                 for i in range(6 - len(splited2[1])):
    #                     string = re.sub(f'insert_prod{6 - i}', '', string)
    #             elif len(splited2[1]) > 6:
    #                 for i in range(len(splited2[1])):
    #                     string = re.sub(f'insert_prod{i + 1}', f'COMO RESOLVER {splited2[1][i]}', string)
    #                 for i in range(21 - len(splited2[1])):
    #                     string = re.sub(f'insert_prod{21 - i}', '', string)
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_10}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             inf.update({'id': id_type_10})
    #             inf.update({'msg': string})
    #             inf.update({'type': '10'})
    #             inf.update({'titulo': 'Notificação Magalu | Aviso importante: seus produtos podem ser inativados'})
    #             inf.update({
    #                 'titulo_nodis': 'Aviso Importante: Alguns de seus produtos no Magalu Marketplace podem ser inativados!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 10: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 10')
    #
    # elif type == '11':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
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
    #             try:
    #                 data = re.search(regex_data, name).group(0)
    #                 endereco = re.search(regex_endereco, name).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar as informações corretamente. FUNÇÃO REWRITE type = 11. Nodis e-mail {seller_id}')
    #                 continue
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_11}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             string = str(soup)
    #             string = re.sub(r'insertdata', data, string)
    #             string = re.sub(r'insertendereco', endereco, string)
    #             inf.update({'id': id_type_11})
    #             inf.update({'msg': string})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '11'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'O local de postagem dos seus produtos foi alterado!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 11: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 11')
    #
    # elif type == '12':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             regex_ticket = r"abra um novo ticket"
    #             body = emails['emails'][i]['body']
    #             try:
    #                 re.search(regex_ticket, body).group(0)
    #                 continue
    #             except:
    #                 pass
    #             try:
    #                 id_type_12 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 12. Nodis e-mail{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_12]
    #             email_lista = "".join(info['email'].tolist())
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_12}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             data = open('static/desligamento15dias.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             inf.update({'id': id_type_12})
    #             inf.update({'msg': str(soup)})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '12'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'mportante: Sua loja no Magalu será desligada por 15 dias!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 12: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 12')
    #
    # elif type == '13':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             regex_ticket = r"abra um novo ticket"
    #             body = emails['emails'][i]['body']
    #             try:
    #                 re.search(regex_ticket, body).group(0)
    #                 continue
    #             except:
    #                 pass
    #             try:
    #                 id_type_13 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 13. Nodis e-mail{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_13]
    #             email_lista = "".join(info['email'].tolist())
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_13}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             data = open('static/desligamento30dias.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             inf.update({'id': id_type_13})
    #             inf.update({'msg': str(soup)})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '13'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'Importante: Sua loja no Magalu será desligada por mais 30 dias!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 13: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 13')
    #
    # elif type == '14':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_14 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 14. Nodis e-mails{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_14]
    #             email_lista = "".join(info['email'].tolist())
    #             data = open('static/produtos_inativos_b2w.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             name = emails['emails'][i]['body']
    #             regex_titular = r"(?s)(?<=direitos).*?(?= alegando)"
    #             regex_produto = r"(?s)(?<=Nome do produto: ).*?(?= <br>)"
    #             regex_propriedade = r"(?s)(?<=Intelectual\(is\) <br> ).*?(?= <br>)"
    #             regex_tipo = r"(?s)(?<=Tipo: ).*?(?= <br>)"
    #             try:
    #                 titular = re.search(regex_titular, name).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar as informações. FUNÇÂO REWRITE type = 14. Nodis e-mails{seller_id}')
    #                 continue
    #             try:
    #                 produto = re.search(regex_produto, name).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar as informações. FUNÇÂO REWRITE type = 14. Nodis e-mails{seller_id}')
    #                 continue
    #             try:
    #                 propriedade = re.search(regex_propriedade, name).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar as informações. FUNÇÂO REWRITE type = 14. Nodis e-mails{seller_id}')
    #                 continue
    #             try:
    #                 tipo = re.search(regex_tipo, name).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar as informações. FUNÇÂO REWRITE type = 14. Nodis e-mails{seller_id}')
    #                 continue
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_14}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             string = str(soup)
    #             string = re.sub(r'FULANO', titular, string)
    #             string = re.sub(r'insert_produto', produto, string)
    #             string = re.sub(r'insert_propriedade', propriedade, string)
    #             string = re.sub(r'insert_tipo', f'Tipo: {tipo}', string)
    #             inf.update({'id': id_type_14})
    #             inf.update({'msg': string})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '14'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'Importante: Você recebeu uma denúncia de infração de propriedade intelectual na Americanas!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 14: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 14')
    #
    # elif type == '15':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_15 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 15. Nodis e-mail{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_15]
    #             email_lista = "".join(info['email'].tolist())
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_15}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             data = open('static/pedidos_atrasados_b2w.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             inf.update({'id': id_type_15})
    #             inf.update({'msg': str(soup)})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '15'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'IMPORTANTE: Você possui pedidos com expedição em atraso!!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 15: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 15')
    #
    # elif type == '16':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             regex_ticket = r"para abrir um ticket"
    #             body = emails['emails'][i]['body']
    #             try:
    #                 re.search(regex_ticket, body).group(0)
    #                 continue
    #             except:
    #                 pass
    #             try:
    #                 id_type_16 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 16. Nodis e-mail{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_16]
    #             email_lista = "".join(info['email'].tolist())
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_16}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             data = open('static/pedidos_atrasados_magalu.html').read()
    #             soup = BeautifulSoup(data, "html.parser")
    #             inf.update({'id': id_type_16})
    #             inf.update({'msg': str(soup)})
    #             inf.update({'email_nodis': emails['emails'][i]['to']})
    #             inf.update({'type': '16'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'IMPORTANTE: Você possui pedidos com expedição em atraso!!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 16: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 16')
    #
    # # elif type == '17':
    # #     try:
    # #         for i in range(emails['qty']):
    # #             seller_id = emails['emails'][i]['to']
    # #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    # #             try:
    # #                 id_type_17 = re.search(regex_id, seller_id).group(0)
    # #             except:
    # #                 log.warning(
    # #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 17. Nodis e-mail{seller_id}')
    # #                 continue
    # #             filtro_churn = df.loc[df['churn'] == False]
    # #             info = filtro_churn.loc[filtro_churn['id'] == id_type_17]
    # #             email_lista = "".join(info['email'].tolist())
    # #             if email_lista == '':
    # #                 log.info(f'O seller {id_type_17}, consta como churn na base')
    # #                 continue
    # #             else:
    # #                 if email_lista not in email_cliente_type_17:
    # #                     email_cliente_type_17.append(email_lista)
    # #                 else:
    # #                     continue
    # #             data = open('static/pedidos_atrasados_b2w.html').read()
    # #             soup = BeautifulSoup(data, "html.parser")
    # #             seller_id_type_17.append(id_type_17)
    # #             msg_type17.append(str(soup))
    # #             to17.append(emails['emails'][i]['to'])
    # #         log.info(f'Quantidade e-mails type = 17: {len(msg_type17)}')
    # #     except:
    # #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 17')
    #
    # elif type == '18':
    #     count = 0
    #     try:
    #         for i in range(emails['qty']):
    #             inf = {}
    #             seller_id = emails['emails'][i]['to']
    #             regex_id = r"(?s)(?<=\+).*?(?=@nodis)"
    #             try:
    #                 id_type_18 = re.search(regex_id, seller_id).group(0)
    #             except:
    #                 log.warning(
    #                     f'Não foi possível localizar o seller id. FUNÇÂO REWRITE type = 18. Nodis e-mails{seller_id}')
    #                 continue
    #             filtro_churn = df.loc[df['churn'] == False]
    #             info = filtro_churn.loc[filtro_churn['id'] == id_type_18]
    #             email_lista = "".join(info['email'].tolist())
    #             name = emails['emails'][i]['body']
    #             regex_produtos = r"(?s)(?<=PRODUTO ).*?(?= <br> \|)"
    #             regex_resolver = r"(?s)(?<=COMO RESOLVER ).*?(?=. <br>)"
    #             regex_produtos2 = r"(?s)(?<=PRODUTO).*?(?=\n|\nCOMO RESOLVER)"
    #             regex_resolver2 = r"(?s)(?<=COMO RESOLVER ).*?(?=.\nPor)"
    #             produtos = re.findall(regex_produtos, name)
    #             if len(produtos) == 0:
    #                 produtos = re.findall(regex_produtos2, name)
    #                 if len(produtos) == 0:
    #                     continue
    #             if len(produtos) > 1:
    #                 n = 2
    #                 splited = []
    #                 len_produtos = len(produtos)
    #                 for i in range(n):
    #                     start = int(i * len_produtos / n)
    #                     end = int((i + 1) * len_produtos / n)
    #                     splited.append(produtos[start:end])
    #             else:
    #                 continue
    #             if len(splited[1]) <= 2:
    #                 string = open('static/produtos_inativos1.html').read()
    #             elif len(splited[1]) > 2 and len(splited[1]) <= 4:
    #                 string = open('static/produtos_inativos2.html').read()
    #             elif len(splited[1]) > 4 and len(splited[1]) <= 6:
    #                 string = open('static/produtos_inativos3.html').read()
    #             elif len(splited[1]) > 6:
    #                 string = open('static/produtos_inativos4.html').read()
    #             if len(splited[1]) <= 6:
    #                 for i in range(len(splited[1])):
    #                     string = re.sub(f'insert_produto{i+1}', f'PRODUTO {splited[1][i]}', string)
    #                 for i in range(6 - len(splited[1])):
    #                     string = re.sub(f'insert_produto{6-i}', '', string)
    #             elif len(splited[1]) > 6:
    #                 for i in range(len(splited[1])):
    #                     string = re.sub(f'insert_produto{i+1}', f'PRODUTO {splited[1][i]}', string)
    #                 for i in range(21 - len(splited[1])):
    #                     string = re.sub(f'insert_produto{21-i}', '', string)
    #             resolver = re.findall(regex_resolver, name)
    #             if len(resolver) == 0:
    #                 resolver = re.findall(regex_resolver2, name)
    #                 if len(resolver) == 0:
    #                     continue
    #             if len(resolver) > 1:
    #                 n = 2
    #                 splited2 = []
    #                 len_resolver = len(resolver)
    #                 for i in range(n):
    #                     start = int(i * len_resolver / n)
    #                     end = int((i + 1) * len_resolver / n)
    #                     splited2.append(resolver[start:end])
    #             else:
    #                 continue
    #             if len(splited2[1]) <= 6:
    #                 for i in range(len(splited2[1])):
    #                     string = re.sub(f'insert_prod{i + 1}', f'COMO RESOLVER {splited2[1][i]}', string)
    #                 for i in range(6 - len(splited2[1])):
    #                     string = re.sub(f'insert_prod{6 - i}', '', string)
    #             elif len(splited2[1]) > 6:
    #                 for i in range(len(splited2[1])):
    #                     string = re.sub(f'insert_prod{i + 1}', f'COMO RESOLVER {splited2[1][i]}', string)
    #                 for i in range(21 - len(splited2[1])):
    #                     string = re.sub(f'insert_prod{21 - i}', '', string)
    #             if email_lista == '':
    #                 log.info(f'O seller {id_type_18}, consta como churn na base')
    #                 continue
    #             else:
    #                 inf.update({'email': 'testeautonodis@outlook.com'})
    #             inf.update({'id': id_type_18})
    #             inf.update({'msg': string})
    #             inf.update({'type': '18'})
    #             inf.update({'titulo': emails['emails'][i]['subject']})
    #             inf.update({
    #                 'titulo_nodis': 'Aviso Importante: Alguns de seus produtos no Magalu Marketplace podem ser inativados!'
    #                         })
    #             inf.update({'date': datetime.date.today()})
    #             if inf not in resp:
    #                 resp.append(inf)
    #             else:
    #                 continue
    #             count += 1
    #         log.info(f'Quantidade e-mails type = 18: {count}')
    #     except:
    #         log.warning('ERRO FUNÇÃO REWRITE TYPE = 18')


def send(key, log, resp):

    for i in range(len(resp)):
        message = Mail(
            from_email= 'atendimento@nodis.com.br',
            to_emails= resp[i]['email'],
            subject= resp[i]['titulo_nodis'],
            html_content= resp[i]['msg'])
        para = resp[i]['email']
        try:
            sg = SendGridAPIClient(key)
            response = sg.send(message)
            log.info(f'{response.status_code} encaminhado para: {para}')
        except Exception as e:
            print(e)


def postgre(log, key_postgre, resp):

    if len(resp) > 0:
        try:
            connection = pg.connect(key_postgre)
            curs = connection.cursor()
            postgres_insert_query = f""" INSERT INTO sc_email_foward (send_date,
                                            seller_id,
                                            subject,
                                            email_type,
                                            email_ds)
                                            VALUES (%(date)s,
                                            %(id)s,
                                            %(titulo)s,
                                            %(type)s,
                                            %(email)s)"""
            pg.extras.execute_batch(curs, postgres_insert_query, resp, page_size=len(resp))
            connection.commit()
            count = curs.rowcount
            log.info(count, "Record inserted successfully into mobile table")
            curs.close()
            connection.close()
            log.info("PostgreSQL connection is closed")
        except (Exception, pg.Error) as error:
            log.warning("Failed to insert record into mobile table", error)

# send(config['KEY_SENDGRID']['URI'], logger, resp)
#
# postgre(logger,config['URL_POSTGRE']['URA'], resp)