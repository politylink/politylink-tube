-- ALTER TABLE clip ADD COLUMN type Integer;
CREATE INDEX ix_videoId ON annotation (video_id);