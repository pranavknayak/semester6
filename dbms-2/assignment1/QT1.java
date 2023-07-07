import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;

public class QT1 {
  private final String url = "jdbc:postgresql://localhost/univdb";
  private final String username = "postgres";
  private final String password = "postgres";

  public Connection connect() throws SQLException {
    return DriverManager.getConnection(url, username, password);
  }

  public void displayResultSet(ResultSet rs) throws SQLException{
    int count = 1;
    while(rs.next()){
      System.out.print(count + "\t\t");
      System.out.println(rs.getString("name"));
      count++;
    }
  }

  public void query() {
    String SQL = "SELECT * FROM INSTRUCTOR LIMIT 10";
    try (
    Connection conn = connect();
    Statement stmt = conn.createStatement();
    ResultSet rs = stmt.executeQuery(SQL)
    ) {
      displayResultSet(rs);
    } catch (SQLException e){
      System.out.println(e.getMessage());
    }
  }

  public static void main(String[] args) {
    QT1 qt = new QT1();
    qt.query();
  }

}
