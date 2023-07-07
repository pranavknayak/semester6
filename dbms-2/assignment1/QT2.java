import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Scanner;

public class QT2 {
  private final String url = "jdbc:postgresql://localhost/univdb";
  private final String username = "postgres";
  private final String password = "postgres";


  public Connection connect() throws SQLException {
    return DriverManager.getConnection(url, username, password);
  }


  public void displayResultSet(ResultSet rs) throws SQLException{
    ResultSetMetaData rsmd =rs.getMetaData();
    int maxLength = 20;
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

  public void getCourseID() {
    Scanner scanner = new Scanner(System.in);
    String course_id;
    System.out.print("Enter the course ID: ");
    course_id = scanner.nextLine();
    printPrerequisites(course_id);
    scanner.close();
  }

  public void printPrerequisites(String course_id){
    // String SQL = "SELECT course_id, prereq_title" +
    //               "FROM (SELECT prereq.course_id, prereq_id, title AS prereq_title" +
    //               "FROM course RIGHT JOIN prereq" +
    //               "ON course.course_id = prereq.prereq_id" +
    //               ") AS t" +
    //               "WHERE course_id = '?'";
    String SQL = "SELECT course_id, title FROM (SELECT prereq.course_id as course_id, prereq_id, title FROM prereq JOIN course ON course.course_id = prereq.prereq_id ORDER BY prereq_id) AS T WHERE course_id = ?";

    try (
      Connection conn = connect();
      PreparedStatement pstmt = conn.prepareStatement(SQL)
    ) {
      pstmt.setString(1,course_id);
      ResultSet rs = pstmt.executeQuery();
      displayResultSet(rs);
    } catch (SQLException e){
      System.out.println(e.getMessage());
    }
  }

  public static void main(String[] args) {
    QT2 answer2 = new QT2();
    answer2.getCourseID();
  }

}
