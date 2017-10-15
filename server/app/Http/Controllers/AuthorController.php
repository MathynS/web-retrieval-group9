<?php

namespace App\Http\Controllers;

use DB;
use App\Author;
use App\Document;
use Illuminate\Http\Request;

class AuthorController extends Controller
{
    public function __construct(){
        $this->author = new Author();
    }

    public function show(Author $author){
    	return view('author', compact('author'));
    }

    public function retrieve(Request $request){
    	$this->validate($request, [
    		'author_id' => 'required|int'
    		]);
        $response = array();
    	$author_id = $request->input('author_id');
    	$label_entries = Author::find($author_id)
    		->select('documents.year', 'documents.title', 'labels.name', DB::raw('count(*) as count'))
    		->leftJoin('document_author', 'document_author.author_id', '=', 'authors.id')
    		->leftJoin('documents', 'documents.id', '=', 'document_author.paper_id')
    		->leftJoin('document_label', 'document_label.paper_id', '=', 'documents.id')
    		->leftJoin('labels', 'labels.id', '=', 'document_label.label_id')
    		->where('authors.id', '=', $author_id)
    		->groupby('documents.year', 'labels.name', 'documents.title')
    		->get();
        #return $label_entries;
        return $label_entries;
        foreach ($label_entries as $label_entry){
            if (!array_key_exists($label_entry->name, $response)){
                $response[$label_entry->name] = array();
            }
            if (array_key_exists($label_entry->year, $response[$label_entry->name])){
                $response[$label_entry->name][$label_entry->year] += $label_entry->count;
            }
            else{
                $response[$label_entry->name][$label_entry->year] = $label_entry->count;
            }
        }

    	return $response;
    }

    public function getGraph(Request $request){
        $this->validate($request, [
            'author_id' => 'required|int'
            ]);
        $author_id = $request->input('author_id');
        return $this->author->makeGraph($author_id);
    }
}
