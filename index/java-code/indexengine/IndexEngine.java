package indexengine;

import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class IndexEngine {
	
	private IndexGenerator indexGenerator;
	
	private DocumentRetriever documentRetriever;
	
	private static final int DEFAULT_NUMBER_OF_DOCS = 10;

	private static final Logger logger = Logger.getLogger(IndexEngine.class.getName());

	public IndexEngine(){
		indexGenerator = new IndexGenerator();
		documentRetriever = new DocumentRetriever();
	}
	
	public void generateIndex(){
		try {
			indexGenerator.generateIndex();
		} catch (Exception e){
			logger.log(Level.SEVERE, "Index generation failed", e);			
		}
	}
	
	public void retrieveDocumentIds(String queryInputString, int numberOfDocs){
		List<Integer> selectedDocuments;
		try {
			selectedDocuments = documentRetriever.searchDocuments(queryInputString, numberOfDocs);
			// Print selected documents
			for (Integer id: selectedDocuments){
				System.out.println(id);
			}
		} catch (Exception e) {
			logger.log(Level.INFO, "There was a problem when querying the index", e);
		}
				
	}
	
	public static void main(String[] args){
	
		IndexEngine engine = new IndexEngine();
		String usage = "Usage:'t java IndexEngine [CREATE_INDEX|QUERY] [queryInput]\n";
		if (args.length >= 1){
			String command = args[0];
			if (command.equals("CREATE_INDEX")){
				engine.generateIndex();
			} else if (command.equals("QUERY")){
				String queryData = args[1];
				int numberOfDocs;
				try {
					numberOfDocs = Integer.parseInt(args[2]);
				} catch (NumberFormatException nfe){
					numberOfDocs = DEFAULT_NUMBER_OF_DOCS;
				}
				engine.retrieveDocumentIds(queryData, numberOfDocs);
			} else {
				System.out.println(usage);
			}
		} else {
			System.out.println(usage);
		}
	}
}
