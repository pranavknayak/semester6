import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.HashMap;
import java.util.Scanner;



public class ex5 {

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


  public double calculateCGPA(String id, Connection conn) throws SQLException{
    String SQL = "select id, course.course_id, credits, grade " +
                  "from takes join course " +
                  "on course.course_id = takes.course_id " +
                  "where id = ?";

    PreparedStatement pstmt = conn.prepareStatement(SQL);
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


    double CGPA = totalGrade * 1.0 / totalCredits;
    return CGPA;
  }

  public void createTable(Connection conn) throws SQLException{
    String SQL = "drop table if exists student_grades; create table student_grades( student_id varchar(5) primary key, department varchar(20), cgpa numeric(4, 2));";
    Statement stmt = conn.createStatement();
    stmt.executeUpdate(SQL);
    System.out.println("Table has been created successfully");
  }

  public void insertStudents(Connection conn) throws SQLException{
    String SQL = "insert into student_grades(student_id, department, cgpa) values(?, ?, ?)";
    PreparedStatement pstmt = conn.prepareStatement(SQL);
    String query = "select id, dept_name from student";
    Statement stmt = conn.createStatement();
    ResultSet student_ids = stmt.executeQuery(query);
    while(student_ids.next()){
      String id = student_ids.getString("id");
      String department = student_ids.getString("dept_name");
      double cgpa = calculateCGPA(id, conn);
      pstmt.setString(1, id);
      pstmt.setString(2, department);
      pstmt.setDouble(3, cgpa);
      pstmt.addBatch();
    }
    pstmt.executeBatch();
    System.out.println("Students inserted into table successfully");
  }

  public void ranking1(){ // across all students
    String SQL = "select student_id, cgpa, rank() over (order by (cgpa) desc) as student_rank from student_grades order by student_rank limit ?";
    Scanner scanner = new Scanner(System.in);
    System.out.print("Enter the value for k: ");
    int k = Integer.valueOf(scanner.nextLine());
    scanner.close();
    try(
      Connection conn = connect();
      PreparedStatement pstmt = conn.prepareStatement(SQL)
    ) {
      pstmt.setInt(1, k);
      ResultSet rs = pstmt.executeQuery();
      displayResultSet(rs);
    } catch (SQLException e) {
      System.out.println(e.getMessage());
    }
  }

  public void ranking2() { // across students within a department
    String SQL = "select student_id, cgpa, rank() over (order by (cgpa) desc) as student_rank from student_grades where department = ? order by student_rank limit ?";
    Scanner scanner = new Scanner(System.in);
    System.out.print("Enter the required department: ");
    String department = scanner.nextLine();
    System.out.print("Enter the value for k: ");
    int k = Integer.valueOf(scanner.nextLine());
    scanner.close();
    try(
      Connection conn = connect();
      PreparedStatement pstmt = conn.prepareStatement(SQL)
    ) {
      pstmt.setString(1, department);
      pstmt.setInt(2, k);
      ResultSet rs = pstmt.executeQuery();
      displayResultSet(rs);
    } catch (SQLException e) {
      System.out.println(e.getMessage());
    }
  }

  public void ranking3(){ // across students within a course
    String SQL = "select student_id, course_id, cgpa, rank() over (order by (cgpa) desc) as student_rank from student_grades join takes on student_id = id where course_id = ? limit ?";
    Scanner scanner = new Scanner(System.in);
    System.out.print("Enter the course ID: ");
    String course_id = scanner.nextLine();
    System.out.print("Enter the value for k: ");
    int k = Integer.valueOf(scanner.nextLine());
    scanner.close();
    try(
      Connection conn = connect();
      PreparedStatement pstmt = conn.prepareStatement(SQL)
    ) {
      pstmt.setString(1, course_id);
      pstmt.setInt(2, k);
      ResultSet rs = pstmt.executeQuery();
      displayResultSet(rs);
    } catch (SQLException e) {
      System.out.println(e.getMessage());
    }
  }

  public void createAndInsert(){
    try(
      Connection conn = connect();
    ) {
      createTable(conn);
      insertStudents(conn);
    } catch (SQLException e) {
      System.out.println(e.getMessage());
    }
  }


  public static void main(String[] args) {
    ex5 test = new ex5();
    test.createAndInsert();
    test.ranking3();

  }

}
