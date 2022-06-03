from infrastructure.email import *
# from teste import *
from catalog_config import CatalogConfig
import pandas as pd
import psycopg2 as pg
import logging


config = CatalogConfig()
config.read()



logger = logging.getLogger('Email SC Foward')
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)



logger.addHandler(ch)


df = ['id','name','email','churn']
data = []

conection = pg.connect(config['URL_POSTGRE']['URA'])
sql = "SELECT  seller_id, contact_nm, email_ds, case when churn_at_dt is not null then True else False end as seller_churn from vw_nodis_seller "
curs = conection.cursor()
curs.execute(sql)
for i in curs.fetchall():
    data.append(dict(zip(df,i)))

df1 = pd.json_normalize(data)
conection.close()
curs.close()





subjects = [
    {
        "type": "1",
        "title": "Cobrança Saldo Devedor Marketplace",
        "marketplace": "b2w",
        "template": "alteracao_dados_bancarios.html"
    },
    {
        "type":"2",
        "title": "Atualize seus dados bancários para receber o seu repasse",
        "marketplace":"b2w",
        "template":"bloqueia.html"
    },
    {   "type":"3",
        "title": "NOTIFICAÇÃO DE RESTRIÇÃO FINANCEIRA",
        "marketplace": "b2w",
        "template": "arquivo.html"
    },
    {
        "type":"4",
        "title": "Política de Frete: Saiba como será o seu desconto no custo de frete!",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"5",
        "title": "Política de Frete: Saiba como será a sua coparticipação no custo de frete!",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"6",
        "title": "IMPORTANTE: O local de postagem dos seus produtos foi alterado! Saiba mais",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"7",
        "title": "[AGÊNCIA MAGALU] - Alteração local de postagem",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"8",
        "title": "Aviso Importante: Sua loja possui notas fiscais inválidas",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"9",
        "title": "Aviso importante: Atualize os dados bancários!",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"10",
        "title": "Notificação Magalu | Aviso importante: seus produtos podem ser inativados",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"11",
        "title": "O local de postagem dos seus produtos foi alterado! Saiba mais",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"12",
        "title": "Notificação Magalu | Aviso importante: Ocorrência no Magalu Marketplace (desligamento por 15 dias)",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"13",
        "title": "Notificação Magalu | Aviso importante: Ocorrência no Magalu Marketplace (desligamento por 30 dias)",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"14",
        "title": "Nova denúncia de infração de propriedade intelectual",
        "marketplace": "b2w",
        "template": "arquivo.html"
    },
    {
        "type":"15",
        "title": "Parceiro, você possui itens com expedição em atraso!",
        "marketplace": "b2w",
        "template": "arquivo.html"
    },
    {
        "type":"16",
        "title": "[COMUNICADO] - Pedidos Magalu",
        "marketplace": "magalu",
        "template": "arquivo.html"
    },
    {
        "type":"17",
        "title": "Atenção ao prazo de entrega dos seus pedidos!",
        "marketplace": "b2w",
        "template": "arquivo.html"
    },
    {
        "type":"18",
        "title": "Notificação Magalu | Aviso importante: Seus itens precisam ser corrigidos",
        "marketplace": "magalu",
        "template": "arquivo.html"
    }


]

for subject in subjects:


        emails = (get_emails(config['EMAIL_API']['URL'],
                        subject['marketplace'],
                        subject['title'],logger)).json()

        rewrite(subject['type'], emails,logger,df1)


for i in subjects:
    send(config['KEY_SENDGRID']['URI'], i['type'], logger)

for i in subjects:
    postgre(i['type'], i['title'], logger,config['URL_POSTGRE']['URA'])




