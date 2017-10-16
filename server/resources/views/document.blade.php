@extends('layouts.master')

@section('content')

<h3>
    {{ $document->title }}
</h3>

@foreach ($document->authors as $author)
<span>
    <span class="glyphicon glyphicon-user"></span>
    <a href="/authors/{{$author->id}}"> {{ $author->name }} </a>
</span>
@endforeach

<br>
<small>Published in <a href="/search?q=year:{{$document->year}}">{{ $document->year }}, </a></small>
<small>Cited by {{ $document->citations }} papers</small>
<br />

<strong>Tags:</strong>

@foreach ($document->labels as $label)
<a href="/search?q=label:%22{{ $label->name }}%22">
    <span class="tag label label-info">{{ $label->name }}</span>
</a>
@endforeach

<br><br>

<pre>{{ $document->paper_text }}</pre>


@endsection