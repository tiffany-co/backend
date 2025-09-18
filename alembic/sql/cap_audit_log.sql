-- Efficient audit_log cap system
-- Uses statement-level trigger + pg_class estimate for performance

CREATE OR REPLACE FUNCTION cap_audit_log_table() RETURNS TRIGGER AS $$
DECLARE
  row_count BIGINT;
  excess BIGINT;
BEGIN
  -- Get estimated row count from Postgres system stats
  SELECT reltuples::BIGINT
  INTO row_count
  FROM pg_class
  WHERE oid = 'audit_log'::regclass;

  -- Only start cleanup if table has grown beyond 5000
  IF row_count > 5000 THEN
    -- Delete enough rows to bring it back down to 4000
    excess := row_count - 4000;

    DELETE FROM audit_log
    WHERE id IN (
      SELECT id FROM audit_log
      ORDER BY created_at ASC
      LIMIT excess
    );
  END IF;

  RETURN NULL; -- statement-level triggers must return null
END;
$$ LANGUAGE plpgsql;

-- Drop the old trigger if it exists
DROP TRIGGER IF EXISTS audit_log_capper ON audit_log;

-- Create a statement-level trigger (fires once per insert statement)
CREATE TRIGGER audit_log_capper
AFTER INSERT ON audit_log
FOR EACH STATEMENT
EXECUTE FUNCTION cap_audit_log_table();
