BEGIN;

-- 1) Add new simplified columns if not already present
ALTER TABLE yoga_poses ADD COLUMN IF NOT EXISTS yoga_name VARCHAR(255);
ALTER TABLE yoga_poses ADD COLUMN IF NOT EXISTS blog_content TEXT;
ALTER TABLE yoga_poses ADD COLUMN IF NOT EXISTS audio_url VARCHAR(1000);
ALTER TABLE yoga_poses ADD COLUMN IF NOT EXISTS video_url VARCHAR(1000);
ALTER TABLE yoga_poses ADD COLUMN IF NOT EXISTS image_url_new VARCHAR(1000);
ALTER TABLE yoga_poses ADD COLUMN IF NOT EXISTS category_new VARCHAR(255);

-- 2) Backfill yoga_name from previous name fields
UPDATE yoga_poses
SET yoga_name = COALESCE(NULLIF(yoga_name, ''), NULLIF(name, ''), NULLIF(english_name, ''), NULLIF(sanskrit_name, ''), 'Untitled Yoga Pose')
WHERE yoga_name IS NULL OR yoga_name = '';

-- 3) Build blog_content from previous yoga_poses columns
UPDATE yoga_poses
SET blog_content = COALESCE(
    NULLIF(blog_content, ''),
    NULLIF(
        CONCAT_WS(E'\n\n',
            NULLIF(description, ''),
            CASE WHEN NULLIF(quick_benefit, '') IS NOT NULL THEN 'Quick Benefit: ' || quick_benefit END,
            CASE WHEN NULLIF(duration, '') IS NOT NULL THEN 'Duration: ' || duration END,
            CASE WHEN NULLIF(difficulty, '') IS NOT NULL THEN 'Difficulty: ' || difficulty END,
            CASE WHEN NULLIF(category, '') IS NOT NULL THEN 'Category: ' || category END
        ),
        ''
    ),
    'Content will be added soon.'
)
WHERE blog_content IS NULL OR blog_content = '';

-- 3a) Optionally append child table content into blog_content if those tables exist
DO $$
BEGIN
    IF to_regclass('public.pose_benefits') IS NOT NULL THEN
        EXECUTE $sql$
            UPDATE yoga_poses yp
            SET blog_content = CONCAT_WS(E'\n\n', yp.blog_content, 'Benefits:\n' || b.benefits_text)
            FROM (
                SELECT pose_id,
                       string_agg(
                           COALESCE(NULLIF(title, ''), 'Benefit') ||
                           CASE WHEN NULLIF(description, '') IS NOT NULL THEN ': ' || description ELSE '' END,
                           E'\n- ' ORDER BY id
                       ) AS benefits_text
                FROM pose_benefits
                GROUP BY pose_id
            ) b
            WHERE yp.id = b.pose_id
        $sql$;
    END IF;

    IF to_regclass('public.detailed_steps') IS NOT NULL THEN
        EXECUTE $sql$
            UPDATE yoga_poses yp
            SET blog_content = CONCAT_WS(E'\n\n', yp.blog_content, 'Detailed Steps:\n' || ds.steps_text)
            FROM (
                SELECT pose_id,
                       string_agg((COALESCE(step_number::text, '?') || '. ' || COALESCE(instruction, '')), E'\n' ORDER BY step_number NULLS LAST, id) AS steps_text
                FROM detailed_steps
                GROUP BY pose_id
            ) ds
            WHERE yp.id = ds.pose_id
        $sql$;
    END IF;

    IF to_regclass('public.pose_contraindications') IS NOT NULL THEN
        EXECUTE $sql$
            UPDATE yoga_poses yp
            SET blog_content = CONCAT_WS(E'\n\n', yp.blog_content, 'Contraindications:\n' || c.txt)
            FROM (
                SELECT pose_id, string_agg(contraindication, E'\n- ') AS txt
                FROM pose_contraindications
                GROUP BY pose_id
            ) c
            WHERE yp.id = c.pose_id
        $sql$;
    END IF;

    IF to_regclass('public.pose_mistakes') IS NOT NULL THEN
        EXECUTE $sql$
            UPDATE yoga_poses yp
            SET blog_content = CONCAT_WS(E'\n\n', yp.blog_content, 'Common Mistakes:\n' || m.txt)
            FROM (
                SELECT pose_id, string_agg(mistake, E'\n- ') AS txt
                FROM pose_mistakes
                GROUP BY pose_id
            ) m
            WHERE yp.id = m.pose_id
        $sql$;
    END IF;

    IF to_regclass('public.pose_tags') IS NOT NULL THEN
        EXECUTE $sql$
            UPDATE yoga_poses yp
            SET blog_content = CONCAT_WS(E'\n\n', yp.blog_content, 'Tags: ' || t.txt)
            FROM (
                SELECT pose_id, string_agg(tag, ', ') AS txt
                FROM pose_tags
                GROUP BY pose_id
            ) t
            WHERE yp.id = t.pose_id
        $sql$;
    END IF;
END $$;

-- 4) Backfill image_url_new from old image_url
UPDATE yoga_poses
SET image_url_new = COALESCE(NULLIF(image_url_new, ''), NULLIF(image_url, ''))
WHERE image_url_new IS NULL OR image_url_new = '';

-- 5) Optional: copy media URLs from old columns if you had equivalents
-- UPDATE yoga_poses SET audio_url = old_audio_column WHERE audio_url IS NULL;
-- UPDATE yoga_poses SET video_url = old_video_column WHERE video_url IS NULL;

-- 5a) Preserve category as a dedicated field
UPDATE yoga_poses
SET category_new = COALESCE(NULLIF(category_new, ''), NULLIF(category, ''))
WHERE category_new IS NULL OR category_new = '';

-- 6) Enforce NOT NULL required by simplified entity
UPDATE yoga_poses SET yoga_name = 'Untitled Yoga Pose' WHERE yoga_name IS NULL OR yoga_name = '';
UPDATE yoga_poses SET blog_content = 'Content will be added soon.' WHERE blog_content IS NULL;
ALTER TABLE yoga_poses ALTER COLUMN yoga_name SET NOT NULL;

-- 7) Replace legacy image column name with new one expected by entity mapping
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS image_url;
ALTER TABLE yoga_poses RENAME COLUMN image_url_new TO image_url;

-- 7a) Replace legacy category column name with new one expected by entity mapping
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS category;
ALTER TABLE yoga_poses RENAME COLUMN category_new TO category;

-- 8) Drop legacy columns from yoga_poses (only after successful backfill)
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS pose_id;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS name;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS english_name;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS sanskrit_name;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS difficulty;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS image_context;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS description;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS quick_benefit;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS duration;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS popularity;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS text;
ALTER TABLE yoga_poses DROP COLUMN IF EXISTS author;

-- 9) Drop no-longer-used child tables
DROP TABLE IF EXISTS pose_benefits CASCADE;
DROP TABLE IF EXISTS detailed_steps CASCADE;
DROP TABLE IF EXISTS pose_contraindications CASCADE;
DROP TABLE IF EXISTS pose_mistakes CASCADE;
DROP TABLE IF EXISTS pose_tags CASCADE;

COMMIT;
