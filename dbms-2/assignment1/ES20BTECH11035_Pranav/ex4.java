import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.util.HashMap;
import java.util.Scanner;

public class ex4 {
  private final String url = "jdbc:postgresql://localhost/univdb";
  private final String username = "postgres";
  private final String password = "postgres";

  HashMap<String, Integer> grades = new HashMap<String, Integer>();

  {
    grades.put("A+", 10);
    grades.put("A", 9);
    grades.put("A-", 8);
    grades.put("B+", 7);
    grades.put("B", 6);
    grades.put("B-", 5);
    grades.put("C+", 4);
    grades.put("C", 3);
    grades.put("C-", 2);
  }

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

  public void getRollNumber(){
    Scanner scanner = new Scanner(System.in);
    System.out.print("Enter the Student ID: ");
    String id = scanner.nextLine();
    calculateCGPA(id);
    scanner.close();
  }

  public void calculateCGPA(String id){
    String SQL = "select id, course.course_id, credits, grade " +
                  "from takes join course " +
                  "on course.course_id = takes.course_id " +
                  "where id = ?";
    try(
      Connection conn = connect();
      PreparedStatement pstmt = conn.prepareStatement(SQL);
    ){
      pstmt.setString(1, id);
      ResultSet rs = pstmt.executeQuery();

      double totalCredits = 0;
      int totalGrade = 0;

      while(rs.next()){
        String letterGrade = rs.getString("grade").trim();
        double credits = rs.getDouble("credits");
        int numberGrade = grades.get(letterGrade);
        totalGrade += numberGrade * credits;
        totalCredits += credits;
      }

      if (totalCredits == 0){
        System.out.println("No such student ID on record");
        return;
      }

      double CGPA = totalGrade * 1.0 / totalCredits;
      System.out.println(String.format("CGPA for student ID %s: %.2f", id, CGPA));

    } catch (SQLException e) {
      System.out.println(e.getMessage());
    }
  }

  public static void main(String[] args) {
    ex4 test = new ex4();
    test.getRollNumber();
  }
}
