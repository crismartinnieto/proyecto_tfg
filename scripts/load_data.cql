// Creación de nodos Universidad
LOAD CSV WITH HEADERS FROM 'file:///universidades_espana.csv' AS row  
CREATE (u:Universidad {
    nombre: row.Universidad,  
    ciudad: row.Ciudad,  
    anio_fundacion: CASE row.`Año de Fundación` WHEN 'Desconocido' THEN NULL ELSE toInteger(row.`Año de Fundación`) END,  
    rector: row.Rector,  
    descripcion: row.Descripción,  
    numero_estudiantes: CASE row.`Número de Estudiantes` WHEN 'Desconocido' THEN NULL ELSE toInteger(row.`Número de Estudiantes`) END,  
    tipo: row.Tipo,  
    dbpedia_uri: row.DBpedia_URI  
});

// Relación UBICADA_EN con Ciudad
LOAD CSV WITH HEADERS FROM 'file:///universidades_espana.csv' AS row
MERGE (c:Ciudad {nombre: row.Ciudad})
WITH c, row
MATCH (u:Universidad {nombre: row.Universidad})
MERGE (u)-[:UBICADA_EN]->(c);

// Relación ES_DE_TIPO con Tipo
LOAD CSV WITH HEADERS FROM 'file:///universidades_espana.csv' AS row
MERGE (t:Tipo {nombre: row.Tipo})
WITH t, row
MATCH (u:Universidad {nombre: row.Universidad})
MERGE (u)-[:ES_DE_TIPO]->(t);

// Relación TIENE_RECTOR con Rector
LOAD CSV WITH HEADERS FROM 'file:///universidades_espana.csv' AS row
MERGE (r:Rector {nombre: row.Rector})
WITH r, row
MATCH (u:Universidad {nombre: row.Universidad})
MERGE (u)-[:TIENE_RECTOR]->(r);

// Relación FUNDADO_EN con AñoFundacion (solo para años conocidos)
LOAD CSV WITH HEADERS FROM 'file:///universidades_espana.csv' AS row
WITH row
WHERE row.`Año de Fundación` <> 'Desconocido' AND row.`Año de Fundación` IS NOT NULL AND row.`Año de Fundación` <> '' AND toInteger(row.`Año de Fundación`) IS NOT NULL
MERGE (a:AñoFundacion {anio: toInteger(row.`Año de Fundación`)})
WITH a, row
MATCH (u:Universidad {nombre: row.Universidad})
MERGE (u)-[:FUNDADO_EN]->(a);

// Relación TIENE_DESCRIPCION con Descripcion
LOAD CSV WITH HEADERS FROM 'file:///universidades_espana.csv' AS row
MERGE (d:Descripcion {texto: row.Descripción})
WITH d, row
MATCH (u:Universidad {nombre: row.Universidad})
MERGE (u)-[:TIENE_DESCRIPCION]->(d);

// Relación TIENE_NUMERO_ESTUDIANTES con NumeroEstudiantes (solo para valores conocidos)
LOAD CSV WITH HEADERS FROM 'file:///universidades_espana.csv' AS row
WITH row
WHERE row.`Número de Estudiantes` <> 'Desconocido'
MERGE (n:NumeroEstudiantes {cantidad: toInteger(row.`Número de Estudiantes`)})
WITH n, row
MATCH (u:Universidad {nombre: row.Universidad})
MERGE (u)-[:TIENE_NUMERO_ESTUDIANTES]->(n);

// Relación TIENE_DBPEDIA_URI con DBpediaURI
LOAD CSV WITH HEADERS FROM 'file:///universidades_espana.csv' AS row
MERGE (db:DBpediaURI {uri: row.DBpedia_URI})
WITH db, row
MATCH (u:Universidad {nombre: row.Universidad})
MERGE (u)-[:TIENE_DBPEDIA_URI]->(db);