
## SQLite Implementation Details

The application now includes enhanced support for SQLite, making it easier to run and develop locally without requiring a PostgreSQL database server. Here are the key improvements:

### How SQLite is Implemented

1. **Automatic Database Detection**: The application checks the DATABASE_URL to determine if it's using SQLite or PostgreSQL:
   ```python
   db_url = os.environ.get("DATABASE_URL", "sqlite:///essay_evaluation.db")
   if db_url.startswith("sqlite"):
       # Apply SQLite-specific configuration
   else:
       # Apply PostgreSQL-specific configuration
   ```

2. **SQLite-Specific Optimizations**: When SQLite is detected, the application automatically:
   - Configures `check_same_thread=False` to prevent locking issues
   - Applies appropriate SQLite-specific settings for optimal performance

3. **Default Database Path**: The SQLite database is stored as `essay_evaluation.db` in the project root directory

### Benefits of SQLite Support

- **Simplified Local Development**: No need to install or configure PostgreSQL
- **Portability**: The entire database is stored in a single file
- **Quick Setup**: Just set the DATABASE_URL environment variable to use SQLite
- **Easy Backup and Restore**: Copy the database file to backup/restore
- **Suitable for Small to Medium Applications**: Perfect for development, testing, and smaller deployments

### Managing SQLite Databases

#### Viewing and Editing SQLite Data
For developers who need to inspect or modify the database directly:
- Use [DB Browser for SQLite](https://sqlitebrowser.org/) (GUI tool)
- Use the SQLite command-line tool: `sqlite3 essay_evaluation.db`

#### Backup and Restore
```bash
# Backup
cp essay_evaluation.db essay_evaluation_backup.db

# Restore
cp essay_evaluation_backup.db essay_evaluation.db
```

#### Reset Database
```bash
# Remove the database file
rm essay_evaluation.db

# Create a new one
python -c "from app import app, db; with app.app_context(): db.create_all()"
```

### SQLite vs PostgreSQL Comparison

| Feature | SQLite | PostgreSQL |
|---------|--------|------------|
| Setup | No setup required | Requires server installation |
| Concurrency | Limited | Excellent |
| Performance | Good for small datasets | Better for large datasets |
| Deployment | Simple | More complex |
| Backup | Copy file | pg_dump command |
| Best for | Development, small apps | Production, large apps |

### When to Switch to PostgreSQL

Consider switching from SQLite to PostgreSQL when:
- Your application has many concurrent users
- Your database exceeds a few GB in size
- You need advanced database features
- You're deploying to production

Switching is simple: just change the DATABASE_URL environment variable.
