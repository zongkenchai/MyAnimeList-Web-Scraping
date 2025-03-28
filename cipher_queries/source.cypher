MATCH (s:Source)<-[rel:HAS_SOURCE]-(a:Anime)-[rel2:HAS_RATING]->(r:Rating)
RETURN s.name AS source, r.name AS rating, COUNT(DISTINCT a.anime_id) AS no_of_anime
ORDER BY no_of_anime DESC