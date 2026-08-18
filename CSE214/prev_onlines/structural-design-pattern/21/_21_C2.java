// Target Interface expected by the legacy system
interface DatabaseQuery {
    void executeQuery(String query);
}

// Existing Legacy Class
class SQLDatabase implements DatabaseQuery {
    @Override
    public void executeQuery(String sqlQuery) {
        System.out.println("Executing SQL query: " + sqlQuery);
    }
}

// New Adaptee Class (Incompatible interface)
class NoSQLDatabase {
    public void runQuery(String noSQLQuery) {
        System.out.println("Executing NoSQL query: " + noSQLQuery);
    }
}

// Adapter: Wraps NoSQLDatabase to make it compatible with DatabaseQuery
class NoSQLAdapter implements DatabaseQuery {
    private NoSQLDatabase noSQLDatabase;

    public NoSQLAdapter(NoSQLDatabase noSQLDatabase) { 
        this.noSQLDatabase = noSQLDatabase;
    }

    @Override
    public void executeQuery(String query) {
        // Translates the standard executeQuery call into runQuery
        noSQLDatabase.runQuery(query);
    }
}

public class _21_C2 {
    public static void main(String[] args) {
        System.out.println("=== Legacy System ===");
        // 1. Using the existing SQL database natively
        DatabaseQuery sqlDB = new SQLDatabase();
        sqlDB.executeQuery("SELECT * FROM users");

        System.out.println("\n=== New Integration ===");
        // 2. Seamlessly using the NoSQL database through the Adapter
        DatabaseQuery noSqlDB = new NoSQLAdapter(new NoSQLDatabase());
        noSqlDB.executeQuery("{ \"collection\": \"users\", \"action\": \"find\" }");
    }
}