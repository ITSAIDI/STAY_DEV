--select * from chaines ;
select * from videos;
--SELECT * FROM videos WHERE requetes IS NULL and id_chaine = 'UCTpOTnJY4eYL9JBV_Nh5R5Q';
--SELECT * FROM videos WHERE id_chaine = 'UCEVmxjvp1oBvtHQ2jpD9frw';
--select * from chaines where nom = 'IADEA';
--SELECT * FROM videos WHERE id_video = 'PaBTFTR_BaA';
--SELECT id_chaine FROM chaines WHERE pertinente = TRUE
--select * from chaines_metriques;

/*
SELECT 
    c.id_chaine,
    c.nom,
    cm.date_releve_chaine,
    cm.nombre_vues_total,
    cm.nombre_abonnes_total,
    cm.nombre_videos_total
FROM chaines_metriques cm
JOIN chaines c ON cm.id_chaine = c.id_chaine;

*/

--SELECT COUNT(*) FROM videos WHERE id_chaine = 'UCxBJustR1tuXVy7tLivER2g';

/*
SELECT nombre_videos_total
        FROM chaines_metriques
        WHERE id_chaine = 'UCxBJustR1tuXVy7tLivER2g'
        ORDER BY date_releve_chaine DESC
        LIMIT 1
*/		