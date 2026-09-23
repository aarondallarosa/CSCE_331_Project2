import java.sql.*;
import java.awt.event.*;
import javax.swing.*;

/*
  TODO:
  1) Change credentials for your own team's database.
  2) Change SQL command to a relevant query of table that retrieves a small amount of data.
  3) Change column name to table's column name containing the data. 
  4) Create a JTextArea object using the queried data.
  5) Add the new object to the JPanel p.
*/

public class GUI extends JFrame implements ActionListener {
    static JFrame f;

    public static void main(String[] args)
    {
      // building the connection
      Connection conn = null;
	  
      //TODO STEP 1 (see line 7)
      String database_name = "DBNAME"; // edit value here
      String database_user = "USERNAME"; // edit value here
      String database_password = "PASSWORD"; // edit value here
	  
      String database_url = String.format("jdbc:postgresql://csce-315-db.engr.tamu.edu/%s", database_name);
      try {
        conn = DriverManager.getConnection(database_url, database_user, database_password);
      } catch (Exception e) {
        e.printStackTrace();
        System.err.println(e.getClass().getName()+": "+e.getMessage());
        System.exit(0);
      }
      JOptionPane.showMessageDialog(null,"Opened database successfully");
      
	  String name = "";
      try{
        // create a statement object
        Statement stmt = conn.createStatement();

        // create a SQL statement
        //TODO Step 2 (see line 8)
        String sqlStatement = "SQL COMMAND"; // edit value here
		    
        //TODO Step 3 (see line 9)
        String columnName = "column_name"; // edit value here
		
        // end statement to DBMS
        ResultSet result = stmt.executeQuery(sqlStatement);
        while (result.next()) {
          name += result.getString(columnName)+"\n";
        }
      } catch (Exception e){
        JOptionPane.showMessageDialog(null,"Error accessing Database.");
      }
      
	    // create a new frame
      f = new JFrame("DB GUI");

      // create a object
      GUI s = new GUI();

      // create a panel
      JPanel p = new JPanel();

      JButton b = new JButton("Close");

      // add actionlistener to button
      b.addActionListener(s);

      //TODO Step 4 (see line 10)
	    // add code here

      //TODO Step 5 (see line 11)
	    // add code here

      // add button to panel
      p.add(b);

      // add panel to frame
      f.add(p);

      // set the size of frame
      f.setSize(400, 400);

      f.setVisible(true);

      // closing the connection
      try {
        conn.close();
        JOptionPane.showMessageDialog(null,"Connection Closed.");
      } catch(Exception e) {
        JOptionPane.showMessageDialog(null,"Connection NOT Closed.");
      }
    }

    // if button is pressed
    public void actionPerformed(ActionEvent e)
    {
        String s = e.getActionCommand();
        if (s.equals("Close")) {
            f.dispose();
        }
    }
}
