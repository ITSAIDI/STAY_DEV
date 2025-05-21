--select * from chaines;
select * from videos;

/*
SELECT 
    c.id_chaine,
    c.nom,
    cm.date_releve_chaine,
    cm.nombre_vues_total,
    cm.nombre_abonnes_total,
    cm.nombre_videos_total
FROM chaines_metriques cm
JOIN chaines c ON cm.id_chaine = c.id_chaine Order by cm.nombre_abonnes_total desc;
*/