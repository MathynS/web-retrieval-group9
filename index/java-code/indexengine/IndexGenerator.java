package indexengine;
 
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
import java.util.Properties;
import java.util.logging.Level;
import java.util.logging.Logger;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
import org.apache.lucene.document.Field;
import org.apache.lucene.document.TextField;
import org.apache.lucene.index.IndexWriter;
import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.store.Directory;
import org.apache.lucene.store.FSDirectory;
 
/**
 *
 * @author sqlitetutorial.net
 */
public class IndexGenerator {	
     
	private String dbUrl;
	
	private String indexDirectory;
	
	private int idsOffset;
	
	private static final Logger logger = Logger.getLogger(IndexGenerator.class.getName());
	
	public IndexGenerator(){
		configure();
	}
	
	private void configure(){
		Properties indexConfiguration = new Properties();
		ClassLoader cl = this.getClass().getClassLoader();	
		try (InputStream in = cl.getResourceAsStream("conf/IndexConfig.properties")) {
			indexConfiguration.load(in);
			this.dbUrl = indexConfiguration.getProperty("dbUrl");
			this.indexDirectory = indexConfiguration.getProperty("indexDirectory");
			this.idsOffset = Integer.parseInt(indexConfiguration.getProperty("idsOffset"));
		} catch (FileNotFoundException fnfe) {
			logger.log(Level.SEVERE, "Error configuring IndexGenerator object", fnfe);
			System.exit(0);
		} catch (IOException ioe) {
			logger.log(Level.SEVERE, "Error configuring IndexGenerator object", ioe);
			System.exit(0);
		} catch (NumberFormatException nfe){
			logger.log(Level.INFO, "Error to parse idOffset value from configuration file", nfe);
			this.idsOffset = 10;
		}
	}
	
	/**
     * Connect to a sample database
	 * @throws SQLException 
     */
    private Connection connect() throws SQLException {
    	return DriverManager.getConnection(this.dbUrl);
    }
        
    public void generateIndex() throws IOException{

    	try (	Connection conn = this.connect();
    			Statement stmt = conn.createStatement()){
    		
        	String firstIdQuery = "select id from papers_nr_nsw limit 1"; 
        	ResultSet rsFirstId = stmt.executeQuery(firstIdQuery);
        	int firstId = -1;
        	if (rsFirstId != null){
        		firstId = rsFirstId.getInt("id");
        	}
        	
        	String maxIdQuery = "select id from papers_nr_nsw order by id desc limit 1";
        	ResultSet rsMaxId = stmt.executeQuery(maxIdQuery);
        	int maxId = -1;
        	if (rsMaxId != null){
        		maxId = rsMaxId.getInt("id");
        	}
        	   		
       		Analyzer analyzer = new StandardAnalyzer();
    		Path dirPath = Paths.get(this.indexDirectory);
    		Directory directory = FSDirectory.open(dirPath);
    		IndexWriterConfig config = new IndexWriterConfig(analyzer);
    		IndexWriter indexWriter = new IndexWriter(directory, config);
    		indexWriter.deleteAll();

    		DocsToIndexQueryGenerator queryGenerator = new DocsToIndexQueryGenerator(firstId, this.idsOffset, maxId);
    		
         	while (queryGenerator.isQueryAvailable()){
         		//System.out.println(queryGenerator.createQueryString());	
        		String queryString = queryGenerator.createQueryString();
        		System.out.println(queryString);
         		ResultSet rs = stmt.executeQuery(queryString);
        		while(rs.next()){        			
        			Document doc = new Document();
        			doc.add(new Field("id", rs.getString("id"), TextField.TYPE_STORED));
        			doc.add(new Field("pdf_name", rs.getString("pdf_name"), TextField.TYPE_STORED));
        			doc.add(new Field("paper_text", rs.getString("paper_text"), TextField.TYPE_STORED));
        			doc.add(new Field("paper_title", rs.getString("paper_title"), TextField.TYPE_STORED));
        			indexWriter.addDocument(doc);
        			//System.out.println(rs);
        		}	
        	}
        	
        	indexWriter.commit();
        	indexWriter.close();
        } catch(SQLException sqle){
        	logger.log(Level.INFO, "Error at processing sql operations", sqle);
        }        	
    	
    }
    
    /**
     * @param args the command line arguments
     * @throws IOException 
     */
    public static void main(String[] args) throws IOException {
        IndexGenerator indexGenerator = new IndexGenerator();
        indexGenerator.generateIndex();
    }
}