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
        $queryTerm = null;
        $i = 0;
        while ($i < count($terms)){
            $lookup = 1;
            if (!array_key_exists($i, $terms)){
                $i ++;
                continue;
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
                $documents = $this->document->filter($documents, $term, 'authors', 'name', 'LIKE', '","');
            }
            elseif(substr($term, 0, 6) === "label:"){
                $documents = $this->document->filter($documents, $term, 'labels', 'name', '=', '","');
                $searchTerm = explode(":", $term, 2)[1];
                if (substr($searchTerm, 0, 1) === "\""){
                    $searchTerm = substr($searchTerm, 1, -1);
                }
                $response['label_data'] = Document::with('labels')->whereHas('labels', function($q) use($searchTerm) {
                    $q->where('labels.name', '=', $searchTerm);
                })->select('year', DB::raw('count(*) as count'))->groupBy('year')->get();
            }
            elseif(substr($term, 0, 5) == "year:"){
                $documents = $this->document->filter($documents, $term, 'documents', 'year', '=', ',');
            }
            else{
                $queryTerm = $term;
            }
        }

        if ($queryTerm != null){
            $documents = $this->document->searchIndex($documents, $queryTerm, $order, $mode);
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
		return $response;

    }
}
