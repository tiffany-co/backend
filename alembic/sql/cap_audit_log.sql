-- Efficient audit_log cap system
CREATE OR REPLACE FUNCTION cap_audit_log_table() RETURNS TRIGGER AS $$
DECLARE
    row_count BIGINT;
    excess BIGINT;
BEGIN
    SELECT reltuples::BIGINT
    INTO row_count
    FROM pg_class
    WHERE oid = 'audit_log'::regclass;

    IF row_count > 5000 THEN
        excess := row_count - 4000;

        DELETE FROM audit_log
        WHERE id IN (
            SELECT id FROM audit_log
            ORDER BY created_at ASC
            LIMIT excess
        );
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS audit_log_capper ON audit_log;

CREATE TRIGGER audit_log_capper
AFTER INSERT ON audit_log
FOR EACH STATEMENT
EXECUTE FUNCTION cap_audit_log_table();
