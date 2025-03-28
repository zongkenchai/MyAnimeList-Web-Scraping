MATCH (studio1:Studio)<-[rel:PRODUCED_BY_STUDIO]-(anime:Anime)-[rel2:PRODUCED_BY_STUDIO]->(studio2:Studio)
WHERE studio1.name < studio2.name // to avoid duplicates
RETURN studio1.name, studio2.name, COUNT(DISTINCT anime.anime_id) AS no_of_collaborations
ORDER BY no_of_collaborations DESC