import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.Scanner;

public class ex1 {
  private final String url = "jdbc:postgresql://localhost/univdb";
  private final String username = "postgres";
  private final String password = "postgres";

  public Connection connect() throws SQLException {
    return DriverManager.getConnection(url, username, password);
  }

  public void displayResultSet(ResultSet rs) throws SQLException{
    ResultSetMetaData rsmd =rs.getMetaData();
    int maxLength = 28;
    for(int i = 1; i <= rsmd.getColumnCount(); i++){
      String output = String.format("%-" + maxLength + "s", rsmd.getColumnName(i));
      System.out.print(output);
    }
    System.out.println(" ");
    while(rs.next()){
      for(int i = 1; i <= rsmd.getColumnCount(); i++){
        String output = String.format("%-" + maxLength + "s", String.valueOf(rs.getObject(i)));
        System.out.print(output);
      }
      System.out.println(" ");
    }
  }

  public void query() {
    Scanner scanner = new Scanner(System.in);
    System.out.print("Enter table: ");
    String table = scanner.nextLine();
    System.out.print("Enter k: ");
    int k = Integer.valueOf(scanner.nextLine());
    scanner.close();
    String SQL = "SELECT * FROM %s LIMIT %d";
    try (
    Connection conn = connect();
    PreparedStatement stmt = conn.prepareStatement(String.format(SQL, table, k));
    ) {
      ResultSet rs = stmt.executeQuery();
      displayResultSet(rs);
    } catch (SQLException e){
      System.out.println(e.getMessage());
    }
  }

  public static void main(String[] args) {
    ex1 answer1 = new ex1();
    answer1.query();
  }

}
