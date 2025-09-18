-- This SQL script creates a trigger function and a trigger to cap the audit_log table.
-- It is executed by the Alembic migration environment in env.py.

CREATE OR REPLACE FUNCTION cap_audit_log_table() RETURNS TRIGGER AS $$
BEGIN
  -- Check if the number of rows exceeds the limit (e.g., 5000)
  IF (SELECT count(*) FROM audit_log) > 5000 THEN
    -- If it does, delete the oldest rows to bring the count back to the limit
    DELETE FROM audit_log WHERE id IN (
      SELECT id FROM audit_log ORDER BY created_at ASC
      LIMIT (SELECT count(*) - 5000 FROM audit_log)
    );
  END IF;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Drop the trigger if it already exists to ensure idempotency
DROP TRIGGER IF EXISTS audit_log_capper ON audit_log;

-- Create the trigger that calls the function after every INSERT
CREATE TRIGGER audit_log_capper
AFTER INSERT ON audit_log
FOR EACH ROW EXECUTE FUNCTION cap_audit_log_table();
