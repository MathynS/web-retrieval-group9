<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Document;

class DocumentController extends Controller
{
    public function show(Document $document){
    	$document['authors'] = $document->authors;
    	$docuemnt['labels'] = $document->labels;
    	return view('document', compact('document'));
    }
}
