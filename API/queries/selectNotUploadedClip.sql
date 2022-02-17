SELECT *
FROM Clips
WHERE Clip_ID NOT IN (
    SELECT Clip_ID
    FROM Clips_Uploaded_To_Channel
    WHERE Channel_ID LIKE ?
)