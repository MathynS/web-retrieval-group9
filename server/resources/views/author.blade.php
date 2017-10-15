@extends('layouts.master')

@section('content')

	
<a href="/search?q=author:%22{{ $author->name }}%22"><h2>Find all papers from {{ $author->name }}</h2></a>
	<div class="container">
  		<div class="row">
  			<div class="col col-lg-6">
				<author-field></author-field>
			</div>

			<div class="col col-lg-6">
				<author-graph></author-graph>
			</div>
		</div>
	</div>

@endsection