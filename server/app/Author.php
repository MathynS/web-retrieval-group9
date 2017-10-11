<?php

namespace App;

use Illuminate\Database\Eloquent\Model;

class Author extends Model
{
    public function documents()
    {
    	return $this->belongsToMany('App\Document', 'document_author', 'paper_id', 'author_id');
    }

}
