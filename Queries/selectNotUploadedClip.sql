SELECT *
FROM Clips c1 INNER JOIN Categories c2 ON (c1.Broadcaster_ID = c2.Broadcaster_ID OR c1.game_id = c2.game_id)
WHERE Clip_ID NOT IN (
    SELECT Clip_ID
    FROM Clips_Uploaded_To_Channel
    WHERE Channel_ID LIKE ?
)
AND Channel_ID LIKE ?
ORDER BY viewcount DESC