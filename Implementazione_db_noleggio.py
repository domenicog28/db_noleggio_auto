#pacchetto python/mysql installato pip install mysql-connector-python
#connessione

import mysql.connector

# connessione a mysql

dtb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
)

# creazione cursore

cursore = dtb.cursor()

#creazione database

cursore.execute("create database noleggio_auto;")

cursore.execute("use noleggio_auto;")

#creazione tabelle 

cursore.execute("create table clienti (id_cliente int primary key auto_increment, nome varchar (16) not null, cognome varchar (16) not null, tipo_via varchar (16) not null, nome_via varchar(16) not null, civ varchar(4) not null, cod_p char(5) not null, città varchar(16), n_tel char(10));")

cursore.execute("create table auto (targa char(7) primary key, marca varchar(16) not null, modello varchar(16) not null, colore varchar(16) not null, anno char(4) not null);")

cursore.execute("create table prenotazioni(id_prenotazioni int primary key auto_increment, data_prenotazione date not null, data_ritiro date not null, data_consegna date not null, cliente int not null references clienti(id_cliente), vettura char(7) not null references auto(targa))engine=innodb;")

cursore.execute("create table noleggio(id_noleggio int primary key auto_increment, cliente int not null references clienti(id_cliente), documento char(9) not null, vettura char(7) not null references auto(targa), data_ritiro date not null, data_consegna date not null)engine=innodb;")

cursore.execute("create table multe(id_multa char(5) primary key, data_multa date not null, importo decimal(4,2) not null, descrizione tinytext not null, noleggio int not null references noleggio(id_noleggio))engine=innodb;")

cursore.execute("create table pagamenti(id_pagamento int primary key auto_increment, noleggio int not null references noleggio(id_noleggio), cliente int not null references clienti(id_cliente), importo decimal(10,2) not null, num_carta char(16) not null)engine=innodb;")

cursore.execute("create table valutazioni(id_valutazione int primary key auto_increment, cliente int not null references clienti(id_cliente), vettura char(7) not null references auto(targa), data_valutazione date not null, valutazione enum('1','2','3','4','5') not null)engine=innodb;")

cursore.execute("create table manutenzioni(id_manutenzione int primary key auto_increment, vettura char(7) not null references auto(targa), data_manutenzione date not null, data_pross_manut date not null, importo decimal(5,2) not null)engine=innodb;")

cursore.execute("create table dipendenti(matricola char(4) primary key, nome varchar(16) not null, cognome varchar(16) not null, tipo_via varchar (16) not null, nome_via varchar(16) not null, civ varchar(4) not null, cod_p char(5) not null, città varchar(16), n_tel char(10), ruolo varchar(16) not null);")

cursore.execute("create table turni(id_turno int primary key auto_increment, dipendente char(4) not null references dipendenti(matricola), data date not null, turno enum ('m','p') not null)engine=innodb;")

#creazione indice

cursore.execute("create index dat_rit_con on prenotazioni (data_ritiro,data_consegna);")
cursore.execute("create index manut on manutenzioni(data_pross_manut);")

#inserimento dati nelle tabelle

in_cli="insert into clienti (nome,cognome,tipo_via,nome_via,civ,cod_p,città,n_tel) values(%s,%s,%s,%s,%s,%s,%s,%s);"
clienti=[
    ("gianni","fabri","piazza","roma","12","80968","firenze","3256985478"),
    ("antonio","cerenzia","via","spagna","6","87064","corigliano","3336547896"),
    ("carmela","prato","viale","della liberta","554","12065","torino","3201447856"),
    ("lorenzo","tito","piazza","del popolo","451","15066","milano","3665984752"),
    ("annina","fiorentino","via","del campo","54","10224","genova","3256647896"),
]

cursore.executemany(in_cli,clienti)

in_aut="insert into auto (targa,marca,modello,colore,anno) values(%s,%s,%s,%s,%s);"
vet=[
    ("cd556ty","ford","focus","grigio","2020"),
    ("fr859gb","mercedes","a180","nero","2022"),
    ("gg546fc","bmw","x1","grigio","2022"),
    ("gh554dc","ferrari","la ferrari","rosso","2014"),
    ("gf541ld","fiat","panda","azzurro","2023"),
]

cursore.executemany(in_aut,vet)

in_pren="insert into prenotazioni(data_prenotazione,data_ritiro,data_consegna,cliente,vettura) values(%s,%s,%s,%s,%s);"
pren=[
    ("2024-07-06","2024-08-31","2024-09-07",3,"gf541ld"),
    ("2024-07-15","2024-08-13","2024-08-20",4,"gg546fc"),
    ("2024-06-01","2024-06-07","2024-06-20",1,"fr859gb")
]

cursore.executemany(in_pren,pren)

in_nol= "insert into noleggio (cliente,documento,vettura,data_ritiro,data_consegna) values(%s,%s,%s,%s,%s);"
nol=[
    (1,"ca668sc","fr859gb","2024-06-07","2024-06-20")
]

cursore.executemany(in_nol,nol)

in_pag="insert into pagamenti(noleggio,cliente,importo,num_carta) values(%s,%s,%s,%s);"
pag=[
    (1,1,556.00,"1245630211558963"),
]

cursore.executemany(in_pag,pag)

in_val="insert into valutazioni(cliente,vettura,data_valutazione,valutazione) values(%s,%s,%s,%s);"
val=[
    (1,"fr859gb","2024-06-20","5"),
]

cursore.executemany(in_val,val)

in_man="insert into manutenzioni (vettura,data_manutenzione,data_pross_manut,importo) values(%s,%s,%s,%s);"
man=[
    ("cd556ty","2024-07-18","2025-07-18", 556.00),
]

cursore.executemany(in_man,man)

in_dip="insert into dipendenti(matricola,nome,cognome,tipo_via,nome_via,civ,cod_p,città,n_tel,ruolo) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
dip=[
    ("0001","claudio","lotito","piazza","firenze","5","12036","firmo","3200114569","accettazione"),
    ("0002","antonio","di gennaro","via","dei lattanti","6","12036","firmo","3002659856","parcheggiatore"),
    ("0003","francesco","sensi","via","del pozzo","7","12036","firmo","3210023652","autolavaggio"),
]

cursore.executemany(in_dip,dip)

in_tu="insert into turni (dipendente,data,turno) values(%s,%s,%s);"
tu=[
    ("0001","2024-07-20","m"),
    ("0002","2024-07-20","p"),
]

cursore.executemany(in_tu,tu)
dtb.commit()