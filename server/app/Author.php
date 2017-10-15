<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Symfony\Component\Process\Exception\ProcessFailedException;
use Symfony\Component\Process\ProcessBuilder;
use Symfony\Component\Process\Process;

class Author extends Model
{
    public function documents()
    {
    	return $this->belongsToMany('App\Document', 'document_author', 'paper_id', 'author_id');
    }

    public function makeGraph($author_id){
    	$snippet_command = array(
    		env('APP_LOCATION') . 'co_authors_graph/generate_local_graph.py',
    		'--author',
    		$author_id
    		);
    	$builder = new ProcessBuilder();
        $builder->setArguments($snippet_command)->getProcess()->getCommandLine();
        $process = $builder->getProcess();
        $process->run();

        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }

    	return $process->getOutput();
    }

}
