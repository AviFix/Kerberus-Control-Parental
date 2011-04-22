CREATE TABLE benchmark(
    id                        integer,
    name                  TEXT,
    descripcion         TEXT
);

CREATE TABLE benchmark_ejecucion(
    id                    INTEGER PRIMARY KEY AUTOINCREMENT,
    fecha             TEXT,
    id_benchmark   integer,
    FOREIGN KEY(id_benchmark) REFERENCES benchmark(id)
);
CREATE TABLE benchmark_result(
    id_ejecucion   integer,
    id_url              integer,
    url                  TEXT,
    tiempo            float,
    tiempo_con_cache  float,
    apto              boolean,
    FOREIGN KEY(id_ejecucion) REFERENCES benchmark_ejecucion(id)
);
insert into benchmark(id,name,descripcion) values (1,'benchmark1','Lee el ranking obtenido de alexa.com del millon de sitios mas visitados, y va uno por uno probando cuando demora en revisarse, y cuanto demora una vez cacheado');
