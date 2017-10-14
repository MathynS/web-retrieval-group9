package indexengine;

import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;

public class IndexEngine {
	
	private IndexGenerator indexGenerator;
	
	private DocumentRetriever documentRetriever;

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
	
	public void retrieveDocumentIds(String queryInputString){
		List<Integer> selectedDocuments;
		try {
			selectedDocuments = documentRetriever.searchDocuments(queryInputString);
		} catch (Exception e) {
			logger.log(Level.INFO, "There was a problem when querying the index", e);
		}
		
		// Print selected documents
		/**
		for (Integer id: selectedDocuments){
			System.out.println(id);
		}
		**/
	}
	
	public static void main(String[] args){
	
		IndexEngine engine = new IndexEngine();
		String usage = "Usage:'t java IndexEngine [CREATE_INDEX|QUERY] [queryInput]\n";
		if (args.length >= 1){
			String command = args[0];
			if (command.equals("CREATE_INDEX")){
				engine.generateIndex();
			} else if (command.equals("QUERY")){
				engine.retrieveDocumentIds(args[1]);
			} else {
				System.out.println(usage);
			}
		} else {
			System.out.println(usage);
		}
	}
}
