<?php

namespace App\Http\Controllers;

use DB;
use App\Author;
use App\Document;
use Illuminate\Http\Request;

class AuthorController extends Controller
{
    public function show(Author $author){
    	return view('author', compact('author'));
    }

    public function retrieve(Request $request){
    	$this->validate($request, [
    		'author_id' => 'required|int'
    		]);
    	$author_id = $request->input('author_id');
    	$author = Author::find($author_id)
    		->select('documents.year', 'labels.name', DB::raw('count(*)'))
    		->leftJoin('document_author', 'document_author.author_id', '=', 'authors.id')
    		->leftJoin('documents', 'documents.id', '=', 'document_author.paper_id')
    		->leftJoin('document_label', 'document_label.paper_id', '=', 'documents.id')
    		->leftJoin('labels', 'labels.id', '=', 'document_label.label_id')
    		->where('authors.id', '=', $author_id)
    		->groupby('documents.year', 'labels.name')
    		->get();
    	return $author;
    }
}
