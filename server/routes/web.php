<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

Route::get('/', function () { return view('builder'); });
Route::get('/search', function () { return view('search'); });

Route::get('/authors/{author}', 'AuthorController@show');
Route::get('/labels/{label}', 'LabelController@show');
Route::get('/documents/{document}', 'DocumentController@show');

Route::prefix('api')->group(function() {
	Route::post('search', 'QueryController@retrieve');
	Route::post('get-author-fields', 'AuthorController@retrieve');
	Route::post('get-author-graph', 'AuthorController@getGraph');
});
