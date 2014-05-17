CREATE TABLE usuarios(
    id          INTEGER PRIMARY KEY,
    username    TEXT    unique,
    admin       boolean,
    safesearch  boolean,
    passwordseteada boolean,
    password     TEXT
);

CREATE TABLE instalacion(
    id               INTEGER,
    serverid         INTEGER,
    nombretitular    TEXT,
    email            TEXT,
    credencial       TEXT,
    password         TEXT,
    version          TEXT,
    passwordnotificada boolean
);

CREATE TABLE servidores(
    ranking    INTEGER,
    ip    TEXT,
    puerto INTEGER
);

CREATE TABLE estado(
    id         INTEGER PRIMARY KEY,
    estado     TEXT
);

CREATE TABLE dominios_usuario(
    url             TEXT,
    usuario         INTEGER,
    estado          INTEGER,
    FOREIGN KEY(usuario) REFERENCES usuario(id),
    FOREIGN KEY(estado) REFERENCES estado(id)
);

CREATE TABLE dominios_kerberus(
  url               TEXT,
  estado            INTEGER,
  FOREIGN KEY(estado) REFERENCES estado(id)
);

CREATE TABLE cache_dominios(
    dominio          TEXT,
    hora             time,
    estado           INTEGER,
    FOREIGN KEY(estado) REFERENCES estado(id)
);

CREATE TABLE sincronizador(
    ultima_actualizacion  real,
    ultima_recarga_completa  real
);

insert into usuarios(username,password,admin,safesearch,passwordseteada) values ('admin','d41d8cd98f00b204e9800998ecf8427e',1,0,0);
insert into usuarios(username,password,admin,safesearch,passwordseteada) values ('usuario','d41d8cd98f00b204e9800998ecf8427e',0,1,1);
insert into usuarios(username,password,admin,safesearch,passwordseteada) values ('','d41d8cd98f00b204e9800998ecf8427e',0,1,1);
insert into sincronizador values (0,0);
insert into instalacion values (0,0,"","","","","1.1",0);
insert into estado(id, estado) values (1, 'Permitido');
insert into estado(id, estado) values (2, 'Denegado');
