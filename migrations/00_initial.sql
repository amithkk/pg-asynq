

CREATE TABLE IF NOT EXISTS asynq_messages (
    id serial PRIMARY KEY,
    queue_name varchar(100),
    payload text,
    queued_at timestamptz DEFAULT now(),
    consumed bool DEFAULT false
);

CREATE INDEX fast_queue_retrieval on asynq_messages(queue_name, id ASC);

CREATE OR REPLACE FUNCTION notify_asynq_message() RETURNS trigger AS $$
BEGIN
  PERFORM pg_notify('asynq_'||NEW.queue_name, 'notify');
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER asynq_messages_notify
AFTER INSERT ON asynq_messages
FOR EACH ROW EXECUTE PROCEDURE notify_asynq_message();
