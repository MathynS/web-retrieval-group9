<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Document;

class QueryController extends Controller
{
	public function __construct()
	{
		$this->document = new Document();
	}

    public function retrieve(Request $request)
    {
    	$this->validate($request, [
    		'query' => 'required|string'
    		]);
    	$query = $request->input('query');

    	//TODO replace by index
    	$doc_ids = Document::take(10)->pluck('id');

    	$response = array();
    	$response['query'] = $query;
    	$response['docs'] = array();
    	foreach ($doc_ids as $doc_id){
    		$response['docs'][] = $this->document->get($doc_id, $query);
		}
		return $response;

    }
}
