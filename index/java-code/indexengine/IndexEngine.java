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
	
	public void searchByContent(String queryInputString, int numberOfDocs){
		List<Integer> selectedDocuments;
		StringBuilder builder = new StringBuilder();
		try {
			selectedDocuments = documentRetriever.searchDocumentsByContent(queryInputString, numberOfDocs);
			// Print selected documents
			for (Integer id: selectedDocuments){
				builder.append(Integer.toString(id) + " ");
			}
		} catch (Exception e) {
			logger.log(Level.INFO, "There was a problem when querying the index", e);
		}
		System.out.println(builder.toString());
	}

	public void searchByTitle(String queryInputString, int numberOfDocs){
		List<Integer> selectedDocuments;
		StringBuilder builder = new StringBuilder();
		try {
			selectedDocuments = documentRetriever.searchDocumentsByTitle(queryInputString, numberOfDocs);
			// Print selected documents
			for (Integer id: selectedDocuments){
				builder.append(Integer.toString(id) + " ");
			}
		} catch (Exception e) {
			logger.log(Level.INFO, "There was a problem when querying the index", e);
		}
		System.out.println(builder.toString());
	}

	
	
	public static void main(String[] args){
	
		IndexEngine engine = new IndexEngine();
		String usage = "Usage:'t java IndexEngine [CREATE_INDEX|QUERY_CONTENT|QUERY_TITLE] [queryInput]\n";
		if (args.length >= 1){
			String command = args[0];
			if (command.equals("CREATE_INDEX")){
				engine.generateIndex();
			} else if (command.equals("QUERY_CONTENT")){
				String queryData = args[1];
				int numberOfDocs;
				try {
					numberOfDocs = Integer.parseInt(args[2]);
				} catch (NumberFormatException nfe){
					numberOfDocs = DEFAULT_NUMBER_OF_DOCS;
				}
				engine.searchByContent(queryData, numberOfDocs);
			} else if (command.equals("QUERY_TITLE")){
				String queryData = args[1];
				int numberOfDocs;
				try {
					numberOfDocs = Integer.parseInt(args[2]);
				} catch (NumberFormatException nfe){
					numberOfDocs = DEFAULT_NUMBER_OF_DOCS;
				}
				engine.searchByTitle(queryData, numberOfDocs);				
			} else {
				System.out.println(usage);
			}
		} else {
			System.out.println(usage);
		}
	}
}
