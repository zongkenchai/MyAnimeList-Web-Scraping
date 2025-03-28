// Create indexes
CREATE INDEX anime_id_index FOR (n:Anime) ON (n.anime_id);

// Node creation queries
LOAD CSV WITH HEADERS FROM 'file:///anime_nodes.csv' AS row
CREATE (:Anime {
    anime_id: toInteger(row.anime_id),
    name: row.name,
    rank: toInteger(row.rank), 
    score: toFloat(row.score),
    scored_by: toInteger(row.scored_by),
    popularity: toInteger(row.popularity),
    members: toInteger(row.members),
    favorites: toInteger(row.favorites),
    episodes: toInteger(row.episodes),
    aired_from: row.aired_from,
    aired_to: row.aired_to,
    length_days: toInteger(row.length_days)
});

LOAD CSV WITH HEADERS FROM 'file:///source_nodes.csv' AS row
CREATE (:Source {source_id: toInteger(row.source_id), name: row.source});

LOAD CSV WITH HEADERS FROM 'file:///type_nodes.csv' AS row
CREATE (:Type {type_id: toInteger(row.type_id), name: row.type});

LOAD CSV WITH HEADERS FROM 'file:///rating_nodes.csv' AS row
CREATE (:Rating {rating_id: toInteger(row.rating_id), name: row.rating});

LOAD CSV WITH HEADERS FROM 'file:///status_nodes.csv' AS row
CREATE (:Status {status_id: toInteger(row.status_id), name: row.status});

LOAD CSV WITH HEADERS FROM 'file:///genres_nodes.csv' AS row
CREATE (:Genre {genre_id: toInteger(row.genre_id), name: row.genre});

LOAD CSV WITH HEADERS FROM 'file:///themes_nodes.csv' AS row
CREATE (:Theme {theme_id: toInteger(row.theme_id), name: row.theme});

LOAD CSV WITH HEADERS FROM 'file:///demographics_nodes.csv' AS row
CREATE (:Demographic {demographic_id: toInteger(row.demographic_id), name: row.demographic});

LOAD CSV WITH HEADERS FROM 'file:///producers_nodes.csv' AS row
CREATE (:Producer {producer_id: toInteger(row.producer_id), name: row.producer});

LOAD CSV WITH HEADERS FROM 'file:///licensors_nodes.csv' AS row
CREATE (:Licensor {licensor_id: toInteger(row.licensor_id), name: row.licensor});

LOAD CSV WITH HEADERS FROM 'file:///studios_nodes.csv' AS row
CREATE (:Studio {studio_id: toInteger(row.studio_id), name: row.studio});

// Relationship creation queries
LOAD CSV WITH HEADERS FROM 'file:///anime_source_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (s:Source {source_id: toInteger(row.source_id)})
CREATE (a)-[:HAS_SOURCE]->(s);

LOAD CSV WITH HEADERS FROM 'file:///anime_type_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (t:Type {type_id: toInteger(row.type_id)})
CREATE (a)-[:HAS_TYPE]->(t);

LOAD CSV WITH HEADERS FROM 'file:///anime_rating_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (r:Rating {rating_id: toInteger(row.rating_id)})
CREATE (a)-[:HAS_RATING]->(r);

LOAD CSV WITH HEADERS FROM 'file:///anime_status_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (s:Status {status_id: toInteger(row.status_id)})
CREATE (a)-[:HAS_STATUS]->(s);

LOAD CSV WITH HEADERS FROM 'file:///anime_genres_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (g:Genre {genre_id: toInteger(row.genre_id)})
CREATE (a)-[:HAS_GENRE]->(g);

LOAD CSV WITH HEADERS FROM 'file:///anime_themes_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (t:Theme {theme_id: toInteger(row.theme_id)})
CREATE (a)-[:HAS_THEME]->(t);

LOAD CSV WITH HEADERS FROM 'file:///anime_demographics_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (d:Demographic {demographic_id: toInteger(row.demographic_id)})
CREATE (a)-[:HAS_DEMOGRAPHIC]->(d);

LOAD CSV WITH HEADERS FROM 'file:///anime_producers_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (p:Producer {producer_id: toInteger(row.producer_id)})
CREATE (a)-[:PRODUCED_BY]->(p);

LOAD CSV WITH HEADERS FROM 'file:///anime_licensors_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (l:Licensor {licensor_id: toInteger(row.licensor_id)})
CREATE (a)-[:LICENSED_BY]->(l);

LOAD CSV WITH HEADERS FROM 'file:///anime_studios_rels.csv' AS row
MATCH (a:Anime {anime_id: toInteger(row.anime_id)})
MATCH (s:Studio {studio_id: toInteger(row.studio_id)})
CREATE (a)-[:PRODUCED_BY_STUDIO]->(s);


