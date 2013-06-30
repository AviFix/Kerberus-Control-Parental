CREATE TABLE usuarios(
    id               INTEGER PRIMARY KEY,
    username    TEXT    unique,
    admin         boolean,
    safesearch   boolean,
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

CREATE TABLE dominios_publicamente_permitidos(
  url               TEXT
);

CREATE TABLE dominios_publicamente_denegados(
    url               TEXT
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
    ultima_actualizacion  real,
    ultima_recarga_completa  real
);

insert into usuarios(username,password,admin,safesearch,passwordseteada) values ('admin','d41d8cd98f00b204e9800998ecf8427e',1,0,0);
insert into usuarios(username,password,admin,safesearch,passwordseteada) values ('usuario','d41d8cd98f00b204e9800998ecf8427e',0,1,1);
insert into usuarios(username,password,admin,safesearch,passwordseteada) values ('','d41d8cd98f00b204e9800998ecf8427e',0,1,1);
insert into sincronizador values (0,0);
insert into instalacion values (0,0,"","","","","1.1",0);
