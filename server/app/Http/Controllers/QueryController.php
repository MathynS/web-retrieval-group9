<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Document;
use App\Label;
use DB;

class QueryController extends Controller
{
	public function __construct()
	{
		$this->document = new Document();
	}

    public function retrieve(Request $request)
    {
        $starttime = microtime(true);
    	$this->validate($request, [
    		'query' => 'required|string',
            'page' => 'required|int',
            'order' => 'required|string'
    		]);

        $query = $request->input('query');
        $page = $request->input('page');
        $orig_order = $request->input('order');
        $order = explode('_', $orig_order);
        $response = array();
        if (count($order) == 1){
            $order = $order[0];
            $mode = 'desc';
        }
        elseif(count($order == 2)){
            $mode = $order[1];
            $order = $order[0];
        }
        $terms = explode(' ', $query);
        $queryTerm = array();
        $i = 0;
        while ($i < count($terms)){
            $lookup = 1;
            if (!array_key_exists($i, $terms)){
                $i ++;
                continue;
            }
            if (substr($terms[$i], -1) == ":"){
                return array("error" => "Missing a term after your filter, is there maybe a space after a :?");
            }
            while (substr_count($terms[$i], "\"") % 2 == 1){
                if (!array_key_exists($i+$lookup, $terms)){
                    return array("error" => "You made a mistake in your query: you forgot a \" somewhere");
                }
                $terms[$i] = $terms[$i] . " " . $terms[$i+$lookup]; 
                unset($terms[$i+$lookup]);
                $lookup++;
            }
            $i++;
        }

        $documents = Document::with(['labels', 'authors']);
        foreach ($terms as $term) {
            if (substr($term, 0, 7) === "author:"){
                $documents = $this->document->filter($documents, $term, 'authors', 'name', 'LIKE');
            }
            elseif(substr($term, 0, 6) === "label:"){
                $documents = $this->document->filter($documents, $term, 'labels', 'name', 'like');
                $searchTerm = explode(":", $term, 2)[1];
                if (substr($searchTerm, 0, 1) === "\""){
                    $searchTerm = substr($searchTerm, 1, -1);
                }
                $response['label_data'] = Document::with('labels')->whereHas('labels', function($q) use($searchTerm) {
                    $q->where('labels.name', 'like', $searchTerm);
                })->select('year', DB::raw('count(*) as count'))->groupBy('year')->get();
            }
            elseif(substr($term, 0, 5) == "year:"){
                $documents = $this->document->filter($documents, $term, 'documents', 'year', '=');
            }
            elseif(substr($term, 0, 6) == "title:"){
                $searchTerm = explode(":", $term, 2)[1];
                if (substr($searchTerm, 0, 1) === "\""){
                    $searchTerm = substr($searchTerm, 1, -1);
                }
                $document = $this->document->searchIndex($documents, $searchTerm, $order, $mode, "QUERY_TITLE");
            }
            else{
                $queryTerm[] = $term;
            }
        }

        if (count($queryTerm) > 0){
            $documents = $this->document->searchIndex($documents, implode(" ", $queryTerm), $order, $mode, "QUERY_CONTENT");
        }
        elseif ($order != 'relevance'){
            $documents = $documents->orderBy($order, $mode);
        }        
        $response['amount'] = $documents->count();
        $documents = $documents->skip(($page-1) * 10)->limit(10)->get();

        if ($queryTerm != null){
            foreach ($documents as $document){
                $document['snippet'] = $this->document->getSnippet($document, $query);
            }
        }
        $response['order'] = $orig_order;
        $response['page'] = intval($page);
        $response['docs'] = $documents;
        $response['query'] = $query;
        $response['time'] = number_format(microtime(true) - $starttime, 2);
		return $response;

    }
}
