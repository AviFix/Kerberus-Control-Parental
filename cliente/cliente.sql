CREATE TABLE usuarios(
    id               INTEGER PRIMARY KEY,
    username    TEXT    unique,
    admin         boolean,
    safesearch   boolean,
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

insert into usuarios(username,password,admin,safesearch) values ('admin','dfe483413e24a5b1506389d36ebfd05c',1,0);
insert into usuarios(username,password,admin,safesearch) values ('mboscovich','dfe483413e24a5b1506389d36ebfd05c',0,1);
insert into usuarios(username,password,admin,safesearch) values ('rtourn','dfe483413e24a5b1506389d36ebfd05c',0,1);
insert into usuarios(username,password,admin,safesearch) values ('mguedes','dfe483413e24a5b1506389d36ebfd05c',0,1);
insert into usuarios(username,password,admin,safesearch) values ('','d41d8cd98f00b204e9800998ecf8427e',0,1);
insert into sincronizador values (0);
