import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.ArrayList;
import java.util.Scanner;

public class ex2 {
  private final String url = "jdbc:postgresql://localhost/univdb";
  private final String username = "postgres";
  private final String password = "postgres";

  ArrayList<String> alreadyVisited = new ArrayList<>();

  public Connection connect() throws SQLException {
    return DriverManager.getConnection(url, username, password);
  }

  public void dislpayColumnHeaders(ResultSet rs) throws SQLException{
    int maxLength = 20;
    ResultSetMetaData rsmd = rs.getMetaData();
    for(int i = 1; i <= rsmd.getColumnCount(); i++){
      String output = String.format("%-" + maxLength + "s", rsmd.getColumnName(i));
      System.out.print(output);
    }
    System.out.println(" ");
  }

  public void displayResultSetRecursive(ResultSet rs, int toplevel) throws SQLException{
    ResultSetMetaData rsmd =rs.getMetaData();
    int maxLength = 20;
    ArrayList<String> prerequisites = new ArrayList<>();
    String prereq_id;
    while(rs.next()){
      for(int i = 1; i <= rsmd.getColumnCount(); i++){
        String output = String.format("%-" + maxLength + "s", String.valueOf(rs.getObject(i)));
        System.out.print(output);
      }
      System.out.println(" ");
      prereq_id = rs.getString("prereq_id");
      // printPrerequisites(prereq_id, toplevel + 1);
      prerequisites.add(prereq_id);
    }
    for(String prq: prerequisites){
      if(alreadyVisited.contains(prq)){
        continue;
      }
      alreadyVisited.add(prq);
      printPrerequisites(prq, toplevel + 1);
    }
  }

  public void getCourseID() {
    Scanner scanner = new Scanner(System.in);
    String course_id;
    System.out.print("Enter the course ID: ");
    course_id = scanner.nextLine();
    printPrerequisites(course_id, 0);
    scanner.close();
  }

  public void printPrerequisites(String course_id, int toplevel){
    String SQL = "SELECT course_id, prereq_id, title FROM (SELECT prereq.course_id as course_id, prereq_id, title FROM prereq JOIN course ON course.course_id = prereq.prereq_id ORDER BY prereq_id) AS T WHERE course_id = ?";

    try (
      Connection conn = connect();
      PreparedStatement pstmt = conn.prepareStatement(SQL)
    ) {
      pstmt.setString(1,course_id);
      ResultSet rs = pstmt.executeQuery();
      if(toplevel == 0){
        dislpayColumnHeaders(rs);
      }
      displayResultSetRecursive(rs, toplevel);
    } catch (SQLException e){
      System.out.println(e.getMessage());
    }
  }

  public static void main(String[] args) {
    ex2 answer2 = new ex2();
    answer2.getCourseID();
  }

}
