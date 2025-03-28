MATCH (p:Producer)<-[rel:PRODUCED_BY]-(anime:Anime)-[rel2:PRODUCED_BY_STUDIO]->(s:Studio{name:'Kyoto Animation'})
WHERE NOT EXISTS
{
    MATCH (p)<-[:PRODUCED_BY]-(anime2:Anime)-[:PRODUCED_BY_STUDIO]->(:Studio {name:'Animation Do'}) 
}
RETURN p.name, s.name, COUNT(DISTINCT anime.anime_id) AS no_of_anime
ORDER BY no_of_anime DESC