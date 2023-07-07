import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;

public class ConnTest {
  private final String url = "jdbc:postgresql://localhost/univdb";
  private final String username = "postgres";
  private final String password = "postgres";

  public Connection connect() throws SQLException {
    return DriverManager.getConnection(url, username, password);
  }

  public void attemptConn(){
    try(
      Connection conn = connect();
    ) {
      System.out.println("Connection Successful");
     } catch(SQLException e) {
      System.out.println("Connection failed");
      System.out.println(e.getMessage());
     }
  }

  public static void main(String[] args) {
    ConnTest ct = new ConnTest();
    ct.attemptConn();
  }
}
