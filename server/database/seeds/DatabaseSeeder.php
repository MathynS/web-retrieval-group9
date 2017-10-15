<?php

use App\Document;
use Illuminate\Database\Seeder;

class DatabaseSeeder extends Seeder
{
    /**
     * Run the database seeds.
     *
     * @return void
     */

    public function csv_to_array($filename='', $delimiter=',')
    {
        if(!file_exists($filename) || !is_readable($filename))
            return FALSE;

        $header = NULL;
        $data = array();
        if (($handle = fopen($filename, 'r')) !== FALSE)
        {
            while (($row = fgetcsv($handle, 1000, $delimiter)) !== FALSE)
            {
                if(!$header)
                    $header = $row;
                else
                    if (sizeof($row) == sizeof($header)){
                        $data[] = array_combine($header, $row);
                    }
            }
            fclose($handle);
        }
        return $data;
 	}

    public function csv_to_index($filename='', $delimiter=',')
    {
        if(!file_exists($filename) || !is_readable($filename))
            return FALSE;
        $header = NULL;
        $data = array();
        if (($handle = fopen($filename, 'r')) !== FALSE)
        {
            while (($row = fgetcsv($handle, 1000, $delimiter)) !== FALSE)
            {
                if(!$header)
                    $header = $row;
                else
                    if (array_key_exists($row[1], $data)){
                        $data[$row[1]][] = $row[2];
                    }
                    else{
                        $data[$row[1]] = array($row[2]);
                    }
            }
            fclose($handle);
        }
        return $data;
    }    

    public function run()
    {
    	$papers = $this->csv_to_array(public_path() . '/csv/papers.csv');
        $authors = $this->csv_to_array(public_path() . '/csv/authors.csv');
        $paper_authors = $this->csv_to_index(public_path() . '/csv/paper_authors.csv');
        $paper_labels = $this->csv_to_index(public_path() . '/csv/paper_labels.csv');
        $labels = $this->csv_to_array(public_path() . '/csv/labels.csv');

        DB::table('authors')->insert($authors);
        DB::table('labels')->insert($labels);
        
        foreach ($papers as $paper){
            try{
                $doc = Document::create($paper);
                if (array_key_exists($paper['id'], $paper_authors)){
                    $doc->authors()->sync($paper_authors[$paper['id']]);
                }
                if (array_key_exists($paper['id'], $paper_labels)){
                    $doc->labels()->sync($paper_labels[$paper['id']]);
                }
            }catch(\Illuminate\Database\QueryException $e){}
        }
        //DB::table('documents')->insert($papers);
        //DB::table('document_author')->insert($paper_authors);

    }
}
