--CREATE DATABASE securedfamily;

CREATE TABLE usuarios(
    id               INTEGER PRIMARY KEY,
    username    TEXT    unique,
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

CREATE TABLE cache_urls_aceptadas(
    url               TEXT,
    hora             time
    );

CREATE TABLE cache_urls_denegadas(
    url               TEXT,
    hora             time
);

insert into usuarios(username,password) values ('admin','2cb501528f3f41d20d8aaa2ab8761e38');
insert into usuarios(username,password) values ('mboscovich','2cb501528f3f41d20d8aaa2ab8761e38');
