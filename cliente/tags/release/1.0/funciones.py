# -*- coding: utf-8 -*-

import sqlite3

def crearDBCliente(PATH_DB):
    conn = sqlite3.connect(PATH_DB)
    cursor = conn.cursor()
    cursor.executescript("""
    CREATE TABLE usuarios(
    id               INTEGER PRIMARY KEY,
    username    TEXT    unique,
    admin         boolean,
    password     TEXT
    );

    CREATE TABLE dominios_permitidos(
        url               TEXT,
        usuario         INTEGER,
        FOREIGN KEY(usuario) REFERENCES usuario(id)
    );

    CREATE TABLE dominios_denegados(
        url               TEXT,
        usuario         INTEGER,
        FOREIGN KEY(usuario) REFERENCES usuario(id)
    );

    CREATE TABLE tipos_de_dominios(
        id       INTEGER PRIMARY KEY,
        tipo    TEXT
    );

    CREATE TABLE dominios_publicamente_permitidos(
        url               TEXT,
        tipo        INTEGER,
        FOREIGN KEY(tipo) REFERENCES tipos_de_dominios(id)
    );

    CREATE TABLE dominios_publicamente_denegados(
        url               TEXT,
        tipo        INTEGER,
        FOREIGN KEY(tipo) REFERENCES tipos_de_dominios(id)
    );

    CREATE TABLE cache_urls_aceptadas(
        url               TEXT,
        hora             time
    );

    CREATE TABLE cache_urls_denegadas(
        url               TEXT,
        hora             time
    );

    CREATE TABLE sincronizador(
        ultima_actualizacion  real
    );
    insert into usuarios(username,password,admin) values ('test_admin','098f6bcd4621d373cade4e832627b4f6',1);
    insert into usuarios(username,password,admin) values ('test_user','098f6bcd4621d373cade4e832627b4f6',0);
    insert into usuarios(username,password,admin) values ('admin','c6ed3da18b23913d2fd664985c5c5f13',1);
    insert into usuarios(username,password,admin) values ('mboscovich','c6ed3da18b23913d2fd664985c5c5f13',0);
    insert into usuarios(username,password,admin) values ('mguedes','c6ed3da18b23913d2fd664985c5c5f13',0);
    insert into usuarios(username,password,admin) values ('rtourn','c6ed3da18b23913d2fd664985c5c5f13',0);
    insert into usuarios(username,password,admin) values ('usuario','f8032d5cae3de20fcec887f395ec9a6a',0);
    insert into usuarios(username,password,admin) values ('','d41d8cd98f00b204e9800998ecf8427e',0);
    insert into sincronizador values (0);
    """)
    conn.commit()
