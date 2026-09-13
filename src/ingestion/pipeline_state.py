

def get_last_successful_window(connection, pipeline_name):
    # get latest successful window for pipeline_name
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT last_successful_window from pipeline.pipeline_state WHERE pipeline_name = %s order by updated_at desc limit 1;",
            (pipeline_name,)
        )
        result = cursor.fetchone()
        return result[0] if result else None

def set_last_successful_window(connection, pipeline_name, window):
    from datetime import datetime, timezone
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO pipeline.pipeline_state
                (pipeline_name, last_successful_window, updated_at)
            VALUES (%s, %s, %s)
            ON CONFLICT (pipeline_name) DO UPDATE
                SET last_successful_window = EXCLUDED.last_successful_window,
                    updated_at = EXCLUDED.updated_at;
            """,
            (
                pipeline_name,
                window,
                datetime.now(timezone.utc),
            ),
        )
        # connection.commit()