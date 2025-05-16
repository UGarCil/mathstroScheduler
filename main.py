from mathstro_scheduler.scheduler import scheduler


if __name__ == "__main__":
    # Example usage
    scheduler(
        epochs=100_000,
        replicates=5,
        max_attempts=3,
        session_file="./mathstro_scheduler/datasets/test2_sessions.txt",
        instructor_pref_file="./mathstro_scheduler/datasets/test2_instructorPrefs.txt",
        output_path = "./",
        verbose=False
    )