<?php

use Illuminate\Support\Facades\Schema;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Database\Migrations\Migration;

class CreateDocumentAuthorTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('document_author', function (Blueprint $table) {
            $table->increments('id');
            $table->timestamps();
            $table->integer('paper_id')->unsigned()->nullable();
            $table->foreign('paper_id')->references('id')->on('documents')->onDelete('cascade');

            $table->integer('author_id')->unsigned()->nullable();
            $table->foreign('author_id')->references('id')->on('authors')->onDelete('cascade');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('document_author');
    }
}
