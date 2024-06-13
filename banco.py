
import mysql.connector
from mysql.connector import errorcode


print("Conexão a ser estabelecida...")
try:
      conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='1234'
      )
except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Usuário ou senha inválida')
      else:
            print(err)


cursor = conn.cursor()
cursor.execute("DROP DATABASE IF EXISTS `votacao`;")
cursor.execute("CREATE DATABASE `votacao`;")
cursor.execute("USE `votacao`;")

TABLES = {}
TABLES['Candidato'] = ('''
      CREATE TABLE `candidato` (
      `id` int(11) NOT NULL AUTO_INCREMENT,
      `nome` varchar(50) NOT NULL,
      `descricao` varchar(120) NOT NULL,
      `imagem` varchar(255) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Voto'] = ('''
      CREATE TABLE `voto` (
      `id` int(11) NOT NULL AUTO_INCREMENT,                     
      `candidato_id` int(11) NOT NULL,
      PRIMARY KEY (`id`),
      FOREIGN KEY (`candidato_id`) REFERENCES `candidato`(`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')


TABLES['Usuario'] = ('''
      CREATE TABLE `usuario` (
      `id` int(11) NOT NULL AUTO_INCREMENT,                     
      `login` varchar(20) NOT NULL,
      `senha` varchar(20) NOT NULL,
      PRIMARY KEY (`id`)
      ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabelaNome in TABLES:
      tabelaSQL = TABLES[tabelaNome]
      try:
            print('Criação da tabela {}:'.format(tabelaNome), end=' ')
            cursor.execute(tabelaSQL)
      except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                  print('Já existe')
            else:
                  print(err.msg)
      else:
            print('OK')

cursor.execute("INSERT INTO candidato (nome, descricao, imagem) VALUES ('João do Óculos', 'Cristão, compenetrado em ajudar a família rondonop...', 'candidato-a.png');")
cursor.execute("INSERT INTO candidato (nome, descricao, imagem) VALUES ('Ana da Prancheta', 'Mãe, batalhadora e focada em mudar o cenário femin...', 'candidata-b.png');")
cursor.execute("INSERT INTO candidato (nome, descricao, imagem) VALUES ('Polaco Kolynos', 'Alegre, determinado em vencer as mazelas de Rondon...', 'candidato-c.png');")

cursor.execute("INSERT INTO candidato (nome, descricao, imagem) VALUES ('Brancos', 'Votos em branco', 'camisa.png');")
cursor.execute("INSERT INTO candidato (nome, descricao, imagem) VALUES ('Nulos', 'Votos nulos', 'nulo.png');")

conn.commit()

cursor.close()
conn.close()