<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\ProcessBuilder;
use Symfony\Component\Process\Process;

class Document extends Model
{
	protected $table = 'documents';

	// public function __construct()
	// {
	// 	$this->builder = new ProcessBuilder();
	// }

	public function authors()
	{
		return $this->belongsToMany('App\Author', 'document_author', 'paper_id', 'author_id');
	}

	public function labels()
	{
		return $this->belongsToMany('App\Label', 'document_label', 'paper_id', 'label_id');
	}
 //->select('id', 'title', 'year')
    public function get($id, $query)
    {
    	$document = Document::with('authors')->with('labels')->where('id', '=', $id)->select('id', 'title', 'year')->first();
    	$snippet_command = array(
    		env('APP_LOCATION') . 'snippets/snippet_creator.py',
    		'--query',
    		$query,
    		'--document',
    		$id
    		);
    	$builder = new ProcessBuilder();
    	$builder->setArguments($snippet_command)->getProcess()->getCommandLine();
    	$process = $builder->getProcess();
    	$process->run();

    	if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

        $document['snippet'] = $process->getOutput();

    	return $document;
    }
}
