package indexengine;

public class DocsToIndexQueryGenerator {

	private int firstId;

	private int maxId;
	
	private int offset;
	
	public DocsToIndexQueryGenerator(int firstId, int offset, int maxId){
		this.firstId = firstId;
		this.offset = offset;
		this.maxId = maxId;
	}
	
	private void updateFirstId(){
		firstId = firstId + offset; 
	}
	
	private int getLastId(){
    	int lastId = firstId + offset - 1;
    	if (lastId > maxId){
    		lastId = maxId;
    	}
    	return lastId;
	}
	
	public boolean isQueryAvailable(){
		if (firstId > maxId){
			return false;
		}
		return true;
	}

	public String createQueryString(){
    	StringBuilder sb = new StringBuilder();
    	sb.append("select id, pdf_name, paper_text, paper_title from papers_nr_nsw where id >= ");
    	sb.append(Integer.toString(firstId));
    	sb.append(" and id <= ");
    	sb.append(Integer.toString(getLastId()));
    	updateFirstId();
    	return sb.toString();
	}
}
