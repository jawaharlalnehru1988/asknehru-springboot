# Yoga Pose Simplification Migration (Manual)

This project currently uses Hibernate auto-update (`spring.jpa.hibernate.ddl-auto=update`) and does **not** use Flyway/Liquibase.

To safely migrate production data to the simplified `YogaPose` model (`yogaName`, `blogContent`, `audioURL`, `videoURL`, `imageURL`, `category`), run the SQL script below manually.

## 1) Backup first

```bash
pg_dump -U <db_user> -h <db_host> -d <db_name> -F c -f asknehrubackend_before_yoga_simplify.dump
```

## 2) Run migration

```bash
psql -U <db_user> -h <db_host> -d <db_name> -f sql/2026-02-17_simplify_yoga_pose.sql
```

## 3) Verify

```sql
SELECT id, yoga_name, left(blog_content, 120), audio_url, video_url, image_url
FROM yoga_poses
LIMIT 20;
```

## 4) Restart app

After successful migration, restart the backend service.

## Notes

- Script consolidates older yoga fields + child table content into `blog_content`.
- It drops legacy columns/tables after backfill.
- If your old DB had different table/column names for detailed steps or media URLs, adjust those sections before running.
