SELECT 
    EXTRACT(YEAR FROM date_publication) AS annee_publication,
    COUNT(*) AS nombre_de_videos
FROM 
    videos
GROUP BY 
    annee_publication
ORDER BY 
    annee_publication;





SELECT 
    EXTRACT(YEAR FROM date_creation) AS annee_creation,
    COUNT(*) AS nombre_de_chaines
FROM 
    chaines
GROUP BY 
    annee_creation
ORDER BY 
    annee_creation;
