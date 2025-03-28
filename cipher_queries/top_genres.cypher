MATCH (a:Anime)-[:HAS_GENRE]->(g1:Genre),
      (a)-[:HAS_GENRE]->(g2:Genre),
      (a)-[:HAS_GENRE]->(g3:Genre)
WHERE g1 <> g2 AND g2 <> g3 AND g1 <> g3 
AND g1.name < g2.name AND g2.name < g3.name
RETURN g1.name AS Genre1, g2.name AS Genre2, g3.name AS Genre3, 
       COUNT(DISTINCT a.anime_id) AS coOccurrence
ORDER BY coOccurrence DESC
