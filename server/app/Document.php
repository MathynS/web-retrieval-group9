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
    public function getSnippet($document, $query)
    {
    	#$document = Document::with('authors')->with('labels')->where('id', '=', $id)->select('id', 'title', 'year')->first();
        $snippet_command = array(
    		env('APP_LOCATION') . 'snippets/snippet_creator.py',
    		'--query',
    		$query,
    		'--document',
    		$document->id
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

    public function searchIndex($documents, $queryTerm, $order, $mode){
        $index_command = array(
            env('APP_LOCATION') . 'index/script_index_engine_controller.py',
            "--command",
            "QUERY",
            "--query",
            $queryTerm,
            "--amount",
            100
            );

        $builder = new ProcessBuilder();
        $builder->setArguments($index_command)->getProcess()->getCommandLine();
        $process = $builder->getProcess();
        $process->run();

        if (!$process->isSuccessful()) {
            throw new ProcessFailedException($process);
        }
        $result = $process->getOutput();
        $result_ids = array_map('intval', explode(' ', $result));
        if ($order == 'relevance'){
            return $documents->whereIn('id', $result_ids)->orderByRaw('Field(id,' . implode(",", $result_ids) . ')');
        }
        else{
            return $documents->whereIn('id', $result_ids)->orderBy($order, $mode);
        }
    }

    public function filter($documents, $searchTerm, $searchEntity, $searchParam, $operator, $delimiter){
        $response = array();
        $whereStatements = array();
        $searchTerm = explode(":", $searchTerm, 2)[1];
        if (substr($searchTerm, 0, 1) === "\""){
            $searchTerm = substr($searchTerm, 1, -1);
        }
        foreach (explode($delimiter, $searchTerm) as $term) {
            if ($operator == "LIKE"){
                $term = "%$term%";
            }
            $whereStatements[] = ["$searchEntity.$searchParam", $operator, $term];
        }
        if ($searchEntity == 'documents'){
            $result = $documents->where(function($q) use($whereStatements){
                foreach($whereStatements as $whereStatement){
                    $q->orWhere($whereStatement[0], $whereStatement[1], $whereStatement[2]);
                }
            });
        }
        else{
            $result = $documents->whereHas($searchEntity, function($q) use($whereStatements){
                    #foreach($whereStatements as $whereStatement){
                    #    var_dump($whereStatement);
                        $q->Where($whereStatements[0][0], $whereStatements[0][1], $whereStatements[0][2]);
                        foreach(array_slice($whereStatements, 1) as $whereStatement){
                            $q->orWhere($whereStatement[0], $whereStatement[1], $whereStatement[2]);
                        }
                    #}
                });
        }
        return $result;
        // $response['amount'] = $result->count();
        // $response['docs'] = $result->skip(0)->limit(10)->get();
        // return $response;
    }
}
